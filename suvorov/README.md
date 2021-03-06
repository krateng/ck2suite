# Suvorov: Expanded scripting language for CK2

[![](https://img.shields.io/pypi/v/suvorov?style=for-the-badge)](https://pypi.org/project/suvorov/)
[![](https://img.shields.io/pypi/dm/suvorov?style=for-the-badge)](https://pypi.org/project/suvorov/)
[![](https://img.shields.io/github/stars/krateng/ck2suite?style=for-the-badge&color=purple)](https://github.com/krateng/ck2suite/stargazers)
[![](https://img.shields.io/pypi/l/suvorov?style=for-the-badge)](https://github.com/krateng/ck2suite/blob/master/LICENSE)

Suvorov allows you to write CK2 modifications in a more concise and organized fashion, grouping features together according to your own file structure instead of splitting each individual feature up over a multitude of folders. For example, if you have an event that fires on a specific action and adds a character modifier, you can group the on_action, the event and the modifier together in the same file. If you add a new province, you can define its history, titles, holder character etc in the same file. If you create a trait that unlocks an associated targetted decision as well as a maintenance event to fire for all trait holders, there is no need to pollute three different subfolders. This way, mods are more maintainable and adding or removing features doesn't mean you have to go through several different files.

## Install and use

Install with `pip install suvorov`. Make sure to use `pip3` if Python 3 isn't your default version.

You can now create new mods in the folder `suvorovmods` in your CK2 user directory.

Call the command `suvorov build (modfoldername)` to prepare the mod so that CK2 can read it. Call `suvorov build` without any arguments to build all your mods.


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
	
Specify your mod metadata (name, picture, esc.) in `modinfo.yml` in the root of your folder directory.

## New Syntax

### Path-independent definitions

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
	
### Templating

In case of `.suv` files, you can also use some basic templating:


	events = {
		namespace = mymod
		
		character_event = {
			id = mymod.2
			is_triggered_only = yes
			
			@forin = {
				@for = choice
				@in = choices
				option = {
					name = $$choice.name
					change_$$choice.attribute = 2
				}
			}
		}
	}
	
The data source for these can be defined over any number of `.yaml` files in your mod under the top key `data`, like this:

```yaml
data:
   choices:
   - name: "Use the dagger"
     attribute: "intrigue"
   - name: "Use the quill"
     attribute: "diplomacy"
```

### Inline localisation

`.suv` files allow you to localize things directly in their definition file - if you don't care about multilingual support, this is a nice way to further lower the amount of files and to keep things together:


	traits = {
		idol = {
			@loc = "Idol"
			@loc_desc = "This character is a K-Pop Idol."
			sex_appeal_opinion = 70
			intrigue = 1
		}
	}
	
	events = {
		character_event = {
			id = 31
			desc = @loc:"Your sister wants to become a K-Pop idol."
			
			option = {
				name = @loc:"Nice"
				FROM = { add_trait = idol }
			}
		}
	
	}
	
<!---
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
-->




