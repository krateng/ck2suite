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
	USERCONFIG["USE_SOCIETY_OVERRIDE"] = False
	

### save config
with open(packageutils.pkgdata("conf.yml"),"w") as conffile:
	conffile.write(yaml.dump(USERCONFIG))
	

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
		"SPRITES": "gfx/characters/stapomog_static_portraits_{idx}.dds"
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
}



