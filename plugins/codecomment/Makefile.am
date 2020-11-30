# Code Comment Plugin
plugindir = $(PLUMA_PLUGINS_LIBS_DIR)
plugin_PYTHON = \
	codecomment.py

plugin_in_files = codecomment.plugin.desktop.in
plugin_DATA = $(plugin_in_files:.desktop.in=)

$(plugin_DATA): $(plugin_in_files)
	$(AM_V_GEN) $(MSGFMT) --keyword=Name --keyword=Description --desktop --template $< -d $(top_srcdir)/po -o $@

metainfodir = $(datadir)/metainfo
metainfo_DATA = pluma-codecomment.metainfo.xml
metainfo_in_files = $(metainfo_DATA:=.in)

$(metainfo_DATA): $(metainfo_in_files)
	$(AM_V_GEN) $(MSGFMT) --xml --template $< -d $(top_srcdir)/po -o $@

EXTRA_DIST = \
	$(metainfo_in_files:=.in) \
	$(plugin_in_files:=.in)

CLEANFILES = \
	$(metainfo_DATA) \
	$(plugin_DATA)

DISTCLEANFILES = \
	$(metainfo_in_files) \
	$(plugin_in_files)

-include $(top_srcdir)/git.mk
