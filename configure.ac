dnl Process this file with autoconf to produce a configure script.

AC_PREREQ([2.63])

m4_define(pluma_plugins_major_version,  1)
m4_define(pluma_plugins_minor_version,  25)
m4_define(pluma_plugins_micro_version,  0)
m4_define(pluma_plugins_version, pluma_plugins_major_version.pluma_plugins_minor_version.pluma_plugins_micro_version)

AC_INIT([pluma-plugins],
        [pluma_plugins_version],
        [https://github.com/mate-desktop/pluma-plugins/issues],
        [pluma-plugins],
        [https://mate-desktop.org/])

AC_CONFIG_HEADERS([config.h])
AC_CONFIG_SRCDIR([plugins])
AC_CONFIG_MACRO_DIR([m4])

AC_PREFIX_PROGRAM([pluma])

AM_INIT_AUTOMAKE([1.11 tar-ustar dist-xz no-dist-gzip foreign subdir-objects -Wno-portability])
AM_MAINTAINER_MODE([enable])

AM_SILENT_RULES([yes])

# Check for programs
AC_PROG_CC
AC_PROG_INSTALL
AC_PROG_MAKE_SET

# Initialize libtool
LT_PREREQ([2.2])
LT_INIT([disable-static])

AM_GNU_GETTEXT_VERSION([0.19.8])
AM_GNU_GETTEXT([external])

# ================================================================
# Gettext stuff.
# ================================================================
GETTEXT_PACKAGE=pluma-plugins
AC_SUBST(GETTEXT_PACKAGE)
AC_DEFINE_UNQUOTED(GETTEXT_PACKAGE,"$GETTEXT_PACKAGE", [Gettext package])

# ================================================================
# Start of pkg-config checks
# ================================================================
GTKSOURCEVIEW_REQUIRED=4.0.2

PKG_CHECK_MODULES(PLUMA, [
	glib-2.0 >= 2.32.0
	gio-2.0 >= 2.32.0
	gtk+-3.0 >= 3.9.0
	gtksourceview-4 >= $GTKSOURCEVIEW_REQUIRED
	libpeas-1.0 >= 1.7.0
	libpeas-gtk-1.0 >= 1.7.0
	pluma >= 1.25.3
])

dnl ================================================================
dnl GSettings stuff
dnl ================================================================
GLIB_GSETTINGS

# ================================================================
# Plugins
# ================================================================

# C plugins that don't need special dependencies
C_PLUGINS="bookmarks"

# Python plugins that don't need special dependencies, besides Python
PYTHON_PLUGINS="bracketcompletion codecomment smartspaces"

PLUGINS="$C_PLUGINS"
disabled_plugins=""

# Check all plugins are built
AC_ARG_ENABLE([verify-all],
              AC_HELP_STRING([--enable-verify-all], [verify that all plugins are enabled]),
              [enable_verify_all=$enableval],
              [enable_verify_all="no"])

# Python
AC_MSG_CHECKING([whether Python support is requested])
AC_ARG_ENABLE([python],
              AS_HELP_STRING([--enable-python], [Enable Python support]),
              [enable_python=$enableval],
              [enable_python=auto])
AC_MSG_RESULT([$enable_python])

if test "x$enable_python" != "xno"
then
	AM_PATH_PYTHON(3, [have_python=yes], [have_python=no])
	if test "x$enable_python" = "xyes" -a "x$have_python" = "xno"; then
		AC_MSG_ERROR([Python support explicitly requested, but not found])
	fi
fi

AM_CONDITIONAL([ENABLE_PYTHON], [test "x$have_python" = "xyes"])

# Python plugins that need special dependencies

# disable all python plugins if there is no python support
if test "x$have_python" = "xyes"
then
	PLUGINS="$PLUGINS $PYTHON_PLUGINS"

	# ================================================================
	# Synctex (dbus-python)
	# ================================================================
	DBUSPYTHON_REQUIRED=0.82
	PKG_CHECK_MODULES([DBUSPYTHON],
		[dbus-python >= $DBUSPYTHON_REQUIRED],
		[have_synctex=yes],
		[have_synctex=no])

	AC_SUBST([DBUS_PYTHON_CFLAGS])
	AC_SUBST([DBUS_PYTHON_LIBS])

	AC_MSG_CHECKING([for synctex dependency dbus-python])
	AC_MSG_RESULT($have_synctex)

	if test "x$have_synctex" = "xyes"; then
		PLUGINS="$PLUGINS synctex"
	else
		AC_MSG_RESULT([yes])
		disabled_plugins="$disabled_plugins synctex (dbus-python not found)"
	fi

	# ================================================================
	# Terminal (vte)
	# ================================================================
	AC_MSG_CHECKING([for terminal dependency vte])

	if `$PYTHON -c "import gi; gi.require_version('Vte', '2.91')" 2>/dev/null`;
	then
		have_vte=yes
		PLUGINS="$PLUGINS terminal"
	else
		have_vte=no
		disabled_plugins="$disabled_plugins terminal (vte not found)"
	fi

	AC_MSG_RESULT($have_vte)

else
	disabled_plugins="$disabled_plugins $PYTHON_PLUGINS synctex terminal (python not found)"
fi

AM_CONDITIONAL([ENABLE_SYNCTEX], test "x$have_synctex" = "xyes")
AM_CONDITIONAL([ENABLE_TERMINAL], test "x$have_vte" = "xyes")

AC_SUBST(PLUGINS)

# ================================================================
# Misc
# ================================================================
AC_PATH_PROG(GLIB_COMPILE_RESOURCES, glib-compile-resources)
AC_PATH_PROG(GLIB_GENMARSHAL, glib-genmarshal)

AC_DEFINE(GDK_VERSION_MIN_REQUIRED, GDK_VERSION_3_8, [minimum gdk version])

YELP_HELP_INIT

AC_ARG_ENABLE(deprecations,
              [AS_HELP_STRING([--enable-deprecations],
                              [warn about deprecated usages [default=no]])],,
              [enable_deprecations=no])

if test "x$enable_deprecations" = "xyes"
then
	DISABLE_DEPRECATED_CFLAGS="\
		-DG_DISABLE_DEPRECATED		\
		-DGDK_DISABLE_DEPRECATED	\
		-DGTK_DISABLE_DEPRECATED	\
		-DGDK_PIXBUF_DISABLE_DEPRECATED	\
		-DGNOME_DISABLE_DEPRECATED"
	AC_SUBST(DISABLE_DEPRECATED_CFLAGS)
fi

PLUGIN_LIBTOOL_FLAGS="-module -avoid-version"
AC_SUBST(PLUGIN_LIBTOOL_FLAGS)

PLUMA_PLUGINS_LIBS_DIR="$libdir/pluma/plugins"
AC_SUBST(PLUMA_PLUGINS_LIBS_DIR)

PLUMA_PLUGINS_DATA_DIR="$datadir/pluma/plugins"
AC_SUBST(PLUMA_PLUGINS_DATA_DIR)

if test "x$enable_verify_all" != "xno" && test ! -z "$disabled_plugins"; then
AC_MSG_ERROR([some plugins are not being built: $disabled_plugins])
fi

AC_CONFIG_FILES([
Makefile
help/Makefile
plugins/gpdefs.py
plugins/bookmarks/bookmarks.plugin.desktop.in
plugins/bookmarks/Makefile
plugins/bookmarks/pluma-bookmarks.metainfo.xml.in
plugins/bracketcompletion/bracketcompletion.plugin.desktop.in
plugins/bracketcompletion/Makefile
plugins/Makefile
plugins/codecomment/codecomment.plugin.desktop.in
plugins/codecomment/Makefile
plugins/codecomment/pluma-codecomment.metainfo.xml.in
plugins/smartspaces/smartspaces.plugin.desktop.in
plugins/smartspaces/Makefile
po/Makefile.in])

AM_COND_IF([ENABLE_SYNCTEX],[AC_CONFIG_FILES([
plugins/synctex/Makefile
plugins/synctex/pluma-synctex.metainfo.xml.in
plugins/synctex/synctex.plugin.desktop.in
plugins/synctex/synctex/Makefile])])

AM_COND_IF([ENABLE_TERMINAL],[AC_CONFIG_FILES([
plugins/terminal/Makefile
plugins/terminal/org.mate.pluma.plugins.terminal.gschema.xml
plugins/terminal/pluma-terminal.metainfo.xml.in
plugins/terminal/terminal.plugin.desktop.in])])

AC_OUTPUT

echo "

Configuration:

	Source code location:   ${srcdir}
	Compiler:               ${CC}
	Prefix:                 ${prefix}
	Python Plugins Support: ${have_python}

	Plugins:
	  ${PLUGINS}

	Disabled plugins:
	  ${disabled_plugins}

Note: you have to install these plugins into the same prefix as your pluma
installation (probably /usr if you're using your distro packages, /usr/local
if you have compiled it on your own).
"

