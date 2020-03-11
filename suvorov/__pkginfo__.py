name = "suvorov"
desc = "Tool to enable a more concise and thematically structured creation of mods for Crusader Kings 2"
author = {
	"name":"Johannes Krattenmacher",
	"email":"misc@krateng.dev",
	"github": "krateng"
}
links = {
	"github":"ck2suite"
}
version = 1,0,2
versionstr = ".".join(str(n) for n in version)


requires = [
	"doreah>=1.6.1",
	"bierstadt>=0.2.0"
]
resources = [
]

commands = {
	"suvorov":"main:main"
}
