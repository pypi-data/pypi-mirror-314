import os
import threading
from typing import Literal, Optional, Tuple

from loguru import logger
from prompt_toolkit import prompt
from prompt_toolkit.completion import (
    Completer,
    FuzzyCompleter,
    WordCompleter,
)

from dspawpy import auto_test_cli
from dspawpy.cli import list_ds, pc
from dspawpy.cli.menu_prompts import Dcheck, Dio, Dparameter, Dresponse, Dselect


def save_figure_dpi300(outfile: str, plt=None):
    """Save matplotlib figure with dpi=300"""
    logger.info(" Saving figure with dpi=300...")
    if plt is None:
        import matplotlib.pyplot as plt

    absfile = os.path.abspath(outfile)
    os.makedirs(os.path.dirname(absfile), exist_ok=True)
    plt.tight_layout()
    plt.savefig(absfile, dpi=300)
    logger.info(f"--> {absfile}")


def get_input(
    user_prompt: str,
    valid_inputs: list,
    completer: Optional[Completer] = None,
    allow_empty: bool = False,
    default_user_input: str = "",
) -> str:
    """Until user give valid input, or return default input if allow_empty is True and user input is empty."""
    if completer is None:
        completer = FuzzyCompleter(WordCompleter(valid_inputs))  # list completion
    from prompt_toolkit import prompt

    while True:
        user_input: str = prompt(user_prompt, completer=completer).strip()
        if allow_empty and len(user_input) == 0:
            return default_user_input
        elif user_input not in valid_inputs:
            continue
        else:
            return user_input


def get_inputs(
    user_prompt: str,
    valid_inputs: list,
    completer: Optional[Completer] = None,
    allow_empty: bool = False,
) -> list:
    """Return valid_inputs list if given empty"""
    if completer is None:
        completer = FuzzyCompleter(WordCompleter(valid_inputs))  # list completion
    from prompt_toolkit import prompt

    while True:
        user_inputs: list = prompt(user_prompt, completer=completer).strip().split()

        if allow_empty and len(user_inputs) == 0:
            return valid_inputs
        else:
            valid = True
            for n in user_inputs:
                if n not in valid_inputs:
                    valid = False
                    break
            if valid:
                return user_inputs
            else:
                continue


def get_lims(
    user_prompt: str,
    language: Literal["EN", "CN"],
) -> Optional[Tuple[float, float]]:
    """Get lower and higher limits from user input"""
    while True:
        userInput = input(user_prompt).strip()
        if userInput == "":
            return None
        elif " " not in userInput:
            logger.warning(f"!!! {userInput}{Dresponse[language][0]}")
            continue
        elif len(userInput.split(" ")) != 2:
            logger.warning(f"!!! {userInput}{Dresponse[language][1]}")
            continue
        else:
            try:
                lims = userInput.split(" ")
                lower = float(lims[0])
                higher = float(lims[1])
                return lower, higher

            except Exception:
                logger.warning(f"!!! {userInput}{Dresponse[language][2]}")
                continue


def online_check(local_dspawpy_version: str, language: Literal["EN", "CN"]):
    """Fetch latses version of dspawpy from pypi"""
    latest_version = None
    # requests is dependency of pymatgen
    from os.path import expanduser

    from requests import exceptions, get

    try:
        logger.info(Dcheck[language][0])
        response = get("https://pypi.org/pypi/dspawpy/json", timeout=3)
        latest_version = response.json()["info"]["version"]
        error_message = None
    except ModuleNotFoundError:
        error_message = Dcheck[language][1]
    except exceptions.Timeout:
        error_message = Dcheck[language][2]
    except exceptions.RequestException as e:
        error_message = f"{Dcheck[language][3]} {e}"
    except Exception as e:
        error_message = f"{Dcheck[language][4]} {e}"
    finally:
        if latest_version:
            if latest_version != local_dspawpy_version:
                logger.info(
                    f"{latest_version} > {local_dspawpy_version}; {Dcheck[language][1]}",
                )
            else:
                logger.info(
                    f"{latest_version} = {local_dspawpy_version}; {Dcheck[language][6]}",
                )

            with open(expanduser("~/.dspawpy_latest_version"), "w") as fin:
                fin.write(latest_version)
        else:
            logger.info(Dcheck[language][7])

    return error_message


def verify_dspawpy_version(check: bool, language: Literal["EN", "CN"]):
    """May skip online check"""
    from os.path import dirname, expanduser, isfile

    import dspawpy

    home = expanduser("~")

    dv = dspawpy.__version__
    df = dirname(dspawpy.__file__).replace(home, "~", 1)

    logger.info(f"{dv}: {df}")

    error_message = None
    if check:
        if isfile(expanduser("~/.dspawpy_latest_version")):
            with open(expanduser("~/.dspawpy_latest_version")) as fin:
                latest_version = fin.read().strip()
            if dv != latest_version:
                error_message = online_check(dv, language)
        else:
            error_message = online_check(dv, language)

        if error_message is not None:
            logger.info(error_message)


def s2(language: Literal["EN", "CN"]) -> dict:
    """structure结构转化"""

    if auto_test_cli:
        from dspawpy.io.structure import convert as cli_convert

        for D in list_ds:
            if D["menu"] == 2:
                cli_convert(infile=D["in"], outfile=D["out"])
        D = {}
    else:

        def imp():
            global convert
            from dspawpy.io.structure import convert

        import_thread = threading.Thread(target=imp)
        import_thread.start()

        D = {}
        D["menu"] = 2
        D["in"] = prompt(Dio[language]["ins"], completer=pc)
        D["out"] = prompt(Dio[language]["outs"], completer=pc)
        import_thread.join()
        logger.info(Dresponse[language][16])

        convert(infile=D["in"], outfile=D["out"])

    return D


def s7(language: Literal["EN", "CN"]) -> dict:
    """optical光学性质数据处理"""
    if auto_test_cli:
        from os import makedirs as cli_makedirs

        from dspawpy.plot import plot_optical as cli_plot_optical

        for D in list_ds:
            if D["menu"] == 7:
                if D["outd"].strip() != "":
                    cli_makedirs(D["outd"], exist_ok=True)
                cli_plot_optical(
                    datafile=D["inf"], keys=D["keys"], axes=D["label"], prefix=D["outd"]
                )

        D = {}
    else:

        def imp():
            global plot_optical, makedirs
            from os import makedirs

            from dspawpy.plot import plot_optical

        import_thread = threading.Thread(target=imp)
        import_thread.start()
        D = {}
        D["menu"] = 7
        D["inf"] = prompt(Dio[language]["optical"], completer=pc)
        _list = [
            "AbsorptionCoefficient",
            "ExtinctionCoefficient",
            "RefractiveIndex",
            "Reflectance",
        ]
        D["keys"] = get_inputs(
            Dselect[language][15],
            _list,
            completer=WordCompleter(_list),
            allow_empty=True,
        )
        _list2 = ["X", "Y", "Z", "XY", "YZ", "ZX"]
        D["label"] = get_inputs(
            Dselect[language][16],
            _list2,
            completer=WordCompleter(_list2),
            allow_empty=True,
        )

        D["outd"] = prompt(Dio[language]["outd"], completer=pc)
        import_thread.join()
        logger.info(Dresponse[language][16])

        if D["outd"].strip() != "":
            makedirs(D["outd"], exist_ok=True)
        plot_optical(
            datafile=D["inf"], keys=D["keys"], axes=D["label"], prefix=D["outd"]
        )

    return D


def s11(language: Literal["EN", "CN"]) -> dict:
    """Polarization铁电极化数据处理"""
    if auto_test_cli:
        from dspawpy.plot import (
            plot_polarization_figure as cli_plot_polarization_figure,
        )

        for D in list_ds:
            if D["menu"] == 7:
                cli_plot_polarization_figure(
                    D["inf"], D["rep"], figname=D["figure"], show=False
                )

        D = {}
    else:

        def imp():
            global plot_polarization_figure
            from dspawpy.plot import plot_polarization_figure

        import_thread = threading.Thread(target=imp)
        import_thread.start()
        D = {}
        D["menu"] = 11
        D["inf"] = prompt(Dio[language]["polarization"], completer=pc)
        D["figure"] = prompt(Dio[language]["figure"], completer=pc)
        D["rep"] = int(input(Dparameter[language][5]) or 2)
        import_thread.join()
        logger.info(Dresponse[language][16])

        plot_polarization_figure(D["inf"], D["rep"], figname=D["figure"], show=False)

    return D


def s12(language: Literal["EN", "CN"]) -> dict:
    """ZPE零点振动能数据处理"""

    if auto_test_cli:
        from dspawpy.io.utils import getZPE as cli_getZPE

        for D in list_ds:
            if D["menu"] == 12:
                cli_getZPE(D["inf"])

        D = {}

    else:

        def imp():
            global getZPE
            from dspawpy.io.utils import getZPE

        import_thread = threading.Thread(target=imp)
        import_thread.start()
        D = {}
        D["menu"] = 12
        D["inf"] = prompt(Dio[language]["txt"], completer=pc)
        import_thread.join()
        logger.info(Dresponse[language][16])

        getZPE(D["inf"])

    return D


def s14(language: Literal["EN", "CN"]) -> dict:
    if auto_test_cli:
        from dspawpy.io.read import read_relax_data as cli_read_relax_data

        for D in list_ds:
            if D["menu"] == 14:
                cli_read_relax_data(D["logfile"])

        D = {}

    else:

        def imp():
            global read_relax_data
            from dspawpy.io.read import read_relax_data

        import_thread = threading.Thread(target=imp)
        import_thread.start()
        D = {}
        D["menu"] = 14
        D["logfile"] = prompt(Dio[language]["logfile"], completer=pc)

        D["printef"] = True if prompt(Dselect[language][20]).startswith("y") else False
        D["relative"] = False
        if D["printef"]:
            D["relative"] = (
                True if prompt(Dselect[language][21]).startswith("y") else False
            )

        D["writetraj"] = (
            True if prompt(Dselect[language][22]).startswith("y") else False
        )
        D["xyzfilename"] = None
        if D["writetraj"]:
            D["xyzfilename"] = prompt(Dio[language]["xyzfilename"], completer=pc)

        D["writeas"] = True if prompt(Dselect[language][23]).startswith("y") else False
        D["asfilename"] = None
        if D["writeas"]:
            D["asfilename"] = prompt(Dio[language]["asfilename"], completer=pc)

        import_thread.join()
        logger.info(Dresponse[language][16])

        read_relax_data(
            D["logfile"],
            D["printef"],
            D["relative"],
            D["writetraj"],
            D["xyzfilename"],
            D["writeas"],
            D["asfilename"],
        )
    return D
