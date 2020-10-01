# pluma-plugins

![pluma-icon](pluma.ico)
![pluma-plugin-icon](pluma-plugin.png)

## General Information

A set set of plugins for Pluma, the standard text editor of the MATE desktop environment. The package pluma-plugins started as a fork of gnome-plugins.

## Installation

For the moment, you have to `./configure` with the same `--prefix` as you configured Pluma with.

How to choose which plugins to build:

`./configure --with-plugins=pl1,pl2,...
`

where pl1, pl2 ... are one of the following:

- **codecomment** - *Comment and uncomment blocks of code.*
- **synctex** - *SyncTeX synchronization of TeX files and PDF output.*
- **terminal** - *Embed a terminal in the bottom pane.*
- **all** - *All of the above plugins*
