import abc
import six

from tempest.test_discover import plugins

@six.add_metaclass(abc.ABCMeta)
class SwiftPlugin(plugins.TempestPlugin):

    @abc.abstractmethod
    def load_tests(self):
        return

    @abc.abstractmethod
    def register_opts(self, conf):
        return

    @abc.abstractmethod
    def get_opt_lists(self):
        return []
