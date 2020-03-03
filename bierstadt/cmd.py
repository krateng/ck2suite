from . import library
from doreah.control import mainfunction


def create(inputfiles,outputfile,also_write_png=True,imgtype=library.Portrait):
	imgs = [imgtype(f) for f in inputfiles]
	sp = library.Sprite(*imgs)
	sp.write(outputfile,also_write_png=also_write_png)
	
def insert(inputfile,outputfile,index,also_write_png=True,imgtype=library.Portrait):
	targetimg = library.Sprite(outputfile)
	srcimg = imgtype(inputfile)
	
	targetimg.insert(srcimg,index)
	targetimg.write(outputfile,also_write_png=also_write_png)
		
types = {
	"portrait":library.Portrait,
	"trait":library.TraitIcon,
	"event":library.EventPicture
}
		
@mainfunction({"t":"type"},shield=True)	
def cmd(command,*args,imgtype="portrait",**kwargs):
	if command == "create":
		inputfiles = args
		create(args,"result.dds",imgtype=types[imgtype])
	elif command == "insert":
		src,target,index = args
		index = int(index)
		insert(src,target,index,imgtype=types[imgtype])
