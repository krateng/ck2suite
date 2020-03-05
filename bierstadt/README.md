# Bierstadt

[![](https://img.shields.io/pypi/v/vermeer?style=for-the-badge)](https://pypi.org/project/vermeer/)
[![](https://img.shields.io/pypi/dm/vermeer?style=for-the-badge)](https://pypi.org/project/vermeer/)
[![](https://img.shields.io/github/stars/krateng/ck2suite?style=for-the-badge&color=purple)](https://github.com/krateng/ck2suite/stargazers)
[![](https://img.shields.io/pypi/l/vermeer?style=for-the-badge)](https://github.com/krateng/ck2suite/blob/master/LICENSE)

A library and command line tool to handle CK2 portrait files

## Install

Install with `pip install vermeer`. Make sure to use `pip3` if Python 3 isn't your default version.


## Use from command line

`vermeer create *[files]*` combines all listed files into a CK2-ready portrait sprite.

`vermeer insert *source* *target* *index*` inserts the source file into the existing target sprite at the specified index.

## Use from code

`vermeer.library` exposes several functions to deal with portrait sprites.
