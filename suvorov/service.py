import time
import os
import shutil
import yaml
from doreah.io import col
from .conf import VANILLAMODFOLDER, SUVOROVMODFOLDER, CK2USERFOLDER
from .convert import build_mod, delete_mod

try:
	with open(os.path.join(CK2USERFOLDER,"suvorov.yml")) as suvorovfile:
		mods = yaml.safe_load(suvorovfile.read())
	assert mods is not None
except:
	mods = {}

def parse_mods():
	actual_mods = {}
	for folder in [f for f in os.listdir(SUVOROVMODFOLDER) if os.path.isdir(os.path.join(SUVOROVMODFOLDER,f))]:
		#modificationtime = os.path.getmtime(os.path.join(SUVOROVMODFOLDER,folder))
		mtime = max(os.path.getmtime(f) for f,_,_ in os.walk(os.path.join(SUVOROVMODFOLDER,folder)))
		actual_mods[folder] = mtime
	
	any_change = False
	for mod in list(actual_mods.keys()) + list(mods.keys()):
		srcdir = os.path.join(SUVOROVMODFOLDER,mod)
		#trgtdir = os.path.join(VANILLAMODFOLDER,"suvorov." + mod)
		if mod in actual_mods and mod not in mods:
			# new mod detected
			print(col["yellow"]("New mod detected: " + mod + " | Building..."))
			build_mod(mod)
			mods[mod] = actual_mods[mod]
			any_change = True
		elif mod in mods and mod not in actual_mods:
			# old mod deleted
			print(col["yellow"]("Mod no longer present: " + mod + " | Removing..."))
			delete_mod(mod)
			mods.pop(mod)
			any_change = True
		elif actual_mods[mod] != mods[mod]:
			# mod changed
			print(col["yellow"]("Mod source changed on disk: " + mod + " | Building..."))
			build_mod(mod)
			mods[mod] = actual_mods[mod]
			any_change = True
			
	
	print(col["green"]("All mods up to date!"))

	# save after check
	if any_change:
		with open(os.path.join(CK2USERFOLDER,"suvorovnew.yml"),"w") as suvorovfile:
			yaml.dump(mods,suvorovfile)
		shutil.move(os.path.join(CK2USERFOLDER,"suvorovnew.yml"),os.path.join(CK2USERFOLDER,"suvorov.yml"))



#while True:
	
#	time.sleep(5)
