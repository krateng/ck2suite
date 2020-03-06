# Bierstadt

[![](https://img.shields.io/pypi/v/bierstadt?style=for-the-badge)](https://pypi.org/project/bierstadt/)
[![](https://img.shields.io/pypi/dm/bierstadt?style=for-the-badge)](https://pypi.org/project/bierstadt/)
[![](https://img.shields.io/github/stars/krateng/ck2suite?style=for-the-badge&color=purple)](https://github.com/krateng/ck2suite/stargazers)
[![](https://img.shields.io/pypi/l/bierstadt?style=for-the-badge)](https://github.com/krateng/ck2suite/blob/master/LICENSE)

A library and command line tool to handle CK2 portrait files

## Install

Install with `pip install bierstadt`. Make sure to use `pip3` if Python 3 isn't your default version.


## Use from command line

`bierstadt create *[files]*` combines all listed files into a CK2-ready portrait sprite.

`bierstadt create *file* -t trait` creates a trait icon.

`bierstadt insert *source* *target* *index*` inserts the source file into the existing target sprite at the specified index.

## Use from code

`bierstadt.library` exposes classes to handle various image types.
