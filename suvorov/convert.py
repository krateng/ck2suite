import os
import shutil
import sys
import yaml
import re
from doreah.io import col, ask

from .conf import *

scope_types = {
	"on_actions":("common/on_actions",False),
	"events":("events",False),
	"character_event":("events",True),
	"province_event":("events",True),
	"decisions":("decisions",True),
	"targetted_decisions":("decisions",True),
	"plot_decisions":("decisions",True),
	"traits":("common/traits",False),
	"artifacts":("common/artifacts",False),
	"bloodlines":("common/bloodlines",False),
	"buildings":("common/buildings",False),
	"cb_types":("common/cb_types",False),
	"council_positions":("common/council_positions",False),
	"cultures":("common/cultures",False),
	"deaths":("common/death",False),
	"diseases":("common/disease",False),
	"dynasties":("common/dynasties",False),
	"event_modifiers":("common/event_modifiers",False),
	"landed_titles":("common/landed_titles",False),
	"minor_titles":("common/minor_titles",False),
	"nicknames":("common/nicknames",False),
	"opinion_modifiers":("common/opinion_modifiers",False),
	"religions":("common/religions",False),
	"societies":("common/societies",False),
	"wonders":("common/wonders",False),
	"wonder_upgrades":("common/wonder_upgrades",False),
	"scripted_effects":("common/scripted_effects",False),
	"scripted_triggers":("common/scripted_triggers",False),
	"mercenaries":("common/mercenaries",False),
	"characters":("history/characters",False)
}


# build_mod: takes mod name, converts in standard directories
# delete_mod: takes mod name, deletes in standard directories
# convert_mod: takes actual source and target folder, converts


def get_top_scopes(txt):
	name = ""
	expr = ""
	depth = 0
	scopes = []
	for char in txt:
		if char == "{":
			if depth == 0: pass 
			else: expr += char
			depth += 1
		elif char == "}":
			depth -= 1
			if depth == 0:
				name = name.replace("=","").strip()
				scopes.append((name,expr))
				name, expr = "",""
			else: expr += char
			
		else:
			if depth == 0: name += char
			else: expr += char
	return scopes
		
	
			

# figures out folders and stuff and generates full mod
def build_mod(modname):

	srcmodfolder = os.path.join(SUVOROVMODFOLDER,modname)	
	
	targetmodfolder = os.path.join(VANILLAMODFOLDER,"suvorov." + modname)
	targetmodfile = os.path.join(VANILLAMODFOLDER,"suvorov." + modname + ".mod")
	
	return convert_mod(srcmodfolder,targetmodfolder,targetmodfile)
	
	
	
def convert_mod(srcfolder,trgtfolder,trgtfile,modname=None):

	if modname == None: modname = os.path.basename(srcfolder)
	
	# check if mod already exists (hostile user :P)
	if os.path.exists(trgtfolder) and not os.path.exists(os.path.join(trgtfolder,METAFILE)) and not ask("Mod " + modname + " already exists, but is not managed by Suvorov. Overwrite?"):
		print("Mod was not created.")
		return False
		
	
	# gather mod data
	srcmodfile = os.path.join(srcfolder,"modinfo.yml")
	modmetadata = {}
	if os.path.exists(srcmodfile):
		with open(srcmodfile) as modfile:
			modmetadata.update(yaml.safe_load(modfile.read()))
	if "name" not in modmetadata: modmetadata["name"] = modname
	
	modmetadata["path"] = os.path.join(os.path.basename(VANILLAMODFOLDER),os.path.basename(trgtfolder))
	
	
	# write modfile
	with open(trgtfile,"w") as modfile:
		for e in modmetadata:
			modfile.write(e + ' = "' + modmetadata[e] + '"\n')
			
			
	
	os.chdir(srcfolder)
	# go to the folder instead of path.join so that all names we print / save are relative to it
	
	# find out if original source files are still the same
	try:
		with open(os.path.join(trgtfolder,METAFILE)) as suvorovfile:
			modinfo = yaml.safe_load(suvorovfile.read())
		assert modinfo is not None and "times" in modinfo and "results" in modinfo
	except:
		modinfo = {"times":{},"results":{}}
		
	
	# all source files with their modify date
	srcfiles = {}
	for (dirpath,dirnames,filenames) in os.walk("."):
		for f in filenames:
			pth = os.path.join(dirpath, f)
			srcfiles[pth] = os.path.getmtime(pth)
	if "modinfo.yml" in srcfiles: srcfiles.pop("modinfo.yml")
	if "./modinfo.yml" in srcfiles: srcfiles.pop("./modinfo.yml")
	
	changed_files = [f for f in srcfiles if f not in modinfo["times"] or modinfo["times"][f] != srcfiles[f]]
	removed_files = [f for f in modinfo["results"] if f not in srcfiles]
	
	# convert individual files
	for f in removed_files:
		for rf in modinfo["results"][f]:
			print("Removing",col["red"](rf),"as its source",col["red"](f),"no longer exists.")
			# os.remove(os.path.join(trgtfolder,rf))
	for f in changed_files:
		
		
		#check if suvorov file
		fullpath = os.path.realpath(f)
		suvdir = os.path.realpath(SRCFOLDER)
		if os.path.commonprefix([fullpath,suvdir]) != suvdir:
			print("Copying",col["green"](f))
			target = os.path.join(trgtfolder,f)
			os.makedirs(os.path.dirname(target),exist_ok=True)
			shutil.copyfile(f,target)
			modinfo["times"][f] = srcfiles[f]
			modinfo["results"].setdefault(f,[]).append(f)
		else:
			print("Parsing",col["yellow"](f))
			identifier = os.path.relpath(os.path.splitext(f)[0],start=SRCFOLDER).replace("/",".")
			with open(f) as fh:
				entries = process_suv_file(fh.read(),trgtfolder)
				
			for folder in entries:
				os.makedirs(os.path.join(trgtfolder,folder),exist_ok=True)
				target = os.path.join(folder,identifier) + ".txt"
				fulltarget = os.path.join(trgtfolder,target)
				
				# check if we're allowed to edit this file or it has been created by someone else
				canown = (not os.path.exists(fulltarget)) or (target in modinfo["results"])
				if canown or ask("File "+col["yellow"](target)+" exists and is not managed by Suvorov! Overwrite?"):
					print("Creating",col["green"](target))
					modinfo["results"].setdefault(f,[]).append(target)
					modinfo["times"][f] = srcfiles[f]
					with open(fulltarget,"w") as tf:
						tf.write("\n".join(entries[folder]))
				else:
					print("Did not create",col["red"](target))
				
			
			
			
	# print suvorov info data
	with open(os.path.join(trgtfolder,METAFILE),"w") as suvorovfile:
		yaml.dump(modinfo,suvorovfile)
	
	
	
	
	
def process_suv_file(content,targetfolder):
	
	l = get_top_scopes(content)
	entries = {} # all entries that belong to this identifier, by folder
	for scope,txt in l:
		if scope in scope_types:
			folder,keep = scope_types[scope]
			
			# decrease tabulation by one
			if not keep:
				txt = "\n".join(l[1:] for l in txt.split("\n") if l.startswith("\t"))
			else:
				txt = scope + " = {\n" + txt + "\n}"
			entries.setdefault(folder,[]).append(txt)
			
			
			
		else:
			print("\tScope",col["red"](scope),"is not valid.")
			
	return entries
	
	
	

		
def delete_mod(name):
	pass
