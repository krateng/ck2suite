from .ck2path import CK2DataDir
from . import conf
from .ck2file.classes import CK2Definition, CK2Localisation
from .suvfile import suv_eval
from .utils import deepadd

import os

from doreah.filesystem import Directory, RelativeFile
from doreah.io import col
from doreah.datatypes import DictStack

import yaml

from pprint import pprint


def build_all_mods(force_rebuild=False):
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
	modinfo = {}
	if os.path.exists(TARGETMETAFILE):
		with open(TARGETMETAFILE,"r") as metaf:
			modinfo.update(yaml.safe_load(metaf.read()))
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
			f.copyinto(targetmod)
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
		if not os.path.exists(os.path.join(srcmod.fullpath,"gfx",gfxtype)): continue
		gfxfiles = srcmod["gfx"][gfxtype].allfiles()
		trgtfolder,bierstadt_type = conf.gfx_types[gfxtype]
		any_changed_files = False
		sprites = []

		spritefile = targetmod.relfile(os.path.join("interface",conf.SUVOROVFILEPREFIX + gfxtype + ".gfx"))
		generated_files.append(spritefile.relpath)

		for f in gfxfiles:

			name = f.relpath.split(".")[0]
			relsrc = f.parentview().parentview()
			target = targetmod.relfile(os.path.join(trgtfolder,".".join(f.relpath.split(".")[:-1] + ["dds"])))
			targetpng = targetmod.relfile(os.path.join(trgtfolder,".".join(f.relpath.split(".")[:-1] + ["png"])))

			generated_files.append(target.relpath)
			generated_files.append(targetpng.relpath)

			if f.mtime() != modinfo["mtimes"].get("gfx",{}).get(gfxtype,{}).get(f.relpath):

				gfx = bierstadt_type(f.pth)
				gfx.write(target.pth)

				any_changed_files = True
				print("\tConverting",col["green"](relsrc))
				modinfo["mtimes"].setdefault("gfx",{}).setdefault(gfxtype,{})[f.relpath] = f.mtime()
			else:
				print("\tSkipping",col["darkgrey"](f))

			sprites.append(bierstadt_type.sprite(None,name))

		if any_changed_files:



			defin = CK2Definition([("spriteTypes","=",sprites)])
			print("\tWriting sprite",col["green"](spritefile))
			defin.write(spritefile.pth)




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
			identifier = conf.SUVOROVFILEPREFIX + ".".join(namewithoutext.split("/"))

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

					if ownfile:
						for entry in res.data:
							targetfile = targetmod.relfile(os.path.join(folder,entry[0] + ".txt"))
							defin = CK2Definition(entry[2])
							print("\tWriting",col["green"](targetfile))
							with targetfile.open("w") as tf:
								defin.write(tf)

							# mark new files as generated (for this run) and remember that they belong to this file (for future)
							generated_files.append(targetfile.relpath)
							deepadd(modinfo,("generated",f.relpath),targetfile.relpath)
							#print(modinfo["generated"][f.relpath])

					else:

						targetfile = targetmod.relfile(os.path.join(folder,identifier + ".txt"))
						print("\tWriting",col["green"](targetfile))
						with targetfile.open("w") as tf:
							res.write(tf)

						# mark new files as generated (for this run) and remember that they belong to this file (for future)
						generated_files.append(targetfile.relpath)
						deepadd(modinfo,("generated",f.relpath),targetfile.relpath)


			# localisation
			if len(localisation) > 0:
				targetfile = targetmod.relfile(os.path.join("localisation",identifier + ".csv"))
				l = CK2Localisation(localisation)
				print("\tWriting",col["green"](targetfile))
				with targetfile.open("w") as tf:
					l.write(tf)

				generated_files.append(targetfile.relpath)
				deepadd(modinfo,("generated",f.relpath),targetfile.relpath)

		else:
			print("\tSkipping",col["darkgrey"](f))
			# mark the files we know have been generated by this file in the past (and are up to date)
			generated_files += modinfo.setdefault("generated",{}).get(f.relpath,[])


	###
	# REMOVE OLD
	###
	print("Removing old files...")
	for f in targetmod.allfiles(exclude=(conf.METAFILE)):
		if f.relpath not in generated_files:
			print("\tRemoving",col["red"](f))
			f.remove()



	# print new suvorov info data
	with open(TARGETMETAFILE,"w") as metaf:
		yaml.dump(modinfo,metaf)
