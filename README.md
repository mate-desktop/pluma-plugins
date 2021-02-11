# pluma-plugins

![pluma-icon](pluma.ico)
![pluma-plugin-icon](pluma-plugin.png)

## General Information

A set set of plugins for Pluma, the MATE text editor. The package *pluma-plugins* started as a fork of *gedit-plugins*.

Currently available plugins:

- **bookmarks** - *Easy document navigation with bookmarks.*
- **codecomment** - *Comment and uncomment blocks of code.*
- **smartspaces** - *Forget you’re not using tabulations.*
- **synctex** - *SyncTeX synchronization of TeX files and PDF output.*
- **terminal** - *Embed a terminal in the bottom pane.*
- **wordcompletion** - *Word completion using the completion framework.*

Note:

- The *synctex* plugin requires `dbus-python` (>= 0.82).
- The *terminal* plugin requires the `VTE` (>= 2.91) library.

See the Pluma [README](https://github.com/mate-desktop/pluma/blob/master/README.md) file for more information.

## Installation

Simple install procedure:

```
$ ./autogen.sh                              # Build configuration
$ make                                      # Build
[ Become root if necessary ]
$ make install                              # Installation
```
