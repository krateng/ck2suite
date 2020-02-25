from PIL import Image, ImageDraw
from wand.image import Image as WandImage
from io import BytesIO


CIRCLEMASK = Image.new("L", (152,152), 0)
draw = ImageDraw.Draw(CIRCLEMASK)
draw.ellipse((0, 0, 152, 152), fill=255)
EMPTY = Image.new("RGBA", (152,152), 0)


def load_from_file(f):
	if f.split(".")[-1].lower() == "dds":
		return load_from_dds_file(f)
	else:
		return load_from_other_file(f)

def load_from_other_file(f):
	img = Image.open(f)
	return img
	
# pillow can open with v7.0.0, but screws up colors
def load_from_dds_file(f):
	wimg = WandImage(filename=f)
	tmp = BytesIO()
	wimg.save(tmp)
	tmp.seek(0)
	img = Image.open(tmp)
	return img

def crop(img):
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
	
	return img
	
def combine(*imgs,lead_empty=0):

	imgs = [EMPTY] * lead_empty + list(imgs)

	num = len(imgs)

	img = Image.new("RGBA",(152*(len(imgs)),152))
	j = 0
	for i in imgs:
		insert(i,img,j)
		j += 1
		
	return img
	
def insert(src,target,index):
	target.paste(src,(index*152,0))
	

def write_to_dds_file(img,f):
			
	tmp = BytesIO()
	img.save(tmp,format="png")
	tmp.seek(0)
	wand_img = WandImage(file=tmp)
	wand_img.compression = 'dxt5'
	wand_img.save(filename=f)
	
def write_to_png_file(img,f):
	img.save(f)
	

