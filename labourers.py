#Imports
import requests
import ujson
import datetime
from flask import Flask, redirect, url_for, render_template, request, jsonify, make_response
import time

#Classes
class Query():
    
    def __init__(self,city,happiness=1):
        self.city = city
        self.happiness = happiness
        self.items = []
        self.prices = {}
        self.quantities = []
        self.item_request_string = ""
        self.profits = {}
        self.zero_prices = []
        self.lab_ratios = {}
        self.journals = []
        self.journal_prices = {} 
        self.search_date = None
        self.lack_enchanted = {}
        
        #Establish the date x days ago, to output x daily price results
        today = datetime.datetime.today()
        week_delta = datetime.timedelta(days = 1)
        self.search_date = today - week_delta
        self.search_date = self.search_date.date()

        
    def establish_ratios(self,laborer_outputs,lab):
        #Divide according to weightings
        self.lab_ratios[lab]={}
        for key,weighting in laborer_outputs[lab][0].items():
            ratio = laborer_outputs[lab][0][key] / laborer_outputs[lab][1]
            self.lab_ratios[lab][key] = ratio
        
        self.profits[lab] = {}
        
    def material_sell(self,base_loot_amounts,lab,tier):
        #Take base quantity for tier and labourer type
        if lab in ["toolmaker","hunter","mage","warrior"]:
            lab_type = "crafter"
        elif lab in ["fiber","wood","stone","ore","hide"]:
            lab_type = "gatherer"
        elif lab == "fishing":
            lab_type = "fisher"
        
        self.profits[lab][tier] = 0
        self.lack_enchanted[lab+tier]=False
        enchantment = 0
        
        #establish tiered item names and sell value for each item, then sum to labourer total resource sell value
        for item,ratio in self.lab_ratios[lab].items():
            tiered_item = tier+"_"+item
            price = self.prices[tiered_item]
            #Identify where the price of non-enchanted materials i not available -> set journal profit to N/A
            if enchantment == 0:
                if price == 0:
                    self.profits[lab][tier] = "N/A"
                    break
            
            #Identify where the price of enchanted materials is not available -> add a "+"" symbol to the profit later
            if enchantment != 0:
                if price == 0:
                    print (item)
                    self.lack_enchanted[lab+tier]=True
                    #self.profits[lab][tier] = "N/A"
                    #break
            quantity = ratio*base_loot_amounts[lab_type][tier]
            sellvalue = quantity*price
            enchantment += 1
            
            self.profits[lab][tier]+=sellvalue
            
            if tier == "t3":
                break
        

        #if self.prices[index] == 0:
            #zero_price(self,self.items[index])
    
    def calculate_profit(self,lab,tier):
        empty_price = self.journal_prices[tier+"_journal_"+lab+"_empty"]
        full_price = self.journal_prices[tier+"_journal_"+lab+"_full"]
        if isinstance(self.profits[lab][tier], str):
            return
        
        ###Account for happiness (happiness HTML entry can post to carrying out this function if API prices are cached)
        self.profits[lab][tier] = self.profits[lab][tier]*self.happiness
        #Sales tax
        self.profits[lab][tier] = self.profits[lab][tier]*0.955
        #Add empty book value after tax
        if empty_price == 0:
            #print (lab + tier + "empty")
            self.profits[lab][tier] = "N/A"
            return
        self.profits[lab][tier] += empty_price*0.955
        #Subract full book value
        if full_price == 0:
            #print (lab + tier + "full")
            self.profits[lab][tier] = "N/A"
            return
        self.profits[lab][tier] -= full_price
        self.profits[lab][tier] = str(round(self.profits[lab][tier]))
        
        if self.lack_enchanted[lab+tier] == True:
            self.profits[lab][tier] += "+"
        
        #if self.journal_values["empty"] == 0: 
            #zero_price(self,empty_book)
        #if self.journal_values["full"] == 0:
            #zero_price(self,full_book)
            
            
            
            
#Functions
def zero_price(query,item):
    ##Change this to making the table entry for [lab][tier] a string saying N/A or something
    query.zero_prices.append(item)
    print (f"One of the materials or journals currently has no listed price on the city market. {item}")
    
def form_base_table_entry(tier_list):
    base =  {}
    lab_list = ["Cropper","Gamekeeper","Fletcher","Imbuer","Prospector","Stonecutter","Tinker","Blacksmith","Lumberjack"]
        
    for lab in lab_list:
        base[lab] = {} 
        for tier in tier_list:
            base[lab][tier] = 0
            
    return base

def current_price_search(query):
    #Obtain prices for appropriate output items
    address = f"https://www.albion-online-data.com/api/v2/stats/prices/{query.item_request_string}?locations={query.city}"
    result = requests.get(address)
    text = ujson.loads(result.text)
    
    #Assign item prices to a dictionary with names lining up with the .items
    for index,item in enumerate(query.items):
        price = text[index]["sell_price_min"]
        query.prices[item]=price

def weekly_price_search_old(query):
    ###Old function uses /history/ instead of /charts/
    #Obtain prices for appropriate output items
    #The /history/ api search term can only deal with 1 item per search. Multiple searches are needed.
    #Assign item prices to a dictionary with names lining up with the .items
    for item in query.items:
            
        result = requests.get(f"https://www.albion-online-data.com/api/v2/stats/History/{item.upper()}?locations={query.city}&date={query.search_date}&time-scale=24")
        text = ujson.loads(result.text)
        day_prices = []
        
        try:
            for day in text[0]["data"]:
                price = day["avg_price"]
                if price == 0:
                    continue
                else: 
                    day_prices.append(day["avg_price"])
        except IndexError:
            #No historic prices available
            query.prices[item]= 0
            continue
        average_price = sum(day_prices) / len(day_prices) 
        query.prices[item]= average_price
        
def weekly_price_search(query):
    #Obtain prices for appropriate output items
    for item in query.items:
            
        result = requests.get(f"https://www.albion-online-data.com/api/v2/stats/Charts/{item.upper()}?locations={query.city}&date={query.search_date}&time-scale=24")
        text = ujson.loads(result.text)
        
        try:
            day_prices =  text[0]["data"]["prices_avg"]
        except IndexError:
            #No historic prices available
            query.prices[item] = 0
            continue
        average_price = sum(day_prices) / len(day_prices) 
        query.prices[item]= average_price
        
        
def current_book_price_search(query):
    #Produce a string for searching the albion data project. The search works best with items in ALL CAPS
    book_search = ",".join(query.journals).upper()


    result = requests.get(f"https://www.albion-online-data.com/api/v2/stats/prices/{book_search}?locations={query.city}&qualities=")
    text = ujson.loads(result.text)

    for index,book in enumerate(query.journals):
        query.journal_prices[book] = text[index]["sell_price_min"]

def weekly_book_price_search(query):    
    for item in query.journals:
    
        address = f"https://www.albion-online-data.com/api/v2/stats/Charts/{item.upper()}?locations={query.city}&date={query.search_date}&time-scale=24"
        
        result = requests.get(address)
        text = ujson.loads(result.text)
        
        try:
            day_prices =  text[0]["data"]["prices_avg"]
        except IndexError:
            #No historic prices available
            query.journal_prices[item] = 0
            continue
        average_price = sum(day_prices) / len(day_prices) 
        query.journal_prices[item]= average_price
            

            
app = Flask(__name__)


tier_list = ["t3","t4","t5","t6","t7","t8"]
lab_list = ["fiber","hide","hunter","mage","ore","stone","toolmaker","warrior","wood"]


@app.route("/profits/results", methods=["POST"])
def create_entry():
    
    req = request.get_json()

    print(req)
    
    request_city = req["city"]
    
    print(request_city)

    #Validate city
    if request_city == "Please select a city...":
        base = form_base_table_entry(tier_list)
        feedback = "Error: Please select a city from the menu"
        
        
        #return render_template(f"profits.html",profits = base, entry = feedback)
        return None

    ##Validate happiness (with 100% / 1 as default if nothing entered)
    #while True:
        #while True:
            #try:
                #request_happ = (input("Please input labourer happiness (Defaults to 100% if left empty): "))
                #if request_happ == "":
                    #request_happ = 100
                #request_happ = int(request_happ)
            #except TypeError:
                #print ("Not a number.")
                #continue
            #except:
                #print ("Unknown error.")
                #continue
            #else:
                #break

        #if request_happ <50 or request_happ >150:
            #print ("Happiness must be between 50% and 150%.")
        #else:
            #break
    request_happ = req["happ"]

    if request_happ == "":
        request_happ = "100"

    request_happ = int(request_happ)

    #Validate happiness
    if request_happ < 50 or request_happ > 150:
        base = form_base_table_entry(tier_list)
        feedback = "Error: Happiness must be between 50% and 150%"
        
        #return render_template(f"profits.html",profits = base, entry = feedback)
        return None

    #Convert happiness to a multiplier where 1 = 100%
    request_happ = request_happ / 100

    print (request_happ)


    #Form query class from user input
    query = Query(request_city,request_happ)


    #Journal output percentages:
    #Basic enchantment: {"":1889/2000,"@1":100/2000,"@2":10/2000,"@3":1/2000
    #Gather: n of resources of same tier as labourer
    #Fishing: Complicated because of rare fish and zone types, may need to copy over or search the .xml
    #{"laborer type":[{dictionary of each enchantment of labourer material (key) with weighting (value)},laborer total weight]...}
    laborer_outputs = {"toolmaker": [{"planks":7556,"planks_level1@1":400,"planks_level2@2":40,"planks_level3@3":4,
                        "metalbar":3778,"metalbar_level1@1":200,"metalbar_level2@2":20,"metalbar_level3@3":2,
                        "cloth":3778,"cloth_level1@1":200,"cloth_level2@2":20,"cloth_level3@3":2,
                        "leather":1889,"leather_level1@1":100,"leather_level2@2":10,"leather_level3@3":1},18000],

        "warrior": [{"metalbar":13223,"metalbar_level1@1":700,"metalbar_level2@2":70,"metalbar_level3@3":7,
                        "planks":3778,"planks_level1@1":200,"planks_level2@2":20,"planks_level3@3":2,
                        "cloth":1889,"cloth_level1@1":100,"cloth_level2@2":10,"cloth_level3@3":1},20000],

        "mage": [{"cloth":9445,"cloth_level1@1":500,"cloth_level2@2":50,"cloth_level3@3":5,
                     "planks":7556,"planks_level1@1":400,"planks_level2@2":40,"planks_level3@3":4,
                     "metalbar":1889,"metalbar_level1@1":100,"metalbar_level2@2":10,"metalbar_level3@3":1},20000],

        "hunter": [{"leather":9445,"leather_level1@1":500,"leather_level2@2":50,"leather_level3@3":5,
                        "planks":5667,"planks_level1@1":300,"planks_level2@2":30,"planks_level3@3":3,
                        "metalbar":5667,"metalbar_level1@1":300,"metalbar_level2@2":30,"metalbar_level3@3":3},22000],

        "fiber":[{"fiber":1889,"fiber_level1@1":100,"fiber_level2@2":10,"fiber_level3@3":1},2000], 
        "wood":[{"wood":1889,"wood_level1@1":100,"wood_level2@2":10,"wood_level3@3":1},2000],  
        "stone":[{"rock":1889,"rock_level1@1":100,"rock_level2@2":10,"rock_level3@3":1},2000], 
        "ore":[{"ore":1889,"ore_level1@1":100,"ore_level2@2":10,"ore_level3@3":1},2000],  
        "hide":[{"hide":1889,"hide_level1@1":100,"hide_level2@2":10,"hide_level3@3":1},2000] 
        }

    base_materials = ["cloth","fiber","hide","leather","metalbar","ore","planks","rock","wood"]
    query.items = []


    for tier in tier_list:

        for item in base_materials:

            query.items.append(tier+"_"+item)

            if tier == "t3":
                continue

            else:
                query.items.append(tier+"_"+item+"_level1@1")
                query.items.append(tier+"_"+item+"_level2@2")
                query.items.append(tier+"_"+item+"_level3@3")

    #Produce a string for searching the albion data project. The search works best with items in ALL CAPS
    query.item_request_string = ",".join(query.items).upper()


    #Obtain prices for appropriate output items
    #current_price_search(query)
    current_price_search(query)


    #print (query.prices)
    print ('Test. T4_cloth in city is ' +str(query.prices['t4_cloth']) )


    #Multiply output prices with weightings for output type and enchantment
    base_loot_amounts = {"crafter":{"t3":24,"t4":16,"t5":8,"t6":5.333,"t7":4.4651,"t8":4.129},
                         "gatherer":{"t3":60,"t4":48,"t5":32,"t6":32,"t7":38.4,"t8":38.4},
                         "fisher":{}}

    #Establish ratios for each labourer from the laborer_outputs weighting values and total weightings
    for lab in lab_list:
        query.establish_ratios(laborer_outputs,lab)


    #Establish material sell values for each labourer and tier   
    for lab in lab_list:
        for tier in tier_list:
            query.material_sell(base_loot_amounts,lab,tier)



    #Obtain prices for empty and full journals
    #Create labourer list in the same order as journal market data outputs
    for tier in tier_list:
        for lab in lab_list:
            empty_book = tier+"_journal_"+lab+"_empty"
            full_book = tier+"_journal_"+lab+"_full"
            query.journals.append(empty_book)
            query.journals.append(full_book)

    #current_book_price_search(query)
    current_book_price_search(query)

    print ('Test. t6_journal_warrior_full in ' + query.city + ' is ' +str(query.journal_prices['t6_journal_warrior_full']) )



    #Calculate profit (Material sale + empty book sale - full book buy)
    for lab in lab_list:
        for tier in tier_list:
            query.calculate_profit(lab,tier)

    print ("Net profit for t6 toolmaker including 4.5% tax on sales is:" + str(query.profits["toolmaker"]["t6"]))



    #Prepare for sending data to front end
    #SHOUTOUT
    #print ("NEWBY IS RECRUITING")


    happiness_percent = str( (query.happiness*100) ) + "%"
    entry = "Results shown for City: " + query.city + ", at happiness: " + happiness_percent

    #Replace API labourer names with in-game names for front end

    query.profits["Cropper"] = query.profits.pop("fiber")
    query.profits["Gamekeeper"] = query.profits.pop("hide")
    query.profits["Fletcher"] = query.profits.pop("hunter")
    query.profits["Imbuer"] = query.profits.pop("mage")
    query.profits["Prospector"] = query.profits.pop("ore")
    query.profits["Stonecutter"] = query.profits.pop("stone")
    query.profits["Tinker"] = query.profits.pop("toolmaker")
    query.profits["Blacksmith"] = query.profits.pop("warrior")
    query.profits["Lumberjack"] = query.profits.pop("wood")

    result = []
    
    for lab in query.profits.keys():
        
        lab_result = {}
        lab_result["lab"] = lab
        
        for tier,profit in query.profits[lab].items():
            
            lab_result[tier] = profit
            
        result.append(lab_result)
    
    #return render_template(f"profits.html",profits = query.profits, entry = entry)
    
    res = make_response(jsonify(result), 200)
    
    print (query.lack_enchanted)

    return res


@app.route("/profits")
def profit_page():
    
    base = form_base_table_entry(tier_list)
              
    return render_template("profits.html",profits = base,entry = "Please submit a request")


                         
@app.route("/payback", methods = ["GET","POST"])
def payback_page():       
    
    base = form_base_table_entry(tier_list)
    
    return render_template("payback.html",payback = base,entry = "Please submit a request")



@app.route("/")
def index():
    return redirect(url_for("profit_page"))



if __name__ == "__main__":
    app.run()
