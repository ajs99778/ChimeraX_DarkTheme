from chimerax.core.toolshed import ProviderManager


class ThemeManager(ProviderManager):
    def __init__(self, session, name):
        self._session = session
        self._themes = dict()
        super().__init__(name)

    def add_provider(self, bundle_info, name):
        """
        name - name of theme
        """
        self._themes[name] = lambda *args, name=name, bi=bundle_info: bi.run_provider(self._session, name, self)
        
        from .settings import ThemeOption
        ThemeOption.values.append(name)
        ThemeOption.labels.append(name)
    
    def execute(self, name):
        if name not in self._themes:
            self._session.logger.warn("no theme named \"%s\"" % name)
            return

        from PySide2.QtWidgets import QApplication
        
        style_sheet = self._themes[name]()

        app = QApplication.instance()
        app.setStyleSheet(style_sheet)
