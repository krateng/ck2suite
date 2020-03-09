from .convert import build_mod, build_all_mods
from .setup import setup
from doreah.control import mainfunction



@mainfunction({"f":"force"},shield=True)
def main(command,*args,force:bool=False):

	if command == "setup":
		setup()
	elif command == "build":
		if len(args) > 0:
			build_mod(args[0],force_rebuild=force)
		else:
			build_all_mods(force_rebuild=force)
