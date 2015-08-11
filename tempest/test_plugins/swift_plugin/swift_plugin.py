from tempest.test_discover import plugins


class SwiftPlugin(plugins.TempestPlugin):

    def load_tests(self):
        return

    def register_opts(self, conf):
        return

    def get_opt_lists(self):
        return []
