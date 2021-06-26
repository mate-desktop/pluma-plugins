/*
 * Copyright (C) 2009 Ignacio Casal Quinteiro <icq@gnome.org>
 * Copyright (C) 2020-2021 MATE Developers
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
 * along with this program. If not, see https://www.gnu.org/licenses/.
 *
 */

#ifndef __PLUMA_WORD_COMPLETION_PLUGIN_H__
#define __PLUMA_WORD_COMPLETION_PLUGIN_H__

#include <glib.h>
#include <glib-object.h>
#include <libpeas/peas-extension-base.h>
#include <libpeas/peas-object-module.h>

G_BEGIN_DECLS

#define PLUMA_TYPE_WORD_COMPLETION_PLUGIN          (pluma_word_completion_plugin_get_type ())
#define PLUMA_WORD_COMPLETION_PLUGIN(o)            (G_TYPE_CHECK_INSTANCE_CAST ((o), PLUMA_TYPE_WORD_COMPLETION_PLUGIN, PlumaWordCompletionPlugin))
#define PLUMA_WORD_COMPLETION_PLUGIN_CLASS(k)      (G_TYPE_CHECK_CLASS_CAST((k), PLUMA_TYPE_WORD_COMPLETION_PLUGIN, PlumaWordCompletionPluginClass))
#define PLUMA_IS_WORD_COMPLETION_PLUGIN(o)         (G_TYPE_CHECK_INSTANCE_TYPE ((o), PLUMA_TYPE_WORD_COMPLETION_PLUGIN))
#define PLUMA_IS_WORD_COMPLETION_PLUGIN_CLASS(k)   (G_TYPE_CHECK_CLASS_TYPE ((k), PLUMA_TYPE_WORD_COMPLETION_PLUGIN))
#define PLUMA_WORD_COMPLETION_PLUGIN_GET_CLASS(o)  (G_TYPE_INSTANCE_GET_CLASS ((o), PLUMA_TYPE_WORD_COMPLETION_PLUGIN, PlumaWordCompletionPluginClass))

typedef struct _PlumaWordCompletionPlugin           PlumaWordCompletionPlugin;
typedef struct _PlumaWordCompletionPluginPrivate    PlumaWordCompletionPluginPrivate;
typedef struct _PlumaWordCompletionPluginClass      PlumaWordCompletionPluginClass;

struct _PlumaWordCompletionPlugin
{
    PeasExtensionBase parent_instance;

    PlumaWordCompletionPluginPrivate *priv;
};

struct _PlumaWordCompletionPluginClass
{
    PeasExtensionBaseClass parent_class;
};

GType                   pluma_word_completion_plugin_get_type    (void) G_GNUC_CONST;

G_MODULE_EXPORT void    peas_register_types                      (PeasObjectModule *module);

G_END_DECLS

#endif /* __PLUMA_WORD_COMPLETION_PLUGIN_H__ */
