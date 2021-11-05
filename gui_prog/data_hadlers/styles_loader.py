import sys

import yaml


class StylesLoader:
    current_dir_abs_path = sys.path[0].replace('\\', '/')  # находим текущюю директорию
    if '/base_library.zip' in current_dir_abs_path:
        current_dir_abs_path = current_dir_abs_path[0:-17]

    MAIN_ICON = current_dir_abs_path + "/gui_prog/external_data/main_icon.png"
    STYLES_FILE = current_dir_abs_path + '/gui_prog/external_data/styles.yaml'

    def get_styles_from_yaml(self):
        with open(self.STYLES_FILE) as f:
            styles = yaml.load(f, Loader=yaml.FullLoader)
        return styles
