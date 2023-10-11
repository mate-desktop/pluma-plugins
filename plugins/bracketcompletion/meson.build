bracketcompletion_sources = files(
  'bracketcompletion.py',
)

install_data(
  bracketcompletion_sources,
  install_dir: join_paths(
    pkglibdir,
    'plugins',
  )
)

bracketcompletion_plugin_in = configure_file(
  input: 'bracketcompletion.plugin.desktop.in.in',
  output: 'bracketcompletion.plugin.desktop.in',
  configuration: plugin_in,
  install: false,
)

bracketcompletion_plugin = custom_target(
  'bracketcompletion.plugin',
  input: bracketcompletion_plugin_in,
  output: 'bracketcompletion.plugin',
  command: msgfmt_plugin_cmd,
  install: true,
  install_dir: join_paths(
    pkglibdir,
    'plugins',
  )
)
