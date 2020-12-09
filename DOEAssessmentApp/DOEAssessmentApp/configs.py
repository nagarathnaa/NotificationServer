import sys
import os
import konfig

_HERE = os.path.dirname(__file__)
_SETTINGS_FILE = os.path.join(_HERE, 'settings.ini')
CONFS = konfig.Config(_SETTINGS_FILE)
if sys.platform == 'linux':
    db_settings_map = CONFS.get_map('dbforlinux')
elif sys.platform == 'win32':
    db_settings_map = CONFS.get_map('dbforwin32')

prod_configs_from_file = [db_settings_map,]
