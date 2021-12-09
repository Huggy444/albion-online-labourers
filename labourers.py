#Imports
import requests
import ujson
import datetime
from flask import Flask, redirect, url_for, render_template, request, jsonify, make_response
import time
from resources import tier_list,lab_list,base_materials,base_loot_amounts,happ_dict,laborer_outputs
#Classes
class Query():

    def __init__(self,city,happiness,house):
        self.city = city
        self.happ = happiness
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
        self.house = house
        self.fish_prices = {}

        #Establish the date x days ago, to output x daily price results
        today = datetime.datetime.today()
        week_delta = datetime.timedelta(days = 1)
        self.search_date = today - week_delta
        self.search_date = self.search_date.date()


    def establish_ratios(self,laborer_outputs,lab):
        #Divide according to weightings
        self.lab_ratios[lab]={}
        for key,weighting in laborer_outputs[lab][0].items():
            ratio = weighting / laborer_outputs[lab][1]
            self.lab_ratios[lab][key] = ratio

        self.profits[lab] = {}

    def establish_fishing_ratios(self,fishing_outputs,tier_list):
        #Divide according to weightings
        self.lab_ratios["fishing"]={}
        for tier in tier_list:
            self.lab_ratios["fishing"][tier]={}
            for key,weighting in fishing_outputs[tier][0].items():
                ratio = weighting / fishing_outputs[tier][1]
                self.lab_ratios["fishing"][tier][key] = ratio
        self.profits["fishing"] = {}


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

        if lab != "fishing":
            #establish tiered item names and sell value for each item, then sum to labourer total resource sell value
            for item,ratio in self.lab_ratios[lab].items():
                tiered_item = tier+"_"+item
                price = self.prices[tiered_item]
                #Identify where the price of non-enchanted materials i not available -> set journal profit to N/A
                if enchantment == 0:
                    if price == 0:
                        self.profits[lab][tier] = ""
                        break

                #Identify where the price of enchanted materials is not available -> add a "+"" symbol to the profit later
                if enchantment != 0:
                    if price == 0:
                        print (tiered_item)
                        self.lack_enchanted[lab+tier]=True
                        #self.profits[lab][tier] = "N/A"
                        #break
                quantity = ratio*base_loot_amounts[lab_type][tier]
                sellvalue = quantity*price
                enchantment += 1

                self.profits[lab][tier]+=sellvalue

                if tier == "t3":
                    break

        elif lab == "fishing":
            for item,ratio in self.lab_ratios[lab][tier].items():
                price = self.prices[item]
#                 if price == 0:
#                     self.profits[lab][tier] = ""
#                     break
                quantity = ratio*base_loot_amounts[lab_type][tier]
                sellvalue = quantity*price   
                self.profits[lab][tier]+=sellvalue

        ###Account for happiness (happiness HTML entry can post to carrying out this function if API prices are cached)
        happ = self.calculate_happiness(lab,tier,lab_type)
        #print(f"{lab}, for {self.house} house, with {tier} journal, happiness ratio = {happ}")
        #If happiness was < 50% it was instead set to 0 as labs will not work under 50%. Turn that into an N/A output.
        try:
            if happ != 0 and self.profits[lab][tier] != "":
                self.profits[lab][tier] = self.profits[lab][tier]*happ
            elif happ == 0:
                self.profits[lab][tier] = ""
        except:
            print(happ)
            print(type(happ))
            print(self.profits[lab][tier])
            print(type(self.profits[lab][tier]))

    def calculate_profit(self,lab,tier):
        empty_price = self.journal_prices[tier+"_journal_"+lab+"_empty"]
        full_price = self.journal_prices[tier+"_journal_"+lab+"_full"]
        if isinstance(self.profits[lab][tier], str):
            return

        #Sales tax
        self.profits[lab][tier] = self.profits[lab][tier]*0.955
        #Add empty book value after tax
        if empty_price == 0:
            print (lab + tier + "empty , no price")
            self.profits[lab][tier] = ""
            return
        self.profits[lab][tier] += empty_price*0.955
        #Subract full book value
        if full_price == 0:
            print (lab + tier + "full , no price")
            self.profits[lab][tier] = ""
            return
        self.profits[lab][tier] -= full_price

        self.profits[lab][tier] = str(round(self.profits[lab][tier]))

        if self.lack_enchanted[lab+tier] == True:
            self.profits[lab][tier] += "+"

        #if self.journal_values["empty"] == 0: 
            #zero_price(self,empty_book)
        #if self.journal_values["full"] == 0:
            #zero_price(self,full_book)

    def calculate_happiness(self,lab,tier,lab_type):
        #For if the request was made with HAPPINESS:
        if self.house == None:
            return float(self.happ)
        #For if the request was made with HOUSE TIER:
        if self.happ == None:
            #Remove the "T" to get the number of the tier for the house and examined labourer
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

    def item_appending(self, tier_list, base_materials):
        for tier in tier_list:

            for item in base_materials:

                self.items.append(tier+"_"+item)

                if tier == "t3":
                    continue

                else:
                    self.items.append(tier+"_"+item+"_level1@1")
                    self.items.append(tier+"_"+item+"_level2@2")
                    self.items.append(tier+"_"+item+"_level3@3")


    def journal_appending(self,tier_list,lab_list):
        #Create labourer list in the same order as journal market data outputs
        for tier in tier_list:
            for lab in lab_list:
                empty_book = tier+"_journal_"+lab+"_empty"
                full_book = tier+"_journal_"+lab+"_full"
                self.journals.append(empty_book)
                self.journals.append(full_book)

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

    def create_response(self):
        result = []

        for lab in self.profits.keys():

            lab_result = {}
            lab_result["lab"] = lab

            for tier,profit in self.profits[lab].items():

                lab_result[tier] = profit

            result.append(lab_result)

        res = make_response(jsonify(result), 200)

        return res


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

    print (query.city)
    if query.city != "Bridgewatch,Caerleon,Fort Sterling,Lymhurst,Martlock,Thetford":
        for json in text:
            price = json["sell_price_min"]
            item = json["item_id"].lower()
            #Sanitise prices very badly. t8 level 3 prices cap out around 350k, use 500k as cut off for real values.
            if price < 500000:
                query.prices[item]=price
            else:
                query.prices[item]=0
    else:
        for i in range(0,len(text),6):
            count = 0
            item = text[i]["item_id"].lower()
            query.prices[item] = 0
            for json in text[i:i+6]:
                new_price = json["sell_price_min"]
                #print (json["item_id"]+str(new_price))
                if new_price > 500000 or new_price == 0:
                    continue
                else:
                    query.prices[item] += new_price
                    count += 1
            try:
                query.prices[item] = query.prices[item] / count
            except ZeroDivisionError:
                query.prices[item] = 0
            #print (query.prices[item])

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

    if query.city != "Bridgewatch,Caerleon,Fort Sterling,Lymhurst,Martlock,Thetford":
        for index,book in enumerate(query.journals):
            price = text[index]["sell_price_min"]
            if price < 500000:
                query.journal_prices[book] = price
            else:
                query.journal_prices[book] = 0


    else:
        for i in range(0,len(text),6):
            count = 0
            book = text[i]["item_id"].lower()
            query.journal_prices[book] = 0       
            for json in text[i:i+6]:
                new_price = json["sell_price_min"]
                #print (json["item_id"]+" "+str(new_price))
                if new_price > 500000 or new_price == 0:
                    continue
                else:
                    query.journal_prices[book] += new_price
                    count += 1
            try:        
                query.journal_prices[book] = query.journal_prices[book] / count
            except ZeroDivisionError:
                query.journal_prices[book] = 0
            #print (query.journal_prices[book])

#     print (query.journals)
#     print (text)
#     print (query.journal_prices) 

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

def main_process(query):
    #Populate query with every material that can be returned from labourers (excluding journals)
    query.items = []
    query.item_appending(tier_list,base_materials)
    #Add fish to the items list
    fish_list = form_fish_list()
    for fish in fish_list:
        query.items.append(fish)

    #Produce a string for searching the albion data project. The search works best with items in ALL CAPS
    query.item_request_string = ",".join(query.items).upper()

    #Obtain prices for appropriate output items
    current_price_search(query)
    print ('Test. T4_cloth in city is ' +str(query.prices['t4_cloth']) )

    #Establish ratios for each labourer from the laborer_outputs weighting values and total weightings
    fishing_outputs = form_fishing_outputs(fish_list,False)
    for lab in lab_list:
        if lab != "fishing":
            query.establish_ratios(laborer_outputs,lab)
        elif lab == "fishing":
            query.establish_fishing_ratios(fishing_outputs,tier_list)

    #Establish material sell values for each labourer and tier   
    for lab in lab_list:
        for tier in tier_list:
            query.material_sell(base_loot_amounts,lab,tier)

    #Obtain prices for empty and full journals
    query.journal_appending(tier_list,lab_list)

    #current_book_price_search(query)
    current_book_price_search(query)
    print ('Test. t6_journal_warrior_full in ' + query.city + ' is ' +str(query.journal_prices['t6_journal_warrior_full']) )

    #Calculate profit (Material sale + empty book sale - full book buy)
    for lab in lab_list:
        for tier in tier_list:
            query.calculate_profit(lab,tier)
    print ("Net profit for t6 toolmaker including 4.5% tax on sales is:" + str(query.profits["toolmaker"]["t6"]))

    #Prepare for sending data to front end
    query.rename_labs()

    #Create the Fetch response to send back to front end
    res = query.create_response()

    return res

def form_fish_list():

    fish_list = []

    for f_type in fish_types:
        if "common" in f_type:
            for tier in ["t1","t2","t3","t4","t5","t6","t7","t8"]:
                fish_list.append(tier +"_"+f_type)
        if "rare" in f_type:
            for tier in ["t3","t5","t7"]:
                fish_list.append(tier +"_"+f_type)
    #fish_list documentation: index 0-7 = fresh common, 8-15 = salt common, 16-18 = forest rare, 19-21 = mountain rare
        #22-24 = highlands rare, 25-27 = steppe rare, 28-30 = swamp rare, 31-33 = salt rare

    return fish_list

def form_fishing_outputs(fish_list,include_t2):
    #Setting the fish that are output from fishing journals of each tier, and the weighting for each fish

    fishing_outputs = {
        "t3":[{fish_list[0]:5,fish_list[1]:5,fish_list[2]:5,fish_list[8]:5,fish_list[9]:5,fish_list[10]:5,
            fish_list[16]:1,fish_list[19]:1,fish_list[22]:1,fish_list[25]:1,fish_list[28]:1,fish_list[31]:1
            },36],
        "t4":[{fish_list[1]:5,fish_list[2]:5,fish_list[3]:5,fish_list[9]:5,fish_list[10]:5,fish_list[11]:5,
            fish_list[16]:1,fish_list[19]:1,fish_list[22]:1,fish_list[25]:1,fish_list[28]:1,fish_list[31]:1
            },36],
        "t5":[{fish_list[2]:10,fish_list[3]:10,fish_list[4]:10,fish_list[10]:10,fish_list[11]:10,fish_list[12]:10,
            fish_list[16]:1,fish_list[19]:1,fish_list[22]:1,fish_list[25]:1,fish_list[28]:1,fish_list[31]:1,
            fish_list[17]:1,fish_list[20]:1,fish_list[23]:1,fish_list[26]:1,fish_list[29]:1,fish_list[32]:1
            },42],   
        "t6":[{fish_list[3]:10,fish_list[4]:10,fish_list[5]:10,fish_list[11]:10,fish_list[12]:10,fish_list[13]:10,
            fish_list[16]:1,fish_list[19]:1,fish_list[22]:1,fish_list[25]:1,fish_list[28]:1,fish_list[31]:1,
            fish_list[17]:1,fish_list[20]:1,fish_list[23]:1,fish_list[26]:1,fish_list[29]:1,fish_list[32]:1
            },42],
        "t7":[{fish_list[4]:15,fish_list[5]:15,fish_list[6]:15,fish_list[12]:15,fish_list[13]:15,fish_list[14]:15,
            fish_list[16]:1,fish_list[19]:1,fish_list[22]:1,fish_list[25]:1,fish_list[28]:1,fish_list[31]:1,
            fish_list[17]:1,fish_list[20]:1,fish_list[23]:1,fish_list[26]:1,fish_list[29]:1,fish_list[32]:1,
            fish_list[18]:1,fish_list[21]:1,fish_list[24]:1,fish_list[27]:1,fish_list[30]:1,fish_list[33]:1
            },108],
        "t8":[{fish_list[5]:15,fish_list[6]:15,fish_list[7]:15,fish_list[13]:15,fish_list[14]:15,fish_list[15]:15,
            fish_list[16]:1,fish_list[19]:1,fish_list[22]:1,fish_list[25]:1,fish_list[28]:1,fish_list[31]:1,
            fish_list[17]:1,fish_list[20]:1,fish_list[23]:1,fish_list[26]:1,fish_list[29]:1,fish_list[32]:1,
            fish_list[18]:1,fish_list[21]:1,fish_list[24]:1,fish_list[27]:1,fish_list[30]:1,fish_list[33]:1
            },108] 
                      }
    #t2 journals are included for the fishing gathering page but not the labourer profit pages
    if include_t2 == True:

        fishing_outputs["t2"] = [{fish_list[0]:1,fish_list[1]:1,fish_list[8]:1,fish_list[9]:1},4]

    return fishing_outputs


#Fishing: Complicated because of rare fish and zone types, may need to copy over or search the .xml
#Common fish go from tiers 1 to 8. Journals (t2 to t8) reward common fish of -2,-1,0 of the current tier.
fish_types = ["fish_freshwater_all_common","fish_saltwater_all_common","fish_freshwater_forest_rare",
            "fish_freshwater_mountain_rare","fish_freshwater_highlands_rare","fish_freshwater_steppe_rare",
            "fish_freshwater_swamp_rare","fish_saltwater_all_rare"]

@app.route("/happiness/results", methods=["POST"])
def create_entry_happ():

    #Recieve the fetch request and save the form JSON to var req
    req = request.get_json()
    print(req)

    ##Pull city from fetch
    request_city = req["city"].lower()
    print(request_city)
    #Validate city
    if request_city == "Please select a city...":
        return None
    elif request_city == "all":
        request_city = "Bridgewatch,Caerleon,Fort Sterling,Lymhurst,Martlock,Thetford"

    ##Pull happiness from fetch
    request_happ = req["happ"].lower()
    if request_happ == "":
        request_happ = "100"
    request_happ = float(request_happ)
    #Validate happiness
    if request_happ < 50 or request_happ > 150:
        return None
    #Convert happiness to a multiplier where 1 = 100%
    request_happ = request_happ / 100
    print (request_happ)

    #Form query class from user input
    query = Query(city = request_city, happiness = request_happ, house = None)

    #Perform the main API search and Fetch response function
    res = main_process(query)
    return res


@app.route("/happiness")
def happ_page():

    return render_template("happiness.html")


@app.route("/house/results", methods=["POST"])
def create_entry_house():

    #Recieve the fetch request and save the form JSON to var req
    req = request.get_json()
    print(req)

    ##Pull city from fetch
    request_city = req["city"].lower()
    print(request_city)
    #Validate city
    if request_city == "Please select a city...":
        return None
    elif request_city == "all":
        request_city = "Bridgewatch,Caerleon,Fort Sterling,Lymhurst,Martlock,Thetford"

    ##Pull house tier from fetch
    request_house = req["house"].lower()
    print (request_house)
    #Validate house tier
    if request_house == "Please select a tier...":
        return None

    #Form query class from user input
    query = Query(city = request_city, house = request_house, happiness = None)

    #Perform the main API search and Fetch response function
    res = main_process(query)
    return res

@app.route("/house")
def house_page():

    #Pull prices for materials and journals, send to HTML with page load return
    #

    return render_template("house.html")

@app.route("/fish")
def fish_page():

    #Use the fish functions to determine the best profit/fame for filling different fishing journals
    fish_list = form_fish_list()
    fishing_outputs = form_fishing_outputs(fish_list,True)
    #print (fishing_outputs["t4"][0])

    #Options: 1) Running the journal, buying and selling everything from 1 city. 2) Filling empty journal and selling full.
        #Do with checkboxes, and have more and drop downs for other stuff too,
        #Chopping all fish,buying empty journals from a labourer etc.
        #Maybe 1 dropdown for empty, 1 dropdown for full





@app.route("/payback", methods = ["GET","POST"])
def payback_page():       

    base = form_base_table_entry(tier_list)

    return render_template("payback.html",payback = base,entry = "Please submit a request")


@app.route("/")
def index():
   return redirect(url_for("house_page"))

if __name__ == "__main__":
    app.run()
