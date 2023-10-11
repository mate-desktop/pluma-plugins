subdir('sourcecodebrowser')
sourcecodebrowser_plugin_in = configure_file(
  input: 'sourcecodebrowser.plugin.desktop.in.in',
  output: 'sourcecodebrowser.plugin.desktop.in',
  configuration: plugin_in,
  install: false,
)

sourcecodebrowser_plugin = custom_target(
  'sourcecodebrowser.plugin',
  input: sourcecodebrowser_plugin_in,
  output: 'sourcecodebrowser.plugin',
  command: msgfmt_plugin_cmd,
  install: true,
  install_dir: join_paths(
    pkglibdir,
    'plugins',
  )
)

configure_file(
  input: 'org.mate.pluma.plugins.sourcecodebrowser.gschema.xml.in',
  output: 'org.mate.pluma.plugins.sourcecodebrowser.gschema.xml',
  configuration: plugin_in,
  install_dir: join_paths(
    glibdir,
    'schemas',
  )
)
