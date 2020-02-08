from doreah import packageutils
import yaml
import os

USERCONFIG = {}

if "GAME_FOLDER" not in USERCONFIG:
	USERCONFIG["GAME_FOLDER"] = os.path.expanduser("~/.steam/steam/steamapps/common/Crusader Kings II")
if "ALSO_SAVE_PNG" not in USERCONFIG:
	USERCONFIG["ALSO_SAVE_PNG"] = True
if "USE_SOCIETY_OVERRIDE" not in USERCONFIG:
	USERCONFIG["USE_SOCIETY_OVERRIDE"] = False
	
	
	
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
