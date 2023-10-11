libwordcompletion_sources = files(
  'pluma-word-completion-plugin.c',
)

libwordcompletion_deps = [
  pluma_dep,
]

libwordcompletion_res = gnome.compile_resources(
  'pluma-word-completion-resources',
  'pluma-word-completion.gresource.xml',
)

libwordcompletion_sources += [
  libwordcompletion_res.get(0),
]

libwordcompletion_sha = shared_module(
  'wordcompletion',
  sources: libwordcompletion_sources,
  include_directories: root_include_dir,
  dependencies: libwordcompletion_deps,
  install: true,
  install_dir: join_paths(
    pkglibdir,
    'plugins',
  )
)

wordcompletion_plugin_in = configure_file(
  input: 'wordcompletion.plugin.desktop.in.in',
  output: 'wordcompletion.plugin.desktop.in',
  configuration: plugin_in,
  install: false,
)

wordcompletion_plugin = custom_target(
  'wordcompletion.plugin',
  input: wordcompletion_plugin_in,
  output: 'wordcompletion.plugin',
  command: msgfmt_plugin_cmd,
  install: true,
  install_dir: join_paths(
    pkglibdir,
    'plugins',
  )
)

configure_file(
  input: 'org.mate.pluma.plugins.wordcompletion.gschema.xml.in',
  output: 'org.mate.pluma.plugins.wordcompletion.gschema.xml',
  configuration: plugin_in,
  install_dir: join_paths(
    glibdir,
    'schemas',
  )
)
