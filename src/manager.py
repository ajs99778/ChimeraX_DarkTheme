from chimerax.core.toolshed import ProviderManager


class ThemeManager(ProviderManager):
    """
    manager to keep track of UI themes
    providers for this manager should implement a run_provider method that returns a style sheet (str)
    Qt style sheets are similar to CSS
    for info on style sheets for Qt-based applications, see https://doc.qt.io/qt-5/stylesheet-reference.html
    for examples, see https://doc.qt.io/qt-5/stylesheet-syntax.html
    """
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
        """
        apply the style sheet specified by "name"
        """
        if name not in self._themes:
            self._session.logger.warning("no theme named \"%s\"" % name)
            return

        from Qt.QtWidgets import QApplication
        
        style_sheet = self._themes[name]()

        app = QApplication.instance()
        app.setStyleSheet(style_sheet)
