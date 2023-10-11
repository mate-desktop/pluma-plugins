libquickhighlight_sources = files(
  'pluma-quickhighlight-plugin.c',
)

libquickhighlight_deps = [
  pluma_dep,
]


libquickhighlight_sha = shared_module(
  'quickhighlight',
  sources: libquickhighlight_sources,
  include_directories: root_include_dir,
  dependencies: libquickhighlight_deps,
  install: true,
  install_dir: join_paths(
    pkglibdir,
    'plugins',
  )
)

quickhighlight_plugin_in = configure_file(
  input: 'quickhighlight.plugin.desktop.in.in',
  output: 'quickhighlight.plugin.desktop.in',
  configuration: plugin_in,
  install: false,
)

quickhighlight_plugin = custom_target(
  'quickhighlight.plugin',
  input: quickhighlight_plugin_in,
  output: 'quickhighlight.plugin',
  command: msgfmt_plugin_cmd,
  install: true,
  install_dir: join_paths(
    pkglibdir,
    'plugins',
  )
)

quickhighlight_metainfo = i18n.merge_file(
  input : configure_file(
    configuration: plugin_in,
    input : 'pluma-quickhighlight.metainfo.xml.in.in',
    output: 'pluma-quickhighlight.metainfo.xml.in'
  ),
  output: 'pluma-quickhighlight.metainfo.xml',
  po_dir: join_paths(srcdir, 'po'),
  type: 'xml',
  install: true,
  install_dir: appstreamdir,
)

if appstream_util.found()
  test(
    'validate-pluma-quickhighlight.metainfo.xml',
    appstream_util,
    args: [
      'validate-relax',
      '--nonet',
      quickhighlight_metainfo.full_path(),
    ]
  )
endif
