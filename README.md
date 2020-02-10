# Benedek: CK2 Mod Creation Helper

[![](https://img.shields.io/pypi/v/benedek?style=for-the-badge)](https://pypi.org/project/benedek/)
[![](https://img.shields.io/pypi/dm/benedek?style=for-the-badge)](https://pypi.org/project/benedek/)
[![](https://img.shields.io/github/stars/krateng/benedek?style=for-the-badge&color=purple)](https://github.com/krateng/benedek/stargazers)
[![](https://img.shields.io/pypi/l/benedek?style=for-the-badge)](https://github.com/krateng/benedek/blob/master/LICENSE)

A tool to enable a more concise and thematically structured creation of mods for Crusader Kings 2.

## Install

Install with `pip install benedek`. Make sure to use `pip3` if Python 3 isn't your default version.


## Use

Instead of lots of small files everywhere over the folder structure, Benedek allows you to group thematically related things (like an event chain and its on_action trigger) together. Create your text files in the folder `benedek` within your mod directory - you can structure it any way you like with subdirectories.

Then simply call the command `benedek (modfolder)` and to prepare the mod so that CK2 can read it. Call the command again after you've made changes.
