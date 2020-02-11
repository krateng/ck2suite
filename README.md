# Benedek: CK2 Mod Creation Helper

[![](https://img.shields.io/pypi/v/benedek?style=for-the-badge)](https://pypi.org/project/benedek/)
[![](https://img.shields.io/pypi/dm/benedek?style=for-the-badge)](https://pypi.org/project/benedek/)
[![](https://img.shields.io/github/stars/krateng/benedek?style=for-the-badge&color=purple)](https://github.com/krateng/benedek/stargazers)
[![](https://img.shields.io/pypi/l/benedek?style=for-the-badge)](https://github.com/krateng/benedek/blob/master/LICENSE)

A tool to enable a more concise and thematically structured creation of mods for Crusader Kings 2.

## Install

Install with `pip install benedek`. Make sure to use `pip3` if Python 3 isn't your default version.


## Use

Instead of lots of small files everywhere over the folder structure, Benedek allows you to group thematically related things (like an event chain and its on_action trigger) together. To create a Benedek-mod, create a new folder in `benedekmod` in your CK2 user directory. You can add any regular CK2 script files in their normal directories in addition to Benedek-files in the `benedek` folder which you can structure in any way you like with subdirectories.

Specify your mod metadata (name, picture, esc.) in `modinfo.yml`. Then simply call the command `benedek (modfolder)` and to prepare the mod so that CK2 can read it. Call the command again after you've made changes.
