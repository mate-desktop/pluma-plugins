install_subdir(
  'gpgcrypt',
  install_dir: join_paths(
    pkglibdir,
    'plugins',
  )
)

gpgcrypt_plugin_in = configure_file(
  input: 'gpgcrypt.plugin.desktop.in.in',
  output: 'gpgcrypt.plugin.desktop.in',
  configuration: plugin_in,
  install: false,
)

gpgcrypt_plugin = custom_target(
  'gpgcrypt.plugin',
  input: gpgcrypt_plugin_in,
  output: 'gpgcrypt.plugin',
  command: msgfmt_plugin_cmd,
  install: true,
  install_dir: join_paths(
    pkglibdir,
    'plugins',
  )
)

gpgcrypt_metainfo = i18n.merge_file(
  input : configure_file(
    configuration: plugin_in,
    input : 'pluma-gpgcrypt.metainfo.xml.in.in',
    output: 'pluma-gpgcrypt.metainfo.xml.in'
  ),
  output: 'pluma-gpgcrypt.metainfo.xml',
  po_dir: join_paths(srcdir, 'po'),
  type: 'xml',
  install: true,
  install_dir: appstreamdir,
)

if appstream_util.found()
  test(
    'validate-pluma-gpgcrypt.metainfo.xml',
    appstream_util,
    args: [
      'validate-relax',
      '--nonet',
      gpgcrypt_metainfo.full_path(),
    ]
  )
endif
