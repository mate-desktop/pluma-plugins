subdir('icons')
sources_files = files(
  'ctags.py',
  '__init__.py',
  'sourcecodebrowser.py'
)
install_data(
  sources_files,
  install_dir: join_paths(
    pkglibdir,
    'plugins',
    'sourcecodebrowser'
  )
)

install_data(
  'configure_dialog.ui',
  install_dir: join_paths(
    pkgdatadir,
    'plugins',
    'sourcecodebrowser',
    'ui'
    )
)
