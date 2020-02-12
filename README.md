# Suvorov: Expanded scripting language for CK2

[![](https://img.shields.io/pypi/v/suvorov?style=for-the-badge)](https://pypi.org/project/suvorov/)
[![](https://img.shields.io/pypi/dm/suvorov?style=for-the-badge)](https://pypi.org/project/suvorov/)
[![](https://img.shields.io/github/stars/krateng/suvorov?style=for-the-badge&color=purple)](https://github.com/krateng/suvorov/stargazers)
[![](https://img.shields.io/pypi/l/suvorov?style=for-the-badge)](https://github.com/krateng/suvorov/blob/master/LICENSE)

Suvorov allows you to write CK2 modifications in a more concise and organized fashion, grouping features together according to your own file structure instead of splitting each individual feature up over a multitude of folders. For example, if you have an event that fires on a specific action and adds a character modifier, you can group the on_action, the event and the modifier together in the same file. If you add a new province, you can define its history, titles, holder character etc in the same file. If you create a trait that unlocks an associated targetted decision as well as a maintenance event to fire for all trait holders, there is no need to pollute three different subfolders. This way, mods are more maintainable and adding or removing features doesn't mean you have to go through several different files.

## Install

Install with `pip install suvorov`. Make sure to use `pip3` if Python 3 isn't your default version.


## Use

In the folder `suvorovmods` in your CK2 user directory, add a folder for your new mod. You can add any files according to the vanilla structure in this folder (e.g. gfx, interface, common), as well as new Suvorov-style files in the subfolder `suvorov` (you can use any folder structure inside this path).

Specify your mod metadata (name, picture, esc.) in `modinfo.yml`. Then simply call the command `suvorov build (modfolder)` to prepare the mod so that CK2 can read it. Call `suvorov` without any arguments to build all your mods.
