markdown_preview_sources = files(
  'markdown_preview.py',
)

install_data(
  markdown_preview_sources,
  install_dir: join_paths(
    pkglibdir,
    'plugins',
  )
)

markdown_preview_plugin_in = configure_file(
  input: 'markdown-preview.plugin.desktop.in.in',
  output: 'markdown-preview.plugin.desktop.in',
  configuration: plugin_in,
  install: false,
)

markdown_preview_plugin = custom_target(
  'markdown-preview.plugin',
  input: markdown_preview_plugin_in,
  output: 'markdown-preview.plugin',
  command: msgfmt_plugin_cmd,
  install: true,
  install_dir: join_paths(
    pkglibdir,
    'plugins',
  )
)

markdown_preview_metainfo = i18n.merge_file(
  input : configure_file(
    configuration: plugin_in,
    input : 'pluma-markdown-preview.metainfo.xml.in.in',
    output: 'pluma-markdown-preview.metainfo.xml.in'
  ),
  output: 'pluma-markdown-preview.metainfo.xml',
  po_dir: join_paths(srcdir, 'po'),
  type: 'xml',
  install: true,
  install_dir: appstreamdir,
)

if appstream_util.found()
  test(
    'validate-pluma-markdown-preview.metainfo.xml',
    appstream_util,
    args: [
      'validate-relax',
      '--nonet',
      markdown_preview_metainfo.full_path(),
    ]
  )
endif
