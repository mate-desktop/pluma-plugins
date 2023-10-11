libbookmarks_sources = files(
  'pluma-bookmarks-plugin.c',
)

libbookmarks_deps = [
  pluma_dep,
]


libbookmarks_sha = shared_module(
  'bookmarks',
  sources: libbookmarks_sources,
  include_directories: root_include_dir,
  dependencies: libbookmarks_deps,
  install: true,
  install_dir: join_paths(
    pkglibdir,
    'plugins',
  )
)

bookmarks_plugin_in = configure_file(
  input: 'bookmarks.plugin.desktop.in.in',
  output: 'bookmarks.plugin.desktop.in',
  configuration: plugin_in,
  install: false,
)

bookmarks_plugin = custom_target(
  'bookmarks.plugin',
  input: bookmarks_plugin_in,
  output: 'bookmarks.plugin',
  command: msgfmt_plugin_cmd,
  install: true,
  install_dir: join_paths(
    pkglibdir,
    'plugins',
  )
)

bookmarks_metainfo = i18n.merge_file(
  input : configure_file(
    configuration: plugin_in,
    input : 'pluma-bookmarks.metainfo.xml.in.in',
    output: 'pluma-bookmarks.metainfo.xml.in'
  ),
  output: 'pluma-bookmarks.metainfo.xml',
  po_dir: join_paths(srcdir, 'po'),
  type: 'xml',
  install: true,
  install_dir: appstreamdir,
)

if appstream_util.found()
  test(
    'validate-pluma-bookmarks.metainfo.xml',
    appstream_util,
    args: [
      'validate-relax',
      '--nonet',
      bookmarks_metainfo.full_path(),
    ]
  )
endif
