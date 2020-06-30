#Imports
import requests
import ujson
from flask import Flask, redirect, url_for, render_template, request

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
        
        #establish tiered item names and sell value for each item, then sum to labourer total resource sell value
        for item,ratio in self.lab_ratios[lab].items():
            tiered_item = tier+"_"+item
            price = self.prices[tiered_item]
            if price == 0:
                self.profits[lab][tier] = "N/A"
                break
            quantity = ratio*base_loot_amounts[lab_type][tier]
            sellvalue = quantity*price
            
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
        
        #Account for happiness (happiness HTML entry can post to carrying out this function?)
        self.profits[lab][tier] = self.profits[lab][tier]*self.happiness
        #Sales tax
        self.profits[lab][tier] = self.profits[lab][tier]*0.955
        #Add empty book value after tax
        if empty_price == 0:
            self.profits[lab][tier] = "N/A"
            return
        self.profits[lab][tier] += empty_price*0.955
        #Subract full book value
        if full_price == 0:
            self.profits[lab][tier] = "N/A"
            return
        self.profits[lab][tier] -= full_price
        self.profits[lab][tier] = round(self.profits[lab][tier])
        
        #if self.journal_values["empty"] == 0: 
            #zero_price(self,empty_book)
        #if self.journal_values["full"] == 0:
            #zero_price(self,full_book)
            
            
            
            
#Functions
def zero_price(query,item):
    ##Change this to making the table entry for [lab][tier] a string saying N/A or something
    query.zero_prices.append(item)
    print (f"One of the materials or journals currently has no listed price on the city market. {item}")

app = Flask(__name__)

@app.route("/", methods = ["GET","POST"])
def home():
    
    tier_list = ["t3","t4","t5","t6","t7","t8"]
    lab_list = ["fiber","hide","hunter","mage","ore","stone","toolmaker","warrior","wood"]
    
    if request.method == "POST":
        
                #Take user input and validate
        ######Expand for multiple labourers
        ##Validate laborer type
        #while True:
        #request_lab =  input("Please request a labourer type: ").lower()
        
        #request_lab = request.form["labDropdown"].lower()

        ####Convert in-game lab names to api ID names
        #if request_lab == "tinker":
                #request_lab = "toolmaker"
        #elif request_lab == "imbuer":
                #request_lab = "mage"
        #elif request_lab == "blacksmith":
                #request_lab = "warrior"
        #elif request_lab == "fletcher":
                #request_lab = "hunter"

        #elif request_lab == "cropper":
                #request_lab = "fiber"
        #elif request_lab == "lumberjack":
                #request_lab = "wood"
        #elif request_lab == "stonecutter" or request_lab == "stone cutter":
                #request_lab = "stone"
        #elif request_lab == "prospector":
                #request_lab = "ore"
        #elif request_lab == "gamekeeper":
                #request_lab = "hide"

        #elif request_lab == "fisherman":
                #request_lab = "fishing"

        ######Check a valid name was obtained  
        #if request_lab in ["toolmaker","mage","warrior","hunter","fiber","wood","stone","ore","hide","fishing"]:
            #break
        #else: 
            #print ("Invalid labourer.")
            #continue


        ######Expand for multiple cities
        ##Validate city
        #while True:
            #request_city = input("Please select a city to check prices for: ").lower()
            #if request_city not in ["caerleon","bridgewatch","fort sterling","martlock","lymhurst","thetford"]:
                #print ("Invalid city.")
            #else:
                #break
        request_city = request.form["cityDropdown"].lower()
        print(request_city)


        ######Expand for multiple tiers        
        ##Validate tier
        #while True:
            #request_tier = input("Please select a labourer tier (T3 to T8: ").lower()
            #if request_tier not in ["t3","t4","t5","t6","t7","t8"]:
                #print ("Invalid tier.")
            #else:
                #break
        #request_tier = request.form["tierDropdown"].lower()

        #if request_tier == "tier 3" or request_tier == "3" or request_tier =="tier3":
            #request_tier = "t3"
        #elif request_tier == "tier 4" or request_tier == "4" or request_tier =="tier4":
            #request_tier = "t3"
        #elif request_tier == "tier 5" or request_tier == "5" or request_tier =="tier5":
            #request_tier = "t5"
        #elif request_tier == "tier 6" or request_tier == "6" or request_tier =="tier6":
            #request_tier = "t6"            
        #elif request_tier == "tier 7" or request_tier == "7" or request_tier =="tier7":
            #request_tier = "t7"
        #elif request_tier == "tier 8" or request_tier == "8" or request_tier =="tier8":
            #request_tier = "t8" 

        #print (request_tier)

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
        request_happ = request.form["happ"]
        
        if request_happ == "":
            request_happ = "100"
        
        request_happ = int(request_happ)
        
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

        #Create items to search for from labourer type and tier
        #request.items[index*4] = request.tier.upper()+"_"+item.upper()
        #request.items[(index*4)+1] = request.tier.upper()+"_"+item.upper()+"_level1@1"
        #request.items[(index*4)+2] = request.tier.upper()+"_"+item.upper()+"_level2@2"
        #request.items[(index*4)+3] = request.tier.upper()+"_"+item.upper()+"_level3@3"
        #Also remove enchanted items for T3 journals, as T3 items can not be enchanted.
        #for index,item in enumerate(list(laborer_outputs[query.lab][0].keys())):
            #if query.tier.lower() == "t3":
                #if "level" in item:
                    #continue
            #query.items.append(query.tier.upper()+"_"+item.upper())
        
    
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
        
        #print (query.items)
        #print (query.item_request_string)
        ###print (request.item_request_string)


        #Obtain prices for appropriate output items
        result = requests.get(f"https://www.albion-online-data.com/api/v2/stats/prices/{query.item_request_string}?locations={query.city}")
        text = ujson.loads(result.text)


        #Assign item prices to a dictionary with names lining up with the .items
        for index,item in enumerate(query.items):
            price = text[index]["sell_price_min"]
            query.prices[item]=price

            #for index,dic in enumerate(text):

                #print (dic.values())
                #if item in dic.values():
                    #price = text[index]["sell_price_min"]
                    #query.prices.append(price)

        #print (query.prices)
        print ('Test. T4_cloth in city is ' +str(query.prices['t4_cloth']) )
        

        #Multiply output prices with weightings for output type and enchantment
        #base_loot_amounts = {"toolmaker":{},"mage","warrior","hunter","fiber","wood","stone","hide","fishing"}
        base_loot_amounts = {"crafter":{"t3":24,"t4":16,"t5":8,"t6":5.333,"t7":4.4651,"t8":4.129},
                             "gatherer":{"t3":60,"t4":48,"t5":32,"t6":32,"t7":38.4,"t8":38.4},
                             "fisher":{}}
        
        #Establish ratios for each labourer from the laborer_outputs weighting values and total weightings
        for lab in lab_list:
            query.establish_ratios(laborer_outputs,lab)
    
        #print (query.lab_ratios)
        
        #Establish material sell values for each labourer and tier
              
        for lab in lab_list:
            for tier in tier_list:
                query.material_sell(base_loot_amounts,lab,tier)
              
 
        #print (f"Materials sell for: {query.sell_value}")

        #Obtain prices for empty and full journals
        #Create labourer list in the same order as journal market data outputs
        for tier in tier_list:
            for lab in lab_list:
                empty_book = tier+"_journal_"+lab+"_empty"
                full_book = tier+"_journal_"+lab+"_full"
                query.journals.append(empty_book)
                query.journals.append(full_book)
        
        #Produce a string for searching the albion data project. The search works best with items in ALL CAPS
        book_search = ",".join(query.journals).upper()
        
        #print(book_search)
                
        result = requests.get(f"https://www.albion-online-data.com/api/v2/stats/prices/{book_search}?locations={query.city}&qualities=")
        text = ujson.loads(result.text)
    
        for index,book in enumerate(query.journals):
            query.journal_prices[book] = text[index]["sell_price_min"]
            
        
        print ('Test. t6_journal_warrior_full in ' + query.city + ' is ' +str(query.journal_prices['t6_journal_warrior_full']) )
        #for index,book in enumerate(text):
            #if "empty" in text[index]["item_id"]:
                
        #query.journal_values["empty"] = (text[0]["sell_price_min"])
        #query.journal_values["full"]  = (text[1]["sell_price_min"])

        #print(f"Empty journal sells for: {query.journal_values['empty']}")
        #print(f"Full journal costs: {query.journal_values['full']}")

        
        
        
        #Calculate profit (Material sale + empty book sale - full book buy)
        for lab in lab_list:
            for tier in tier_list:
                query.calculate_profit(lab,tier)
                
        print ("Net profit for t6 toolmaker including 4.5% tax on sales is:" + str(query.profits["toolmaker"]["t6"]))

        #####SHOUTOUT
        #print ("NEWBY IS RECRUITING")
        
        happiness_percent = str( (query.happiness*100) ) + "%"
        entry = "City: " + query.city + ", at happiness: " + happiness_percent

        return render_template(f"home.html",profits = query.profits, entry = entry)

    
    else:
        
        base =  {}
        
        for lab in lab_list:
            base[lab] = {} 
            for tier in tier_list:
                base[lab][tier] = 0
              
        return render_template("home.html",profits = base,entry = "Please submit a request")
                               
              
if __name__ == "__main__":
    app.run()
