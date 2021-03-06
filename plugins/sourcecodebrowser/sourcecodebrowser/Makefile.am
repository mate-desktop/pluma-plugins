# SourceCodeBrowser plugin
SUBDIRS = icons

plugindir = $(PLUMA_PLUGINS_LIBS_DIR)/sourcecodebrowser
plugin_PYTHON =		\
	__init__.py	\
	ctags.py	\
	sourcecodebrowser.py

uidir = $(PLUMA_PLUGINS_DATA_DIR)/sourcecodebrowser/ui
ui_files = configure_dialog.ui
ui_DATA = $(ui_files)

EXTRA_DIST = \
	$(ui_DATA)

CLEANFILES =
DISTCLEANFILES =

-include $(top_srcdir)/git.mk
