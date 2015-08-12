import tools.install_venv_common as install_venv
import os
import swift
import sys

from tempest.test_discover import plugins


swift_root = os.path.abspath(swift.__file__).split("/")[:-2]
test_path = os.path.join("/", (os.path.join(*swift_root)),
                         "test", "functional")

root = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

if os.environ.get('TOOLS_PATH'):
    root = os.environ['TOOLS_PATH']
venv = os.path.join(root, '.venv')
if os.environ.get('VENV'):
    venv = os.environ['VENV']
swift_test_requires = os.path.join(os.path.join(*swift_root),
                                   'test-requirements.txt')
py_version = "python%s.%s" % (sys.version_info[0], sys.version_info[1])
project = 'Tempest'


# class SwiftRequirementsInstall(install_venv.InstallVenv):
#
#     def __init__(self):
#         super(SwiftRequirementsInstall, self).__init__(
#             root=root,
#             venv=venv,
#             requirements=None,
#             test_requirements=swift_test_requires,
#             py_version=py_version,
#             project=project)


install = install_venv.InstallVenv(
    root=root, venv=venv, requirements=None,
    test_requirements=swift_test_requires,
    py_version=py_version, project=project)

install.check_python_version()
install.check_dependencies()
install.pip_install()


class SwiftPlugin(plugins.TempestPlugin):

    def load_tests(self):
        return (test_path,
                test_path)

    def register_opts(self, conf):
        return

    def get_opt_lists(self):
        return []
