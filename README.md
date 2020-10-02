# pluma-plugins

![pluma-icon](pluma.ico)
![pluma-plugin-icon](pluma-plugin.png)

## General Information

A set set of plugins for Pluma, the MATE text editor. The package pluma-plugins started as a fork of gedit-plugins.

Currently available plugins:

- **codecomment** - *Comment and uncomment blocks of code.*
- **synctex** - *SyncTeX synchronization of TeX files and PDF output.*
- **terminal** - *Embed a terminal in the bottom pane.*

Note:

- For the synctex plugin to get enabled you will need to have dbus-python installed.
- For the terminal plugin to get enabled you will need to have vte installed.

See the Pluma [README](https://github.com/mate-desktop/pluma/blob/master/README) file for more information.

## Installation

Simple install procedure:

```
$ ./autogen.sh                              # Build configuration
$ make                                      # Build
[ Become root if necessary ]
$ make install                              # Installation
```
