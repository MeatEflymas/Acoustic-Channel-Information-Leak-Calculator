import os
import sys
import yaml
from numpy import genfromtxt
from calc_acoustic_ch.external_data.text_constant import REC_MESSAGE


class DataLoader:
    current_dir_abs_path = sys.path[0].replace('\\', '/')  # находим текущюю директорию
    if '/base_library.zip' in current_dir_abs_path:
        current_dir_abs_path = current_dir_abs_path[0:-17]

    IMAGES_FOLDER = current_dir_abs_path + '/calc_acoustic_ch/plot_images/'
    REC_FILE = current_dir_abs_path + '/calc_acoustic_ch/external_data/rec.yaml'

    # метод очистки папки с изображениями при закрытии программы
    @staticmethod
    def clear_images_dir():
        for the_file in os.listdir(DataLoader.IMAGES_FOLDER):
            file_path = os.path.join(DataLoader.IMAGES_FOLDER, the_file)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception as e:
                print(e)

    # метод получения данных из csv файла и преобразования их в numpy-массив
    def read_lower_higher_f_from_csv(self, path):
        data = genfromtxt(self.current_dir_abs_path + path, delimiter=',', dtype=int)
        return data

    # метод получения рекомендаций из yaml файла
    def get_rec_from_yaml(self, W_S, W_R):
        percent = round((W_R + W_S) * 100 / 2)

        if percent >= 60:
            current_rec = "vhig"
        elif 40 <= percent < 60:
            current_rec = "hig"
        elif 20 <= percent < 40:
            current_rec = "mid"
        else:
            current_rec = "low"

        lower_limit = round(min(W_S, W_R) * 100, 3)
        upper_limit = round(max(W_S, W_R) * 100, 3)

        return self._read_rec_from_yaml(percent, lower_limit, upper_limit, current_rec)

    def _read_rec_from_yaml(self, percent, lower_limit, upper_limit, current_rec):
        with open(self.REC_FILE) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        current_rec = REC_MESSAGE.format(
            percent,
            lower_limit,
            upper_limit,
            data[current_rec])
        return current_rec

    def get_help_mes_from_yaml(self):
        path = self.current_dir_abs_path + '/src/external_data/help.yaml'
        with open(path) as f:
            help_mes = yaml.load(f, Loader=yaml.FullLoader)
        return help_mes

    # метод получения данных из csv файла и преобразования их в numpy-массив
    def read_csv_to_numpy_array(self, path):
        data = genfromtxt(self.current_dir_abs_path + path, delimiter=',', dtype=int)
        return data