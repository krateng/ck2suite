### PACKAGE DATA

name = "stapomog"
desc = "Tool to quickly create Static Portrait Mods for Crusader Kings 2"
author = {
	"name":"Johannes Krattenmacher",
	"email":"misc@krateng.dev",
	"github": "krateng"
}
version = 0,2,1
versionstr = ".".join(str(n) for n in version)


requires = [
	"doreah>=1.4.5",
	"wand>=0.5.4",
	"pillow>=7.0.0",
	"suvorov>=0.6.0",
	"oyaml",
	"vermeer>=0.1.0"
]
resources = [
]

commands = {
	"stapomog":"generate:main"
}

from . import config
