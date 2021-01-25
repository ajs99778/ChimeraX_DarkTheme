from chimerax.core.toolshed import BundleAPI


class _THEME_API(BundleAPI):

    api_version = 1
    
    @staticmethod
    def initialize(session, bundle_info):
        from themes import settings as theme_settings
        theme_settings.settings = settings._ThemeSettings(session, "ui")
        if session.ui.is_gui:
            import os.path
            
            session.ui.triggers.add_handler(
                "ready",
                lambda *args, ses=session: theme_settings.register_settings_options(ses)
            )
            
            if theme_settings.settings.THEME:
                session.theme_manager.execute(theme_settings.settings.THEME)

    @staticmethod
    def init_manager(session, bundle_info, name, **kwargs):
        """
        initialize theme manager
        """
        if name == "theme_manager":
            from .manager import ThemeManager
            session.theme_manager = ThemeManager(session, name)
            return session.theme_manager
    
    @staticmethod
    def run_provider(session, name, mgr, **kw):
        """
        returns the style sheet for the theme specified by "name"
        """
        if mgr is session.theme_manager:
            if name == "Default":
                return ""
            else:
                import os.path
                import themes
                pkg_dir = os.path.dirname(themes.__file__)
                theme_dir = os.path.join(pkg_dir, "style_sheets")
                sheet_path = os.path.join(theme_dir, "%s.qss" % name)
                with open(sheet_path, "r") as f:
                    style_sheet = f.read()
                
                return style_sheet

bundle_api = _THEME_API()
