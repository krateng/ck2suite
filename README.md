# Suvorov: Expanded scripting language for CK2

[![](https://img.shields.io/pypi/v/suvorov?style=for-the-badge)](https://pypi.org/project/suvorov/)
[![](https://img.shields.io/pypi/dm/suvorov?style=for-the-badge)](https://pypi.org/project/suvorov/)
[![](https://img.shields.io/github/stars/krateng/suvorov?style=for-the-badge&color=purple)](https://github.com/krateng/suvorov/stargazers)
[![](https://img.shields.io/pypi/l/suvorov?style=for-the-badge)](https://github.com/krateng/suvorov/blob/master/LICENSE)

Suvorov allows you to write CK2 modifications in a more concise and organized fashion, grouping features together according to your own file structure instead of splitting each individual feature up over a multitude of folders. For example, if you have an event that fires on a specific action and adds a character modifier, you can group the on_action, the event and the modifier together in the same file. If you add a new province, you can define its history, titles, holder character etc in the same file. If you create a trait that unlocks an associated targetted decision as well as a maintenance event to fire for all trait holders, there is no need to pollute three different subfolders. This way, mods are more maintainable and adding or removing features doesn't mean you have to go through several different files.

## Install

Install with `pip install suvorov`. Make sure to use `pip3` if Python 3 isn't your default version.

You can now create new mods in the folder `suvorovmods` in your CK2 user directory.


## Mod structure

In a suvorov mod, you can add any files according to the vanilla structure (e.g. gfx, interface, common) in the `pdx` subfolder. For new, suvorov-style files, you can follow any folder structure you like (except the `pdx` folder of course). So your mod could look like this:

	mymod
	├ pdx
	| ├ gfx
	| | └ trait.png
	| └ localisation
	|   └ texts.csv
	├ crusade_changes
	|  ├ crusade_start.txt
	|  └ crusade_end.txt
	├ various.txt
	└ modinfo.yml

These new files with the ending `.txt` or `.suv` accept a syntax like vanilla files, only with an enclosing scope defining their type, e.g.:


	events = {
		namespace = mymod
		
		character_event = {
			id = mymod.1
			is_triggered_only = yes
			
			option = {
				name = mymod.eventoption.1
				add_trait = patient
				remove_trait = cynical
				remove_trait = arbitrary
			}
		}
	}
	
	on_actions = {
		on_crusade_preparation_starts = {
			events = {
				mymod.1
			}
		}
	}
	
You may also use yaml to define various things in `.yml` or `.svy` files, though this is hightly experimental. 'Keys' that appear multiple times must be specified as a list instead:

	events:
	   namespace: mymod
	   character_event:
	   - id: mymod.1
	     is_triggered_only: yes
	     option:
	     - name: mymod.eventoption.1
	       add_trait: patient
	       remove_trait:
	       - cynical
	       - arbitrary
	on_actions:
	   on_crusade_preparation_starts:
	      events:
	      - mymod.1


Specify your mod metadata (name, picture, esc.) in `modinfo.yml` in the root of your folder directory. Then simply call the command `suvorov build (modfoldername)` to prepare the mod so that CK2 can read it. Call `suvorov build` without any arguments to build all your mods.
