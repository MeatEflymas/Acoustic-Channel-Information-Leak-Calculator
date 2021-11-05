import numpy as np
import math

from calc_acoustic_ch.data_handlers.data_loader import DataLoader

class CalcCharAcousticChInfLeak:
    """
    Класс для основных расчетов
    Один экземпляр предназначен только для одного набора речь/шумы
    То есть, по факту, для одного листа из excel файла
    Attributes
    ----------
    data : list
        входной массив данных, содержит
        1) имя листа
        2) уровни речевого сигнала
        3) уровни шумов
    name : str
        связывает реальный excel лист с данным экзмепляром
    signal_level : numpy array
        уровни речевого сигнала
    noise_level : numpy array
        уровни шумов
    f_lower : numpy array
        нижние границы частотных полос
    f_higher : numpy array
        верхние границы частотных полос
    qi : numpy array
        отношение сигнал/шум qi, Дб на каждой полосе
    f_i_average : numpy array
        среднегеометрические частоты для каждой полосы
    delta_A_i : numpy array
        форматный параметр ∆Ai на ср. геом. частоте
    ki : numpy array
        весовые коэффициенты для каждой полосы
    Qi : numpy array
        уровень шума (помехи) в месте измерения в i-й спектральной полосе
    pi : numpy array
        вероятное относительное количество формантных составляющих речи,
        которые будут иметь уровни интенсивности выше порогового значения
    Ri : numpy array
        спектральный индекс артикуляции
    R : float
        спектральный индекс артикуляции
    S : float
        слоговая разборчивость
    W_S : float
        словесная разборчивость от S
    W_R : float
        словесная разборчивость от R
    """
    # Атрибуты класса, подгружаются только один раз, далее используются всеми экземплярами
    __f_lower = np.array([])
    __f_higher = np.array([])
    if len(__f_lower) == 0 or len(__f_higher) == 0:
        reader = DataLoader()
        array = reader.read_csv_to_numpy_array("/calc_acoustic_ch/external_data/lower_f_higher_f.csv")
        __f_lower = array[0:-1]
        __f_higher = array[1:]

    # Подгрузка основных параметров для расчетов
    # data[0] - имя листа
    # data[1] - путь к файлу, откуда были взяты данные
    # data[2] - массив уровней сигнала
    # data[3] - массив уровней шума
    # data[4] - показывает, используются значения для уровней частот по умолчанию или пользовательские
    # data[5] - если data[4], то это массив с нижними границами частотных полос
    # data[6] - если data[4], то это массив с верхними границами частотных полос
    # dimension - размерность для всех данных, считается по размеру массива уровней сигнала
    def __init__(self, data):
        self.name = data[0]
        self.native_path = data[1]
        self.signal_level = data[2]
        self.dimension = len(self.signal_level)
        self.noise_level = data[3]
        if data[4]:
            self.f_lower = data[5][:self.dimension]
            self.f_higher = data[6][:self.dimension]
        else:
            self.f_lower = CalcCharAcousticChInfLeak.__f_lower[:self.dimension]
            self.f_higher = CalcCharAcousticChInfLeak.__f_higher[:self.dimension]

    # расчет всех параметров
    def calculate_all(self):
        self.qi = self._signal_to_noise_ratio()
        self.f_i_average = self._geometric_mean_frequency()
        self.delta_A_i = self._formant_parameter()
        self.ki = self._weighting_coefficients()
        self.Qi = self._noise_level_i()
        self.pi = self._coefficient_of_perception_of_formant()
        self.Ri = self._spectral_index_of_articulation()
        self.R = self._integral_index_of_articulation()
        self.S = self._syllabic_intelligibility()
        self.W_S = self._verbal_intelligibility_s()
        self.W_R = self._verbal_intelligibility_r()

        # создание словаря с значениями, которые требуются при записи данных в excel
        # ключи словаря намеренно совпадают с ключами в классе ReadersWriters
        self.data_to_write = {
            "NUMBER": np.arange(1, self.dimension + 1),
            "SIGNAL_LEVEL": self.signal_level,
            "NOISE_LEVEL": self.noise_level,
            "Q_I": self.qi,
            "F_LOWER_I": self.f_lower,
            "F_HIGHER_I": self.f_higher,
            "DELTA_A_I": self.delta_A_i,
            "K_I": self.ki,
            "R_I": self.Ri,
            "R": self.R,
            "S": self.S,
            "W_S": self.W_S,
            "W_R": self.W_R
        }

    # ниже представлены методы, которые выполняют различные этапы расчетов
    # все они сделаны приватными, потому что не требуется их вызов вне класса

    def _signal_to_noise_ratio(self):
        return self.signal_level - self.noise_level

    def _geometric_mean_frequency(self):
        return np.sqrt(self.f_lower * self.f_higher)

    def _formant_parameter(self):
        delta_A = []
        for f in np.nditer(self.f_i_average):
            if f <= 1000:
                delta_A.append((200 / (f ** 0.43) - 0.37))
            else:
                delta_A.append((1.38 + 1000 / (f ** 0.69)))
        return np.array(delta_A)

    def _weighting_coefficients(self):
        k_i = []
        for i in range(len(self.f_lower)):
            k_i.append(self._w_coef(self.f_higher[i]) - self._w_coef(self.f_lower[i]))
        return np.array(k_i)

    def _spectral_index_of_articulation(self):
        return self.pi * self.ki

    def _integral_index_of_articulation(self):
        return np.sum(self.Ri)

    def _syllabic_intelligibility(self):
        S = 0
        R = self.R
        if R < 0.15:
            S = 4 * (R ** 1.43)
        elif 0.15 <= R <= 0.7:
            S = 1.1 * (1 - 1.17 * math.exp((-2.9) * R))
        elif R > 0.7:
            S = 1.01 * (1 - 9.1 * math.exp((-6.9) * R))
        return S

    def _verbal_intelligibility_s(self):
        return 1.05 * (1 - math.exp((-6.15 * self.S) / (1 + self.S)))

    def _verbal_intelligibility_r(self):
        R = self.R
        if R < 0.15:
            w_r = 1.54 * (R ** 0.25) * (1 - math.exp(-11 * R))
        else:
            w_r = 1 - math.exp(-(11 * R) / (1 + 0.7 * R))
        return w_r

    def _coefficient_of_perception_of_formant(self):
        p_i = []
        for Q in self.Qi:
            p_i.append(self._p_coef(Q))
        return np.array(p_i)

    def _p_coef(self, Q):
        p = 0
        exp_arg = ((-4.3) * (10 ** (-3)) * ((27.3 - abs(Q)) ** 2))
        denominator = (1 + (10 ** (0.1 * abs(Q))))
        p = (0.78 + 5.46 * math.exp(exp_arg)) / denominator
        if Q > 0:
            p = 1 - p
        return p

    def _noise_level_i(self):
        return self.qi - self.delta_A_i

    def _w_coef(self, f):
        k = 0
        if 100 < f <= 400:
            k = 2.57 * (10 ** (-8)) * (f ** 2, 4)
        elif 400 < f <= (10 ** 4):
            k = 1 - 1.074 * math.exp((-10 ** (-4)) * (f ** 1.18))
        return k
