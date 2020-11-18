# Bookmarks Plugin
plugindir = $(PLUMA_PLUGINS_LIBS_DIR)

AM_CPPFLAGS = \
	-I$(top_srcdir) \
	$(PLUMA_CFLAGS) \
	$(WARN_CFLAGS)

plugin_LTLIBRARIES = libbookmarks.la

libbookmarks_la_SOURCES = \
	pluma-bookmarks-plugin.c \
	pluma-bookmarks-plugin.h

libbookmarks_la_LDFLAGS = $(PLUGIN_LIBTOOL_FLAGS)
libbookmarks_la_LIBADD  = $(PLUMA_LIBS)

plugin_in_files = bookmarks.plugin.desktop.in
plugin_DATA = $(plugin_in_files:.plugin.desktop.in=.plugin)

$(plugin_DATA): $(plugin_in_files)
	$(AM_V_GEN) $(MSGFMT) --keyword=Name --keyword=Description --desktop --template $< -d $(top_srcdir)/po -o $@

metainfodir = $(datadir)/metainfo
metainfo_in_files = template.pluma-bookmarks.metainfo.xml
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
	$(metainfo_DATA) \
	$(plugin_DATA)

-include $(top_srcdir)/git.mk
