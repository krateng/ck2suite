# CK2 STAtic POrtrait MOd Generator

[![](https://img.shields.io/pypi/v/stapomog?style=for-the-badge)](https://pypi.org/project/stapomog/)
[![](https://img.shields.io/pypi/dm/stapomog?style=for-the-badge)](https://pypi.org/project/stapomog/)
[![](https://img.shields.io/github/stars/krateng/stapomog?style=for-the-badge&color=purple)](https://github.com/krateng/stapomog/stargazers)
[![](https://img.shields.io/pypi/l/stapomog?style=for-the-badge)](https://github.com/krateng/stapomog/blob/master/LICENSE)

A quick tool to generate static portrait mods for Crusader Kings 2.

## Install

Install with `pip install stapomog`. Make sure to use `pip3` if Python 3 isn't your default version.


## Use

Copy all your image files into a folder. There's no need to crop them into circles, but make sure your character's face is somewhat centered. Name the files following the pattern `name_agerange.ext`. Everything after the first dot is ignored, so you can have multiple files with the same attributes.

Example:

	hannah_20-30.png # will be used for the "hannah" portrait between ages 20 and 30
	steve_mid.jpg	# will be used for the "steve" portrait between ages 30 and 49, regardless of portrait settings in defines
	mike_35-40.alternate.jpeg # will be used for the "mike" portrait between ages 35 and 40
	emily_-30.png # will be used for the "emily" portrait up to age 30
	tiffany.jpg # will be used for the "tiffany" portrait at any age
	gilly_young.png # will be used for the "gilly" portrait from ages 16-29, regardless of portrait settings in defines
	
Then simply run the command `stapomog (folder)`. It will generate a new mod in the folder `stapomog_portrait_mod`. Merge this folder with your existing mod or use it as a standalone mod (make sure to create a .mod file).

You can now assign the new portraits by adding traits with events, decisions or console commands - they are simply named `portrait_(name)`.

If you add additional pictures, you can simply update your existing mod (even if you moved and renamed it) by running `stapomog (modfolder)`. Keep in mind that updating mods midgame will break your savegames if traits are added or removed.
