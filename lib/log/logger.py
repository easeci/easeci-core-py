from colorama import Style, Fore
from datetime import datetime


def log(content, err=False):
    dt = datetime.today()
    if not err:
        print(Fore.LIGHTCYAN_EX, f"==> [EaseCI] [{dt}]", Style.RESET_ALL, content, Style.RESET_ALL)
    else:
        print(Fore.RED, f"ERR! ==> [EaseCI] [{dt}]", content, Style.RESET_ALL)
