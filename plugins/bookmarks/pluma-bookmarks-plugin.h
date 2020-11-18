/*
 * pluma-bookmarks-plugin.h - Bookmarking for pluma
 *
 * Copyright (C) 2008 Jesse van den Kieboom
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
 * along with this program; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
 *
 */

#ifndef __PLUMA_BOOKMARKS_PLUGIN_H__
#define __PLUMA_BOOKMARKS_PLUGIN_H__

#include <glib.h>
#include <glib-object.h>
#include <libpeas/peas-extension-base.h>
#include <libpeas/peas-object-module.h>

G_BEGIN_DECLS

#define PLUMA_TYPE_BOOKMARKS_PLUGIN		(pluma_bookmarks_plugin_get_type ())
#define PLUMA_BOOKMARKS_PLUGIN(o)		(G_TYPE_CHECK_INSTANCE_CAST ((o), PLUMA_TYPE_BOOKMARKS_PLUGIN, PlumaBookmarksPlugin))
#define PLUMA_BOOKMARKS_PLUGIN_CLASS(k)		(G_TYPE_CHECK_CLASS_CAST((k), PLUMA_TYPE_BOOKMARKS_PLUGIN, PlumaBookmarksPluginClass))
#define PLUMA_IS_BOOKMARKS_PLUGIN(o)		(G_TYPE_CHECK_INSTANCE_TYPE ((o), PLUMA_TYPE_ADVANCED_EDITING_PLUGIN))
#define PLUMA_IS_BOOKMARKS_PLUGIN_CLASS(k)	(G_TYPE_CHECK_CLASS_TYPE ((k), PLUMA_TYPE_BOOKMARKS_PLUGIN))
#define PLUMA_BOOKMARKS_PLUGIN_GET_CLASS(o)	(G_TYPE_INSTANCE_GET_CLASS ((o), PLUMA_TYPE_BOOKMARKS_PLUGIN, PlumaBookmarksPluginClass))

typedef struct _PlumaBookmarksPlugin		PlumaBookmarksPlugin;
typedef struct _PlumaBookmarksPluginPrivate	PlumaBookmarksPluginPrivate;
typedef struct _PlumaBookmarksPluginClass	PlumaBookmarksPluginClass;

struct _PlumaBookmarksPlugin
{
	PeasExtensionBase parent_instance;

	/*< private >*/
	PlumaBookmarksPluginPrivate *priv;
};

struct _PlumaBookmarksPluginClass
{
	PeasExtensionBaseClass parent_class;
};

GType			pluma_bookmarks_plugin_get_type	(void) G_GNUC_CONST;

G_MODULE_EXPORT void	peas_register_types		(PeasObjectModule *module);

G_END_DECLS

#endif /* __PLUMA_BOOKMARKS_PLUGIN_H__ */

/* ex:set ts=8 noet: */
