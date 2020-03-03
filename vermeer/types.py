from PIL import Image, ImageDraw

CIRCLEMASK = Image.new("L", (152,152), 0)
draw = ImageDraw.Draw(CIRCLEMASK)
draw.ellipse((0, 0, 152, 152), fill=255)

types = {
	"traiticon":{"dimensions":(24,24),"mask":None},
	"portrait":{"dimensions":(152,152),"mask":CIRCLEMASK,"spritesize":26},
	"eventpicture":{"dimensions":(450,150),"mask":None}
}


for t in types:
	types[t]["empty"] = Image.new("RGBA", types[t]["dimensions"], 0)
