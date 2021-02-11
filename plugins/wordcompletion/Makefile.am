# Word Completion plugin
plugindir = $(PLUMA_PLUGINS_LIBS_DIR)

AM_CPPFLAGS = \
	-I$(top_srcdir) 				\
	$(PLUMA_CFLAGS) 				\
	$(WARN_CFLAGS)

plugin_LTLIBRARIES = libwordcompletion.la

BUILT_SOURCES = \
	pluma-word-completion-resources.c

nodist_libwordcompletion_la_SOURCES = \
	$(BUILT_SOURCES)

libwordcompletion_la_SOURCES = \
	pluma-word-completion-plugin.h	\
	pluma-word-completion-plugin.c

libwordcompletion_la_LDFLAGS = $(PLUGIN_LIBTOOL_FLAGS)
libwordcompletion_la_LIBADD = $(PLUMA_LIBS)

# Generate resources
pluma-word-completion-resources.c: pluma-word-completion.gresource.xml Makefile $(shell $(GLIB_COMPILE_RESOURCES) --generate-dependencies --sourcedir $(srcdir) $(srcdir)/pluma-word-completion.gresource.xml)
	$(AM_V_GEN) XMLLINT=$(XMLLINT) $(GLIB_COMPILE_RESOURCES) --target $@ --sourcedir $(srcdir) --generate --c-name pluma $<

plugin_in_in_files = wordcompletion.plugin.desktop.in.in
plugin_in_files = $(plugin_in_in_files:.in=)
plugin_DATA = $(plugin_in_files:.desktop.in=)

$(plugin_DATA): $(plugin_in_files)
	$(AM_V_GEN) $(MSGFMT) --keyword=Name --keyword=Description --desktop --template $< -d $(top_srcdir)/po -o $@

wordcompletion_gschema_in = org.mate.pluma.plugins.wordcompletion.gschema.xml.in
gsettings_SCHEMAS = $(wordcompletion_gschema_in:.in=)
@GSETTINGS_RULES@

EXTRA_DIST = \
	$(plugin_in_in_files)				\
	$(wordcompletion_gschema_in)		\
	pluma-word-completion.gresource.xml \
	pluma-word-completion-configure.ui

CLEANFILES = \
	$(BUILT_SOURCES) \
	$(plugin_DATA)

DISTCLEANFILES = \
	$(gsettings_SCHEMAS) \
	$(plugin_in_files)

-include $(top_srcdir)/git.mk
