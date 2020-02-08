import os
from PIL import Image, ImageDraw
from wand.image import Image as WandImage
from zipfile import ZipFile
import re
from io import BytesIO
import yaml

from doreah.control import mainfunction
from doreah.io import col

from .config import GLOBALCONFIG, USERCONFIG
from .templates import *





### PREPARATIONS

# predefine mask
CIRCLEMASK = Image.new("L", (152,152), 0)
draw = ImageDraw.Draw(CIRCLEMASK)
draw.ellipse((0, 0, 152, 152), fill=255)
EMPTY = Image.new("RGBA", (152,152), 0)

# regex for portrait files
regex_portraitfile = re.compile(r"[0-9]*_?portraits+(" + "|".join(["_" + s for s in GLOBALCONFIG["GFX_CULTURES"]] + [""]) + ")(" + "|".join(["_" + s for s in GLOBALCONFIG["GFX_AGES"]] + [""]) + ").gfx")





def create_mod(inputdir,moddir):

	#create directory structure
	for directory in [os.path.dirname(f) for t,f in GLOBALCONFIG["MOD_FILES"].items()] + [f for t,f in GLOBALCONFIG["MOD_FOLDERS"].items()]:
		os.makedirs(os.path.join(moddir,directory),exist_ok=True)
		
		
	# read portraits
	portraits = read_raw_portraits(inputdir)
	
	# create layers
	layers = combine_frames(portraits)
	
	# create sprites
	sprites = create_sprites(layers,moddir)
		
	
	if USERCONFIG["USE_SOCIETY_OVERRIDE"]:
		create_society_overrides(sprites,moddir)
	else:
		create_portrait_properties(sprites,moddir)
		
	
	people = set(entry["name"] for entry in portraits)
		
		
	create_traits(people,moddir)
	create_documentation(people,moddir)
	create_metadata(moddir,inputdir)




### READ ALL INDIVIDUAL PORTRAITS
def read_raw_portraits(folder):
	portraits = []

	for f in os.listdir(folder):
		if f.split(".")[-1].lower() in GLOBALCONFIG["IMAGE_EXTENSIONS"]:
			rawname = f.split(".")[0]
			name,agerange, *_ = rawname.split("_") + ["",""]
			try:
				minage,maxage = agerange.split("-")
				try: minage = int(minage)
				except: minage = None
				try: maxage = int(maxage)
				except: maxage = None
			except: minage,maxage = None,None
			
			
			img = Image.open(os.path.join(folder,f))
			# SCALE
			width, height = img.width, img.height
			scale = 152 / min(width,height)
			if scale != 1:
				img = img.resize((int(scale*width),int(scale*height)))
			# CROP TO SQUARE
			width, height = img.width, img.height
			left_offset = (width - 152) / 2
			top_offset = (height - 152) / 2
			img = img.crop((left_offset,top_offset,152+left_offset,152+top_offset))
			# CROP TO CIRCLE
			img = Image.composite(img,EMPTY,CIRCLEMASK)
			
				
			
			portraits.append({"name":name,"minage":minage,"maxage":maxage,"img":img})
			#img.show()
	#print(portraits)
	
	return portraits




### COMBINE FRAMES TO LAYERS
def combine_frames(portraits):
	layers = []


	# sort entries by person
	people = {}
	for entry in portraits:
		people.setdefault(entry["name"],[]).append(entry)
	# create layer list
	for name in people:
		layers.append(people[name])
	layers.sort(key=len,reverse=True)


	# split layers if too big
	while len(layers[0]) > GLOBALCONFIG["FRAMES_PER_LAYER"]:
		l = layers.pop(0)
		l1,l2 = l[0:GLOBALCONFIG["FRAMES_PER_LAYER"]],l[GLOBALCONFIG["FRAMES_PER_LAYER"]:]
		layers += [l1,l2]
		layers.sort(key=len,reverse=True)
		

	# combine smaller layers
	# TODO
	
	return layers


### GENERATE SPRITES
def create_sprites(layers,moddir):
	sprites = {}

	spfile = os.path.join(moddir,GLOBALCONFIG["MOD_FILES"]["PORTRAIT_SPRITES_DEFINITION"])
	with open(spfile,"w") as spritefile:

		spritefile.write("spriteTypes = {")

		i = 0
		for layer in layers:
			filename = GLOBALCONFIG["MOD_FILES"]["SPRITES"].format(idx=i)
			fullpath = os.path.join(moddir,filename)
			spritename = GLOBALCONFIG["SPRITE_NAME"].format(idx=i)
			sprites[spritename] = [None] * (len(layer) + 1)
			
			img = Image.new("RGBA",(152*(len(layer)+1),152))
			j = 0
			for frame in layer:
				j += 1
				img.paste(frame["img"],(j * 152,0))
				frame["sprite"] = (spritename,j)
				sprites[spritename][j] = frame
			
			
			spritefile.write(template_sprite.format(reference=spritename,filename=filename.replace("/",r"\\"),frames=len(layer)+1))
			
			if USERCONFIG["ALSO_SAVE_PNG"]:
				png_filename = os.path.splitext(fullpath)[0] + ".png"
				img.save(png_filename)	
			
			# convert to wand (pillow has no DDS)
			tmp = BytesIO()
			img.save(tmp,format="png")
			tmp.seek(0)
			wand_img = WandImage(file=tmp)
			wand_img.compression = 'dxt5'
			wand_img.save(filename=fullpath)
			
			i += 1

		
		spritefile.write("}")	
	
	return sprites
	
	

### DEFINE SOCIETY OVERRIDES
def create_society_overrides(sprites,moddir):
	orfile = os.path.join(moddir,GLOBALCONFIG["MOD_FILES"]["PORTRAIT_TYPES_DEFINITION"])
	with open(orfile,"w") as overridesfile:
		overridesfile.write("spriteTypes = {")
		for spritename in sprites:
			entries = [entry for entry in sprites[spritename] if entry is not None]
			persons = set(entry["name"] for entry in entries)
			
			overridesfile.write(template_portraittype.format(spritename=spritename,
									conditions_portrait_trait="\n".join(template_condition_portraittrait.format(name=p) for p in persons),
									portrait_props="\n".join(template_portrait_prop.format(index=entry["sprite"][1]) for entry in entries)))
		overridesfile.write("}")


### CREATE OLD STYLE PORTRAIT PROPERTIES
def create_portrait_properties(sprites,moddir):

	# write portrait properties
	spriteentries = []
	prfile = os.path.join(moddir,GLOBALCONFIG["MOD_FILES"]["PORTRAIT_PROPERTIES"])
	with open(prfile,"w") as prop_file:
		overview, mainsection = [], []
		layernum = GLOBALCONFIG["FIRST_LAYER"]
		for spritename in sprites:
		
			entries = [entry for entry in sprites[spritename] if entry is not None]
		
			persons = set(entry["name"] for entry in entries)
			overview.append("# p" + str(layernum) + " " + ", ".join(persons))
			spriteentries.append("\t\t\t" + '"' + spritename + ":p" + str(layernum) + '"')
			mainsection.append("# " + spritename)
			mainsection.append(str(layernum) + " = {")
			# add blank default
			mainsection.append(template_layerentry_blank.format(noblank_modifiers="\n".join(template_noblank.format(name=p) for p in persons)))
			idx = 1
			for entry in entries:
				modifier_min = "" if entry["minage"] is None else template_layerentry_minage.format(age=entry["minage"])
				modifier_max = "" if entry["maxage"] is None else template_layerentry_maxage.format(age=entry["maxage"])
				mainsection.append(template_layerentry.format(index=entry["sprite"][1],name=entry["name"],agemodifiers=modifier_min + "\n" + modifier_max))
					
				idx += 1
				
			mainsection.append("}")
			mainsection.append("")
			mainsection.append("")
			layernum += 1
			
		content = "\n".join(overview + ["",""] + mainsection)
		
		prop_file.write(content)
		
	# copy over portrait logic files
	
	for folder in GLOBALCONFIG["GAME_FOLDERS_PORTRAIT_DEFINITIONS"]:

		srcdir = os.path.join(USERCONFIG["GAME_FOLDER"],folder)
		trgtdir = os.path.join(moddir,folder)
		for f in os.listdir(srcdir):
			if regex_portraitfile.fullmatch(f):
				with open(os.path.join(srcdir,f),"r") as src:
					with open(os.path.join(trgtdir,f),"w") as trgt:
						for l in src.readlines():
							if "GFX_character_imprisoned:p6" in l:
								trgt.write("\n".join(spriteentries))
								trgt.write("\n")
							trgt.write(l)

	
	# DLCs
	dlcfolder = os.path.join(USERCONFIG["GAME_FOLDER"],GLOBALCONFIG["GAME_FOLDER_DLC"])
	for zf in os.listdir(dlcfolder):
		if zf.endswith(".zip"):
			with ZipFile(os.path.join(dlcfolder,zf)) as zipf:
				zip_content = zipf.filelist
				for f in zip_content:
					for folder in GLOBALCONFIG["GAME_FOLDERS_PORTRAIT_DEFINITIONS"]:
						
						if f.filename.startswith(folder):
							#print(f.filename,"could be relevant")
							name = f.filename.split("/")[-1]
							if regex_portraitfile.fullmatch(name):
								with zipf.open(f,"r") as src:
									with open(os.path.join(moddir,f.filename),"w") as trgt:
									#same path relative to mod because we want to overwrite
										for l in src.readlines():
											l = l.decode("UTF-8")
											if "GFX_character_imprisoned:p6" in l:
												trgt.write("\n".join(spriteentries))
												trgt.write("\n")
											trgt.write(l)


# create traits
def create_traits(people,moddir):
	tfile = os.path.join(moddir,GLOBALCONFIG["MOD_FILES"]["TRAITS"])
	with open(tfile,"w") as trait_file:
		for person in people:
			trait_file.write(template_trait.format(name=person))
		
		

		
		
		
		
# info file
def create_documentation(people,moddir):
	ifile = os.path.join(moddir,"info.txt")
	with open(ifile,"w") as infofile:
		infofile.write("This is your generated portrait mod. The following traits are available to assign to characters:\n\n")
		for person in people:
			infofile.write("portrait_" + person + "\n")
			
			

def create_metadata(moddir,inputdir):
	mfile = os.path.join(moddir,"stapomog.yml")
	with open(mfile,"w") as metafile:
		metafile.write(yaml.dump({
			"picture_source":os.path.abspath(inputdir)
		}))
			
			
			
			
			
			
@mainfunction({},shield=True)
def main(inputdir):
	if os.path.exists(os.path.join(inputdir,"stapomog.yml")):
		print("Found existing mod, updating...")
		with open(os.path.join(inputdir,"stapomog.yml")) as metafile:
			meta = yaml.safe_load(metafile.read())
		if os.path.exists(meta["picture_source"]):
			create_mod(meta["picture_source"],inputdir)
			print("Your mod can be found in",col["yellow"](inputdir))
		else:
			print("Original picture source could not be found.")
	else:
		print("Creating new mod...")
		create_mod(inputdir,"stapomog_portrait_mod")
		print("Your mod can be found in",col["yellow"]("stapomog_portrait_mod"))
