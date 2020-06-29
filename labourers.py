#Imports
import requests
import ujson
from flask import Flask, redirect, url_for, render_template, request

#Classes
class Query():
    
    def __init__(self,lab,city,tier,happiness=1):
        self.lab = lab
        self.city = city
        self.tier = tier
        self.happiness = happiness
        self.items = []
        self.prices = []
        self.quantities = []
        self.item_request_string = ""
        self.sell_value = 0
        self.journal_values = {}
        self.profit = 0
        self.zero_prices = []
        
    def establish_quantities(self,base_loot_amounts,laborer_outputs):
        #Take base quantity for tier and labourer type
        if self.lab in ["toolmaker","hunter","mage","warrior"]:
            lab_type = "crafter"
        elif self.lab in ["fiber","wood","stone","ore","hide"]:
            lab_type = "gatherer"
        elif self.lab == "fishing":
            lab_type = "fisher"
        base_output = base_loot_amounts[lab_type][self.tier]
        output = base_output * self.happiness
        
        #Divide according to weightings
        for item in self.items:
            item_detiered = item[3:].lower()
            weighting = laborer_outputs[self.lab][0][item_detiered] / laborer_outputs[self.lab][1]
            self.quantities.append(weighting*output)
        
    def material_sell(self):
        for index,item in enumerate(self.quantities):
            if self.prices[index] == 0:
                zero_price(self.items[index])
            self.sell_value+= item*self.prices[index]
    
    def calculate_profit(self,empty_book,full_book):
        self.profit += self.sell_value*0.955
        self.profit += self.journal_values["empty"]*0.955
        self.profit -= self.journal_values["full"]
        if self.journal_values["empty"] == 0: 
            zero_price(self,empty_book)
        if self.journal_values["full"] == 0:
            zero_price(self,full_book)
#Functions
def zero_price(query,item):
    self.zero_prices.append(item)
    print (f"One of the materials or journals currently has no listed price on the city market. {item}")

app = Flask(__name__)

@app.route("/", methods = ["POST","GET"])
def home():
    
    if request.method == "POST":
        
                #Take user input and validate
        ######Expand for multiple labourers
        ##Validate laborer type
        #while True:
        #request_lab =  input("Please request a labourer type: ").lower()
        
        request_lab = request.form["lab"].lower()

        ####Convert in-game lab names to api ID names
        if request_lab == "tinker":
                request_lab = "toolmaker"
        elif request_lab == "imbuer":
                request_lab = "mage"
        elif request_lab == "blacksmith":
                request_lab = "warrior"
        elif request_lab == "fletcher":
                request_lab = "hunter"

        elif request_lab == "cropper":
                request_lab = "fiber"
        elif request_lab == "lumberjack":
                request_lab = "wood"
        elif request_lab == "stonecutter":
                request_lab = "stone"
        elif request_lab == "prospector":
                request_lab = "ore"
        elif request_lab == "gamekeeper":
                request_lab = "hide"

        elif request_lab == "fisherman":
                request_lab = "fishing"

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
        request_city = request.form["city"].lower()


        ######Expand for multiple tiers        
        ##Validate tier
        #while True:
            #request_tier = input("Please select a labourer tier (T3 to T8: ").lower()
            #if request_tier not in ["t3","t4","t5","t6","t7","t8"]:
                #print ("Invalid tier.")
            #else:
                #break
        request_tier = request.form["tier"].lower()  

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
        request_happ = int(request.form["happ"])
        
        #Convert happiness to a multiplier where 1 = 100%
        request_happ = request_happ / 100

        #Form query class from user input
        query = Query(request_lab,request_city,request_tier,request_happ)



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


        #Create items to search for from labourer type and tier
        #request.items[index*4] = request.tier.upper()+"_"+item.upper()
        #request.items[(index*4)+1] = request.tier.upper()+"_"+item.upper()+"_level1@1"
        #request.items[(index*4)+2] = request.tier.upper()+"_"+item.upper()+"_level2@2"
        #request.items[(index*4)+3] = request.tier.upper()+"_"+item.upper()+"_level3@3"
        for index,item in enumerate(list(laborer_outputs[query.lab][0].keys())):
            query.items.append(query.tier.upper()+"_"+item.upper())
        query.item_request_string = ",".join(query.items)
        print (query.items)
        ###print (request.item_request_string)


        #Obtain prices for appropriate output items
        result = requests.get(f"https://www.albion-online-data.com/api/v2/stats/prices/{query.item_request_string}?locations={query.city}")
        text = ujson.loads(result.text)


        #Assign item prices to parameter and align with items
        for item in query.items:

            for index,dic in enumerate(text):

                #print (dic.values())
                if item in dic.values():
                    price = text[index]["sell_price_min"]
                    query.prices.append(price)

        print (query.prices)


        #Multiply output prices with weightings for output type and enchantment
        #base_loot_amounts = {"toolmaker":{},"mage","warrior","hunter","fiber","wood","stone","hide","fishing"}
        base_loot_amounts = {"crafter":{"t3":24,"t4":16,"t5":8,"t6":5.333,"t7":4.4651,"t8":4.129},
                             "gatherer":{"t3":60,"t4":48,"t5":32,"t6":32,"t7":38.4,"t8":38.4},
                             "fisher":{}}

        query.establish_quantities(base_loot_amounts,laborer_outputs)
        ###print (request.quantities)  

        query.material_sell()
        print (f"Materials sell for: {query.sell_value}")

        #Obtain prices for empty and full journals
        empty_book = query.tier+"_journal_"+query.lab+"_empty"
        full_book = query.tier+"_journal_"+query.lab+"_full"
        book_search = empty_book.upper()+","+full_book.upper()

        result = requests.get(f"https://www.albion-online-data.com/api/v2/stats/prices/{book_search}?locations={query.city}&qualities=")
        text = ujson.loads(result.text)

        query.journal_values["empty"] = (text[0]["sell_price_min"])
        query.journal_values["full"]  = (text[1]["sell_price_min"])

        print(f"Empty journal sells for: {query.journal_values['empty']}")
        print(f"Full journal costs: {query.journal_values['full']}")

        #Calculate profit (Material sale + empty book sale - full book buy)
        query.calculate_profit(empty_book, full_book)
        print (f"Net profit including 4.5% tax on sales is: {round(query.profit)}")


        #####SHOUTOUT
        #print ("NEWBY IS RECRUITING")
              
              
        if len(query.zero_prices) > 0:
              zero_price_string = ",".join(query.zero_prices)
        else:
              zero_price_string = ""
        
        return render_template(f"home.html",profit = round(query.profit),if_zero = zero_price_string)
    
    else:
              
        return render_template("home.html",profit = "Please enter journal information.", if_zero = "")
                               
              
if __name__ == "__main__":
    app.run()
    
