SUBDIRS = $(PLUGINS)

plugindir = $(libdir)/pluma/plugins

if ENABLE_PYTHON
plugin_PYTHON = gpdefs.py
endif

DISTCLEANFILES = \
	gpdefs.py

EXTRA_DIST = \
	gpdefs.py.in

-include $(top_srcdir)/git.mk
