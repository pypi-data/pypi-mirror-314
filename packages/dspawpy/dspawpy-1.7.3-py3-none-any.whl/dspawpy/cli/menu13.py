import threading
from typing import Literal

from loguru import logger
from prompt_toolkit import prompt

from dspawpy import auto_test_cli
from dspawpy.cli import list_ds, pc
from dspawpy.cli.menu_prompts import Dio, Dparameter, Dresponse


def s13_1(language: Literal["EN", "CN"]) -> dict:
    """吸附质"""
    if auto_test_cli:
        from dspawpy.io.utils import getTSads as cli_getTSads

        for D in list_ds:
            if D["menu"] == 131:
                cli_getTSads(D["inf"], float(D["T"] or 298.15))

        D = {}
    else:

        def imp():
            global getTSads
            from dspawpy.io.utils import getTSads

        import_thread = threading.Thread(target=imp)
        import_thread.start()
        D = {}
        D["menu"] = 131
        D["inf"] = prompt(Dio[language]["txt"], completer=pc)
        D["T"] = float(input(Dparameter[language][6]) or 298.15)
        import_thread.join()
        logger.info(Dresponse[language][16])

        getTSads(D["inf"], D["T"])

    return D


def s13_2(language: Literal["EN", "CN"]) -> dict:
    """理想气体"""
    if auto_test_cli:
        from dspawpy.io.utils import getTSgas as cli_getTSgas

        for D in list_ds:
            if D["menu"] == 132:
                cli_getTSgas(
                    fretxt=D["inf"],
                    datafile=D["dataf"],
                    temperature=float(D["T"] or 298.15),
                    pressure=float(D["P"] or 101325.0),
                )

        D = {}
    else:

        def imp():
            global getTSgas
            from dspawpy.io.utils import getTSgas

        import_thread = threading.Thread(target=imp)
        import_thread.start()
        D = {}
        D["menu"] = 132
        D["inf"] = prompt(Dio[language]["txt"], completer=pc)
        D["dataf"] = prompt(Dio[language]["datafile"], completer=pc)
        D["T"] = float(input(Dparameter[language][6]) or 298.15)
        D["P"] = float(input(Dparameter[language][7]) or 101325.0)
        import_thread.join()
        logger.info(Dresponse[language][16])

        getTSgas(
            fretxt=D["inf"],
            datafile=D["dataf"],
            temperature=D["T"],
            pressure=D["P"],
        )
    return D
