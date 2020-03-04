from PIL import Image, ImageDraw
from wand.image import Image as WandImage
from io import BytesIO




class AbstractPdxImage:
	def __init__(self,*args):
		# create empty image of correct dimensions
		if len(args) == 0:
			self.srcimage = self.empty()
			self.resultimage = self.srcimage
		
		# create from file
		else:
			f = args[0]
			self.srcimage = load_from_file(f)
			
			# SCALE
			width, height = self.srcimage.width, self.srcimage.height
			targetwidth, targetheight = self.DIMENSIONS
			scale = max(targetwidth/width,targetheight/height)
			if scale != 1:
				self.resultimage = self.srcimage.resize((int(scale*width),int(scale*height)))
			else:
				self.resultimage = self.srcimage
				
			# CROP TO RATIO
			width, height = self.resultimage.width, self.resultimage.height
			left_offset = (width - targetwidth) / 2
			top_offset = (height - targetheight) / 2
			self.resultimage = self.resultimage.crop((left_offset,top_offset,targetwidth+left_offset,targetheight+top_offset))
			
			# CROP SHAPE
			self.resultimage = self.crop(self.resultimage)
		
	
	def crop(self,img):
		return img
		
		
	def write(self,f,also_write_png=True):
		write_to_dds_file(self.resultimage,f)
		if also_write_png:
			write_to_png_file(self.resultimage,".".join(f.split(".")[:-1] + ["png"]))
	
	# get empty frame	
	def empty(self):
		return Image.new("RGBA",self.DIMENSIONS)
		
	def show(self):
		self.resultimage.show()


class Sprite(AbstractPdxImage):
	def __init__(self,*args,imagetype=None,**kwargs):
		# create from images
		if all(isinstance(a,AbstractPdxImage) for a in args):
			self.create(*args,**kwargs)
			
		# load existing
		elif len(args) == 1:
			self.resultimage = load_from_file(args[0])
			self.DIMENSIONS = self.resultimage.width, self.resultimage.height
			# assume that its frames are portraits as we cannot know what it was created from
			self.imagetype = imagetype or Portrait
			
	def create(self,*imgs,lead_empty=0):
		self.imagetype = type(imgs[0])
		assert all(isinstance(i,self.imagetype) for i in imgs)
		frames = [self.imagetype()] * lead_empty + list(imgs)
		
		maxnum = self.imagetype.SPRITE_SIZE
		num = len(frames)
		assert num <= maxnum
		
		
		height = self.imagetype.DIMENSIONS[1]
		width = self.imagetype.DIMENSIONS[0] * num
		self.DIMENSIONS = (width,height)

		

		self.resultimage = Image.new("RGBA",(width,height))
		j = 0
		for f in frames:
			self.insert(f,j)
			j += 1

		
	def insert(self,img,index):
		self.resultimage.paste(img.resultimage,(index*self.imagetype.DIMENSIONS[0],0))
		
		
		
class Portrait(AbstractPdxImage):
	DIMENSIONS = (152,152)
	SPRITE_SIZE = 26
	
	def crop(self,img):
		mask = Image.new("L", (152,152), 0)
		draw = ImageDraw.Draw(mask)
		draw.ellipse((0, 0, 152, 152), fill=255)
		return Image.composite(img,self.empty(),mask)
	
class EventPicture(AbstractPdxImage):
	DIMENSIONS = (450,150)
	SPRITE_SIZE = 1
	
class TraitIcon(AbstractPdxImage):
	DIMENSIONS = (24,24)
	SPRITE_SIZE = 1







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
	
	
def write_to_dds_file(img,f):
			
	tmp = BytesIO()
	img.save(tmp,format="png")
	tmp.seek(0)
	wand_img = WandImage(file=tmp)
	wand_img.compression = 'dxt5'
	wand_img.save(filename=f)
	
def write_to_png_file(img,f):
	img.save(f)
	
	

	

