terminal_sources = files(
  'terminal.py',
)

install_data(
  terminal_sources,
  install_dir: join_paths(
    pkglibdir,
    'plugins',
  )
)

terminal_plugin_in = configure_file(
  input: 'terminal.plugin.desktop.in.in',
  output: 'terminal.plugin.desktop.in',
  configuration: plugin_in,
  install: false,
)

terminal_plugin = custom_target(
  'terminal.plugin',
  input: terminal_plugin_in,
  output: 'terminal.plugin',
  command: msgfmt_plugin_cmd,
  install: true,
  install_dir: join_paths(
    pkglibdir,
    'plugins',
  )
)

configure_file(
  input: 'org.mate.pluma.plugins.terminal.gschema.xml.in',
  output: 'org.mate.pluma.plugins.terminal.gschema.xml',
  configuration: plugin_in,
  install_dir: join_paths(
    glibdir,
    'schemas',
  )
)

terminal_metainfo = i18n.merge_file(
  input : configure_file(
    configuration: plugin_in,
    input : 'pluma-terminal.metainfo.xml.in.in',
    output: 'pluma-terminal.metainfo.xml.in'
  ),
  output: 'pluma-terminal.metainfo.xml',
  po_dir: join_paths(srcdir, 'po'),
  type: 'xml',
  install: true,
  install_dir: appstreamdir,
)

if appstream_util.found()
  test(
    'validate-pluma-terminal.metainfo.xml',
    appstream_util,
    args: [
      'validate-relax',
      '--nonet',
      terminal_metainfo.full_path(),
    ]
  )
endif
