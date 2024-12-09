import os
import sys
import threading
from typing import Literal

from loguru import logger
from prompt_toolkit import prompt

from dspawpy import auto_test_cli
from dspawpy.cli import list_ds, pc
from dspawpy.cli.auxiliary import get_lims, save_figure_dpi300
from dspawpy.cli.menu_prompts import Dio, Dparameter, Dresponse


class HidePrints:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, "w")

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


def pre_ph_band(language: Literal["EN", "CN"]):
    if auto_test_cli:
        from dspawpy.io.read import (
            get_phonon_band_data as cli_get_phonon_band_data,
        )

        with HidePrints():
            from pymatgen.phonon.plotter import (
                PhononBSPlotter as cli_PhononBSPlotter,
            )

        for D in list_ds:
            if D["menu"] == 91:
                cli_band_data = cli_get_phonon_band_data(D["inf"])
                cli_bsp = cli_PhononBSPlotter(cli_band_data)
                cli_bsp.get_plot(ylim=D["ylims"])  # pyright: ignore [reportArgumentType]
                save_figure_dpi300(D["figure"])

    def imp():
        global get_phonon_band_data, PhononBSPlotter
        from dspawpy.io.read import get_phonon_band_data

        with HidePrints():
            from pymatgen.phonon.plotter import PhononBSPlotter

    import_thread = threading.Thread(target=imp)
    import_thread.start()

    D = {}
    D["inf"] = prompt(Dio[language]["phband"], completer=pc)
    D["ylims"] = get_lims(Dparameter[language][10], language)
    D["figure"] = prompt(Dio[language]["figure"], completer=pc) or "ph_band.png"

    import_thread.join()
    logger.info(Dresponse[language][16])

    return D, get_phonon_band_data, PhononBSPlotter


def s9_1(language: Literal["EN", "CN"]) -> dict:
    """声子能带数据处理"""

    if auto_test_cli:
        from pymatgen.phonon.plotter import PhononBSPlotter as cli_PhononBSPlotter

        from dspawpy.io.read import get_phonon_band_data as cli_get_phonon_band_data

        for D in list_ds:
            if D["menu"] == 91:
                band_data = cli_get_phonon_band_data(D["inf"])
                bsp = cli_PhononBSPlotter(band_data)
                bsp.get_plot(ylim=D["ylims"])  # pyright: ignore [reportArgumentType]
                save_figure_dpi300(D["figure"])
        D = {}

    else:
        D, get_phonon_band_data, PhononBSPlotter = pre_ph_band(language)
        D["menu"] = 91

        band_data = get_phonon_band_data(D["inf"])
        logger.debug("got data, initializing plotter...")
        bsp = PhononBSPlotter(band_data)
        logger.debug("plotter initialized")
        bsp.get_plot(ylim=D["ylims"])  # pyright: ignore [reportArgumentType]
        save_figure_dpi300(D["figure"])

    return D


def pre_ph_dos(language: Literal["EN", "CN"]):
    def imp():
        global PhononDosPlotter, get_phonon_dos_data
        from dspawpy.io.read import get_phonon_dos_data

        with HidePrints():
            from pymatgen.phonon.plotter import PhononDosPlotter

    import_thread = threading.Thread(target=imp)
    import_thread.start()

    D = {}
    D["inf"] = prompt(Dio[language]["phdos"], completer=pc)
    D["xlims"] = get_lims(Dparameter[language][9], language)
    D["ylims"] = get_lims(Dparameter[language][10], language)
    D["figure"] = prompt(Dio[language]["figure"], completer=pc) or "ph_dos.png"
    import_thread.join()
    logger.info(Dresponse[language][16])

    return D, get_phonon_dos_data, PhononDosPlotter


def s9_2(language: Literal["EN", "CN"]) -> dict:
    """声子态密度数据处理"""
    if auto_test_cli:
        from pymatgen.phonon.plotter import PhononDosPlotter as cli_PhononDosPlotter

        from dspawpy.io.read import get_phonon_dos_data as cli_get_phonon_dos_data

        for D in list_ds:
            if D["menu"] == 92:
                dos_data = cli_get_phonon_dos_data(D["inf"])
                dos_plotter = cli_PhononDosPlotter(stack=False, sigma=None)
                dos_plotter.add_dos(label="Phonon", dos=dos_data)
                dos_plotter.get_plot(
                    xlim=D["xlims"],  # pyright: ignore [reportArgumentType]
                    ylim=D["ylims"],  # pyright: ignore [reportArgumentType]
                    units="thz",
                )
                save_figure_dpi300(D["figure"])
        D = {}

    else:
        D, get_phonon_dos_data, PhononDosPlotter = pre_ph_dos(language)
        D["menu"] = 92

        dos_data = get_phonon_dos_data(D["inf"])
        logger.debug("got data, initializing plotter...")
        dos_plotter = PhononDosPlotter(stack=False, sigma=None)
        logger.debug("plotter initialized")

        dos_plotter.add_dos(label="Phonon", dos=dos_data)
        dos_plotter.get_plot(
            xlim=D["xlims"],  # pyright: ignore [reportArgumentType]
            ylim=D["ylims"],  # pyright: ignore [reportArgumentType]
            units="thz",
        )

        save_figure_dpi300(D["figure"])

    return D


def s9_3(language: Literal["EN", "CN"]) -> dict:
    """声子热力学数据处理"""
    if auto_test_cli:
        from dspawpy.plot import plot_phonon_thermal as cli_plot_phonon_thermal

        for D in list_ds:
            if D["menu"] == 93:
                cli_plot_phonon_thermal(D["inf"], D["figure"], True)
        D = {}

    else:

        def imp():
            global plot_phonon_thermal
            from dspawpy.plot import plot_phonon_thermal

        import_thread = threading.Thread(target=imp)
        import_thread.start()
        D = {}
        D["menu"] = 93
        D["inf"] = prompt(Dio[language]["inf"], completer=pc)
        D["figure"] = prompt(Dio[language]["figure"], completer=pc)
        import_thread.join()
        logger.info(Dresponse[language][16])

        plot_phonon_thermal(D["inf"], D["figure"], False)

    return D
