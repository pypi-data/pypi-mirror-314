import threading
from typing import Literal

from loguru import logger
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

from dspawpy import auto_test_cli
from dspawpy.cli import list_ds, pc
from dspawpy.cli.auxiliary import get_input, get_lims
from dspawpy.cli.menu_prompts import Dio, Dparameter, Dresponse, Dselect


def s6_1(language: Literal["EN", "CN"]) -> dict:
    """将能带和态密度显示在一张图上"""
    if auto_test_cli:
        from pymatgen.electronic_structure.plotter import (
            BSDOSPlotter as cli_BSDOSPlotter,
        )

        from dspawpy.io.read import (
            get_band_data as cli_get_band_data,
        )
        from dspawpy.io.read import (
            get_dos_data as cli_get_dos_data,
        )
        from dspawpy.plot import pltbd as cli_pltbd

        D = {}
        for D in list_ds:
            if D["menu"] == 61:
                band_data = cli_get_band_data(D["bandf"])
                dos_data = cli_get_dos_data(D["dosf"])

                bdp = cli_BSDOSPlotter(bs_projection=None, dos_projection=None)  # pyright: ignore [reportArgumentType]

                cli_pltbd(
                    bdp,
                    band_data,
                    dos_data,  # type: ignore
                    ylim=D["ylims"],
                    filename=D["outfile"],
                )

    else:

        def imp():
            global BSDOSPlotter, pltbd, get_band_data, get_dos_data
            from pymatgen.electronic_structure.plotter import BSDOSPlotter

            from dspawpy.io.read import get_band_data, get_dos_data
            from dspawpy.plot import pltbd

        import_thread = threading.Thread(target=imp)
        import_thread.start()

        D = {}
        D["menu"] = 61
        D["bandf"] = prompt(Dio[language]["band"], completer=pc)
        D["dosf"] = prompt(Dio[language]["dos"], completer=pc)
        D["ylims"] = get_lims(Dparameter[language][10], language)
        D["outfile"] = prompt(Dio[language]["figure"], completer=pc)
        import_thread.join()
        logger.info(Dresponse[language][16])

        band_data = get_band_data(D["bandf"])
        dos_data = get_dos_data(D["dosf"])

        bdp = BSDOSPlotter(bs_projection=None, dos_projection=None)  # pyright: ignore [reportArgumentType]

        pltbd(bdp, band_data, dos_data, ylim=D["ylims"], filename=D["outfile"])  # type: ignore

    return D


def s6_2(language: Literal["EN", "CN"]) -> dict:
    """将能带和投影态密度显示在一张图上"""
    if auto_test_cli:
        from pymatgen.electronic_structure.plotter import (
            BSDOSPlotter as cli_BSDOSPlotter,
        )

        from dspawpy.io.read import (
            get_band_data as cli_get_band_data,
        )
        from dspawpy.io.read import (
            get_dos_data as cli_get_dos_data,
        )
        from dspawpy.plot import pltbd as cli_pltbd

        for D in list_ds:
            if D["menu"] == 62:
                band_data = cli_get_band_data(D["bandf"])
                dos_data = cli_get_dos_data(D["dosf"])

                bdp = cli_BSDOSPlotter(
                    bs_projection=D["pband"], dos_projection=D["pdos"]
                )  # type: ignore

                cli_pltbd(
                    bdp,
                    band_data,
                    dos_data,  # type: ignore
                    ylim=D["ylims"],
                    filename=D["outfile"],
                )

        D = {}
    else:

        def imp():
            global BSDOSPlotter, pltbd, get_band_data, get_dos_data
            from pymatgen.electronic_structure.plotter import BSDOSPlotter

            from dspawpy.io.read import get_band_data, get_dos_data
            from dspawpy.plot import pltbd

        import_thread = threading.Thread(target=imp)
        import_thread.start()
        D = {}
        D["menu"] = 61
        D["bandf"] = prompt(Dio[language]["band"], completer=pc)
        D["dosf"] = prompt(Dio[language]["dos"], completer=pc)
        D["ylims"] = get_lims(Dparameter[language][10], language)
        D["outfile"] = prompt(Dio[language]["figure"], completer=pc)
        projs = ["elements"]
        D["pband"] = get_input(
            Dselect[language][17],
            projs,
            completer=WordCompleter(projs),
            allow_empty=True,
        )
        projs2 = ["elements", "orbitals"]
        D["pdos"] = get_input(
            Dselect[language][17],
            projs2,
            completer=WordCompleter(projs2),
            allow_empty=True,
        )
        import_thread.join()
        logger.info(Dresponse[language][16])

        band_data = get_band_data(D["bandf"])
        dos_data = get_dos_data(D["dosf"])

        bdp = BSDOSPlotter(bs_projection=D["pband"], dos_projection=D["pdos"])  # type: ignore

        pltbd(bdp, band_data, dos_data, ylim=D["ylims"], filename=D["outfile"])  # type: ignore

    return D
