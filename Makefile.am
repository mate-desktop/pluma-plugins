SUBDIRS = po help plugins

ACLOCAL_AMFLAGS = -I m4 ${ACLOCAL_FLAGS}

EXTRA_DIST =			\
	autogen.sh		\
	its			\
	pluma-plugins.doap

MAINTAINERCLEANFILES = 		\
	aclocal.m4		\
	config.guess		\
	config.h.in		\
	config.sub		\
	depcomp			\
	install-sh		\
	ltmain.sh		\
	missing			\
	mkinstalldirs		\
	py-compile		\
	m4/gnome-doc-utils.m4	\
	m4/gtk-doc.m4		\
	m4/intltool.m4		\
	m4/libtool.m4		\
	m4/ltoptions.m4		\
	m4/ltsugar.m4		\
	m4/ltversion.m4		\
	m4/lt~obsolete.m4	\
	`find "$(srcdir)" -type f -name Makefile.in -print`

DISTCHECK_CONFIGURE_FLAGS = --enable-verify-all

CLEANFILES = ChangeLog

# Build ChangeLog from GIT history
ChangeLog:
	@echo Creating $@
	@if test -d $(top_srcdir)/.git; then \
		(GIT_DIR=$(top_srcdir)/.git $(top_srcdir)/missing --run git log --stat -M -C --name-status  --date=short --no-color) | fmt --split-only > $@.tmp \
		 && mv -f $@.tmp $@ \
		 || ($(RM) $@.tmp; \
		     echo Failed to generate ChangeLog, your ChangeLog may be outdated >&2; \
		     (test -f $@ || echo git-log is required to generate this file >> $@)); \
	else \
		test -f $@ || \
		(echo A git checkout and git-log is required to generate ChangeLog >&2 && \
		echo A git checkout and git-log is required to generate this file >> $@); \
	fi

dist: ChangeLog

.PHONY: ChangeLog

-include $(top_srcdir)/git.mk
