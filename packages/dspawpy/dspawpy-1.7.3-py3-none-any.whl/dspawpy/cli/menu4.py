import threading
from typing import Literal

from loguru import logger
from prompt_toolkit import prompt

from dspawpy import auto_test_cli
from dspawpy.cli import list_ds, pc
from dspawpy.cli.auxiliary import get_input, get_inputs, get_lims, save_figure_dpi300
from dspawpy.cli.menu_prompts import Dio, Dparameter, Dresponse, Dselect


def pre_ele_band(language: Literal["EN", "CN"]):
    def imp():
        global get_band_data, BSPlotter
        from pymatgen.electronic_structure.plotter import BSPlotter

        from dspawpy.io.read import get_band_data

    import_thread = threading.Thread(target=imp)
    import_thread.start()

    D = {}
    D["inf"] = prompt(Dio[language]["band"], completer=pc)
    D["ylims"] = get_lims(Dparameter[language][10], language)
    D["figure"] = prompt(Dio[language]["figure"], completer=pc) or "band.png"

    import_thread.join()
    logger.info(Dresponse[language][16])

    return D, BSPlotter, get_band_data


def pre_ele_pband(language: Literal["EN", "CN"]):
    def imp():
        global get_band_data, BSPlotterProjected
        from pymatgen.electronic_structure.plotter import BSPlotterProjected

        from dspawpy.io.read import get_band_data

    import_thread = threading.Thread(target=imp)
    import_thread.start()

    D = {}
    D["inf"] = prompt(Dio[language]["pband"], completer=pc)
    D["ylims"] = get_lims(Dparameter[language][10], language)
    D["figure"] = prompt(Dio[language]["figure"], completer=pc) or "band_projected.png"

    import_thread.join()
    logger.info(Dresponse[language][16])

    return D, BSPlotterProjected, get_band_data


def s4_1(language: Literal["EN", "CN"]) -> dict:
    """普通能带"""
    if auto_test_cli:
        from pymatgen.electronic_structure.plotter import BSPlotter as cli_BSPlotter

        from dspawpy.io.read import get_band_data as cli_get_band_data

        for D in list_ds:
            band_data = cli_get_band_data(D["inf"], zero_to_efermi=True)
            is_metal = band_data.is_metal()

            if not is_metal and D["shift"] == "y":
                band_data = cli_get_band_data(D["inf"], zero_to_efermi=True)
                bsp = cli_BSPlotter(band_data)
                bsp.get_plot(False, ylim=D["ylims"])
            else:
                bsp = cli_BSPlotter(band_data)
                bsp.get_plot(True, ylim=D["ylims"])
            save_figure_dpi300(D["figure"])

        D = {}
    else:
        D, BSPlotter, get_band_data = pre_ele_band(language)
        D["menu"] = 41

        band_data = get_band_data(D["inf"])
        logger.debug("got data, initializing plotter...")
        bsp = BSPlotter(band_data)
        logger.debug("plotter initialized")

        is_metal = band_data.is_metal()
        if is_metal:
            bsp.get_plot(ylim=D["ylims"])
        else:
            D["shift"] = get_input(Dselect[language][3], ["y", "n"])
            if D["shift"] == "y":
                from pymatgen.electronic_structure.plotter import BSPlotter

                from dspawpy.io.read import get_band_data

                band_data = get_band_data(D["inf"], zero_to_efermi=True)
                bsp = BSPlotter(band_data)
                bsp.get_plot(False, ylim=D["ylims"])
            else:
                bsp.get_plot(ylim=D["ylims"])

        save_figure_dpi300(D["figure"])
    return D


def s4_2(language: Literal["EN", "CN"]) -> dict:
    """将能带投影到每一种元素分别作图，数据点大小表示该元素对该轨道的贡献"""
    if auto_test_cli:
        from pymatgen.electronic_structure.plotter import (
            BSPlotterProjected as cli_BSPlotterProjected,
        )

        from dspawpy.io.read import get_band_data as cli_get_band_data

        for D in list_ds:
            band_data = cli_get_band_data(D["inf"], zero_to_efermi=False)
            is_metal = band_data.is_metal()
            if not is_metal and D["shift"] == "y":
                band_data = cli_get_band_data(D["inf"], zero_to_efermi=True)
                bsp = cli_BSPlotterProjected(band_data)
                bsp.get_elt_projected_plots(ylim=D["ylims"])
            else:
                bsp = cli_BSPlotterProjected(band_data)
                bsp.get_elt_projected_plots(ylim=D["ylims"])

            save_figure_dpi300(D["figure"])
        D = {}
    else:
        D, BSPlotterProjected, get_band_data = pre_ele_pband(language)
        D["menu"] = 42
        band_data = get_band_data(D["inf"])
        logger.debug("got data, initializing plotter...")
        bsp = BSPlotterProjected(band_data)
        logger.debug("plotter initialized")

        is_metal = band_data.is_metal()
        if is_metal:
            bsp.get_elt_projected_plots(ylim=D["ylims"])
        else:
            D["shift"] = get_input(Dselect[language][3], ["y", "n"])
            if D["shift"] == "y":
                from pymatgen.electronic_structure.plotter import BSPlotterProjected

                from dspawpy.io.read import get_band_data

                band_data = get_band_data(D["inf"], zero_to_efermi=True)
                bsp = BSPlotterProjected(band_data)
                bsp.get_elt_projected_plots(ylim=D["ylims"])
            else:
                bsp.get_elt_projected_plots(ylim=D["ylims"])

        save_figure_dpi300(D["figure"])
    return D


def s4_3(language: Literal["EN", "CN"]) -> dict:
    """能带投影到不同元素的不同轨道"""
    if auto_test_cli:
        from pymatgen.electronic_structure.plotter import (
            BSPlotterProjected as cli_BSPlotterProjected,
        )

        from dspawpy.io.read import get_band_data as cli_get_band_data

        for D in list_ds:
            band_data = cli_get_band_data(D["inf"], zero_to_efermi=False)
            is_metal = band_data.is_metal()
            if not is_metal and D["shift"] == "y":
                band_data = cli_get_band_data(D["inf"], zero_to_efermi=True)
                bsp = cli_BSPlotterProjected(band_data)
                bsp.get_projected_plots_dots(D["dictio"], False, ylim=D["ylims"])
            else:
                bsp = cli_BSPlotterProjected(band_data)
                bsp.get_projected_plots_dots(D["dictio"], False, ylim=D["ylims"])

            save_figure_dpi300(D["figure"])
        D = {}

    else:
        D, BSPlotterProjected, get_band_data = pre_ele_pband(language)
        D["menu"] = 43
        band_data = get_band_data(D["inf"])
        logger.debug("got data, initializing plotter...")
        bsp = BSPlotterProjected(band_data)
        logger.debug("plotter initialized")

        banddatatructure = band_data.structure
        assert banddatatructure is not None
        logger.info(banddatatructure)
        es = banddatatructure.composition.elements
        D["dictio"] = {}

        from pymatgen.core import Element

        while True:
            _e = get_input(Dselect[language][4], [str(e) for e in es], allow_empty=True)
            if _e == "":
                break
            e = Element(_e)

            available_orbitals = ["s"]
            orbitals = e.atomic_orbitals
            assert isinstance(orbitals, dict)
            for o in orbitals:
                if "p" in o:
                    available_orbitals.append("p")
                elif "d" in o:
                    available_orbitals.append("d")
                elif "f" in o:
                    available_orbitals.append("f")
            unique_orbitals = list(set(available_orbitals))
            _o = get_input(Dselect[language][5], unique_orbitals)
            _os = _o.split(" ")
            dict_eo = {_e: _os}
            # update dictio
            D["dictio"].update(dict_eo)

        is_metal = band_data.is_metal()
        if is_metal:
            bsp.get_projected_plots_dots(D["dictio"])
        else:
            D["shift"] = get_input(Dselect[language][3], ["y", "n"])
            if D["shift"] == "y":
                from pymatgen.electronic_structure.plotter import BSPlotterProjected

                from dspawpy.io.read import get_band_data

                band_data = get_band_data(D["inf"], zero_to_efermi=True)
                bsp = BSPlotterProjected(band_data)
                bsp.get_projected_plots_dots(D["dictio"], False, ylim=D["ylims"])
            else:
                bsp.get_projected_plots_dots(D["dictio"], ylim=D["ylims"])

        save_figure_dpi300(D["figure"])
    return D


def s4_4(language: Literal["EN", "CN"]) -> dict:
    """将能带投影到不同原子的不同轨道"""
    if auto_test_cli:
        from pymatgen.electronic_structure.plotter import (
            BSPlotterProjected as cli_BSPlotterProjected,
        )

        from dspawpy.io.read import get_band_data as cli_get_band_data

        for D in list_ds:
            band_data = cli_get_band_data(D["inf"], zero_to_efermi=False)
            is_metal = band_data.is_metal()
            if not is_metal and D["shift"] == "y":
                band_data = cli_get_band_data(D["inf"], zero_to_efermi=True)
                bsp = cli_BSPlotterProjected(band_data)
                bsp.get_projected_plots_dots_patom_pmorb(
                    D["dictio"],
                    D["dictpa"],
                    zero_to_efermi=False,
                    ylim=D["ylims"],
                )
            else:
                bsp = cli_BSPlotterProjected(band_data)
                bsp.get_projected_plots_dots_patom_pmorb(
                    D["dictio"],
                    D["dictpa"],
                    ylim=D["ylims"],
                )

            save_figure_dpi300(D["figure"])

        D = {}
    else:
        D, BSPlotterProjected, get_band_data = pre_ele_pband(language)
        D["menu"] = 44
        band_data = get_band_data(D["inf"])
        logger.debug("got data, initializing plotter...")
        bsp = BSPlotterProjected(band_data)
        logger.debug("plotter initialized")

        banddatatructure = band_data.structure
        assert banddatatructure is not None
        logger.info(banddatatructure)
        sites = banddatatructure.sites
        ns = [str(i) for i in range(len(sites))]
        D["dictio"] = {}
        D["dictpa"] = {}
        while True:
            _n = get_input(Dselect[language][6], ns, allow_empty=True)
            if _n == "":
                break
            _e = sites[int(_n)].specie
            available_orbitals = ["s"]
            orbitals = _e.atomic_orbitals
            assert orbitals is not None
            for o in orbitals:
                if "p" in o:
                    available_orbitals.append("p")
                    available_orbitals.append("px")
                    available_orbitals.append("py")
                    available_orbitals.append("pz")
                elif "d" in o:
                    available_orbitals.append("d")
                    available_orbitals.append("dxy")
                    available_orbitals.append("dyz")
                    available_orbitals.append("dxz")
                    available_orbitals.append("dx2")
                    available_orbitals.append("dz2")
                elif "f" in o:
                    available_orbitals.append("f")
                    available_orbitals.append("f_3")
                    available_orbitals.append("f_2")
                    available_orbitals.append("f_1")
                    available_orbitals.append("f0")
                    available_orbitals.append("f1")
                    available_orbitals.append("f2")
                    available_orbitals.append("f3")

            unique_orbitals = list(set(available_orbitals))
            D["dictpa"].update({str(_e): [int(_n) + 2]})
            _os = get_inputs(Dselect[language][7], unique_orbitals)
            dict_eo = {str(_e): _os}
            # update dictio
            D["dictio"].update(dict_eo)

        logger.info(f"dictpa: {D['dictpa']}")
        logger.info(f"dictio: {D['dictio']}")

        is_metal = band_data.is_metal()
        if is_metal:
            bsp.get_projected_plots_dots_patom_pmorb(
                D["dictio"],
                D["dictpa"],
                ylim=D["ylims"],
            )
        else:
            D["shift"] = get_input(Dselect[language][3], ["y", "n"])
            if D["shift"] == "y":
                from pymatgen.electronic_structure.plotter import BSPlotterProjected

                from dspawpy.io.read import get_band_data

                band_data = get_band_data(D["inf"], zero_to_efermi=True)

                bsp = BSPlotterProjected(band_data)
                bsp.get_projected_plots_dots_patom_pmorb(
                    D["dictio"],
                    D["dictpa"],
                    zero_to_efermi=False,
                    ylim=D["ylims"],
                )
            else:
                bsp.get_projected_plots_dots_patom_pmorb(
                    D["dictio"],
                    D["dictpa"],
                    ylim=D["ylims"],
                )

        save_figure_dpi300(D["figure"])

    return D


def s4_5(language: Literal["EN", "CN"]) -> dict:
    """能带反折叠处理"""

    if auto_test_cli:
        from dspawpy.plot import plot_bandunfolding as cli_plot_bandunfolding

        for D in list_ds:
            cli_plt = cli_plot_bandunfolding(D["inf"])
            cli_plt.ylim(D["ylims"])
            save_figure_dpi300(D["figure"], cli_plt)

        D = {}
    else:

        def imp():
            global plot_bandunfolding, plt
            import matplotlib.pyplot as plt

            from dspawpy.plot import plot_bandunfolding

        import_thread = threading.Thread(target=imp)
        import_thread.start()
        D, _, _ = pre_ele_pband(language)
        D["menu"] = 45
        import_thread.join()
        logger.info(Dresponse[language][16])

        plt = plot_bandunfolding(D["inf"])
        plt.ylim(D["ylims"])
        save_figure_dpi300(D["figure"], plt)

    return D


def s4_6(language: Literal["EN", "CN"]) -> dict:
    """band-compare能带对比图处理"""

    if auto_test_cli:
        from pymatgen.electronic_structure.plotter import BSPlotter as cli_BSPlotter

        from dspawpy.io.read import get_band_data as cli_get_band_data

        for D in list_ds:
            band_data = cli_get_band_data(D["inf"])
            bsp = cli_BSPlotter(band_data)
            if isinstance(D["infile2"], list):
                bd1 = cli_get_band_data(D["infile2"][0], D["infile2"][1])
            else:  # str
                bd1 = cli_get_band_data(D["infile2"])
            assert bd1 is not None, Dresponse[language][6]
            bsp = cli_BSPlotter(bs=bd1)
            bsp2 = cli_BSPlotter(bs=band_data)
            bsp.add_bs(bsp2._bs)
            bsp.get_plot(bs_labels=["wannier interpolated", "DFT"], ylim=D["ylims"])
            save_figure_dpi300(D["figure"])

        D = {}
    else:

        def imp():
            global get_band_data, BSPlotter
            from pymatgen.electronic_structure.plotter import BSPlotter

            from dspawpy.io.read import get_band_data

        import_thread = threading.Thread(target=imp)
        import_thread.start()
        D, _, get_band_data = pre_ele_pband(language)
        D["menu"] = 46
        band_data = get_band_data(D["inf"])
        logger.debug("got data, initializing plotter...")
        bsp = BSPlotterProjected(band_data)
        logger.debug("plotter initialized")

        D["infile2"] = prompt(Dio[language]["wband"], completer=pc)
        if D["infile2"].endswith(".json"):
            D["infile3"] = prompt(
                Dio[language]["sysjson"],
                completer=pc,
            )
            D["infile2"] = [D["infile2"], D["infile3"]]
        import_thread.join()
        logger.info(Dresponse[language][16])

        if isinstance(D["infile2"], list):
            bd1 = get_band_data(D["infile2"][0], D["infile2"][1])
        else:  # str
            bd1 = get_band_data(D["infile2"])
        assert bd1 is not None, Dresponse[language][6]
        bsp = BSPlotter(bs=bd1)
        bsp2 = BSPlotter(bs=band_data)
        bsp.add_bs(bsp2._bs)
        bsp.get_plot(bs_labels=["wannier interpolated", "DFT"], ylim=D["ylims"])
        save_figure_dpi300(D["figure"])

    return D
