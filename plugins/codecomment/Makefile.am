# Code Comment Plugin
plugindir = $(PLUMA_PLUGINS_LIBS_DIR)
plugin_PYTHON = \
	codecomment.py

plugin_in_files = codecomment.plugin.desktop.in
plugin_DATA = $(plugin_in_files:.desktop.in=)

$(plugin_DATA): $(plugin_in_files)
	$(AM_V_GEN) $(MSGFMT) --keyword=Name --keyword=Description --desktop --template $< -d $(top_srcdir)/po -o $@

metainfodir = $(datadir)/metainfo
metainfo_in_files = template.pluma-codecomment.metainfo.xml
metainfo_DATA = $(metainfo_in_files:template.%=%)

$(metainfo_DATA): $(metainfo_in_files)
	$(AM_V_GEN) $(MSGFMT) --xml --template $< -d $(top_srcdir)/po -o $@

EXTRA_DIST = \
	$(plugin_in_files) \
	$(metainfo_in_files)

CLEANFILES = \
	$(plugin_DATA) \
	$(metainfo_DATA)

DISTCLEANFILES = \
	$(plugin_DATA) \
	$(metainfo_DATA)

-include $(top_srcdir)/git.mk
