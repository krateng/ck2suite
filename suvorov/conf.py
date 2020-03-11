import os
from bierstadt import library as bt


METAFILE = "suvorov.yml"
MODINFOFILE = "modinfo.yml"

SUVOROVSRCFOLDER = "."
VANILLASRCFOLDER = "pdx"
GFXSRCFOLDER = "gfx"

SUVOROVMODPREFIX = "suvorov."
SUVOROVFILEPREFIX = "svrv."

SERVICEUNITFILE = os.path.expanduser("/usr/lib/systemd/system/suvorov.service")

TXT_FILE_EXTENSIONS = ("txt")
SUV_FILE_EXTENSIONS = ("suv")
DATA_FILE_EXTENSIONS = ("yml","yaml","svy")
IMG_FILE_EXTENSIONS = ("dds","tga","png","jpg","jpeg","bmp","gif")

ENCODING = "cp1252"


scope_types = {
	# SCOPE						# DIRECTORY					# KEEP TOP SCOPE	# SEPARATE FILE
	"on_actions":				("common/on_actions",		False,				False),
	"events":					("events",					False,				False),
	"character_event":			("events",					True,				False),
	"province_event":			("events",					True,				False),
	"decisions":				("decisions",				True,				False),
	"targetted_decisions":		("decisions",				True,				False),
	"plot_decisions":			("decisions",				True,				False),
	"traits":					("common/traits",			False,				False),
	"artifacts":				("common/artifacts",		False,				False),
	"bloodlines":				("common/bloodlines",		False,				False),
	"buildings":				("common/buildings",		False,				False),
	"cb_types":					("common/cb_types",			False,				False),
	"council_positions":		("common/council_positions",False,				False),
	"cultures":					("common/cultures",			False,				False),
	"deaths":					("common/death",			False,				False),
	"diseases":					("common/disease",			False,				False),
	"dynasties":				("common/dynasties",		False,				False),
	"event_modifiers":			("common/event_modifiers",	False,				False),
	"landed_titles":			("common/landed_titles",	False,				False),
	"minor_titles":				("common/minor_titles",		False,				False),
	"nicknames":				("common/nicknames",		False,				False),
	"opinion_modifiers":		("common/opinion_modifiers",False,				False),
	"religions":				("common/religions",		False,				False),
	"societies":				("common/societies",		False,				False),
	"wonders":					("common/wonders",			False,				False),
	"wonder_upgrades":			("common/wonder_upgrades",	False,				False),
	"scripted_effects":			("common/scripted_effects",	False,				False),
	"scripted_triggers":		("common/scripted_triggers",False,				False),
	"mercenaries":				("common/mercenaries",		False,				False),
	"characters":				("history/characters",		False,				False),
	"death":					("common/death",			False,				False),
	"objectives":				("common/objectives",		False,				False),
	"provinces":				("history/provinces",		False,				True),
	"titles":					("history/titles",			False,				True)
}

gfx_types = {
	# SUVOROV FOLDER			# VANILLA FOLDER			# bierstadt type
	"traits":					("gfx/traits",				bt.TraitIcon		),
	"event_pictures":			("gfx/event_pictures",		bt.EventPicture		)
}
