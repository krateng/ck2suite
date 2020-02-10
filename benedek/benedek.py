import os
import sys
import yaml
import re
from doreah.control import mainfunction
from doreah.io import col, ask

scope_types = {
	"on_actions":("common/on_actions",False),
	"character_event":("events",True),
	"events":("events",False)
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
		
def find_real_modfolder(modfolder):
	if os.path.isfile(modfolder):
		dirname = os.path.dirname(modfolder)
		# .mod file
		if modfolder.split(".")[-1].lower() == "mod":
			with open(modfolder) as modfile:
				lines = modfile.readlines()
				for line in lines:
					try:
						modpath = re.match(r'path="mod/(.*)"',line).groups()[0]
						modfolder = os.path.join(dirname,modpath)
						return modfolder
					except: pass
		# metafile
		elif os.path.basename(modfolder) == METAFILE:
			return dirname
			
	return modfolder
		
			

@mainfunction({},shield=True)
def main(modfolder):

	# recover from different passed arguments
	modfolder = find_real_modfolder(modfolder)
	
	try:
		with open(os.path.join(modfolder,METAFILE)) as metaf:
			modinfo = yaml.safe_load(metaf.read()) or {}
	except:
		modinfo = {}
	if "files" not in modinfo: modinfo["files"] = []
	
	os.chdir(modfolder)
	# go to the folder instead of path.join so that all names we print / save are relative to it
	
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
			os.makedirs(os.path.join(modfolder,folder),exist_ok=True)
			target = os.path.join(folder,identifier)
			if not os.path.exists(target) or target in modinfo["files"] or ask("File "+col["yellow"](target)+" already exists and is not managed by Benedek! Overwrite?"):
				with open(target,"w") as targetfile:
					targetfile.write("\n".join(entries[folder]))
				modinfo["files"].append(target)
				print("Created file",col["green"](target))
			
			else:
				print("File",col["red"](target),"was not written!")
				
	modinfo["files"] = list(set(modinfo["files"]))
	
	with open(os.path.join(modfolder,METAFILE),"w") as metaf:
		yaml.dump(modinfo,metaf)
