#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Pluma Markdown Preview Plugin

A markdown preview plugin for Pluma text editor using WebKit2.
"""

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Pluma', '1.0')
gi.require_version('WebKit2', '4.1')

from gi.repository import Gtk, Gio, Pluma, GObject, WebKit2
import html as html_module

try:
    import markdown
    MARKDOWN_AVAILABLE = True
except ImportError:
    MARKDOWN_AVAILABLE = False


class PlumaMarkdownPreviewPlugin(GObject.Object, Pluma.WindowActivatable):
    """Markdown Preview Plugin for Pluma"""

    __gtype_name__ = "PlumaMarkdownPreviewPlugin"
    window = GObject.property(type=Pluma.Window)

    def __init__(self):
        GObject.Object.__init__(self)
        self._preview_widget = None
        self._webview = None
        self._update_timer = None
        self._available_extensions = None  # Cache for detected extensions

    def do_activate(self):
        if not MARKDOWN_AVAILABLE:
            return

        self._create_preview_widget()
        self._add_menu_items()

    def do_deactivate(self):
        if not MARKDOWN_AVAILABLE:
            return

        self._remove_preview_widget()
        self._remove_menu_items()

    def do_update_state(self):
        """Update plugin state when document changes"""
        doc = self.window.get_active_document()
        if doc and self._is_markdown_file(doc):
            self._show_preview()
            self._schedule_update()
        else:
            self._load_welcome_content()

    def _create_preview_widget(self):
        """Create the preview widget with WebKit2"""
        if self._preview_widget:
            return

        # Create scrolled window container
        self._preview_widget = Gtk.ScrolledWindow()
        self._preview_widget.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

        # Create WebKit2 webview
        self._webview = WebKit2.WebView()
        self._webview.connect("decide-policy", self._on_decide_policy)

        # Load initial content
        self._load_welcome_content()

        self._preview_widget.add(self._webview)
        self._preview_widget.show_all()

        # Add to right panel
        panel = self.window.get_right_panel()
        icon_theme = Gtk.IconTheme.get_default()
        if icon_theme.has_icon("text-x-markdown"):
            icon_name = "text-x-markdown"
        else:
            icon_name = "text-x-generic"
        icon = Gtk.Image.new_from_icon_name(icon_name, Gtk.IconSize.MENU)
        panel.add_item(self._preview_widget, "Markdown Preview", icon)

    def _remove_preview_widget(self):
        """Remove the preview widget"""
        if self._preview_widget:
            panel = self.window.get_right_panel()
            panel.remove_item(self._preview_widget)
            self._preview_widget = None
            self._webview = None

    def _add_menu_items(self):
        """Add menu items to Tools menu"""
        manager = self.window.get_ui_manager()

        # Create action group
        self._action_group = Gtk.ActionGroup("MarkdownPreviewActions")

        # Add preview action
        preview_action = Gtk.Action("MarkdownPreview", "Show Markdown Preview",
                                    "Preview the current markdown document", None)
        preview_action.connect("activate", self._on_preview_activate)
        self._action_group.add_action(preview_action)

        # Add update action
        update_action = Gtk.Action("MarkdownUpdate", "Update Markdown Preview",
                                   "Update the markdown preview", None)
        update_action.connect("activate", self._on_update_activate)
        self._action_group.add_action(update_action)

        manager.insert_action_group(self._action_group, -1)

        # Add UI elements
        self._ui_id = manager.new_merge_id()
        manager.add_ui(self._ui_id, "/MenuBar/ToolsMenu/ToolsOps_4",
                       "MarkdownPreview", "MarkdownPreview",
                       Gtk.UIManagerItemType.MENUITEM, False)
        manager.add_ui(self._ui_id, "/MenuBar/ToolsMenu/ToolsOps_4",
                       "MarkdownUpdate", "MarkdownUpdate",
                       Gtk.UIManagerItemType.MENUITEM, False)

    def _remove_menu_items(self):
        if hasattr(self, '_ui_id'):
            manager = self.window.get_ui_manager()
            manager.remove_ui(self._ui_id)
            manager.remove_action_group(self._action_group)

    def _on_decide_policy(self, webview, decision, decision_type):
        """Open clicked links in the default browser instead of the preview"""
        if decision_type in (WebKit2.PolicyDecisionType.NAVIGATION_ACTION,
                             WebKit2.PolicyDecisionType.NEW_WINDOW_ACTION):
            nav_action = decision.get_navigation_action()
            if nav_action.get_navigation_type() == WebKit2.NavigationType.LINK_CLICKED:
                uri = nav_action.get_request().get_uri()
                Gio.AppInfo.launch_default_for_uri(uri, None)
                decision.ignore()
                return True
        return False

    def _on_preview_activate(self, action):
        panel = self.window.get_right_panel()
        panel.show()
        panel.activate_item(self._preview_widget)
        self._update_preview()

    def _on_update_activate(self, action):
        """Force update the preview"""
        self._update_preview()

    def _is_markdown_file(self, doc):
        """Check if document is a markdown file"""
        if not doc:
            return False

        # Check by language
        lang = doc.get_language()
        if lang and lang.get_id() == "markdown":
            return True

        # Check by filename
        location = doc.get_location()
        if location:
            filename = location.get_basename()
            if filename:
                name_lower = filename.lower()
                return any(name_lower.endswith(ext) for ext in
                          ['.md', '.markdown'])

        return False

    def _show_preview(self):
        """Activate the preview tab if the panel is already visible"""
        panel = self.window.get_right_panel()
        if panel.get_visible() and not panel.item_is_active(self._preview_widget):
            panel.activate_item(self._preview_widget)

    def _schedule_update(self):
        """Schedule a preview update with debouncing"""
        panel = self.window.get_right_panel()
        if not panel.get_visible() or not panel.item_is_active(self._preview_widget):
            return

        if self._update_timer:
            GObject.source_remove(self._update_timer)
        self._update_timer = GObject.timeout_add(500, self._update_preview)

    def _update_preview(self):
        """Update the markdown preview"""
        doc = self.window.get_active_document()
        if not doc or not self._is_markdown_file(doc):
            self._load_welcome_content()
            return False

        # Get document text
        start = doc.get_start_iter()
        end = doc.get_end_iter()
        text = doc.get_text(start, end, True)

        if not text.strip():
            self._load_welcome_content()
            return False

        # Convert markdown to HTML
        html = self._markdown_to_html(text)

        # Load in webview
        self._webview.load_html(html, None)

        self._update_timer = None
        return False

    def _detect_available_extensions(self):
        """Detect which markdown extensions are available and working"""
        # Extensions to test for availability
        extensions = [
            'extra',      # Compilation of Python-Markdown extensions
            'admonition', # Warning/note boxes
            'codehilite', # Code highlighting
            'nl2br',      # Newline to break
            'smarty',     # Smart quotes
            'toc',        # Table of contents
        ]

        available = []
        test_text = "# Test\n\nTest text."

        # Test each extension individually
        for ext in extensions:
            try:
                markdown.markdown(test_text, extensions=[ext])
                available.append(ext)
            except Exception:
                pass

        return available


    def _markdown_to_html(self, text):
        try:
            # Detect available extensions (cached after first run)
            if self._available_extensions is None:
                self._available_extensions = self._detect_available_extensions()

            # Convert markdown with detected extensions
            html_content = markdown.markdown(text, extensions=self._available_extensions)

            # Wrap in full HTML document
            html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Markdown Preview</title>
    <style>
        body {{
            font-family: sans-serif;
            line-height: 1.5;
            color: #2e3436;
            max-width: 800px;
            margin: 0 auto;
            padding: 1rem;
            background: white;
        }}
        pre {{
            background: #eeeeec;
            border: 1px solid #babdb6;
            padding: 0.5rem;
            overflow-x: auto;
        }}
        code {{
            background: #eeeeec;
            padding: 2px 4px;
        }}
        blockquote {{
            margin: 0;
            padding-left: 1rem;
            border-left: 3px solid #888A85;
            color: #888A85;
        }}
        table {{
            border-collapse: collapse;
        }}
        th, td {{
            border: 1px solid #babdb6;
            padding: 0.5rem;
        }}
        th {{
            background: #eeeeec;
        }}
        a {{
            color: #3465a4;
        }}
        /* Admonitions */
        .admonition {{
            margin: 0.5rem 0;
            padding: 0.1rem 1rem;
            background: #eeeeec;
            border-left: 3px solid #729fcf;
        }}
        .admonition.warning {{
            border-left-color: #f57900;
        }}
        .admonition.danger, .admonition.error {{
            border-left-color: #cc0000;
        }}
        .admonition-title {{
            font-weight: bold;
        }}
    </style>
</head>
<body>
    {html_content}
</body>
</html>
"""
            return html

        except Exception as e:
            escaped = html_module.escape(text)
            return f"<html><body><h1>Markdown Error</h1><p>Error converting markdown: {html_module.escape(str(e))}</p><pre>{escaped}</pre></body></html>"

    def _load_welcome_content(self):
        """Load welcome content when no markdown is active"""
        welcome_html = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Markdown Preview</title>
    <style>
        body {
            font-family: system-ui, sans-serif;
            text-align: center;
            padding: 2rem;
            color: #2e3436;
            background: #ffffff;
        }
    </style>
</head>
<body>
    <h2>Markdown Preview</h2>
    <p>Open a markdown file (.md, .markdown) to see the preview here.</p>
    <p><small>This is a markdown preview plugin for Pluma</small></p>
</body>
</html>
"""
        if self._webview:
            self._webview.load_html(welcome_html, None)
