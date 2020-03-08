from .ck2path import CK2DataDir
from . import conf
from .ck2file.classes import CK2Definition, CK2Localisation
from .suvfile import suv_eval

import os

from doreah.filesystem import Directory, RelativeFile
from doreah.io import col
from doreah.datatypes import DictStack

import yaml


def build_all_mods():
	pass

def build_mod(modname,force_rebuild=False):
	TARGETMOD = CK2DataDir.MOD(conf.SUVOROVMODPREFIX + modname)
	SRCMOD = CK2DataDir.SUVOROVMOD(modname)

	TARGETMODFILE = TARGETMOD + ".mod"
	TARGETMETAFILE = os.path.join(TARGETMOD,conf.METAFILE)
	SRCMODINFOFILE = os.path.join(SRCMOD,conf.MODINFOFILE)


	# gather mod data
	modmetadata = {}
	if os.path.exists(SRCMODINFOFILE):
		with open(SRCMODINFOFILE) as modfile:
			modmetadata.update(yaml.safe_load(modfile.read()))
	if "name" not in modmetadata: modmetadata["name"] = modname
	modmetadata["path"] = os.path.join("mod",conf.SUVOROVMODPREFIX + modname)




	# write modfile
	with open(TARGETMODFILE,"w") as modfile:
		for e in modmetadata:
			modfile.write(e + ' = "' + modmetadata[e] + '"\n')






	# load info from last build
	with open(TARGETMETAFILE,"r") as metaf:
		modinfo = yaml.safe_load(metaf.read())
	if modinfo is None: modinfo = {}
	if not "mtimes" in modinfo: modinfo["mtimes"] = {}
	if force_rebuild: modinfo["mtimes"] = {}

	# get mtimes for files
#	times = directory_dict(SRCMOD,file_values=os.path.getmtime)
#	prevtimes = modinfo["times"]


	srcmod = Directory(SRCMOD)
	targetmod = Directory(TARGETMOD)

	generated_files = []


	# get existing files in target folder
#	filestodelete = list(f.relpath for f in targetmod.allfiles())
#	filestodelete.remove(conf.METAFILE)



	data = {}



	#####
	#####
	## OVERRIDES / VANILLA STRUCTURE
	#####
	#####

	print("Copying vanilla files...")
	pdxfiles = srcmod["pdx"].allfiles()
	for f in pdxfiles:

		generated_files.append(f.relpath)

		if f.mtime() != modinfo["mtimes"].get("pdx",{}).get(f.relpath):
			#f.copyinto(targetmod)
			print("\tCopying",col["green"](f))
			modinfo["mtimes"].setdefault("pdx",{})[f.relpath] = f.mtime()
		else:
			print("\tSkipping",col["darkgrey"](f))

	#####
	#####
	## SMART GFX
	#####
	#####

	print("Handling graphics files...")
	for gfxtype in conf.gfx_types:
		gfxfiles = srcmod["gfx"][gfxtype].allfiles()
		any_changed_files = False
		for f in gfxfiles:

			targetname = f.parentview().parentview()

			generated_files.append(targetname.relpath)

			if f.mtime() != modinfo["mtimes"].get("gfx",{}).get(gfxtype,{}).get(f.relpath):
				#f.copyinto(targetmod)
				any_changed_files = True
				print("\tCopying",col["green"](targetname))
				modinfo["mtimes"].setdefault("gfx",{}).setdefault(gfxtype,{})[f.relpath] = f.mtime()
			else:
				print("\tSkipping",col["darkgrey"](f))

		if any_changed_files:
			print("\tCreating sprite...")



	from pprint import pprint
	#####
	#####
	## ANY LOCATION FILES
	#####
	#####

	otherfiles = list(srcmod.allfiles(exclude=("gfx","pdx","modinfo.yml")))

	###
	# DATA
	###
	print("Loading data...")
	for f in (f for f in otherfiles if f.ext() in conf.DATA_FILE_EXTENSIONS):
		print("Loading",col["purple"](f))
		with f.open() as dataf:
			data.update(yaml.safe_load(dataf).get("data",{}))

	###
	# TXT
	###
	print("Parsing text files...")
	for f in (f for f in otherfiles if f.ext() in conf.TXT_FILE_EXTENSIONS + conf.SUV_FILE_EXTENSIONS):

		if f.mtime() != modinfo["mtimes"].get(f.relpath):
			#f.copyinto(targetmod)
			print("\tParsing",col["cyan"](f))
			modinfo["mtimes"][f.relpath] = f.mtime()

			with f.open() as df:
				defin = CK2Definition(df)

			namewithoutext = ".".join(f.relpath.split(".")[:-1])
			identifier = "svrv." + ".".join(namewithoutext.split("/"))

			localisation = {}

			# if suv file, parse first
			if f.ext() in conf.SUV_FILE_EXTENSIONS:
				datastack = DictStack(data)
				result = list(suv_eval(defin.data,datastack,loc_keys=localisation))
				defin = CK2Definition(result)

			# get top scopes and deal with them according to rules
			topscopes = defin.separate_top_scopes()
			for scope in topscopes:
				if scope in conf.scope_types:
					folder,keep,ownfile = conf.scope_types[scope]

					res = topscopes[scope]
					if keep:
						res = CK2Definition([(scope,"=",res.data)])

					# TODO: separate files

					targetfile = targetmod.relfile(os.path.join(folder,identifier + ".txt"))
					print("\tWriting",col["green"](targetfile))
					with targetfile.open("w") as tf:
						res.write(tf)

					generated_files.append(targetfile.relpath)
					modinfo.get("generated",{}).get(f.relpath,[]).append(targetfile.relpath)


			# localisation
			if len(localisation) > 0:
				targetfile = targetmod.relfile(os.path.join("localisation",identifier + ".csv"))
				l = CK2Localisation(localisation)
				print("\tWriting",col["green"](targetfile))
				with targetfile.open("w") as tf:
					l.write(tf)
				modinfo.get("generated",{}).get(f.relpath,[]).append(targetfile.relpath)


		else:
			print("\tSkipping",col["darkgrey"](f))
			generated_files += modinfo.get("generated",{}).get(f.relpath,[])


	# TODO: delete old files



	# print new suvorov info data
	with open(TARGETMETAFILE,"w") as metaf:
		yaml.dump(modinfo,metaf)
