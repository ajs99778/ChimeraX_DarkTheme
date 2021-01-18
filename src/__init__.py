from chimerax.core.toolshed import BundleAPI


class _THEME_API(BundleAPI):

    api_version = 1
    
    @staticmethod
    def initialize(session, bundle_info):
        from themes import settings as theme_settings
        theme_settings.settings = settings._ThemeSettings(session, "UI Theme")
        if session.ui.is_gui:
            import os.path
            
            session.ui.triggers.add_handler(
                "ready",
                lambda *args, ses=session: theme_settings.register_settings_options(ses)
            )
            
            if theme_settings.settings.THEME and os.path.isfile(theme_settings.settings.THEME):
                session.logger.info(theme_settings.settings.THEME)
                from PySide2.QtWidgets import QApplication
                app = QApplication.instance()
                with open(theme_settings.settings.THEME, "r") as f:
                    sheet = f.read()
                app.setStyleSheet(sheet)
        
bundle_api = _THEME_API()
