name = "vermeer"
desc = "Library and command line tool to handle CK2 portrait files"
author = {
	"name":"Johannes Krattenmacher",
	"email":"misc@krateng.dev",
	"github": "krateng"
}
version = 0,1,0
versionstr = ".".join(str(n) for n in version)


requires = [
	"doreah>=1.4.5",
	"wand>=0.5.4",
	"pillow>=7.0.0"
]
resources = [
]

commands = {
	"vermeer":"api:main"
}
