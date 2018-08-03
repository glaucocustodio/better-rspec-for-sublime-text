import sublime, sublime_plugin
import re
import os

def log(message):
  print("=> RSpec Buddy: %s" % (message))

CREATE_IMPLEMENTATION_FILE_MESSAGE = """
The implementation file doesn't exist.
Do you want to create it?

%s
"""

CREATE_SPEC_FILE_MESSAGE = """
The spec file doesn't exist.
Do you want to create it?

%s
"""

SPEC_TEMPLATE = """
RSpec.describe %s do %s
end
"""

DESCRIBE_TEMPLATE = """
  describe '%s' do
    it do
    end
  end
""".rstrip('\n')

class RspecToggleCommand(sublime_plugin.WindowCommand):
  def run(self):
    folders = self.window.folders()

    if len(folders) == 0:
      return

    current_file = self.window.active_view().file_name()
    current_folder = None

    for folder in folders:
      if current_file.startswith(folder):
        current_folder = folder
        break

    if not current_folder:
      return

    relative_path = current_file.replace("%s/" % current_folder, "")

    if relative_path.startswith("spec"):
      self._open_implementation_file(folder, relative_path)
    else:
      self._open_spec_file(folder, relative_path)

  def _open_implementation_file(self, folder, file):
    base_path = re.sub(r"^spec\/(.*?)_spec\.rb$", "\\1.rb", file)

    candidates = [base_path, "lib/%s" % base_path, "app/%s" % base_path]

    if self._dotfile_custom_path(folder):
      candidates.append("%s%s" % (self._dotfile_custom_path(folder), base_path))

    for path in candidates:
      fullpath = os.path.join(folder, path)
      if os.path.isfile(fullpath):
        return self.window.open_file(fullpath)

    if not sublime.ok_cancel_dialog(CREATE_IMPLEMENTATION_FILE_MESSAGE % (path)):
      return

    candidates = [
      os.path.join(folder, "app"),
      os.path.join(folder, "lib")
    ]

    for dir in candidates:
      fullpath = os.path.join(dir, base_path)
      basedir = os.path.dirname(fullpath)

      if os.path.isdir(basedir):
        open(fullpath, "w+").close()
        self.window.open_file(fullpath)
        break

  def _is_rails(self, folder):
    return os.path.isdir(os.path.join(folder, "app")) and \
           os.path.isdir(os.path.join(folder, "config"))

  def _dotfile_custom_path(self, folder):
    dotfile = os.path.join(folder, ".rspec-buddy")
    if os.path.isfile(dotfile):
      with open(dotfile, 'r') as file:
        # remove empty lines
        return "".join(line for line in file.read() if not line.isspace())

  def _infer_file_constant(self, base_path):
    path = re.sub("spec/|_spec.rb", "", base_path).title().replace('/', '::')
    to_replace = {
      '_': '', 'Lib::': '', 'Models::': '', 'Controllers::': '', 'Jobs::': '', 'Mailers::': ''
    }
    for old, new in to_replace.items():
      path = path.replace(old, new)
    return path

  def _describe_methods_from_implementation(self, folder, file):
    implementation_file_path = open(os.path.join(folder, file))

    public_methods = []
    for line in implementation_file_path:
      clean_line = line.strip(' ')
      if clean_line == 'private\n':
        break
      else:
        public_methods.append(re.findall(r"\s*def\s((?!initialize)[\w\.]+)", line))

    public_methods_flatten = [current[0].replace('self.', '.') for current in public_methods if current]

    result = ''

    last_method = public_methods_flatten[-1] if public_methods_flatten else None

    for method_name in public_methods_flatten:
      if not method_name.startswith('.'):
        result += DESCRIBE_TEMPLATE % ('#' + method_name)
      else:
        result += DESCRIBE_TEMPLATE % (method_name)

      if last_method != method_name:
        result += '\n'

    return result

  def _spec_file_content(self, base_path, folder, file):
    methods_described = self._describe_methods_from_implementation(folder, file)

    if methods_described != '':
      return SPEC_TEMPLATE % (self._infer_file_constant(base_path), methods_described)
    else:
      return SPEC_TEMPLATE % (self._infer_file_constant(base_path), DESCRIBE_TEMPLATE % '')

  def _open_spec_file(self, folder, file):
    if self._is_rails(folder):
      regex = r"^(?:app\/)?(.*?)\.rb$"
    else:
      if self._dotfile_custom_path(folder):
        regex = re.compile("^%s(.*?)\.rb$" % (self._dotfile_custom_path(folder).replace("/", "\/")))
      else:
        regex = r"^lib\/(.*?)\.rb$"

    base_path = re.sub(regex, "spec/\\1_spec.rb", file)
    fullpath = os.path.join(folder, base_path)

    if os.path.isfile(fullpath):
      self.window.open_file(fullpath)
    elif sublime.ok_cancel_dialog(CREATE_SPEC_FILE_MESSAGE % (base_path)):
      self._make_dir_for_path(fullpath)
      handler = open(fullpath, "w+")
      handler.write(self._spec_file_content(base_path, folder, file))
      handler.close()
      self.window.open_file(fullpath)

  def _make_dir_for_path(self, filepath):
    basedir = os.path.dirname(filepath)

    if not os.path.isdir(basedir):
      os.makedirs(basedir)
