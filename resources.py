#Establish static objects
tier_list = ["t3","t4","t5","t6","t7","t8"]
lab_list = ["fiber","fishing","hide","hunter","mage","ore","stone","toolmaker","warrior","wood"]

#Establish a list of the basic materials returned, to create a list of all materials for the API query
base_materials = ["cloth","fiber","hide","leather","metalbar","ore","planks","rock","wood"]

#Multiply output prices with weightings for output type and enchantment
base_loot_amounts = {"crafter":{"t3":24,"t4":16,"t5":8,"t6":5.333,"t7":4.4651,"t8":4.129},
                     "gatherer":{"t3":60,"t4":48,"t5":32,"t6":32,"t7":38.4,"t8":38.4},
                     "fisher":{"t2":9.6,"t3":8.976,"t4":12.9112,"t5":16.0301,"t6":19.0528,"t7":21.3876,"t8":24.119}}

#Dictionary of the happinesses of a house and furniture of a tier. 
    #I.e. a t4 house with t4 bed,t4 table, and trophies up to t4 gives 415 happiness for a CRAFTER
happ_dict= {"crafter":{"t2":205,"t3":310,"t4":415,"t5":520,"t6":625,"t7":730,"t8":835},
            "gatherer":{"t2":210,"t3":320,"t4":430,"t5":540,"t6":650,"t7":760,"t8":870},
            "fisher":{"t2":210,"t3":320,"t4":430,"t5":540,"t6":650,"t7":760,"t8":870}}
            #Note fishers have the same happiness as gatherer here, there are fishing trophies


#Journal output percentages:
#Basic enchantment: {"":1889/2000,"@1":100/2000,"@2":10/2000,"@3":1/2000
#Gather: n of resources of same tier as labourer
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
