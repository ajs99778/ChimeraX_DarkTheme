from chimerax.core.toolshed import BundleAPI


class _DARKTHEME_API(BundleAPI):

    api_version = 1
    
    @staticmethod
    def initialize(session, bundle_info):
        import DarkTheme
        import os.path
        try:
            from PySide2.QtWidgets import QApplication
        except (ModuleNotFoundError, ImportError):
            from PyQt5.QtWidgets import QApplication 
        
        app = QApplication.instance()
        
        pkg_dir = os.path.dirname(DarkTheme.__file__)
        
        style_sheet_path = os.path.join(pkg_dir, "dark.qss")
        with open(style_sheet_path, "r") as f:
            style_sheet = f.read()
        
        app.setStyleSheet(style_sheet)
        
bundle_api = _DARKTHEME_API()
