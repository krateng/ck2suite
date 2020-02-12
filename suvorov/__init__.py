### PACKAGE DATA

name = "suvorov"
desc = "Tool to enable a more concise and thematically structured creation of mods for Crusader Kings 2"
author = {
	"name":"Johannes Krattenmacher",
	"email":"misc@krateng.dev",
	"github": "krateng"
}
version = 0,3,1
versionstr = ".".join(str(n) for n in version)


requires = [
	"doreah>=1.4.5"
]
resources = [
]

commands = {
	"suvorov":"main:main"
}

