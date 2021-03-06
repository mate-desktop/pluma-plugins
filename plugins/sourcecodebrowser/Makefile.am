# SourceCodeBrowser Plugin
SUBDIRS = sourcecodebrowser
plugindir = $(PLUMA_PLUGINS_LIBS_DIR)

plugin_DATA = sourcecodebrowser.plugin
plugin_in_files = $(plugin_DATA:.plugin=.plugin.desktop.in)
plugin_in_in_files = $(plugin_in_files:.plugin.desktop.in=.plugin.desktop.in.in)

$(plugin_DATA): $(plugin_in_files)
	$(AM_V_GEN) $(MSGFMT) --keyword=Name --keyword=Description --desktop --template $< -d $(top_srcdir)/po -o $@

sourcecodebrowser_gschema_in = org.mate.pluma.plugins.sourcecodebrowser.gschema.xml.in
gsettings_SCHEMAS = $(sourcecodebrowser_gschema_in:.xml.in=.xml)
@GSETTINGS_RULES@

EXTRA_DIST = \
	$(plugin_in_in_files)		\
	$(sourcecodebrowser_gschema_in)

CLEANFILES = \
	$(plugin_DATA)

DISTCLEANFILES = \
	$(plugin_in_files)		\
	$(gsettings_SCHEMAS_in)		\
	$(gsettings_SCHEMAS)

-include $(top_srcdir)/git.mk
