from .convert import build_mod
from .setup import setup
from .service import parse_mods
from doreah.control import mainfunction
		
	
		
@mainfunction({},shield=True)
def main(command,*args):

	if command == "setup":
		setup()
	elif command == "build":
		if len(args) > 0:
			build_mod(args[0])
		else:
			parse_mods()
