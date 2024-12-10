from inspect import currentframe, getframeinfo
from colorama import Fore, Back
from datetime import datetime
import re
import pathlib
import colorama


class Logging:

    def __init__(self):

        self.max_len = 63

        self.clr_err = Fore.RED
        self.clr_warn = Fore.LIGHTYELLOW_EX
        self.clr_succ = Fore.LIGHTGREEN_EX

        self.clr_blue = Fore.BLUE
        self.clr_cyan = Fore.CYAN
        self.clr_magenta = Fore.MAGENTA

        self.clr_blue_light = Fore.LIGHTBLUE_EX
        self.clr_cyan_light = Fore.LIGHTCYAN_EX
        self.clr_magenta_light = Fore.LIGHTMAGENTA_EX

        self.clr_reset = Fore.RESET





    def print(self, txt: str, fore_color: Fore = None, end: str = None, is_remove_prev: bool = False):

        frameinfo = getframeinfo(currentframe().f_back)
        filename = re.split(r"[/|\\]", frameinfo.filename)[-1]
        linenumber = frameinfo.lineno
        now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

        txt = re.sub('Completed', f'{self.clr_succ}Completed{self.clr_reset}', txt)


        str_prefix = f"{Fore.LIGHTBLACK_EX}{now} {self.clr_blue}{filename}:{linenumber}{Fore.RESET}"
        str_prefix += " " * (self.max_len - len(str_prefix))
        str_suffix = f"{fore_color if fore_color else ""}{txt}{Fore.RESET}"
        str_content = f"{'\r' if is_remove_prev else ''}{str_prefix} {str_suffix}"

        if end is None:
            print(str_content)
        else:
            if end == '\n':
                print(f'\r{str_content}')
            else:
                print(f'\r{str_content}', end=end)










    # import inspect
    # @staticmethod
    # def print_link(*, txt, file=None, line=None):
    #     """ Print a link in PyCharm to a line in file.
    #         Defaults to line where this function was called. """
    #
    #     if file is None:
    #         file = inspect.stack()[1].filename
    #
    #     if line is None:
    #         line = inspect.stack()[1].lineno
    #
    #     str_out = f'File "{file}", line {max(line, 1)}'.replace("\\", "/")
    #
    #     # str_out = f"{txt} {Fore.LIGHTBLACK_EX}(file: {file}, line: {max(line, 1)}){Fore.RESET}"
    #
    #     print(str_out)

