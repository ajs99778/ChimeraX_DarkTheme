import os

from chimerax.core.settings import Settings
from chimerax.core.configfile import Value
from chimerax.core.commands.cli import StringArg, EnumOf, ListOf
from chimerax.ui.options import EnumOption


class ThemeOption(EnumOption):
    values = []
    labels = []


class _ThemeSettings(Settings):
    EXPLICIT_SAVE = {
        "THEME": "Default",
    }


def register_settings_options(session):
    settings_info = {
        "THEME": (
            "UI Theme",
            ThemeOption,
            "changes the color scheme of UI elements",
        )
    }
    
    for setting, setting_info in settings_info.items():
        opt_name, opt_class, balloon = setting_info
        
        session.logger.info(opt_name)
        
        def _opt_cb(opt, ses=session):
            setting = opt.attr_name
            val = opt.value
            if setting == "THEME":
                opt.settings.THEME = val
                session.theme_manager.execute(val)
            
        opt = opt_class(
            opt_name,
            getattr(settings, setting),
            _opt_cb,
            attr_name=setting,
            settings=settings,
            balloon=balloon,
            auto_set_attr=False,
        )
            
        session.ui.main_window.add_settings_option("Window", opt)
