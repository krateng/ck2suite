import os
import shutil
import sys
import yaml
import csv
import re
from doreah.io import col, ask
from doreah.datatypes import DictStack

from .conf import *
from .ck2file.classes import CK2Definition

from vermeer.library import load_from_file, write_to_dds_file, crop

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
	"characters":("history/characters",False),
	"death":("common/death",False),
	"objectives":("common/objectives",False)
}

scope_types_separate_files = {
	"provinces":("history/provinces",),
	"titles":("history/titles",)
}

gfx_types = {
	"traits":("gfx/traits","traiticon")
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
			
		elif char == "\n" and depth == 0:
			name = ""
			
		else:
			if depth == 0: name += char
			else: expr += char
	return scopes
		
	
			

# figures out folders and stuff and generates full mod
def build_mod(modname,force=False):

	srcmodfolder = os.path.join(SUVOROVMODFOLDER,modname)	
	
	targetmodfolder = os.path.join(VANILLAMODFOLDER,"suvorov." + modname)
	targetmodfile = os.path.join(VANILLAMODFOLDER,"suvorov." + modname + ".mod")
	
	return convert_mod(srcmodfolder,targetmodfolder,targetmodfile,force=force)
	
	
	
def convert_mod(srcfolder,trgtfolder,trgtfile,modname=None,force=False):

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
		if force: modinfo["times"] = {f:0 for f in modinfo["times"]}
	except:
		modinfo = {"times":{},"results":{}}
		
	
	# all source files with their modify date
	srcfiles = {}
	for (dirpath,dirnames,filenames) in os.walk("."):
		for f in filenames:
			if f.startswith("."): continue
			pth = os.path.join(dirpath, f)
			srcfiles[pth] = os.path.getmtime(pth)
	if "modinfo.yml" in srcfiles: srcfiles.pop("modinfo.yml")
	if "./modinfo.yml" in srcfiles: srcfiles.pop("./modinfo.yml")
	
	
	# check changed / removed files
	removed_files = [f for f in modinfo["results"] if f not in srcfiles]
	changed_files = [f for f in srcfiles if f not in modinfo["times"] or modinfo["times"][f] != srcfiles[f]]

	
	# has any data changed?
	data_changed = any((f.split(".")[-1].lower() in DATA_FILE_EXTENSIONS) for f in changed_files + removed_files)
	
	# clear data files from the file lists (we don't convert them directly into mod files)
	removed_files = [f for f in removed_files if f.split(".")[-1].lower() not in DATA_FILE_EXTENSIONS]
	changed_files = [f for f in changed_files if f.split(".")[-1].lower() not in DATA_FILE_EXTENSIONS]
	
	# we need to keep track if gfx files have been changed in order to recreate sprite definitions etc
	changed_gfx_files = {f:False for f in gfx_types}
	
	# if data has changed, all suv files need to be reevaluated
	if data_changed: changed_files = list(set(changed_files + [f for f in srcfiles if f.split(".")[-1].lower() in SUV_FILE_EXTENSIONS]))
	
	
	
	
	for f in removed_files:
		for rf in modinfo["results"][f]:
			print("Removing",col["red"](rf),"as its source",col["red"](f),"no longer exists.")
			try:
				os.remove(os.path.join(trgtfolder,rf))
			except FileNotFoundError:
				pass
		modinfo["results"].pop(f)
	
	
	
	
	# if we evaluate any suv files (bc they have changed OR data itself has been changed), we need to load all data!
	if any(f.split(".")[-1].lower() in SUV_FILE_EXTENSIONS for f in changed_files):
		
		data = {}
		for f in srcfiles:
			if f.split(".")[-1].lower() in DATA_FILE_EXTENSIONS:
				with open(f,"r") as ymlfile:
					content = yaml.safe_load(ymlfile.read())
				if "data" in content:
					data.update(content["data"])
					print("Loaded data from",col["purple"](f))
					modinfo["times"][f] = srcfiles[f]
					

				
	
	

	
	# parse all the files	
	for f in changed_files:
	
		# f is the path relative to the (suvorov) mod folder
		# naming convention for below:
		# 	relativepath		path relative to relevant suvorov-structural subfolder
		#	target			file to be written relative to result mod folder
		#	targetfolder		folder to be written inside relative to result mod folder
		#	fulltarget		absolute path of target file
		#	name			name of the file
		#	rawname			name of the file without extensions
		#	
	
		# get all files that have been created from this file
		old_createdfiles = modinfo["results"].get(f) or []
		new_createdfiles = []
		
		
		#check if suvorov file
		fullpath = os.path.realpath(f)
		#suvdir = os.path.realpath(SRCFOLDER)
		vanilladir = os.path.realpath(VANILLASRCFOLDER)
		gfxdir = os.path.realpath(GFXSRCFOLDER)
		
		
		# VANILLA FILE - COPY AS IS
		if os.path.commonprefix([fullpath,vanilladir]) == vanilladir:		
			relativepath = os.path.relpath(f,start=vanilladir)
			print("Copying",col["green"](relativepath))
			target = os.path.join(trgtfolder,relativepath)
			os.makedirs(os.path.dirname(target),exist_ok=True)
			shutil.copyfile(f,target)
			new_createdfiles.append(f)
			
		
		# GFX FILE - convert, add gfx definition file	
		elif os.path.commonprefix([fullpath,gfxdir]) == gfxdir:
			relativepath = os.path.relpath(f,start=gfxdir)
			print("Loading GFX file",col["yellow"](relativepath))
			folder,name = relativepath.split("/")
			rawname = name.split(".")[0]
			targetfolder,gfxtype = gfx_types[folder]
			target = os.path.join(targetfolder,rawname + ".dds")
			fulltarget = os.path.join(trgtfolder,target)
			
			img = load_from_file(fullpath)
			img = crop(img,type=gfxtype)
			print("\tCreating",col["green"](target))
			os.makedirs(os.path.join(trgtfolder,targetfolder),exist_ok=True)
			write_to_dds_file(img,fulltarget)
			new_createdfiles.append(target)
			
			changed_gfx_files[folder] = True
			
		
		
		# DATA FILE - interpret, write in correct folders	
		else:
			
			identifier = os.path.relpath(os.path.splitext(f)[0],start=SUVOROVSRCFOLDER).replace("/",".")
			ext = f.split(".")[-1].lower()
			if ext in TXT_FILE_EXTENSIONS + SUV_FILE_EXTENSIONS:
				print("Parsing",col["yellow"](f))
				if ext in TXT_FILE_EXTENSIONS:
					with open(f) as fh:
						entries,individual_files = process_txt_file(fh.read())
						loc_keys = {}
				#elif ext in YML_FILE_EXTENSIONS:
				#	with open(f) as fh:
				#		entries,individual_files = process_svy_file(fh.read())
				#		loc_keys = {}
				if ext in SUV_FILE_EXTENSIONS:
					with open(f) as fh:
						entries,individual_files,loc_keys = process_suv_file(fh.read(),data)
				
				
				for folder in entries:
					os.makedirs(os.path.join(trgtfolder,folder),exist_ok=True)
					target = os.path.join(folder,identifier) + ".txt"
					fulltarget = os.path.join(trgtfolder,target)
					
					# check if we're allowed to edit this file or it has been created by someone else
					canown = (not os.path.exists(fulltarget)) or (target in modinfo["results"].get(f,[]))
					if canown or ask("File "+col["yellow"](target)+" exists, but is not tied to this source file! Overwrite?"):
						print("\tCreating",col["green"](target))
						new_createdfiles.append(target)
						with open(fulltarget,"w",encoding=ENCODING) as tf:
							tf.write("\n".join(entries[folder]))
					else:
						print("\tDid not create",col["red"](target))
						
				for target in individual_files:
					directory = os.path.dirname(target)
					os.makedirs(os.path.join(trgtfolder,directory),exist_ok=True)
					fulltarget = os.path.join(trgtfolder,target)
					
					# check if we're allowed to edit this file or it has been created by someone else
					canown = (not os.path.exists(fulltarget)) or (target in modinfo["results"].get(f,[]))
					if canown or ask("File "+col["yellow"](target)+" exists, but is not tied to this source file! Overwrite?"):
						print("\tCreating",col["green"](target))
						new_createdfiles.append(target)
						with open(fulltarget,"w",encoding=ENCODING) as tf:
							tf.write(individual_files[target])
					else:
						print("\tDid not create",col["red"](target))
						
						
				if len(loc_keys) != 0:
					target = os.path.join("localisation",identifier + ".csv")
					fulltarget = os.path.join(trgtfolder,target)
					os.makedirs(os.path.join(trgtfolder,"localisation"),exist_ok=True)
					canown = (not os.path.exists(fulltarget)) or (target in modinfo["results"].get(f,[]))
					if canown or ask("File "+col["yellow"](target)+" exists, but is not tied to this source file! Overwrite?"):
						print("\tCreating",col["green"](target))
						new_createdfiles.append(target)
						with open(fulltarget,"w",encoding=ENCODING) as tf:
							writer = csv.writer(tf,delimiter=";")
							for key in loc_keys:
								writer.writerow([key] + [loc_keys[key]] + [""] * 12 + ["x"])
					else:
						print("\tDid not create",col["red"](target))
					
					
			else:
				print("File",col["red"](f),"will be ignored...")
				
				
				
		
			
				
		
		modinfo["times"][f] = srcfiles[f]
		modinfo["results"][f] = list(set(new_createdfiles))
		for fr in [fil for fil in old_createdfiles if fil not in new_createdfiles]:
			print("Removing",col["red"](fr),"as its no longer created by source",col["red"](f))
				
	
	
	# GFX DEFINITIONS
	if changed_gfx_files["traits"]:
		sprites = []
		for f in os.listdir(os.path.join(srcfolder,"gfx","traits")):
			name = f.split(".")[0]	
			sprites.append(("spriteType","=",[
				("name","=","GFX_trait_" + name),
				("texturefile","=","gfx\\\\traits\\\\" + name + ".dds"),
				("noOfFrames","=",1),
				("norefcount","=","yes"),
				("effectFile","=","gfx/FX/buttonstate.lua")
			]))
		
		defin = CK2Definition([("spriteTypes","=",sprites)])
			
		gfxfilefolder = os.path.join("interface")
		gfxfile = os.path.join(gfxfilefolder,modname + "_svrvtraits.gfx")
		os.makedirs(os.path.join(trgtfolder,gfxfilefolder),exist_ok=True)
		print("Creating",col["green"](gfxfile))
		defin.write(os.path.join(trgtfolder,gfxfile),format="ck2")
			
			
	# print suvorov info data
	with open(os.path.join(trgtfolder,METAFILE),"w") as suvorovfile:
		yaml.dump(modinfo,suvorovfile)
	
	
	
	
# text files with enclosing scopes
def process_txt_file(content):
	
	l = get_top_scopes(content)
	entries = {} # all entries that belong to this identifier, by folder
	individual_files = {}
	for scope,txt in l:
		if scope in scope_types:
			folder,keep = scope_types[scope]
			
			# decrease tabulation by one
			if not keep:
				txt = "\n".join(l[1:] for l in txt.split("\n") if l.startswith("\t"))
			else:
				txt = scope + " = {\n" + txt + "\n}"
			entries.setdefault(folder,[]).append(txt)
			
			
		elif scope in scope_types_separate_files:
			folder, = scope_types_separate_files[scope]
			txt = "\n".join(l[1:] for l in txt.split("\n") if l.startswith("\t"))
			subscopes = get_top_scopes(txt)
			for sscope,stxt in subscopes:
				filename = os.path.join(folder,sscope + ".txt")
				stxt = "\n".join(l[1:] for l in stxt.split("\n") if l.startswith("\t"))
				individual_files[filename] = stxt
			
		else:
			print("\tScope",col["red"](scope),"is not valid.")
			
			
	return entries,individual_files
	
# text files with additional logic
def process_suv_file(content,data):
	from .ck2file import CK2Definition
	from .suvfile import suv_eval
	
	localisation = {}
	
	t = CK2Definition(content)
	datastack = DictStack(data)
	result = list(suv_eval(t.data,datastack,loc_keys=localisation))
	#print(localisation)
	r = CK2Definition(result)
	return process_txt_file(r.generate(format="ck2")) + (localisation,) # for now

	
	
# yml files
def process_svy_file(content):

	from .ck2file import CK2Definition
	
	keepaslist = [
		("on_actions",None,"events"),
		("traits",None,"opposites")
	]
	
	r = CK2Definition(yaml.safe_load(content))
	return process_txt_file(r.generate(format="ck2")) #for now
	
	
	

		
def delete_mod(name):
	pass
