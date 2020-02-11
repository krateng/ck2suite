import os
import shutil
import sys
import yaml
import re
from doreah.control import mainfunction
from doreah.io import col, ask

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

METAFILE = "benedek.yml"
SRCFOLDER = "benedek"

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
		
	
			





def convert_mod(srcmodfolder,targetmodfolder):

	modname = os.path.basename(srcmodfolder)

	try:
		with open(os.path.join(targetmodfolder,METAFILE)) as metaf:
			modinfo = yaml.safe_load(metaf.read()) or {}
	except:
		modinfo = {}
	if "files" not in modinfo: modinfo["files"] = []
	
	os.chdir(srcmodfolder)
	# go to the folder instead of path.join so that all names we print / save are relative to it
	
	# delete old mod folder
	if os.path.exists(targetmodfolder):
		shutil.rmtree(targetmodfolder)
		
	
	
	# copy all non-benedek files
	for folderorfile in os.listdir():
		if folderorfile not in [SRCFOLDER,"modinfo.yml"]:
			if os.path.isdir(folderorfile):
				shutil.copytree(folderorfile,os.path.join(targetmodfolder,folderorfile))
			else:
				shutil.copy(folderorfile,os.path.join(targetmodfolder,folderorfile))
			print("Copying",folderorfile)
			
	
	
	# evaluate benedek
	srcfiles = []
	for (dirpath,dirnames,filenames) in os.walk(SRCFOLDER):
		srcfiles += [os.path.join(dirpath, f) for f in filenames if f.endswith(".txt")]
	
	for f in srcfiles:
		identifier = f.replace("/",".")
		
		with open(f) as fi:
			l = get_top_scopes(fi.read())
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
				print("File",col["yellow"](f),":","Scope",col["cyan"](scope),"is not valid.")
				
		for folder in entries:
			os.makedirs(os.path.join(targetmodfolder,folder),exist_ok=True)
			target = os.path.join(folder,identifier)
			fulltarget = os.path.join(targetmodfolder,target)
			if not os.path.exists(fulltarget) or target in modinfo["files"] or ask("File "+col["yellow"](target)+" already exists and is not managed by Benedek! Overwrite?"):
				with open(fulltarget,"w") as targetfile:
					targetfile.write("\n".join(entries[folder]))
				modinfo["files"].append(target)
				print("Created file",col["green"](target))
			
			else:
				print("File",col["red"](target),"was not written!")
				
	modinfo["files"] = list(set(modinfo["files"]))
	
	with open(os.path.join(targetmodfolder,METAFILE),"w") as metaf:
		yaml.dump(modinfo,metaf)
		
		
		
@mainfunction({},shield=True)
def main(srcmodfolder):

	srcmodfolder = os.path.abspath(srcmodfolder)
	srcmodfile = os.path.join(srcmodfolder,"modinfo.yml")
	modname = os.path.basename(srcmodfolder)
	ck2userfolder = os.path.abspath(os.path.dirname(os.path.dirname(srcmodfolder)))
	targetmodfolder = os.path.join(ck2userfolder,"mod","benedek." + modname)
	targetmodfile = os.path.join(ck2userfolder,"mod","benedek." + modname + ".mod")
	
	
	
	if os.path.exists(targetmodfolder) and not os.path.exists(os.path.join(targetmodfolder,METAFILE)) and not ask("Mod " + targetmodfolder + " already exists, but is not managed by Benedek. Overwrite?"):
		print("Mod was not created.")
		return
		
	convert_mod(srcmodfolder,targetmodfolder)
	
	# gather mod data
	modmetadata = {}
	if os.path.exists(srcmodfile):
		with open(srcmodfile) as modfile:
			modmetadata.update(yaml.safe_load(modfile.read()))
	if "name" not in modmetadata: modmetadata["name"] = modname
	
	# write modfile
	with open(targetmodfile,"w") as modfile:
		for e in modmetadata:
			modfile.write(e + ' = "' + modmetadata[e] + '"\n')
		modfile.write('path = "mod/' + "benedek." + modname + '"')
