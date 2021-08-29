@YELP_HELP_RULES@

PLUGINS_WITHOUT_HELP = quickhighlight smartspaces sourcecodebrowser
HELP_ID = pluma-plugins
HELP_FILES = index.page legal-plugins.xml $(foreach plugin,$(filter-out $(PLUGINS_WITHOUT_HELP),$(PLUGINS)),$(plugin).page)
HELP_MEDIA = figures/pluma-icon.png \
	figures/pluma-plugin-icon.png

# Add linguas to be ignored, e.g. IGNORE_HELP_LINGUAS = ca de es fr
IGNORE_HELP_LINGUAS =
HELP_LINGUAS = $(if $(IGNORE_HELP_LINGUAS), \
	$(filter-out $(IGNORE_HELP_LINGUAS),$(subst /,,$(dir $(wildcard */*.po)))), \
	$(subst /,,$(dir $(wildcard */*.po))) )

-include $(top_srcdir)/git.mk
