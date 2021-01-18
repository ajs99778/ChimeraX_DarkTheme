import os

from chimerax.core.settings import Settings
from chimerax.core.configfile import Value
from chimerax.core.commands.cli import StringArg, EnumOf, ListOf
from chimerax.ui.options import InputFolderOption, SymbolicEnumOption


def get_themes():
    import themes
    pkg_dir = os.path.dirname(themes.__file__)
    theme_dir = os.path.join(pkg_dir, "themes")
    theme_names = ["Default"]
    theme_files = [""]
    
    for f in os.listdir(theme_dir):
        if f.endswith(".qss"):
            theme_file = os.path.join(theme_dir, f)
            theme_files.append(theme_file)
            
            name = os.path.basename(f)
            name, _ = os.path.splitext(name)
            theme_names.append(name)
    
    return theme_files, theme_names


class ThemeOption(SymbolicEnumOption):
    values, labels = get_themes()
    
    def __init__(self, *args, **kwargs):
        self._callback = None
        super().__init__(*args, **kwargs)
    

class _ThemeSettings(Settings):
    EXPLICIT_SAVE = {
        "THEME": "",
    }


def register_settings_options(session):
    settings_info = {
        "THEME": (
            "UI Theme",
            ThemeOption,
            "changes the colors of UI elements",
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
                from PySide2.QtWidgets import QApplication
                
                app = QApplication.instance()
                if val and os.path.isfile(val):
                    with open(val, "r") as f:
                        sheet = f.read()
                    app.setStyleSheet(sheet)
                
                else:
                    app.setStyleSheet("")
            
        opt = opt_class(
            opt_name,
            getattr(settings, setting),
            _opt_cb,
            attr_name=setting,
            settings=settings,
            balloon=balloon,
            auto_set_attr=False,
        )
            
        session.ui.main_window.add_settings_option("UI Theme", opt)

def get_sheet_for_style(name):
    ndx = ThemeOption.labels.index(name)
    return ThemeOption.values[ndx]