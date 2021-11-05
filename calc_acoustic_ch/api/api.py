from abc import abstractmethod

from calc_acoustic_ch.data_handlers.excel_readers_writers import ReadersWriters
from calc_acoustic_ch.external_data.text_constant import *
from calc_acoustic_ch.math_handler.math_func import CalcCharAcousticChInfLeak


class GenerateObject:
    @abstractmethod
    def run_input(self):
        pass

    @abstractmethod
    def get_path(self):
        pass

    @abstractmethod
    def get_sheet_count(self):
        pass

    @abstractmethod
    def success_input(self):
        pass


class ProvideDataObject:
    @abstractmethod
    def get_path(self):
        pass


class SaveDataObject:
    @abstractmethod
    def get_path(self):
        pass


class MainObject:
    def __init__(self):
        self.main_status: Field = NotImplemented
        self.gen_status: Field = NotImplemented
        self.prov_status: Field = NotImplemented
        self.calc_status: Field = NotImplemented
        self.save_status: Field = NotImplemented
        self.generate_file_pr_func: ProgramFunction = NotImplemented
        self.provide_data_pr_func: ProgramFunction = NotImplemented
        self.calculate_pr_func: ProgramFunction = NotImplemented
        self.save_results_pr_func: ProgramFunction = NotImplemented
        self.parsed_data = NotImplemented
        self.math_objects = NotImplemented


class Field:
    def __init__(self):
        self.text: str = NotImplemented

    @abstractmethod
    def set_text(self, text):
        pass


class ProgramFunction:
    @abstractmethod
    def enable(self):
        pass

    @abstractmethod
    def disable(self):
        pass


def get_dir_for_gen(main_object, generate_object):
    generate_object.run_input()
    try:
        gen_path = generate_object.get_path()
        sheet_count = generate_object.get_sheet_count()
        if generate_object.success_input():
            writer = ReadersWriters()
            writer.generate_excel(gen_path, sheet_count)
            main_object.gen_status.set_text(TEXT_GEN_SUCCESS)
            main_object.main_status.set_text(STATUS_INPUT_WELCOME)
        else:
            raise Exception
    except Exception:
        main_object.gen_status.set_text(TEXT_GEN_FAIL)
        main_object.main_status.set_text(STATUS_INPUT_WARNING)
    finally:
        main_object.prov_status.set_text(TEXT_PROV_INIT)


def get_file_with_data(main_object, provide_object):
    reader = ReadersWriters()
    data_path = provide_object.get_path()
    try:
        main_object.parsed_data = reader.read_all_sheets_with_signal_noise(data_path)
        main_object.prov_status.set_text(TEXT_PROV_SUCCESS)
        main_object.main_status.set_text(STATUS_INPUT_SUCCESS)
        main_object.calculate_pr_func.enable()
        main_object.calc_status.set_text(TEXT_CALC_WELCOME)
    except Exception:
        main_object.prov_status.set_text(TEXT_PROV_FAIL)
        main_object.calculate_pr_func.disable()
        main_object.save_results_pr_func.disable()
        main_object.calc_status.set_text(TEXT_CALC_INIT)
        main_object.save_status.set_text(TEXT_SAVE_INIT)
        main_object.main_status.set_text(STATUS_INPUT_FAIL)


def calculate(main_object):
    try:
        main_object.math_objects = []
        for data in main_object.parsed_data:
            main_object.math_objects.append(CalcCharAcousticChInfLeak(data))
        for obj in main_object.math_objects:
            obj.calculate_all()
        main_object.calc_status.set_text(TEXT_CALC_SUCCESS)
        main_object.save_results_pr_func.enable()
        main_object.save_status.set_text(TEXT_SAVE_WELCOME)
        main_object.main_status.set_text(STATUS_CALC_SUCCESS)
    except Exception:
        main_object.calc_status.set_text(TEXT_CALC_FAIL)
        main_object.main_status.set_text(STATUS_CALC_FAIL)
        main_object.save_results_pr_func.disable()
        main_object.save_status.set_text(TEXT_SAVE_INIT)


def save(main_object, save_object):
    try:
        main_object.save_status.set_text(TEXT_SAVE_PROCESSING)
        save_path = save_object.get_path()
        writer = ReadersWriters()
        writer.write_all_results_to_excel(main_object.math_objects, same_path=False, new_path=save_path)
        main_object.save_status.set_text(TEXT_SAVE_SUCCESS)
        main_object.main_status.set_text(STATUS_SAVE_SUCCESS)
    except Exception as e:
        print(e)
        main_object.save_status.set_text(TEXT_SAVE_FAIL)
        main_object.main_status.set_text(STATUS_SAVE_FAIL)
