#Imports
import requests
import ujson
import statistics
from flask import Flask, redirect, url_for, render_template, request, jsonify, make_response
from time import time
from resources import base_loot_amounts, lab_ratios, fishing_ratios, happ_dict, lab_list, tier_list, city_list, base_table, request_string,seaweed_quant

#Variable definition
#mew_prices are prices from a new API request
#old_prices are those currently stored in the prices json file
#refreshed_prices are old_prices with all values replaced with non-0 values from new_prices, and new averages calculated

#Classes

class Query():
#A query is sent from the front end to the back
#This query contains: city, happiness OR house, and may contain manually adjusted prices by the user
    
    def __init__(self,city,happiness,house):
        #Fixed on init
        self.city = city
        self.happ = happiness
        self.house = house
        
        #To be populated later
        #Will store the profit for each Labourer and Tier. Goes to front end.
        self.profits = {"toolmaker":{},"warrior":{},"mage":{},"hunter":{},"fiber":{},"wood":{},"stone":{},
                        "ore":{},"hide":{},"fishing":{}}
        #Will store the items and their prices used for each labourer and tier. Goes to front end.
        #Format, i.e. for T2 cropper: {"fiber":{"t2":[{"item_id":"T2_FIBER","item_price":20,"item_quant":10,"sell_value":200]}}
            #Numbers above are representative.
        self.lab_prices = {"toolmaker":{},"warrior":{},"mage":{},"hunter":{},"fiber":{},"wood":{},"stone":{},
                        "ore":{},"hide":{},"fishing":{}}

    def material_sell(self,base_loot_amounts,lab,tier,prices):
        #Each labourer type has a standard material output. Identify which type of labourer we are handling.
        if lab in ["toolmaker","hunter","mage","warrior"]:
            lab_type = "crafter"
        elif lab in ["fiber","wood","stone","ore","hide"]:
            lab_type = "gatherer"
        elif lab == "fishing":
            lab_type = "fisher"
            
        #Add the current tier to self.lab_prices.
        self.lab_prices[lab][tier]=[]
        
        #Setting current calculated profit to 0 for each LAB and TIER.
        self.profits[lab][tier] = 0
        
        ###Account for happiness
        #If happiness was < 50% it was instead set to 0 as labs will not work under 50%.
        happiness = self.calculate_happiness(lab,tier,lab_type)
        
        if lab != "fishing":
            #Establish tiered item names and sell value for each item, then sum to labourer total resource sell value
            #The materials from non-fishing labourers are standardised, only the material tier changes across journal tier.
            for item,ratio in lab_ratios[lab].items():
                #Turn the standardised name i.e. "planks_level1@1" to a tiered version like "t6_planks_level1@1"
                tiered_item = tier+"_"+item
                
                #Tier3 items cannot be enchanted. Queries for the prices of enchanted t3 items will fail.
                #If the current item being handled is enchanted, and the labourer tier is T3. Skip it and go to the next item.         if tier == "t3" and "level" in tiered_item:
                if tier == "t3" and "@" in item:
                    continue
                    
                #Find the price, quantity returned, and estimated revenue from the item and add it to tiered lab profit.
                self.one_item_sell(base_loot_amounts,lab_type,lab,tier,happiness,tiered_item,prices,ratio)
            
        elif lab == "fishing":
            #Fishing journal output varies with tier, and does not provide enchanted items. Handle differently to other LABs.
            for item,ratio in fishing_ratios[tier].items():
                #Find the price, quantity returned, and estimated revenue from the item and add it to tiered lab profit.
                self.one_item_sell(base_loot_amounts,lab_type,lab,tier,happiness,item,prices,ratio)

    def one_item_sell(self,base_loot_amounts,lab_type,lab,tier,happiness,item,prices,ratio):
        #Takes an item from material_sell for a lab and tier.
        #Finds the item price, the proper item quantity (including happiness), and sell value.
        #Done as a separate method as this is used for both Fisher and Non-fisher labourers.
        price = prices[item]
              
        #Using base loot amounts for the labourer type, calculate the quantity returned of each item
        #Happiness will cause the quantity to be multiplied by: 0 OR 0.5 to 1.5
        quantity = ratio*happiness*base_loot_amounts[lab_type][tier]
        
        #T2 gathering labourers need quantitiy corrected to account for lack of enchanted materials in weighting
        if lab != "fishing" and tier == "t3":
            quantity = quantity/0.9445
        
        #Seaweed is unique in that when rewarded it returns more than 1 item.
        #So if base loot amount is 10, and 2 seaweed are awarded per proc, a total of 20 seaweed could be returned from the journal.
        if item == "t1_seaweed":
            quantity = quantity*seaweed_quant[tier]
        
        #Value of selling all projected quantity of an item at market price
        sellvalue = quantity*price
        
        #Add the item to self.lab_prices for later sending to front end.
        self.lab_prices[lab][tier].append({"item_id":item,"item_price":price,"item_quant":round(quantity,4),"sell_value":round(sellvalue,0)})

        #Update tiered labourer profit from selling the full projected quantity of a returned item.
        self.profits[lab][tier]+=sellvalue
                
        
            

    def calculate_happiness(self,lab,tier,lab_type):
        #Covers if the request was made with HAPPINESS:
        if self.house == None:
            return self.happ
        #Covers if the request was made with HOUSE TIER:
        if self.happ == None:
            #Remove the "T" to get the number of the tier for the house and examined labourer. Ie T7 (Tier 7) becomes 7.
            house_tier = int(self.house[1])
            lab_tier = int(tier[1])
            lab_happ = happ_dict[lab_type][self.house]
            if house_tier < lab_tier:
                #Happiness ratio (% / 100)  = house happiness level / journal tier*100
                ratio = lab_happ / (lab_tier*100)
                #The mininum happiness a labourer will work with is 50%
                if ratio < 0.5:
                    return 0
            elif house_tier == lab_tier:
                #Once 100% happiness is reached, any excess effect from the happ level/journal tier*100 is halved.
                excess = lab_happ - (lab_tier*100)
                ratio = 1 +  (excess / 200)
            elif house_tier > lab_tier:
                #With journals lower tier than a house with proper furniture, the happiness is always 150%
                ratio = 1.5

            return ratio          
            
    def journals_and_profit(self,lab,tier,prices):
        #Using revenue from material_sell, then adding journal buy/sell and sales tax to give final profit.
        #Create a tiered journal name, similar to tiered items in material_sell
        full = tier+"_journal_"+lab+"_full"
        empty = tier+"_journal_"+lab+"_empty"
        
        #Obtain journal prices for this LAB and TIER
        full_price = prices[full]
        empty_price = prices[empty]
    
        #Add empty journal sale price to the material outputs revenue
        self.profits[lab][tier] += empty_price
        
        #Multiply current profit by 0.955 to account for the 4.5% setup fee and premium sales tax, assuming using sale orders
        self.profits[lab][tier] = self.profits[lab][tier]*0.955
    
        #Subract full book value
        self.profits[lab][tier] -= full_price
        
        #Round profit values for presentability on front end
        self.profits[lab][tier] = round(self.profits[lab][tier])
        
        #Add the journals to the front of the labourer price list.
        #####Improvement: Inserting them after creating the list is slower than putting them there to begin with.
        self.lab_prices[lab][tier].insert(0,({"item_id":full,"item_price":full_price,"item_quant":-1,"sell_value":-full_price}))
        self.lab_prices[lab][tier].insert(1,({"item_id":empty,"item_price":empty_price,"item_quant":1,"sell_value":empty_price}))
                                          
    


    def rename_labs(self):
        #Replace API labourer names with in-game names for front end
        self.profits["Cropper"] = self.profits.pop("fiber")
        self.profits["Gamekeeper"] = self.profits.pop("hide")
        self.profits["Fletcher"] = self.profits.pop("hunter")
        self.profits["Imbuer"] = self.profits.pop("mage")
        self.profits["Prospector"] = self.profits.pop("ore")
        self.profits["Stonecutter"] = self.profits.pop("stone")
        self.profits["Tinker"] = self.profits.pop("toolmaker")
        self.profits["Blacksmith"] = self.profits.pop("warrior")
        self.profits["Lumberjack"] = self.profits.pop("wood")
        self.profits["Fisherman"] = self.profits.pop("fishing")
        
        #Need to do the same for lab_prices so that the javascript price_table function knows which lab to use.
        self.lab_prices["Cropper"] = self.lab_prices.pop("fiber")
        self.lab_prices["Gamekeeper"] = self.lab_prices.pop("hide")
        self.lab_prices["Fletcher"] = self.lab_prices.pop("hunter")
        self.lab_prices["Imbuer"] = self.lab_prices.pop("mage")
        self.lab_prices["Prospector"] = self.lab_prices.pop("ore")
        self.lab_prices["Stonecutter"] = self.lab_prices.pop("stone")
        self.lab_prices["Tinker"] = self.lab_prices.pop("toolmaker")
        self.lab_prices["Blacksmith"] = self.lab_prices.pop("warrior")
        self.lab_prices["Lumberjack"] = self.lab_prices.pop("wood")
        self.lab_prices["Fisherman"] = self.lab_prices.pop("fishing")
    
    def create_response(self,prices):
        #Creating a fetch response using profit data. This will be sent to the front end in response to the Fetch request.
        result = [[],[]]
        
        #List 1 = Profits to be formatted for a table.
        #Format is: [{"lab":"cropper","t2":t2profit},{"lab":"hunter","t2":t2profit}}
        #When put to a table, each dict is 1 row, where column 1 has the ID "lab", column 2 has the ID "t2".
        #A list of dictionaries. Each dictionary is for 1 labourer, holding their name and profits for each journal tier.
        #This is to match the table on the front end.
        for lab in self.profits.keys():
            lab_result = {}
            #Add the labourer name to the dict
            lab_result["lab"] = lab

            for tier,profit in self.profits[lab].items():
                #Add the labourer profits for each tier to the dict
                lab_result[tier] = profit
            
            #Add the dict to the results list, then move to the next labourer
            result[0].append(lab_result)
        
        ################################################################################################
        #Make result = [[],[]]
        #1st list holds the above dictionaries
        #2nd list holds pricing data
        #Can use the same javascript fetch response, just update multiple tables rather than 1.
            #Maybe have 1 small table for prices. 
            #2nd list has all the prices for each LAB and TIER. 
            #clicking a cell in the profits table loads those items in the price table. 
            #Maybe with quantities expected to output, for quick maths.
        
        #List 2 = Prices to be formatted for a table.
        #Uses Query self.lab_prices, same format.
        #When put to a table, each dict is 1 row, where column 1 has the ID "item_id", column 2 has the ID "item_price".
        result[1] = self.lab_prices

        
        #Turn the resultant list into a JSON to be sent to the front end.
        res = make_response(jsonify(result), 200)
        
        return res
           
#Functions
def calculation(query):
    #Follow the process:
    #1) Bring up price information from the JSON, specify the city we want prices from.
    #2) For each labourer and each tier, calculate the revenue from materials outputted from a journal
    #3) Calculate profit, using journal prices, material revenue, and sales tax
    #4) Make profits data visually readable for the end user
    #5) Create a fetch response using profits data, to send to the front end

    #1)Bring up price information
    all_prices = read_json()
    prices = all_prices[query.city]
    
    #2) Establish revenue from selling labourer material output (excluding empty journals, excluding sale tax)   
    for lab in lab_list:
        for tier in tier_list:
            query.material_sell(base_loot_amounts,lab,tier,prices)

    #3) Finish calculating profit: (Material sale order + empty book sale order)*0.955 - full book buy from sale order
    for lab in lab_list:
        for tier in tier_list:
            query.journals_and_profit(lab,tier,prices)
        
    #4) Prepare for sending data to front end
    query.rename_labs()
    
    #5) Create the Fetch response to send back to front end
    res = query.create_response(prices)
    
    return res

def price_check():
    #Send item_request_string and journal_request_string to the API for data on each city
    #Use recieved JSON from the API to create a new dictionary of prices for each city, not including an avereage
    
    #Api returns city values as Capitalised, and item values as UPPER
    city_string = "bridgewatch,caerleon,fort sterling,lymhurst,martlock,thetford"
    address = f"https://www.albion-online-data.com/api/v2/stats/prices/{request_string}?locations={city_string}"  
    result = requests.get(address)
    text = ujson.loads(result.text)
    
    #Setup a new dictionary in the desired format (see below)
    new_prices = {"bridgewatch":{},"caerleon":{},"fort sterling":{},"lymhurst":{},"martlock":{},"thetford":{},"average":{}}
    
    #Produce a dictionary of new prices for each item and journal in each city
    #text comes in the format [{item 1 in city 1},{item 1 in city 2},{item 2 in city 1},{item 2 in city 2}]]
    #Want to save to the format [{city1}:{"item 1":price,"item 2":price},{city 2}:{"item 1":price,"item 2":price}
    for item in text:
        price = item["sell_price_min"]
        item_id = item["item_id"].lower()
        city = item["city"].lower()
        new_prices[city][item_id] = price   
            
    return new_prices
    
def read_json():
    #Read the "prices.json" and return the prices of all items and journals as a dictionary
    #During price updates, these are "old prices". During profit calculation these are "prices"
    with open('prices.json',"r") as f:
        old_prices = ujson.load(f)
    
    return old_prices
    
def write_json(updated_prices):
    #Write the updated prices dictionary to the "prices.JSON"
    with open('prices.json',"w") as f:
        ujson.dump(updated_prices,f)

def update_json():
    global time_stamp
    time_stamp = time()
    #Obtain new prices for each item and journal in each city
    new_prices = price_check()
    
    #Read the current prices.json to obtain the old prices
    old_prices = read_json()
    
    #Compare and update the city prices
    for city in city_list:
        for item_id in old_prices[city]:
            #Find the new price of an item or journal
            new_price = new_prices[city][item_id]
            
            #Replace the old price if the new price is neither 0 nor over 500,000 (8.3 doesnt get this high)
            if new_prices[city][item_id] != 0 and new_prices[city][item_id] < 500000:
                old_prices[city][item_id] = new_price
    
    #Save the edited old_prices dictionary to updated_prices
    updated_prices = old_prices
             
    #Form a new average price for items and journals across each city, using the updated prices
    for item_id in updated_prices["average"]:
        #Going to make a list of prices for an item in the cities, then average the values in the list
        averaging_list = []
        
        for city in city_list:
            city_price = updated_prices[city][item_id]
            
            #Do not want to include empty values
            if city_price != 0:
                averaging_list.append(city_price)
        
        #If there is at least 1 value (that is not 0, as 0s have not been included), calculate the average
        if averaging_list != []:
            updated_prices["average"][item_id] = round(statistics.fmean(averaging_list))
        #If there are no non-0 values available, no change is made, so the old average is kept
    
    #The prices for each city, plus the average price across cities, have now been updated for every new non-0 value
    #Write the updated prices to the prices.json. To be used until the next update.
    write_json(updated_prices)
    
def check_time(time_stamp):
    #Compares the current time to the time stamp. Runs "update_json" if X seconds have passed since the last price check.
    current_time = time()
    if current_time > time_stamp + 300:
        update_json()
    
    
#Main

#Set the website flask app
app = Flask(__name__)

#Pull the first set of price data, which also sets a time stamp for future reference during this session
update_json()

#Flask sites
@app.route("/house/results", methods=["POST"])
def create_entry_house():
    #POST request, as fetch request from the user has been recieved. Follow the process:
    #1) Check_time, to see if old_prices need updating
    #2) Recieve the fetch request from the front end
    #3) Retrieve the CITY and HOUSE TIER/HAPPINESS from the fetch request
    #4) Use the prices of the requested CITY to calculate profits for the requestd HOUSE TIER
    #5) Send profits JSON to the user.
    
    #1)
    check_time(time_stamp)
    
    
    #2) Recieve the fetch request and save the form JSON to var req
    #UPDATE: Was going to use something else here for forms? Check the old lab py file
    req = request.get_json()
    print(req)
    
    #3)Handling CITY and HOUSE TIER
    ##Pull CITY from fetch
    request_city = req["city"].lower()
    #Validate city
    if request_city == "unselected city":
        return None
    elif request_city == "all":
        request_city = "average"
    
    ##Pull Happiness from fetch
    try:
        #Validate happiness
        request_happ = float(req["happ"].lower())        
        if request_happ < 50 or request_happ > 150:
            return None
        #Convert happiness to a multiplier where 1 = 100%
        request_happ = request_happ / 100
        #Set request_house to none so it is not used by the profit calculation
        request_house = None

    ##If pulling happiness fails, try to pull house tier
    except:
        request_house = req["house"].lower()
        #Validate house tier
        if request_house == "unselected tier":
            return None
        #Set request_happ to none so it is not used by the profit calculation
        request_happ = None

    #4)
    #Form query class from user input
    query = Query(city = request_city, house = request_house, happiness = request_happ)

    #Perform the main API search and Fetch response function
    res = calculation(query)
    
    #5)
    return res

@app.route("/house")
def house_page():
    #GET request. Send the house html file so the user can select a CITY and HOUSE TIER
    return render_template("house.html")

@app.route("/happiness")
def happiness_page():
    return redirect(url_for("house_page"))

@app.route("/")
def index():
    return redirect(url_for("house_page"))

if __name__ == "__main__":
    app.run()
