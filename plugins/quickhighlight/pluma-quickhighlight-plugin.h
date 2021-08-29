/*
 * pluma-quick-highlight-plugin.h
 *
 * Copyright (C) 2018 Martin Blanchard
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2, or (at your option)
 * any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program; if not, see <http://www.gnu.org/licenses/>.
 *
 */

#ifndef PLUMA_QUICK_HIGHLIGHT_PLUGIN_H
#define PLUMA_QUICK_HIGHLIGHT_PLUGIN_H

#include <glib.h>
#include <glib-object.h>
#include <libpeas/peas-extension-base.h>
#include <libpeas/peas-object-module.h>

G_BEGIN_DECLS

#define PLUMA_TYPE_QUICK_HIGHLIGHT_PLUGIN        (pluma_quick_highlight_plugin_get_type ())
#define PLUMA_QUICK_HIGHLIGHT_PLUGIN(o)          (G_TYPE_CHECK_INSTANCE_CAST ((o), PLUMA_TYPE_QUICK_HIGHLIGHT_PLUGIN, PlumaQuickHighlightPlugin))
#define PLUMA_QUICK_HIGHLIGHT_PLUGIN_CLASS(k)    (G_TYPE_CHECK_CLASS_CAST((k), PLUMA_TYPE_QUICK_HIGHLIGHT_PLUGIN, PlumaQuickHighlightPluginClass))
#define PLUMA_IS_QUICK_HIGHLIGHT_PLUGIN(o)       (G_TYPE_CHECK_INSTANCE_TYPE ((o), PLUMA_TYPE_QUICK_HIGHLIGHT_PLUGIN))
#define PLUMA_IS_QUICK_HIGHLIGHT_PLUGIN_CLASS(k) (G_TYPE_CHECK_CLASS_TYPE ((k), PLUMA_TYPE_QUICK_HIGHLIGHT_PLUGIN))
#define PLUMA_QUICK_HIGHLIGHT_GET_CLASS(o)       (G_TYPE_INSTANCE_GET_CLASS ((o), PLUMA_TYPE_QUICK_HIGHLIGHT_PLUGIN, PlumaQuickHighlightPluginClass))

typedef struct _PlumaQuickHighlightPlugin        PlumaQuickHighlightPlugin;
typedef struct _PlumaQuickHighlightPluginPrivate PlumaQuickHighlightPluginPrivate;
typedef struct _PlumaQuickHighlightPluginClass   PlumaQuickHighlightPluginClass;

struct _PlumaQuickHighlightPlugin
{
    PeasExtensionBase parent_instance;

    /* < private > */
    PlumaQuickHighlightPluginPrivate *priv;
};

struct _PlumaQuickHighlightPluginClass
{
    PeasExtensionBaseClass parent_class;
};

GType pluma_quick_highlight_plugin_get_type (void) G_GNUC_CONST;

G_MODULE_EXPORT void peas_register_types (PeasObjectModule *module);

G_END_DECLS

#endif /* PLUMA_QUICK_HIGHLIGHT_PLUGIN_H */

