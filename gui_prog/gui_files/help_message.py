from gui_prog.data_hadlers.help_mes_loader import HelpMessageLoader
from gui_prog.external_data.gui_text import help_btn


class HelpMessage:
    reader = HelpMessageLoader()
    help_mes = reader.get_help_mes_from_yaml()

    def get_message(self, name):
        self.title = help_btn[name][0]
        self.text = self.help_mes[help_btn[name][1]]


if __name__ == '__main__':
    mes = HelpMessage()
    mes.get_message("btn_generate_get_help")
    print(mes.title)
    print(mes.text)


