/*
 * pluma-quick-highlight-plugin.c
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

#include "config.h"

#include <glib/gi18n.h>

#include <pluma/pluma-debug.h>
#include <pluma/pluma-document.h>
#include <pluma/pluma-view-activatable.h>
#include <pluma/pluma-view.h>

#include "pluma-quickhighlight-plugin.h"

struct _PlumaQuickHighlightPluginPrivate
{
    PlumaView              *view;

    PlumaDocument          *buffer;
    GtkTextMark            *insert_mark;

    GtkSourceSearchContext *search_context;
    GtkSourceStyle         *style;

    gulong                  buffer_handler_id;
    gulong                  mark_set_handler_id;
    gulong                  delete_range_handler_id;
    gulong                  style_scheme_handler_id;

    guint                   queued_highlight;
};

enum
{
    PROP_0,
    PROP_VIEW
};

static void pluma_view_activatable_iface_init (PlumaViewActivatableInterface *iface);

G_DEFINE_DYNAMIC_TYPE_EXTENDED (PlumaQuickHighlightPlugin,
                                pluma_quick_highlight_plugin,
                                PEAS_TYPE_EXTENSION_BASE,
                                0,
                                G_IMPLEMENT_INTERFACE_DYNAMIC (PLUMA_TYPE_VIEW_ACTIVATABLE,
                                                               pluma_view_activatable_iface_init)
                                G_ADD_PRIVATE_DYNAMIC (PlumaQuickHighlightPlugin))

static void pluma_quick_highlight_plugin_notify_buffer_cb (GObject *object, GParamSpec *pspec, gpointer user_data);
static void pluma_quick_highlight_plugin_mark_set_cb (GtkTextBuffer *textbuffer, GtkTextIter *location, GtkTextMark *mark, gpointer user_data);
static void pluma_quick_highlight_plugin_delete_range_cb (GtkTextBuffer *textbuffer, GtkTextIter *start, GtkTextIter *end, gpointer user_data);
static void pluma_quick_highlight_plugin_notify_style_scheme_cb (GObject *object, GParamSpec *pspec, gpointer user_data);

static void
pluma_quick_highlight_plugin_load_style (PlumaQuickHighlightPlugin *plugin)
{
    GtkSourceStyleScheme *style_scheme;
    GtkSourceStyle *style = NULL;

    g_return_if_fail (PLUMA_IS_QUICK_HIGHLIGHT_PLUGIN (plugin));

    if (plugin->priv->buffer == NULL)
    {
        return;
    }

    pluma_debug (DEBUG_PLUGINS);

    g_clear_object (&plugin->priv->style);

    style_scheme = gtk_source_buffer_get_style_scheme (GTK_SOURCE_BUFFER (plugin->priv->buffer));

    if (style_scheme != NULL)
    {
        style = gtk_source_style_scheme_get_style (style_scheme, "quick-highlight-match");

        if (style != NULL)
        {
            plugin->priv->style = gtk_source_style_copy (style);
        }
    }
}

static gboolean
pluma_quick_highlight_plugin_highlight_worker (gpointer user_data)
{
    PlumaQuickHighlightPlugin *plugin = PLUMA_QUICK_HIGHLIGHT_PLUGIN (user_data);
    GtkSourceSearchSettings *search_settings;
    GtkTextIter start, end;
    g_autofree gchar *text = NULL;

    g_assert (PLUMA_IS_QUICK_HIGHLIGHT_PLUGIN (plugin));

    plugin->priv->queued_highlight = 0;

    if (!gtk_text_buffer_get_selection_bounds (GTK_TEXT_BUFFER (plugin->priv->buffer), &start, &end))
    {
        g_clear_object (&plugin->priv->search_context);
        return G_SOURCE_REMOVE;
    }

    if (gtk_text_iter_get_line (&start) != gtk_text_iter_get_line (&end))
    {
        g_clear_object (&plugin->priv->search_context);
        return G_SOURCE_REMOVE;
    }

    if (plugin->priv->search_context == NULL)
    {
        search_settings =
            g_object_new (GTK_SOURCE_TYPE_SEARCH_SETTINGS,
                          "at-word-boundaries", FALSE,
                          "case-sensitive", TRUE,
                          "regex-enabled", FALSE,
                          NULL);

        plugin->priv->search_context =
            g_object_new (GTK_SOURCE_TYPE_SEARCH_CONTEXT,
                          "buffer", plugin->priv->buffer,
                          "highlight", FALSE,
                          "match-style", plugin->priv->style,
                          "settings", search_settings,
                          NULL);

        g_object_unref (search_settings);
    }
    else
    {
        search_settings =
            gtk_source_search_context_get_settings (plugin->priv->search_context);
    }

    text = gtk_text_iter_get_slice (&start, &end);

    gtk_source_search_settings_set_search_text (search_settings, text);

    gtk_source_search_context_set_highlight (plugin->priv->search_context, TRUE);

    return G_SOURCE_REMOVE;
}

static void
pluma_quick_highlight_plugin_queue_update (PlumaQuickHighlightPlugin *plugin)
{
    g_return_if_fail (PLUMA_IS_QUICK_HIGHLIGHT_PLUGIN (plugin));

    if (plugin->priv->queued_highlight != 0)
    {
        return;
    }

    plugin->priv->queued_highlight =
        gdk_threads_add_idle_full (G_PRIORITY_LOW,
                                   pluma_quick_highlight_plugin_highlight_worker,
                                   g_object_ref (plugin),
                                   g_object_unref);
}

static void
pluma_quick_highlight_plugin_notify_weak_buffer_cb (gpointer data,
                                                    GObject *where_the_object_was)
{
    PlumaQuickHighlightPlugin *plugin = PLUMA_QUICK_HIGHLIGHT_PLUGIN (data);

    g_assert (PLUMA_IS_QUICK_HIGHLIGHT_PLUGIN (plugin));

    plugin->priv->style_scheme_handler_id = 0;
    plugin->priv->buffer = NULL;
}

static void
pluma_quick_highlight_plugin_unref_weak_buffer (PlumaQuickHighlightPlugin *plugin)
{
    g_return_if_fail (PLUMA_IS_QUICK_HIGHLIGHT_PLUGIN (plugin));

    if (plugin->priv->buffer == NULL)
    {
        return;
    }

    if (plugin->priv->delete_range_handler_id != 0)
    {
        g_signal_handler_disconnect (plugin->priv->buffer,
                                     plugin->priv->delete_range_handler_id);
        plugin->priv->delete_range_handler_id = 0;
    }

    if (plugin->priv->mark_set_handler_id != 0)
    {
        g_signal_handler_disconnect (plugin->priv->buffer,
                                     plugin->priv->mark_set_handler_id);
        plugin->priv->mark_set_handler_id = 0;
    }

    if (plugin->priv->style_scheme_handler_id != 0)
    {
        g_signal_handler_disconnect (plugin->priv->buffer,
                                     plugin->priv->style_scheme_handler_id);
        plugin->priv->style_scheme_handler_id = 0;
    }

    g_object_weak_unref (G_OBJECT (plugin->priv->buffer),
                         pluma_quick_highlight_plugin_notify_weak_buffer_cb,
                         plugin);

    plugin->priv->buffer = NULL;
}

static void
pluma_quick_highlight_plugin_set_buffer (PlumaQuickHighlightPlugin *plugin,
                                         PlumaDocument             *buffer)
{
    g_return_if_fail (PLUMA_IS_QUICK_HIGHLIGHT_PLUGIN (plugin));
    g_return_if_fail (PLUMA_IS_DOCUMENT (buffer));

    if (plugin->priv->buffer == buffer)
    {
        return;
    }

    pluma_debug (DEBUG_PLUGINS);

    pluma_quick_highlight_plugin_unref_weak_buffer (plugin);

    plugin->priv->buffer = buffer;

    if (plugin->priv->buffer != NULL)
    {
        g_object_weak_ref (G_OBJECT (plugin->priv->buffer),
                           pluma_quick_highlight_plugin_notify_weak_buffer_cb,
                           plugin);

        plugin->priv->style_scheme_handler_id =
            g_signal_connect (plugin->priv->buffer, "notify::style-scheme",
                              G_CALLBACK (pluma_quick_highlight_plugin_notify_style_scheme_cb),
                              plugin);

        plugin->priv->mark_set_handler_id =
            g_signal_connect (plugin->priv->buffer, "mark-set",
                              G_CALLBACK (pluma_quick_highlight_plugin_mark_set_cb),
                              plugin);

        plugin->priv->delete_range_handler_id =
            g_signal_connect (plugin->priv->buffer, "delete-range",
                              G_CALLBACK (pluma_quick_highlight_plugin_delete_range_cb),
                              plugin);

        plugin->priv->insert_mark =
            gtk_text_buffer_get_insert (GTK_TEXT_BUFFER (plugin->priv->buffer));

        pluma_quick_highlight_plugin_load_style (plugin);

        pluma_quick_highlight_plugin_queue_update (plugin);
    }
}

static void
pluma_quick_highlight_plugin_mark_set_cb (GtkTextBuffer *textbuffer,
                                          GtkTextIter   *location,
                                          GtkTextMark   *mark,
                                          gpointer       user_data)
{
    PlumaQuickHighlightPlugin *plugin = PLUMA_QUICK_HIGHLIGHT_PLUGIN (user_data);

    g_assert (PLUMA_QUICK_HIGHLIGHT_PLUGIN (plugin));

    if (G_LIKELY (mark != plugin->priv->insert_mark))
    {
        return;
    }

    pluma_quick_highlight_plugin_queue_update (plugin);
}

static void
pluma_quick_highlight_plugin_delete_range_cb (GtkTextBuffer *textbuffer,
                                              GtkTextIter   *start,
                                              GtkTextIter   *end,
                                              gpointer       user_data)
{
    PlumaQuickHighlightPlugin *plugin = PLUMA_QUICK_HIGHLIGHT_PLUGIN (user_data);

    g_assert (PLUMA_QUICK_HIGHLIGHT_PLUGIN (plugin));

    pluma_quick_highlight_plugin_queue_update (plugin);
}

static void
pluma_quick_highlight_plugin_notify_style_scheme_cb (GObject    *object,
                                                     GParamSpec *pspec,
                                                     gpointer    user_data)
{
    PlumaQuickHighlightPlugin *plugin = PLUMA_QUICK_HIGHLIGHT_PLUGIN (user_data);

    g_assert (PLUMA_QUICK_HIGHLIGHT_PLUGIN (plugin));

    pluma_quick_highlight_plugin_load_style (plugin);
}

static void
pluma_quick_highlight_plugin_dispose (GObject *object)
{
    PlumaQuickHighlightPlugin *plugin = PLUMA_QUICK_HIGHLIGHT_PLUGIN (object);

    g_clear_object (&plugin->priv->search_context);

    pluma_quick_highlight_plugin_unref_weak_buffer (plugin);

    g_clear_object (&plugin->priv->view);

    G_OBJECT_CLASS (pluma_quick_highlight_plugin_parent_class)->dispose (object);
}

static void
pluma_quick_highlight_plugin_finalize (GObject *object)
{
    PlumaQuickHighlightPlugin *plugin = PLUMA_QUICK_HIGHLIGHT_PLUGIN (object);

    g_clear_object (&plugin->priv->style);

    G_OBJECT_CLASS (pluma_quick_highlight_plugin_parent_class)->finalize (object);
}

static void
pluma_quick_highlight_plugin_get_property (GObject    *object,
                                           guint       prop_id,
                                           GValue     *value,
                                           GParamSpec *pspec)
{
    PlumaQuickHighlightPlugin *plugin = PLUMA_QUICK_HIGHLIGHT_PLUGIN (object);

    switch (prop_id)
    {
        case PROP_VIEW:
            g_value_set_object (value, plugin->priv->view);
            break;

        default:
            G_OBJECT_WARN_INVALID_PROPERTY_ID (object, prop_id, pspec);
            break;
    }
}

static void
pluma_quick_highlight_plugin_set_property (GObject      *object,
                                           guint         prop_id,
                                           const GValue *value,
                                           GParamSpec   *pspec)
{
    PlumaQuickHighlightPlugin *plugin = PLUMA_QUICK_HIGHLIGHT_PLUGIN (object);

    switch (prop_id)
    {
        case PROP_VIEW:
            plugin->priv->view = PLUMA_VIEW (g_value_dup_object (value));
            break;

        default:
            G_OBJECT_WARN_INVALID_PROPERTY_ID (object, prop_id, pspec);
            break;
    }
}

static void
pluma_quick_highlight_plugin_class_init (PlumaQuickHighlightPluginClass *klass)
{
    GObjectClass *object_class = G_OBJECT_CLASS (klass);

    object_class->dispose = pluma_quick_highlight_plugin_dispose;
    object_class->finalize = pluma_quick_highlight_plugin_finalize;
    object_class->set_property = pluma_quick_highlight_plugin_set_property;
    object_class->get_property = pluma_quick_highlight_plugin_get_property;

    g_object_class_override_property (object_class, PROP_VIEW, "view");
}

static void
pluma_quick_highlight_plugin_class_finalize (PlumaQuickHighlightPluginClass *klass)
{
}

static void
pluma_quick_highlight_plugin_init (PlumaQuickHighlightPlugin *plugin)
{
    plugin->priv = pluma_quick_highlight_plugin_get_instance_private (plugin);
}

static void
pluma_quick_highlight_plugin_activate (PlumaViewActivatable *activatable)
{
    PlumaQuickHighlightPlugin *plugin;
    GtkTextBuffer *buffer;

    pluma_debug (DEBUG_PLUGINS);

    plugin = PLUMA_QUICK_HIGHLIGHT_PLUGIN (activatable);

    plugin->priv->buffer_handler_id =
        g_signal_connect (plugin->priv->view,
                          "notify::buffer",
                          G_CALLBACK (pluma_quick_highlight_plugin_notify_buffer_cb),
                          plugin);

    buffer = gtk_text_view_get_buffer (GTK_TEXT_VIEW (plugin->priv->view));

    pluma_quick_highlight_plugin_set_buffer (plugin, PLUMA_DOCUMENT (buffer));
}

static void
pluma_quick_highlight_plugin_deactivate (PlumaViewActivatable *activatable)
{
    PlumaQuickHighlightPlugin *plugin;

    pluma_debug (DEBUG_PLUGINS);

    plugin = PLUMA_QUICK_HIGHLIGHT_PLUGIN (activatable);

    g_clear_object (&plugin->priv->style);
    g_clear_object (&plugin->priv->search_context);

    pluma_quick_highlight_plugin_unref_weak_buffer (plugin);

    if (plugin->priv->view != NULL && plugin->priv->buffer_handler_id > 0)
    {
        g_signal_handler_disconnect (plugin->priv->view,
                                     plugin->priv->buffer_handler_id);
        plugin->priv->buffer_handler_id = 0;
    }
}

static void
pluma_quick_highlight_plugin_notify_buffer_cb (GObject    *object,
                                               GParamSpec *pspec,
                                               gpointer    user_data)
{
    PlumaQuickHighlightPlugin *plugin = PLUMA_QUICK_HIGHLIGHT_PLUGIN (user_data);
    GtkTextBuffer *buffer;

    g_assert (PLUMA_IS_QUICK_HIGHLIGHT_PLUGIN (plugin));

    buffer = gtk_text_view_get_buffer (GTK_TEXT_VIEW (plugin->priv->view));

    pluma_quick_highlight_plugin_set_buffer (plugin, PLUMA_DOCUMENT (buffer));
}

static void
pluma_view_activatable_iface_init (PlumaViewActivatableInterface *iface)
{
    iface->activate = pluma_quick_highlight_plugin_activate;
    iface->deactivate = pluma_quick_highlight_plugin_deactivate;
}

G_MODULE_EXPORT void
peas_register_types (PeasObjectModule *module)
{
    pluma_quick_highlight_plugin_register_type (G_TYPE_MODULE (module));

    peas_object_module_register_extension_type (module,
                                                PLUMA_TYPE_VIEW_ACTIVATABLE,
                                                PLUMA_TYPE_QUICK_HIGHLIGHT_PLUGIN);
}

