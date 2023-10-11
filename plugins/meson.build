msgfmt_plugin_cmd = [
  find_program('msgfmt'),
  '--desktop',
  '--keyword=Name',
  '--keyword=Description',
  '--template=@INPUT@',
  '-d', join_paths(srcdir, 'po'),
  '--output=@OUTPUT@'
]

plugin_in = configuration_data()
plugin_in.set('VERSION', meson.project_version())
plugin_in.set('PACKAGE_URL', 'https://mate-desktop.org/')
plugin_in.set('PACKAGE_BUGREPORT', 'https://github.com/mate-desktop/pluma-plugins/issues')
plugin_in.set('GETTEXT_PACKAGE', meson.project_name())

gpdefs_py = configuration_data()
gpdefs_py.set('GETTEXT_PACKAGE', meson.project_name())
gpdefs_py.set('VERSION', meson.project_version())
gpdefs_py.set('PACKAGE', meson.project_name())
gpdefs_py.set('PACKAGE_STRING', '@0@-@1@'.format(meson.project_name(), meson.project_version()))

configure_file(
  input: 'gpdefs.py.in',
  output: 'gpdefs.py',
  configuration: gpdefs_py,
  install: true,
  install_dir: join_paths(
    pkglibdir,
    'plugins',
  )
)

foreach plugin_name : enabled_plugins
  subdir(plugin_name)
endforeach
