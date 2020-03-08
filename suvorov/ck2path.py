## module to handle the paths for CK2 files

import os

ck2userdir = os.path.expanduser("~/.paradoxinteractive/Crusader Kings II")
ck2gamedir = os.path.expanduser("~/.steam/steam/steamapps/common/Crusader Kings II")
ck2permissions = os.stat(ck2userdir)

class CK2DataDir:
	VANILLA = ck2gamedir
	MOD = lambda modname: os.path.join(ck2userdir,"mod",modname)
	SUVOROVMOD = lambda modname: os.path.join(ck2userdir,"suvorovmods",modname)
		
		



