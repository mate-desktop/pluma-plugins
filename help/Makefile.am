@YELP_HELP_RULES@

HELP_ID = pluma-plugins
HELP_FILES = bookmarks.page code-comment.page index.page legal-plugins.xml terminal.page
HELP_MEDIA =

# Add linguas to be ignored, e.g. IGNORE_HELP_LINGUAS = ca de es fr
IGNORE_HELP_LINGUAS =
HELP_LINGUAS = $(if $(IGNORE_HELP_LINGUAS), \
	$(filter-out $(IGNORE_HELP_LINGUAS),$(subst /,,$(dir $(wildcard */*.po)))), \
	$(subst /,,$(dir $(wildcard */*.po))) )

-include $(top_srcdir)/git.mk
