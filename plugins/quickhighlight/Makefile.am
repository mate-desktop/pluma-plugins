# Quickhighlight Plugin
plugindir = $(PLUMA_PLUGINS_LIBS_DIR)

AM_CPPFLAGS = \
	-I$(top_srcdir) \
	$(PLUMA_CFLAGS) \
	$(WARN_CFLAGS)

plugin_LTLIBRARIES = libquickhighlight.la

libquickhighlight_la_SOURCES = \
	pluma-quickhighlight-plugin.c \
	pluma-quickhighlight-plugin.h

libquickhighlight_la_LDFLAGS = $(PLUGIN_LIBTOOL_FLAGS)
libquickhighlight_la_LIBADD  = $(PLUMA_LIBS)

plugin_in_files = quickhighlight.plugin.desktop.in
plugin_DATA = $(plugin_in_files:.plugin.desktop.in=.plugin)

$(plugin_DATA): $(plugin_in_files)
	$(AM_V_GEN) $(MSGFMT) --keyword=Name --keyword=Description --desktop --template $< -d $(top_srcdir)/po -o $@

metainfodir = $(datadir)/metainfo
metainfo_DATA = pluma-quickhighlight.metainfo.xml
metainfo_in_files = $(metainfo_DATA:=.in)

$(metainfo_DATA): $(metainfo_in_files)
	$(AM_V_GEN) GETTEXTDATADIR=$(top_srcdir) $(MSGFMT) --xml --template $< -d $(top_srcdir)/po -o $@

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
