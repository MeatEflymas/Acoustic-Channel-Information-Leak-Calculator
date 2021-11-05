import sys

import yaml


class HelpMessageLoader:
    current_dir_abs_path = sys.path[0].replace('\\', '/')  # находим текущюю директорию
    if '/base_library.zip' in current_dir_abs_path:
        current_dir_abs_path = current_dir_abs_path[0:-17]

    HELP_FILE = current_dir_abs_path + '/gui_prog/external_data/help.yaml'

    def get_help_mes_from_yaml(self):
        with open(self.HELP_FILE) as f:
            help_mes = yaml.load(f, Loader=yaml.FullLoader)
        return help_mes