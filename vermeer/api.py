from . import library
from doreah.control import mainfunction


def create(inputfiles,outputfile,also_write_png=True):
	imgs = [library.load_from_file(f) for f in inputfiles]
	imgs = [library.crop(img) for img in imgs]
	img = library.combine(*imgs)
	library.write_to_dds_file(img,outputfile)
	if also_write_png:
		library.write_to_png_file(img,".".join(outputfile.split(".")[:-1] + ["png"]))
	
def insert(inputfile,outputfile,index,also_write_png=True):
	srcimg = library.load_from_file(inputfile)
	srcimg = library.crop(srcimg)
	targetimg = library.load_from_file(outputfile)
	library.insert(srcimg,targetimg,index)
	library.write_to_dds_file(targetimg,outputfile)
	if also_write_png:
		library.write_to_png_file(targetimg,".".join(outputfile.split(".")[:-1] + ["png"]))
		
@mainfunction({},shield=True)	
def cmd(command,*args,**kwargs):
	if command == "create":
		inputfiles = args
		create(args,"result.dds")
	elif command == "insert":
		src,target,index = args
		index = int(index)
		insert(src,target,index)
