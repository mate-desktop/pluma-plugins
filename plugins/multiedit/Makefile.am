# Multiedit Plugin
SUBDIRS = multiedit
plugindir = $(PLUMA_PLUGINS_LIBS_DIR)

plugin_in_in_files = multiedit.plugin.desktop.in.in
plugin_in_files = $(plugin_in_in_files:.in=)
plugin_DATA = $(plugin_in_files:.desktop.in=)

$(plugin_DATA): $(plugin_in_files)
	$(AM_V_GEN) $(MSGFMT) --keyword=Name --keyword=Description --desktop --template $< -d $(top_srcdir)/po -o $@

EXTRA_DIST = \
	$(plugin_in_in_files)

CLEANFILES = \
	$(plugin_DATA)

DISTCLEANFILES = \
	$(plugin_in_files)

-include $(top_srcdir)/git.mk
