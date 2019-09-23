from plugin_framework.plugin import Plugin
from .widgets.login_widget import LoginWidget

class Main(Plugin):

    def __init__(self, spec):

        super().__init__(spec)

    def get_widget(self, parent=None):

        return LoginWidget(parent), None, None