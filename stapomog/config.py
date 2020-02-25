from doreah import packageutils
import yaml
import os
import sys

USERCONFIG = {}

packageutils.config(packagename="stapomog")


### load config
try:
	with open(packageutils.pkgdata("conf.yml"),"r") as conffile:
		USERCONFIG.update(yaml.safe_load(conffile.read()))
	print("Loaded user configuration")
except:
	print("Could not find user configuration.")


### set defaults
if "GAME_FOLDER" not in USERCONFIG:
	print("Finding game install folder...")
	possibilities = [
		"~/.steam/steam/steamapps/common/Crusader Kings II"
	]
	for p in possibilities:
		if os.path.exists(os.path.join(os.path.expanduser(p),"ck2")):
			USERCONFIG["GAME_FOLDER"] = os.path.expanduser(p)
			break
	else:
		USERCONFIG["GAME_FOLDER"] = None
		
			
if "ALSO_SAVE_PNG" not in USERCONFIG:
	USERCONFIG["ALSO_SAVE_PNG"] = True
if "USE_SOCIETY_OVERRIDE" not in USERCONFIG:
	USERCONFIG["USE_SOCIETY_OVERRIDE"] = True
if "CREATE_MOD_FILE" not in USERCONFIG:
	USERCONFIG["CREATE_MOD_FILE"] = True
if "FLAG_TO_SHOW_ASSIGN_DECISIONS" not in USERCONFIG:
	USERCONFIG["FLAG_TO_SHOW_ASSIGN_DECISIONS"] = "debug_stapomog"
	
	

		

### save config
with open(packageutils.pkgdata("conf.yml"),"w") as conffile:
	conffile.write(yaml.dump(USERCONFIG))
	
# current forced settings
USERCONFIG["USE_SOCIETY_OVERRIDE"] = True
	

if not os.path.exists(USERCONFIG["GAME_FOLDER"]):
	print("Could not find CK 2 installation. Please specify in",packageutils.pkgdata("conf.yml"))
	sys.exit(1)



	
GLOBALCONFIG = {
	"IMAGE_EXTENSIONS":("png","jpg","tga","jpeg"),
	"MOD_FILES":{
		"PORTRAIT_PROPERTIES": "interface/portrait_properties/stapomog_static_portraits.txt",
		"PORTRAIT_SPRITES_DEFINITION": "interface/portraits/stapomog_static_portrait_sprites.gfx",
		"PORTRAIT_TYPES_DEFINITION": "interface/portraits/stapomog_static_portrait_types.gfx",
		"TRAITS": "common/traits/stapomog_static_portrait_traits.txt",
		"DECISIONS": "decisions/stapomog_static_portrait_decisions.txt",
		"SPRITES": "gfx/characters/stapomog_static_portraits_{idx}.dds",
		"SCRIPTED_EFFECTS":"common/scripted_effects/stapomog_effects.txt",
		"SCRIPTED_TRIGGERS":"common/scripted_triggers/stapomog_triggers.txt"
	},
	"MOD_FOLDERS":{
		"PORTRAITS": "gfx/characters/",
		"PORTRAIT_DEFINITIONS": "interface/portraits/"
	},
	"SPRITE_NAME":"GFX_character_stapomog_{idx}",
	"GAME_FOLDERS_PORTRAIT_DEFINITIONS": ("interface/portraits/","interface/"),
	"GAME_FOLDER_DLC": "dlc",
	"GFX_CULTURES": ["byzantine","muslim","norse","western","german","english","saxon","frankish","norman","italian","trueoccitan","roman","dalmatian","outremer",
		"southern","easternslavic","persian","crimean","celtic","ugric","turkish","cuman","mongol","chinese","arabic","berber","levantine","westernslavic",
		"croatsoutslavic","serbsouthslavic","magyar","african","westafrican","mesoamerican","indian","bodpa","southindian"],
	"GFX_AGES": ["early","late"],
	
	"FIRST_LAYER": 38,
	"FRAMES_PER_LAYER": 26,
	"MOD_FOLDER_NAME":"stapomog_portrait_mod",
	"AGE_RANGES":{
		"teen":{
			"range":(None,19),
			"aliases":("t","teen"),
			"portrait_age_range":("young","midage")
		},
		"young":{
			"range":(None,29),
			"aliases":("y","young"),
			"portrait_age_range":("young","midage")
		},
		"middleaged":{
			"range":(30,49),
			"aliases":("m","middle","mid"),
			"portrait_age_range":("midage","oldage")
		},
		"old":{
			"range":(50,None),
			"aliases":("o","old"),
			"portrait_age_range":("oldage",None)
		},
		"youngmiddle":{
			"range":(None,49),
			"aliases":("ym",),
			"portrait_age_range":("young","oldage")
		},
		"midold":{
			"range":(30,None),
			"aliases":("mo",),
			"portrait_age_range":("midage",None)
		},
		"full":{
			"range":(None,None),
			"aliases":("ymo",""),
			"portrait_age_range":("young",None)
		}
	}
}



