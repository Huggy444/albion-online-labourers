#Establish static objects
tier_list = ["t3","t4","t5","t6","t7","t8"]
t2_tier_list = ["t2","t3","t4","t5","t6","t7","t8"]
lab_list = ["fiber","fishing","hide","hunter","mage","ore","stone","toolmaker","warrior","wood"]
city_list = ["bridgewatch","caerleon","fort sterling","lymhurst","martlock","thetford"]

#Establish a list of the basic materials returned, to create a list of all materials for the API query
base_materials = ["cloth","fiber","hide","leather","metalbar","ore","planks","rock","wood"]

#Multiply output prices with weightings for output type and enchantment
base_loot_amounts = {"crafter":{"t3":24,"t4":16,"t5":8,"t6":5.333,"t7":4.4651,"t8":4.129},
                     "gatherer":{"t3":60,"t4":48,"t5":32,"t6":32,"t7":38.4,"t8":38.4},
                     "fisher":{"t2":10.6,"t3":9.976,"t4":13.9112,"t5":17.0301,"t6":20.0528,"t7":22.3876,"t8":25.119}}

#Dictionary of the happinesses of a house and furniture of a tier. 
#I.e. a t4 house with t4 bed,t4 table, and trophies up to t4 gives 415 happiness for a CRAFTER
#Note fishers have the same happiness as gatherer here, there are fishing trophies
happ_dict = {"crafter":{"t2":205,"t3":310,"t4":415,"t5":520,"t6":625,"t7":730,"t8":835},
            "gatherer":{"t2":215,"t3":330,"t4":445,"t5":560,"t6":675,"t7":780,"t8":885},
            "fisher":{"t2":215,"t3":330,"t4":445,"t5":560,"t6":675,"t7":780,"t8":885}}


#Journal output percentages:
#Basic enchantment: {"":1889/2000,"@1":100/2000,"@2":10/2000,"@3":1/2000} 
#Gather: n of resources of same tier as labourer
#{"laborer type":[{dictionary of each enchantment of labourer material (key) with weighting (value/total weight value)}}
lab_ratios = {"toolmaker": {"planks":7556/18000,"planks_level1@1":400/18000,"planks_level2@2":40/18000,"planks_level3@3":4/18000,
                    "metalbar":3778/18000,"metalbar_level1@1":200/18000,"metalbar_level2@2":20/18000,"metalbar_level3@3":2/18000,
                    "cloth":3778/18000,"cloth_level1@1":200/18000,"cloth_level2@2":20/18000,"cloth_level3@3":2/18000,
                    "leather":1889/18000,"leather_level1@1":100/18000,"leather_level2@2":10/18000,"leather_level3@3":1/18000},

    "warrior": {"metalbar":13223/20000,"metalbar_level1@1":700/20000,"metalbar_level2@2":70/20000,"metalbar_level3@3":7/20000,
                    "planks":3778/20000,"planks_level1@1":200/20000,"planks_level2@2":20/20000,"planks_level3@3":2/20000,
                    "cloth":1889/20000,"cloth_level1@1":100/20000,"cloth_level2@2":10/20000,"cloth_level3@3":1/20000},

    "mage": {"cloth":9445/20000,"cloth_level1@1":500/20000,"cloth_level2@2":50/20000,"cloth_level3@3":5/20000,
                 "planks":7556/20000,"planks_level1@1":400/20000,"planks_level2@2":40/20000,"planks_level3@3":4/20000,
                 "metalbar":1889/20000,"metalbar_level1@1":100/20000,"metalbar_level2@2":10/20000,"metalbar_level3@3":1/20000},

    "hunter": {"leather":9445/22000,"leather_level1@1":500/22000,"leather_level2@2":50/22000,"leather_level3@3":5/22000,
                    "planks":5667/22000,"planks_level1@1":300/22000,"planks_level2@2":30/22000,"planks_level3@3":3/22000,
                    "metalbar":5667/22000,"metalbar_level1@1":300/22000,"metalbar_level2@2":30/22000,"metalbar_level3@3":3/22000},

    "fiber":{"fiber":1889/2000,"fiber_level1@1":100/2000,"fiber_level2@2":10/2000,"fiber_level3@3":1/2000}, 
    "wood":{"wood":1889/2000,"wood_level1@1":100/2000,"wood_level2@2":10/2000,"wood_level3@3":1/2000},  
    "stone":{"rock":1889/2000,"rock_level1@1":100/2000,"rock_level2@2":10/2000,"rock_level3@3":1/2000}, 
    "ore":{"ore":1889/2000,"ore_level1@1":100/2000,"ore_level2@2":10/2000,"ore_level3@3":1/2000},  
    "hide":{"hide":1889/2000,"hide_level1@1":100/2000,"hide_level2@2":10/2000,"hide_level3@3":1/2000}}
    
fishing_ratios = {'t2': {'t1_seaweed':10/106,'t1_fish_freshwater_all_common': 24/106, 't2_fish_freshwater_all_common': 24/106, 't1_fish_saltwater_all_common': 24/106, 't2_fish_saltwater_all_common': 24/106},
                  
    't3': {'t1_seaweed':41/411, 't1_fish_freshwater_all_common': 50/411, 't2_fish_freshwater_all_common': 50/411, 't3_fish_freshwater_all_common': 50/411,
    't1_fish_saltwater_all_common': 50/411, 't2_fish_saltwater_all_common': 50/411, 't3_fish_saltwater_all_common': 50/411, 
    't3_fish_freshwater_forest_rare': 10/411, 't3_fish_freshwater_mountain_rare': 10/411, 't3_fish_freshwater_highlands_rare': 10/411, 't3_fish_freshwater_steppe_rare': 10/411, 't3_fish_freshwater_swamp_rare': 10/411, 't3_fish_saltwater_all_rare': 10/411,
    't3_fish_freshwater_avalon_rare': 10/411},
     
    't4': {'t1_seaweed':29/399, 't2_fish_freshwater_all_common': 50/399, 't3_fish_freshwater_all_common': 50/399, 't4_fish_freshwater_all_common': 50/399, 
    't2_fish_saltwater_all_common': 50/399, 't3_fish_saltwater_all_common': 50/399, 't4_fish_saltwater_all_common': 50/399, 
    't3_fish_freshwater_forest_rare': 10/399, 't3_fish_freshwater_mountain_rare': 10/399, 't3_fish_freshwater_highlands_rare': 10/399, 't3_fish_freshwater_steppe_rare': 10/399, 't3_fish_freshwater_swamp_rare': 10/399, 't3_fish_saltwater_all_rare': 10/399,
    't3_fish_freshwater_avalon_rare': 10/399},

    't5': {'t1_seaweed':46/786, 't3_fish_freshwater_all_common': 100/786, 't4_fish_freshwater_all_common': 100/786, 't5_fish_freshwater_all_common': 100/786, 
    't3_fish_saltwater_all_common': 100/786, 't4_fish_saltwater_all_common': 10/786, 't5_fish_saltwater_all_common': 100/786, 
    't3_fish_freshwater_forest_rare': 10/786, 't3_fish_freshwater_mountain_rare': 10/786, 't3_fish_freshwater_highlands_rare': 10/786, 't3_fish_freshwater_steppe_rare': 10/786, 't3_fish_freshwater_swamp_rare': 10/786, 't3_fish_saltwater_all_rare': 10/786, 
    't5_fish_freshwater_forest_rare': 10/786, 't5_fish_freshwater_mountain_rare': 10/786, 't5_fish_freshwater_highlands_rare': 10/786, 't5_fish_freshwater_steppe_rare': 10/786, 't5_fish_freshwater_swamp_rare': 10/786, 't5_fish_saltwater_all_rare': 10/786,
    't3_fish_freshwater_avalon_rare': 10/786, 't5_fish_freshwater_avalon_rare': 10/786},
     
    't6': {'t1_seaweed':39/779, 't4_fish_freshwater_all_common': 100/779, 't5_fish_freshwater_all_common': 100/779, 't6_fish_freshwater_all_common': 100/779, 
    't4_fish_saltwater_all_common': 100/779, 't5_fish_saltwater_all_common': 100/779, 't6_fish_saltwater_all_common': 100/779, 
    't3_fish_freshwater_forest_rare': 10/779, 't3_fish_freshwater_mountain_rare': 10/779, 't3_fish_freshwater_highlands_rare': 10/779, 't3_fish_freshwater_steppe_rare': 10/779, 't3_fish_freshwater_swamp_rare': 10/779, 't3_fish_saltwater_all_rare': 10/779, 
    't5_fish_freshwater_forest_rare': 10/779, 't5_fish_freshwater_mountain_rare': 10/779, 't5_fish_freshwater_highlands_rare': 10/779, 't5_fish_freshwater_steppe_rare': 10/779, 't5_fish_freshwater_swamp_rare': 10/779, 't5_fish_saltwater_all_rare': 10/779,
    't3_fish_freshwater_avalon_rare': 10/779, 't5_fish_freshwater_avalon_rare': 10/779},
     
    't7': {'t1_seaweed':52/1162, 't5_fish_freshwater_all_common': 150/1162, 't6_fish_freshwater_all_common': 150/1162, 't7_fish_freshwater_all_common': 150/1162, 
    't5_fish_saltwater_all_common': 150/1162, 't6_fish_saltwater_all_common': 150/1162, 't7_fish_saltwater_all_common': 150/1162, 
    't3_fish_freshwater_forest_rare': 10/1162, 't3_fish_freshwater_mountain_rare': 10/1162, 't3_fish_freshwater_highlands_rare': 10/1162, 't3_fish_freshwater_steppe_rare': 10/1162, 't3_fish_freshwater_swamp_rare': 10/1162, 't3_fish_saltwater_all_rare': 10/1162, 
    't5_fish_freshwater_forest_rare': 10/1162, 't5_fish_freshwater_mountain_rare': 10/1162, 't5_fish_freshwater_highlands_rare': 10/1162, 't5_fish_freshwater_steppe_rare': 10/1162, 't5_fish_freshwater_swamp_rare': 10/1162, 't5_fish_saltwater_all_rare': 10/1162, 
    't7_fish_freshwater_forest_rare': 10/1162, 't7_fish_freshwater_mountain_rare': 10/1162, 't7_fish_freshwater_highlands_rare': 10/1162, 't7_fish_freshwater_steppe_rare': 10/1162, 't7_fish_freshwater_swamp_rare': 10/1162, 't7_fish_saltwater_all_rare': 10/1162,
    't3_fish_freshwater_avalon_rare': 10/1162, 't5_fish_freshwater_avalon_rare': 10/1162, 't7_fish_freshwater_avalon_rare': 10/1162},
     
    't8': {'t1_seaweed':46/1156, 't6_fish_freshwater_all_common': 150/1156, 't7_fish_freshwater_all_common': 150/1156, 't8_fish_freshwater_all_common': 150/1156, 
    't6_fish_saltwater_all_common': 150/1156, 't7_fish_saltwater_all_common': 150/1156, 't8_fish_saltwater_all_common': 150/1156, 
    't3_fish_freshwater_forest_rare': 10/1156, 't3_fish_freshwater_mountain_rare': 10/1156, 't3_fish_freshwater_highlands_rare': 10/1156, 't3_fish_freshwater_steppe_rare': 10/1156, 't3_fish_freshwater_swamp_rare': 10/1156, 't3_fish_saltwater_all_rare': 10/1156, 
    't5_fish_freshwater_forest_rare': 10/1156, 't5_fish_freshwater_mountain_rare': 10/1156, 't5_fish_freshwater_highlands_rare': 10/1156, 't5_fish_freshwater_steppe_rare': 10/1156, 't5_fish_freshwater_swamp_rare': 10/1156, 't5_fish_saltwater_all_rare': 10/1156, 
    't7_fish_freshwater_forest_rare': 10/1156, 't7_fish_freshwater_mountain_rare': 10/1156, 't7_fish_freshwater_highlands_rare': 10/1156, 't7_fish_freshwater_steppe_rare': 10/1156, 't7_fish_freshwater_swamp_rare': 10/1156, 't7_fish_saltwater_all_rare': 10/1156,
    't3_fish_freshwater_avalon_rare': 10/1156, 't5_fish_freshwater_avalon_rare': 10/1156, 't7_fish_freshwater_avalon_rare': 10/1156}}

seaweed_quant = {"t2":1,"t3":1,"t4":2,"t5":4,"t6":6,"t7":9,"t8":14}

#Fishing: Complicated because of rare fish and zone types, may need to copy over or search the .xml
#Common fish go from tiers 1 to 8. Journals (t2 to t8) reward common fish of -2,-1,0 of the current tier.
fish_types = ["fish_freshwater_all_common","fish_saltwater_all_common","fish_freshwater_forest_rare",
            "fish_freshwater_mountain_rare","fish_freshwater_highlands_rare","fish_freshwater_steppe_rare",
            "fish_freshwater_swamp_rare","fish_saltwater_all_rare"]

items = ['t3_cloth', 't3_fiber', 't3_hide', 't3_leather', 't3_metalbar', 't3_ore', 't3_planks', 't3_rock', 't3_wood',
 't4_cloth', 't4_cloth_level1@1', 't4_cloth_level2@2', 't4_cloth_level3@3', 't4_fiber', 't4_fiber_level1@1', 't4_fiber_level2@2', 't4_fiber_level3@3', 
 't4_hide', 't4_hide_level1@1', 't4_hide_level2@2', 't4_hide_level3@3', 't4_leather', 't4_leather_level1@1', 't4_leather_level2@2', 't4_leather_level3@3', 
 't4_metalbar', 't4_metalbar_level1@1', 't4_metalbar_level2@2', 't4_metalbar_level3@3', 't4_ore', 't4_ore_level1@1', 't4_ore_level2@2', 't4_ore_level3@3', 
 't4_planks', 't4_planks_level1@1', 't4_planks_level2@2', 't4_planks_level3@3', 't4_rock', 't4_rock_level1@1', 't4_rock_level2@2', 't4_rock_level3@3', 
 't4_wood', 't4_wood_level1@1', 't4_wood_level2@2', 't4_wood_level3@3', 't5_cloth', 't5_cloth_level1@1', 't5_cloth_level2@2', 't5_cloth_level3@3', 
 't5_fiber', 't5_fiber_level1@1', 't5_fiber_level2@2', 't5_fiber_level3@3', 't5_hide', 't5_hide_level1@1', 't5_hide_level2@2', 't5_hide_level3@3', 
 't5_leather', 't5_leather_level1@1', 't5_leather_level2@2', 't5_leather_level3@3', 't5_metalbar', 't5_metalbar_level1@1', 't5_metalbar_level2@2', 't5_metalbar_level3@3', 
 't5_ore', 't5_ore_level1@1', 't5_ore_level2@2', 't5_ore_level3@3', 't5_planks', 't5_planks_level1@1', 't5_planks_level2@2', 't5_planks_level3@3', 
 't5_rock', 't5_rock_level1@1', 't5_rock_level2@2', 't5_rock_level3@3', 't5_wood', 't5_wood_level1@1', 't5_wood_level2@2', 't5_wood_level3@3', 
 't6_cloth', 't6_cloth_level1@1', 't6_cloth_level2@2', 't6_cloth_level3@3', 't6_fiber', 't6_fiber_level1@1', 't6_fiber_level2@2', 't6_fiber_level3@3', 
 't6_hide', 't6_hide_level1@1', 't6_hide_level2@2', 't6_hide_level3@3', 't6_leather', 't6_leather_level1@1', 't6_leather_level2@2', 't6_leather_level3@3', 
 't6_metalbar', 't6_metalbar_level1@1', 't6_metalbar_level2@2', 't6_metalbar_level3@3', 't6_ore', 't6_ore_level1@1', 't6_ore_level2@2', 't6_ore_level3@3', 
 't6_planks', 't6_planks_level1@1', 't6_planks_level2@2', 't6_planks_level3@3', 't6_rock', 't6_rock_level1@1', 't6_rock_level2@2', 't6_rock_level3@3', 
 't6_wood', 't6_wood_level1@1', 't6_wood_level2@2', 't6_wood_level3@3', 't7_cloth', 't7_cloth_level1@1', 't7_cloth_level2@2', 't7_cloth_level3@3', 
 't7_fiber', 't7_fiber_level1@1', 't7_fiber_level2@2', 't7_fiber_level3@3', 't7_hide', 't7_hide_level1@1', 't7_hide_level2@2', 't7_hide_level3@3', 
 't7_leather', 't7_leather_level1@1', 't7_leather_level2@2', 't7_leather_level3@3', 't7_metalbar', 't7_metalbar_level1@1', 't7_metalbar_level2@2', 't7_metalbar_level3@3', 
 't7_ore', 't7_ore_level1@1', 't7_ore_level2@2', 't7_ore_level3@3', 't7_planks', 't7_planks_level1@1', 't7_planks_level2@2', 't7_planks_level3@3', 
 't7_rock', 't7_rock_level1@1', 't7_rock_level2@2', 't7_rock_level3@3', 't7_wood', 't7_wood_level1@1', 't7_wood_level2@2', 't7_wood_level3@3', 
 't8_cloth', 't8_cloth_level1@1', 't8_cloth_level2@2', 't8_cloth_level3@3', 't8_fiber', 't8_fiber_level1@1', 't8_fiber_level2@2', 't8_fiber_level3@3', 
 't8_hide', 't8_hide_level1@1', 't8_hide_level2@2', 't8_hide_level3@3', 't8_leather', 't8_leather_level1@1', 't8_leather_level2@2', 't8_leather_level3@3', 
 't8_metalbar', 't8_metalbar_level1@1', 't8_metalbar_level2@2', 't8_metalbar_level3@3', 't8_ore', 't8_ore_level1@1', 't8_ore_level2@2', 't8_ore_level3@3', 
 't8_planks', 't8_planks_level1@1', 't8_planks_level2@2', 't8_planks_level3@3', 't8_rock', 't8_rock_level1@1', 't8_rock_level2@2', 't8_rock_level3@3', 
 't8_wood', 't8_wood_level1@1', 't8_wood_level2@2', 't8_wood_level3@3', 't1_seaweed', 't1_fish_freshwater_all_common', 't2_fish_freshwater_all_common', 't3_fish_freshwater_all_common', 
 't4_fish_freshwater_all_common', 't5_fish_freshwater_all_common', 't6_fish_freshwater_all_common', 't7_fish_freshwater_all_common', 't8_fish_freshwater_all_common', 
 't1_fish_saltwater_all_common', 't2_fish_saltwater_all_common', 't3_fish_saltwater_all_common', 't4_fish_saltwater_all_common', 't5_fish_saltwater_all_common', 
 't6_fish_saltwater_all_common', 't7_fish_saltwater_all_common', 't8_fish_saltwater_all_common', 't3_fish_freshwater_forest_rare', 't5_fish_freshwater_forest_rare', 
 't7_fish_freshwater_forest_rare', 't3_fish_freshwater_mountain_rare', 't5_fish_freshwater_mountain_rare', 't7_fish_freshwater_mountain_rare', 't3_fish_freshwater_highlands_rare', 
 't5_fish_freshwater_highlands_rare', 't7_fish_freshwater_highlands_rare', 't3_fish_freshwater_steppe_rare', 't5_fish_freshwater_steppe_rare', 't7_fish_freshwater_steppe_rare', 
 't3_fish_freshwater_swamp_rare', 't5_fish_freshwater_swamp_rare', 't7_fish_freshwater_swamp_rare', 't3_fish_saltwater_all_rare', 't5_fish_saltwater_all_rare', 't7_fish_saltwater_all_rare',
 't3_fish_freshwater_avalon_rare', 't5_fish_freshwater_avalon_rare', 't7_fish_freshwater_avalon_rare']

journals = ['t3_journal_fiber_empty', 't3_journal_fiber_full', 't3_journal_fishing_empty', 't3_journal_fishing_full', 't3_journal_hide_empty', 't3_journal_hide_full', 
't3_journal_hunter_empty', 't3_journal_hunter_full', 't3_journal_mage_empty', 't3_journal_mage_full', 't3_journal_ore_empty', 't3_journal_ore_full', 
't3_journal_stone_empty', 't3_journal_stone_full', 't3_journal_toolmaker_empty', 't3_journal_toolmaker_full', 't3_journal_warrior_empty', 't3_journal_warrior_full', 
't3_journal_wood_empty', 't3_journal_wood_full', 't4_journal_fiber_empty', 't4_journal_fiber_full', 't4_journal_fishing_empty', 't4_journal_fishing_full', 't4_journal_hide_empty', 't4_journal_hide_full', 
't4_journal_hunter_empty', 't4_journal_hunter_full', 't4_journal_mage_empty', 't4_journal_mage_full', 't4_journal_ore_empty', 't4_journal_ore_full', 
't4_journal_stone_empty', 't4_journal_stone_full', 't4_journal_toolmaker_empty', 't4_journal_toolmaker_full', 't4_journal_warrior_empty', 't4_journal_warrior_full', 
't4_journal_wood_empty', 't4_journal_wood_full', 't5_journal_fiber_empty', 't5_journal_fiber_full', 't5_journal_fishing_empty', 't5_journal_fishing_full', 't5_journal_hide_empty', 't5_journal_hide_full', 
't5_journal_hunter_empty', 't5_journal_hunter_full', 't5_journal_mage_empty', 't5_journal_mage_full', 't5_journal_ore_empty', 't5_journal_ore_full', 
't5_journal_stone_empty', 't5_journal_stone_full', 't5_journal_toolmaker_empty', 't5_journal_toolmaker_full', 't5_journal_warrior_empty', 't5_journal_warrior_full', 
't5_journal_wood_empty', 't5_journal_wood_full', 't6_journal_fiber_empty', 't6_journal_fiber_full', 't6_journal_fishing_empty', 't6_journal_fishing_full', 't6_journal_hide_empty', 't6_journal_hide_full', 
't6_journal_hunter_empty', 't6_journal_hunter_full', 't6_journal_mage_empty', 't6_journal_mage_full', 't6_journal_ore_empty', 't6_journal_ore_full', 
't6_journal_stone_empty', 't6_journal_stone_full', 't6_journal_toolmaker_empty', 't6_journal_toolmaker_full', 't6_journal_warrior_empty', 't6_journal_warrior_full', 
't6_journal_wood_empty', 't6_journal_wood_full', 't7_journal_fiber_empty', 't7_journal_fiber_full', 't7_journal_fishing_empty', 't7_journal_fishing_full', 't7_journal_hide_empty', 't7_journal_hide_full', 
't7_journal_hunter_empty', 't7_journal_hunter_full', 't7_journal_mage_empty', 't7_journal_mage_full', 't7_journal_ore_empty', 't7_journal_ore_full', 
't7_journal_stone_empty', 't7_journal_stone_full', 't7_journal_toolmaker_empty', 't7_journal_toolmaker_full', 't7_journal_warrior_empty', 't7_journal_warrior_full', 
't7_journal_wood_empty', 't7_journal_wood_full', 't8_journal_fiber_empty', 't8_journal_fiber_full', 't8_journal_fishing_empty', 't8_journal_fishing_full', 't8_journal_hide_empty', 't8_journal_hide_full', 
't8_journal_hunter_empty', 't8_journal_hunter_full', 't8_journal_mage_empty', 't8_journal_mage_full', 't8_journal_ore_empty', 't8_journal_ore_full', 
't8_journal_stone_empty', 't8_journal_stone_full', 't8_journal_toolmaker_empty', 't8_journal_toolmaker_full', 't8_journal_warrior_empty', 't8_journal_warrior_full', 
't8_journal_wood_empty', 't8_journal_wood_full']

building = ['t2_furnitureitem_bed', 't2_furnitureitem_table', 't2_furnitureitem_trophy_fiber', 't2_furnitureitem_trophy_fish', 't2_furnitureitem_trophy_general', 
't2_furnitureitem_trophy_hide', 't2_furnitureitem_trophy_ore', 't2_furnitureitem_trophy_rock', 't2_furnitureitem_trophy_wood', 't2_stoneblock', 
't3_furnitureitem_bed', 't3_furnitureitem_table', 't3_furnitureitem_trophy_fiber', 't3_furnitureitem_trophy_fish', 't3_furnitureitem_trophy_general', 
't3_furnitureitem_trophy_hide', 't3_furnitureitem_trophy_ore', 't3_furnitureitem_trophy_rock', 't3_furnitureitem_trophy_wood', 't3_stoneblock', 
't4_furnitureitem_bed', 't4_furnitureitem_table', 't4_furnitureitem_trophy_fiber', 't4_furnitureitem_trophy_fish', 't4_furnitureitem_trophy_general', 
't4_furnitureitem_trophy_hide', 't4_furnitureitem_trophy_ore', 't4_furnitureitem_trophy_rock', 't4_furnitureitem_trophy_wood', 't4_stoneblock', 
't5_furnitureitem_bed', 't5_furnitureitem_table', 't5_furnitureitem_trophy_fiber', 't5_furnitureitem_trophy_fish', 't5_furnitureitem_trophy_general', 
't5_furnitureitem_trophy_hide', 't5_furnitureitem_trophy_ore', 't5_furnitureitem_trophy_rock', 't5_furnitureitem_trophy_wood', 't5_stoneblock', 
't6_furnitureitem_bed', 't6_furnitureitem_table', 't6_furnitureitem_trophy_fiber', 't6_furnitureitem_trophy_fish', 't6_furnitureitem_trophy_general', 
't6_furnitureitem_trophy_hide', 't6_furnitureitem_trophy_ore', 't6_furnitureitem_trophy_rock', 't6_furnitureitem_trophy_wood', 't6_stoneblock', 
't7_furnitureitem_bed', 't7_furnitureitem_table', 't7_furnitureitem_trophy_fiber', 't7_furnitureitem_trophy_fish', 't7_furnitureitem_trophy_general', 
't7_furnitureitem_trophy_hide', 't7_furnitureitem_trophy_ore', 't7_furnitureitem_trophy_rock', 't7_furnitureitem_trophy_wood', 't7_stoneblock', 
't8_furnitureitem_bed', 't8_furnitureitem_table', 't8_furnitureitem_trophy_fiber', 't8_furnitureitem_trophy_fish', 't8_furnitureitem_trophy_general', 
't8_furnitureitem_trophy_hide', 't8_furnitureitem_trophy_ore', 't8_furnitureitem_trophy_rock', 't8_furnitureitem_trophy_wood', 't8_stoneblock']

#Empty table of profits to use with the GET house.html page, before a user request is made
##This may not actually be needed. Check later.
base_table = {'Cropper': {'t3': 0, 't4': 0, 't5': 0, 't6': 0, 't7': 0, 't8': 0},
 'Gamekeeper': {'t3': 0, 't4': 0, 't5': 0, 't6': 0, 't7': 0, 't8': 0},
 'Fletcher': {'t3': 0, 't4': 0, 't5': 0, 't6': 0, 't7': 0, 't8': 0},
 'Imbuer': {'t3': 0, 't4': 0, 't5': 0, 't6': 0, 't7': 0, 't8': 0},
 'Prospector': {'t3': 0, 't4': 0, 't5': 0, 't6': 0, 't7': 0, 't8': 0},
 'Stonecutter': {'t3': 0, 't4': 0, 't5': 0, 't6': 0, 't7': 0, 't8': 0},
 'Tinker': {'t3': 0, 't4': 0, 't5': 0, 't6': 0, 't7': 0, 't8': 0},
 'Blacksmith': {'t3': 0, 't4': 0, 't5': 0, 't6': 0, 't7': 0, 't8': 0},
 'Lumberjack': {'t3': 0, 't4': 0, 't5': 0, 't6': 0, 't7': 0, 't8': 0}}

request_string = 'T3_CLOTH,T3_FIBER,T3_HIDE,T3_LEATHER,T3_METALBAR,T3_ORE,T3_PLANKS,T3_ROCK,T3_WOOD,T4_CLOTH,T4_CLOTH_LEVEL1@1,T4_CLOTH_LEVEL2@2,T4_CLOTH_LEVEL3@3,T4_FIBER,T4_FIBER_LEVEL1@1,T4_FIBER_LEVEL2@2,T4_FIBER_LEVEL3@3,T4_HIDE,T4_HIDE_LEVEL1@1,T4_HIDE_LEVEL2@2,T4_HIDE_LEVEL3@3,T4_LEATHER,T4_LEATHER_LEVEL1@1,T4_LEATHER_LEVEL2@2,T4_LEATHER_LEVEL3@3,T4_METALBAR,T4_METALBAR_LEVEL1@1,T4_METALBAR_LEVEL2@2,T4_METALBAR_LEVEL3@3,T4_ORE,T4_ORE_LEVEL1@1,T4_ORE_LEVEL2@2,T4_ORE_LEVEL3@3,T4_PLANKS,T4_PLANKS_LEVEL1@1,T4_PLANKS_LEVEL2@2,T4_PLANKS_LEVEL3@3,T4_ROCK,T4_ROCK_LEVEL1@1,T4_ROCK_LEVEL2@2,T4_ROCK_LEVEL3@3,T4_WOOD,T4_WOOD_LEVEL1@1,T4_WOOD_LEVEL2@2,T4_WOOD_LEVEL3@3,T5_CLOTH,T5_CLOTH_LEVEL1@1,T5_CLOTH_LEVEL2@2,T5_CLOTH_LEVEL3@3,T5_FIBER,T5_FIBER_LEVEL1@1,T5_FIBER_LEVEL2@2,T5_FIBER_LEVEL3@3,T5_HIDE,T5_HIDE_LEVEL1@1,T5_HIDE_LEVEL2@2,T5_HIDE_LEVEL3@3,T5_LEATHER,T5_LEATHER_LEVEL1@1,T5_LEATHER_LEVEL2@2,T5_LEATHER_LEVEL3@3,T5_METALBAR,T5_METALBAR_LEVEL1@1,T5_METALBAR_LEVEL2@2,T5_METALBAR_LEVEL3@3,T5_ORE,T5_ORE_LEVEL1@1,T5_ORE_LEVEL2@2,T5_ORE_LEVEL3@3,T5_PLANKS,T5_PLANKS_LEVEL1@1,T5_PLANKS_LEVEL2@2,T5_PLANKS_LEVEL3@3,T5_ROCK,T5_ROCK_LEVEL1@1,T5_ROCK_LEVEL2@2,T5_ROCK_LEVEL3@3,T5_WOOD,T5_WOOD_LEVEL1@1,T5_WOOD_LEVEL2@2,T5_WOOD_LEVEL3@3,T6_CLOTH,T6_CLOTH_LEVEL1@1,T6_CLOTH_LEVEL2@2,T6_CLOTH_LEVEL3@3,T6_FIBER,T6_FIBER_LEVEL1@1,T6_FIBER_LEVEL2@2,T6_FIBER_LEVEL3@3,T6_HIDE,T6_HIDE_LEVEL1@1,T6_HIDE_LEVEL2@2,T6_HIDE_LEVEL3@3,T6_LEATHER,T6_LEATHER_LEVEL1@1,T6_LEATHER_LEVEL2@2,T6_LEATHER_LEVEL3@3,T6_METALBAR,T6_METALBAR_LEVEL1@1,T6_METALBAR_LEVEL2@2,T6_METALBAR_LEVEL3@3,T6_ORE,T6_ORE_LEVEL1@1,T6_ORE_LEVEL2@2,T6_ORE_LEVEL3@3,T6_PLANKS,T6_PLANKS_LEVEL1@1,T6_PLANKS_LEVEL2@2,T6_PLANKS_LEVEL3@3,T6_ROCK,T6_ROCK_LEVEL1@1,T6_ROCK_LEVEL2@2,T6_ROCK_LEVEL3@3,T6_WOOD,T6_WOOD_LEVEL1@1,T6_WOOD_LEVEL2@2,T6_WOOD_LEVEL3@3,T7_CLOTH,T7_CLOTH_LEVEL1@1,T7_CLOTH_LEVEL2@2,T7_CLOTH_LEVEL3@3,T7_FIBER,T7_FIBER_LEVEL1@1,T7_FIBER_LEVEL2@2,T7_FIBER_LEVEL3@3,T7_HIDE,T7_HIDE_LEVEL1@1,T7_HIDE_LEVEL2@2,T7_HIDE_LEVEL3@3,T7_LEATHER,T7_LEATHER_LEVEL1@1,T7_LEATHER_LEVEL2@2,T7_LEATHER_LEVEL3@3,T7_METALBAR,T7_METALBAR_LEVEL1@1,T7_METALBAR_LEVEL2@2,T7_METALBAR_LEVEL3@3,T7_ORE,T7_ORE_LEVEL1@1,T7_ORE_LEVEL2@2,T7_ORE_LEVEL3@3,T7_PLANKS,T7_PLANKS_LEVEL1@1,T7_PLANKS_LEVEL2@2,T7_PLANKS_LEVEL3@3,T7_ROCK,T7_ROCK_LEVEL1@1,T7_ROCK_LEVEL2@2,T7_ROCK_LEVEL3@3,T7_WOOD,T7_WOOD_LEVEL1@1,T7_WOOD_LEVEL2@2,T7_WOOD_LEVEL3@3,T8_CLOTH,T8_CLOTH_LEVEL1@1,T8_CLOTH_LEVEL2@2,T8_CLOTH_LEVEL3@3,T8_FIBER,T8_FIBER_LEVEL1@1,T8_FIBER_LEVEL2@2,T8_FIBER_LEVEL3@3,T8_HIDE,T8_HIDE_LEVEL1@1,T8_HIDE_LEVEL2@2,T8_HIDE_LEVEL3@3,T8_LEATHER,T8_LEATHER_LEVEL1@1,T8_LEATHER_LEVEL2@2,T8_LEATHER_LEVEL3@3,T8_METALBAR,T8_METALBAR_LEVEL1@1,T8_METALBAR_LEVEL2@2,T8_METALBAR_LEVEL3@3,T8_ORE,T8_ORE_LEVEL1@1,T8_ORE_LEVEL2@2,T8_ORE_LEVEL3@3,T8_PLANKS,T8_PLANKS_LEVEL1@1,T8_PLANKS_LEVEL2@2,T8_PLANKS_LEVEL3@3,T8_ROCK,T8_ROCK_LEVEL1@1,T8_ROCK_LEVEL2@2,T8_ROCK_LEVEL3@3,T8_WOOD,T8_WOOD_LEVEL1@1,T8_WOOD_LEVEL2@2,T8_WOOD_LEVEL3@3,T1_FISH_FRESHWATER_ALL_COMMON,T2_FISH_FRESHWATER_ALL_COMMON,T3_FISH_FRESHWATER_ALL_COMMON,T4_FISH_FRESHWATER_ALL_COMMON,T5_FISH_FRESHWATER_ALL_COMMON,T6_FISH_FRESHWATER_ALL_COMMON,T7_FISH_FRESHWATER_ALL_COMMON,T8_FISH_FRESHWATER_ALL_COMMON,T1_FISH_SALTWATER_ALL_COMMON,T2_FISH_SALTWATER_ALL_COMMON,T3_FISH_SALTWATER_ALL_COMMON,T4_FISH_SALTWATER_ALL_COMMON,T5_FISH_SALTWATER_ALL_COMMON,T6_FISH_SALTWATER_ALL_COMMON,T7_FISH_SALTWATER_ALL_COMMON,T8_FISH_SALTWATER_ALL_COMMON,T3_FISH_FRESHWATER_FOREST_RARE,T5_FISH_FRESHWATER_FOREST_RARE,T7_FISH_FRESHWATER_FOREST_RARE,T3_FISH_FRESHWATER_MOUNTAIN_RARE,T5_FISH_FRESHWATER_MOUNTAIN_RARE,T7_FISH_FRESHWATER_MOUNTAIN_RARE,T3_FISH_FRESHWATER_HIGHLANDS_RARE,T5_FISH_FRESHWATER_HIGHLANDS_RARE,T7_FISH_FRESHWATER_HIGHLANDS_RARE,T3_FISH_FRESHWATER_STEPPE_RARE,T5_FISH_FRESHWATER_STEPPE_RARE,T7_FISH_FRESHWATER_STEPPE_RARE,T3_FISH_FRESHWATER_SWAMP_RARE,T5_FISH_FRESHWATER_SWAMP_RARE,T7_FISH_FRESHWATER_SWAMP_RARE,T3_FISH_SALTWATER_ALL_RARE,T5_FISH_SALTWATER_ALL_RARE,T7_FISH_SALTWATER_ALL_RARE,T1_SEAWEED,T3_FISH_FRESHWATER_AVALON_RARE,T5_FISH_FRESHWATER_AVALON_RARE,T7_FISH_FRESHWATER_AVALON_RARE,T3_JOURNAL_FIBER_EMPTY,T3_JOURNAL_FIBER_FULL,T3_JOURNAL_FISHING_EMPTY,T3_JOURNAL_FISHING_FULL,T3_JOURNAL_HIDE_EMPTY,T3_JOURNAL_HIDE_FULL,T3_JOURNAL_HUNTER_EMPTY,T3_JOURNAL_HUNTER_FULL,T3_JOURNAL_MAGE_EMPTY,T3_JOURNAL_MAGE_FULL,T3_JOURNAL_ORE_EMPTY,T3_JOURNAL_ORE_FULL,T3_JOURNAL_STONE_EMPTY,T3_JOURNAL_STONE_FULL,T3_JOURNAL_TOOLMAKER_EMPTY,T3_JOURNAL_TOOLMAKER_FULL,T3_JOURNAL_WARRIOR_EMPTY,T3_JOURNAL_WARRIOR_FULL,T3_JOURNAL_WOOD_EMPTY,T3_JOURNAL_WOOD_FULL,T4_JOURNAL_FIBER_EMPTY,T4_JOURNAL_FIBER_FULL,T4_JOURNAL_FISHING_EMPTY,T4_JOURNAL_FISHING_FULL,T4_JOURNAL_HIDE_EMPTY,T4_JOURNAL_HIDE_FULL,T4_JOURNAL_HUNTER_EMPTY,T4_JOURNAL_HUNTER_FULL,T4_JOURNAL_MAGE_EMPTY,T4_JOURNAL_MAGE_FULL,T4_JOURNAL_ORE_EMPTY,T4_JOURNAL_ORE_FULL,T4_JOURNAL_STONE_EMPTY,T4_JOURNAL_STONE_FULL,T4_JOURNAL_TOOLMAKER_EMPTY,T4_JOURNAL_TOOLMAKER_FULL,T4_JOURNAL_WARRIOR_EMPTY,T4_JOURNAL_WARRIOR_FULL,T4_JOURNAL_WOOD_EMPTY,T4_JOURNAL_WOOD_FULL,T5_JOURNAL_FIBER_EMPTY,T5_JOURNAL_FIBER_FULL,T5_JOURNAL_FISHING_EMPTY,T5_JOURNAL_FISHING_FULL,T5_JOURNAL_HIDE_EMPTY,T5_JOURNAL_HIDE_FULL,T5_JOURNAL_HUNTER_EMPTY,T5_JOURNAL_HUNTER_FULL,T5_JOURNAL_MAGE_EMPTY,T5_JOURNAL_MAGE_FULL,T5_JOURNAL_ORE_EMPTY,T5_JOURNAL_ORE_FULL,T5_JOURNAL_STONE_EMPTY,T5_JOURNAL_STONE_FULL,T5_JOURNAL_TOOLMAKER_EMPTY,T5_JOURNAL_TOOLMAKER_FULL,T5_JOURNAL_WARRIOR_EMPTY,T5_JOURNAL_WARRIOR_FULL,T5_JOURNAL_WOOD_EMPTY,T5_JOURNAL_WOOD_FULL,T6_JOURNAL_FIBER_EMPTY,T6_JOURNAL_FIBER_FULL,T6_JOURNAL_FISHING_EMPTY,T6_JOURNAL_FISHING_FULL,T6_JOURNAL_HIDE_EMPTY,T6_JOURNAL_HIDE_FULL,T6_JOURNAL_HUNTER_EMPTY,T6_JOURNAL_HUNTER_FULL,T6_JOURNAL_MAGE_EMPTY,T6_JOURNAL_MAGE_FULL,T6_JOURNAL_ORE_EMPTY,T6_JOURNAL_ORE_FULL,T6_JOURNAL_STONE_EMPTY,T6_JOURNAL_STONE_FULL,T6_JOURNAL_TOOLMAKER_EMPTY,T6_JOURNAL_TOOLMAKER_FULL,T6_JOURNAL_WARRIOR_EMPTY,T6_JOURNAL_WARRIOR_FULL,T6_JOURNAL_WOOD_EMPTY,T6_JOURNAL_WOOD_FULL,T7_JOURNAL_FIBER_EMPTY,T7_JOURNAL_FIBER_FULL,T7_JOURNAL_FISHING_EMPTY,T7_JOURNAL_FISHING_FULL,T7_JOURNAL_HIDE_EMPTY,T7_JOURNAL_HIDE_FULL,T7_JOURNAL_HUNTER_EMPTY,T7_JOURNAL_HUNTER_FULL,T7_JOURNAL_MAGE_EMPTY,T7_JOURNAL_MAGE_FULL,T7_JOURNAL_ORE_EMPTY,T7_JOURNAL_ORE_FULL,T7_JOURNAL_STONE_EMPTY,T7_JOURNAL_STONE_FULL,T7_JOURNAL_TOOLMAKER_EMPTY,T7_JOURNAL_TOOLMAKER_FULL,T7_JOURNAL_WARRIOR_EMPTY,T7_JOURNAL_WARRIOR_FULL,T7_JOURNAL_WOOD_EMPTY,T7_JOURNAL_WOOD_FULL,T8_JOURNAL_FIBER_EMPTY,T8_JOURNAL_FIBER_FULL,T8_JOURNAL_FISHING_EMPTY,T8_JOURNAL_FISHING_FULL,T8_JOURNAL_HIDE_EMPTY,T8_JOURNAL_HIDE_FULL,T8_JOURNAL_HUNTER_EMPTY,T8_JOURNAL_HUNTER_FULL,T8_JOURNAL_MAGE_EMPTY,T8_JOURNAL_MAGE_FULL,T8_JOURNAL_ORE_EMPTY,T8_JOURNAL_ORE_FULL,T8_JOURNAL_STONE_EMPTY,T8_JOURNAL_STONE_FULL,T8_JOURNAL_TOOLMAKER_EMPTY,T8_JOURNAL_TOOLMAKER_FULL,T8_JOURNAL_WARRIOR_EMPTY,T8_JOURNAL_WARRIOR_FULL,T8_JOURNAL_WOOD_EMPTY,T8_JOURNAL_WOOD_FULL'
