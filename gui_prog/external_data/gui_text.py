from calc_acoustic_ch.external_data.text_constant import *

MAIN_WIN_TITLE = "Расчет возможности существования акустических КУИ"

BTN_GEN_INIT = GEN_INIT
BTN_PROV_INIT = PROV_INIT
BTN_CALC_INIT = CALC_INIT
BTN_SAVE_INIT = SAVE_INIT

LBL_GEN_INIT = TEXT_GEN_INIT
LBL_PROV_INIT = TEXT_PROV_INIT
LBL_CALC_INIT = TEXT_CALC_INIT
LBL_SAVE_INIT = TEXT_SAVE_INIT
LBL_STATUS_INIT = STATUS_INIT

BTN_HELP = "?"
STATUS_DESC = "Статус:"

BTN_GEN_HELP = "[Info] Создать файл"
BTN_PROV_HELP = "[Info] Предоставить файл с данными"
BTN_CALC_HELP = "[Info] Произвести расчеты"
BTN_SAVE_HELP = "[Info] Сохранить результаты"

help_btn = {
    "btn_generate_get_help": (BTN_GEN_HELP, "help_gen"),
    "btn_provide_get_help": (BTN_PROV_HELP, "help_prov"),
    "btn_calculate_get_help": (BTN_CALC_HELP, "help_calc"),
    "btn_save_get_help": (BTN_SAVE_HELP, "help_save")
}

TITLE_CHOOSE_FILE = "Выберите файл с данными"
EXIST_FILE_NAME = ""

TITLE_CREATE_FILE = "Создать новый файл"
NEW_FILE_NAME = "новый_файл.xlsx"
EXCEL_FORMAT = "Microsoft Excel (*.xlsx)"
