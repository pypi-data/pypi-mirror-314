import os
import threading
from typing import Literal

from loguru import logger
from prompt_toolkit import prompt

from dspawpy import auto_test_cli
from dspawpy.cli import list_ds, pc
from dspawpy.cli.auxiliary import get_input, get_inputs, get_lims, save_figure_dpi300
from dspawpy.cli.menu_prompts import Dio, Dparameter, Dresponse, Dselect


def pre_ele_dos(language: Literal["EN", "CN"]):
    def imp():
        global DosPlotter, get_dos_data
        from pymatgen.electronic_structure.plotter import DosPlotter

        from dspawpy.io.read import get_dos_data

    import_thread = threading.Thread(target=imp)
    import_thread.start()

    D = {}
    D["inf"] = prompt(Dio[language]["dos"], completer=pc)
    D["xlims"] = get_lims(Dparameter[language][9], language)
    D["ylims"] = get_lims(Dparameter[language][10], language)
    D["shift"] = get_input(Dselect[language][3], ["y", "n"])
    D["figure"] = prompt(Dio[language]["figure"], completer=pc) or "dos.png"

    import_thread.join()
    logger.info(Dresponse[language][16])

    return D, DosPlotter, get_dos_data


def s5_1(language: Literal["EN", "CN"]) -> dict:
    """总的态密度"""

    if auto_test_cli:
        from pymatgen.electronic_structure.plotter import DosPlotter as cli_DosPlotter

        from dspawpy.io.read import get_dos_data as cli_get_dos_data

        for D in list_ds:
            if D["menu"] == 51:
                dos_data = cli_get_dos_data(D["inf"])
                logger.debug("got data, initializing plotter...")
                if D["shift"] == "y":
                    dos_plotter = cli_DosPlotter(stack=False, zero_at_efermi=True)
                else:
                    dos_plotter = cli_DosPlotter(stack=False, zero_at_efermi=True)
                dos_plotter.add_dos("total dos", dos=dos_data)
                dos_plotter.get_plot(xlim=D["xlims"], ylim=D["ylims"])
                save_figure_dpi300(D["figure"])

        D = {}
    else:
        D, DosPlotter, get_dos_data = pre_ele_dos(language)
        D["menu"] = 51
        dos_data = get_dos_data(D["inf"])
        logger.debug("got data, initializing plotter...")
        if D["shift"] == "y":
            dos_plotter = DosPlotter(stack=False, zero_at_efermi=True)
        else:
            dos_plotter = DosPlotter(stack=False, zero_at_efermi=True)
        logger.debug("plotter initialized")
        dos_plotter.add_dos("total dos", dos=dos_data)
        dos_plotter.get_plot(xlim=D["xlims"], ylim=D["ylims"])
        save_figure_dpi300(D["figure"])

    return D


def pre_ele_pdos(language: Literal["EN", "CN"]):
    def imp():
        global DosPlotter, get_dos_data, CompleteDos
        from pymatgen.electronic_structure.plotter import DosPlotter

        from dspawpy.io.read import get_dos_data

    import_thread = threading.Thread(target=imp)
    import_thread.start()

    D = {}
    D["inf"] = prompt(Dio[language]["pdos"], completer=pc)
    D["xlims"] = get_lims(Dparameter[language][9], language)
    D["ylims"] = get_lims(Dparameter[language][10], language)
    D["shift"] = get_input(Dselect[language][3], ["y", "n"])
    D["figure"] = prompt(Dio[language]["figure"], completer=pc) or "pdos.png"

    import_thread.join()
    logger.info(Dresponse[language][16])

    return D, DosPlotter, get_dos_data


def s5_2(language: Literal["EN", "CN"]) -> dict:
    """将态密度投影到不同的轨道上"""

    if auto_test_cli:
        from pymatgen.electronic_structure.plotter import DosPlotter as cli_DosPlotter

        from dspawpy.io.read import get_dos_data as cli_get_dos_data

        for D in list_ds:
            if D["menu"] == 52:
                dos_data = cli_get_dos_data(D["inf"])
                if D["shift"] == "y":
                    dos_plotter = cli_DosPlotter(stack=False, zero_at_efermi=True)
                else:
                    dos_plotter = cli_DosPlotter(stack=False, zero_at_efermi=True)
                dos_plotter.add_dos_dict(dos_data.get_spd_dos())  # type: ignore
                dos_plotter.get_plot(xlim=D["xlims"], ylim=D["ylims"])
                save_figure_dpi300(D["figure"])
        D = {}
    else:
        D, DosPlotter, get_dos_data = pre_ele_pdos(language)
        D["menu"] = 52
        dos_data = get_dos_data(D["inf"])
        logger.debug("got data, initializing plotter...")
        if D["shift"] == "y":
            dos_plotter = DosPlotter(stack=False, zero_at_efermi=True)
        else:
            dos_plotter = DosPlotter(stack=False, zero_at_efermi=True)
        logger.debug("plotter initialized")
        dos_plotter.add_dos_dict(dos_data.get_spd_dos())  # type: ignore
        dos_plotter.get_plot(xlim=D["xlims"], ylim=D["ylims"])
        save_figure_dpi300(D["figure"])

    return D


def s5_3(language: Literal["EN", "CN"]) -> dict:
    """将态密度投影到不同的元素上"""
    if auto_test_cli:
        from pymatgen.electronic_structure.plotter import DosPlotter as cli_DosPlotter

        from dspawpy.io.read import get_dos_data as cli_get_dos_data

        for D in list_ds:
            if D["menu"] == 52:
                dos_data = cli_get_dos_data(D["inf"])
                if D["shift"] == "y":
                    dos_plotter = cli_DosPlotter(stack=False, zero_at_efermi=True)
                else:
                    dos_plotter = cli_DosPlotter(stack=False, zero_at_efermi=True)
                dos_plotter.add_dos_dict(dos_data.get_element_dos())  # type: ignore
                dos_plotter.get_plot(xlim=D["xlims"], ylim=D["ylims"])
                save_figure_dpi300(D["figure"])
        D = {}
    else:
        D, DosPlotter, get_dos_data = pre_ele_pdos(language)
        D["menu"] = 53
        dos_data = get_dos_data(D["inf"])
        logger.debug("got data, initializing plotter...")
        if D["shift"] == "y":
            dos_plotter = DosPlotter(stack=False, zero_at_efermi=True)
        else:
            dos_plotter = DosPlotter(stack=False, zero_at_efermi=True)
        logger.debug("plotter initialized")
        dos_plotter.add_dos_dict(dos_data.get_element_dos())  # type: ignore
        dos_plotter.get_plot(xlim=D["xlims"], ylim=D["ylims"])
        save_figure_dpi300(D["figure"])

    return D


def s5_4(language: Literal["EN", "CN"]) -> dict:
    """将态密度投影到不同原子的不同轨道上"""
    if auto_test_cli:
        from pymatgen.electronic_structure.core import Orbital as cli_Orbital
        from pymatgen.electronic_structure.plotter import DosPlotter as cli_DosPlotter

        from dspawpy.io.read import get_dos_data as cli_get_dos_data

        for D in list_ds:
            if D["menu"] == 52:
                dos_data = cli_get_dos_data(D["inf"])
                if D["shift"] == "y":
                    dos_plotter = cli_DosPlotter(stack=False, zero_at_efermi=True)
                else:
                    dos_plotter = cli_DosPlotter(stack=False, zero_at_efermi=True)

                for _n, _os, _e in zip(D["ns"], D["oss"], D["es"]):
                    for _orb in _os:
                        logger.info(f"atom-{_n} {_orb}")
                        dos_plotter.add_dos(
                            f"{_e}(atom-{_n}) {_orb}",  # label
                            dos_data.get_site_orbital_dos(  # type: ignore
                                dos_data.structure[int(_n)],  # type: ignore
                                getattr(cli_Orbital, _orb),
                            ),
                        )
                dos_plotter.get_plot(xlim=D["xlims"], ylim=D["ylims"])
                save_figure_dpi300(D["figure"])
        D = {}
    else:

        def imp():
            global Orbital
            from pymatgen.electronic_structure.core import Orbital

        import_thread = threading.Thread(target=imp)
        import_thread.start()
        D, DosPlotter, get_dos_data = pre_ele_pdos(language)
        D["menu"] = 54
        dos_data = get_dos_data(D["inf"])
        logger.debug("got data, initializing plotter...")
        if D["shift"] == "y":
            dos_plotter = DosPlotter(stack=False, zero_at_efermi=True)
        else:
            dos_plotter = DosPlotter(stack=False, zero_at_efermi=True)
        logger.debug("plotter initialized")
        logger.info(dos_data.structure)  # type: ignore
        sites = dos_data.structure.sites  # type: ignore
        numbers = [str(i) for i in range(len(sites))]

        D["ns"] = []
        D["es"] = []
        D["oss"] = []
        _e = None
        while True:
            _n = get_input(Dselect[language][6], numbers, allow_empty=True)
            if _n == "":
                break
            available_orbitals = ["s"]
            _e = sites[int(_n)].specie
            orbitals = _e.atomic_orbitals
            assert isinstance(orbitals, dict)
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
            _os = get_inputs(Dselect[language][7], unique_orbitals)
            D["ns"].append(_n)
            D["oss"].append(_os)
            D["es"].append(_e)

        assert _e is not None
        import_thread.join()
        logger.info(Dresponse[language][16])
        for _n, _os, _e in zip(D["ns"], D["oss"], D["es"]):
            for _orb in _os:
                logger.info(f"atom-{_n} {_orb}")
                dos_plotter.add_dos(
                    f"{_e}(atom-{_n}) {_orb}",  # label
                    dos_data.get_site_orbital_dos(  # type: ignore
                        dos_data.structure[int(_n)],  # type: ignore
                        getattr(Orbital, _orb),
                    ),
                )
        dos_plotter.get_plot(xlim=D["xlims"], ylim=D["ylims"])
        save_figure_dpi300(D["figure"])

    return D


def s5_5(language: Literal["EN", "CN"]) -> dict:
    """将态密度投影到不同原子的分裂d轨道(t2g, eg)上"""
    if auto_test_cli:
        from pymatgen.electronic_structure.plotter import DosPlotter as cli_DosPlotter

        from dspawpy.io.read import get_dos_data as cli_get_dos_data

        for D in list_ds:
            if D["menu"] == 52:
                dos_data = cli_get_dos_data(D["inf"])
                if D["shift"] == "y":
                    dos_plotter = cli_DosPlotter(stack=False, zero_at_efermi=True)
                else:
                    dos_plotter = cli_DosPlotter(stack=False, zero_at_efermi=True)
                atom_indices = [int(ai) for ai in D["ais"].split()]
                for atom_index in atom_indices:
                    dos_plotter.add_dos_dict(
                        dos_data.get_site_t2g_eg_resolved_dos(  # type: ignore
                            dos_data.structure[atom_index]  # type: ignore
                        )
                    )

                dos_plotter.get_plot(xlim=D["xlims"], ylim=D["ylims"])
                save_figure_dpi300(D["figure"])
        D = {}
    else:
        D, DosPlotter, get_dos_data = pre_ele_pdos(language)
        D["menu"] = 55
        dos_data = get_dos_data(D["inf"])
        logger.debug("got data, initializing plotter...")
        if D["shift"] == "y":
            dos_plotter = DosPlotter(stack=False, zero_at_efermi=True)
        else:
            dos_plotter = DosPlotter(stack=False, zero_at_efermi=True)
        logger.debug("plotter initialized")
        logger.info(dos_data.structure)  # type: ignore
        sites = dos_data.structure.sites  # type: ignore
        numbers = [str(e) for e in range(len(sites))]
        D["ais"] = get_input(Dselect[language][6], numbers)

        atom_indices = [int(ai) for ai in D["ais"].split()]
        for atom_index in atom_indices:
            dos_plotter.add_dos_dict(  # type: ignore
                dos_data.get_site_t2g_eg_resolved_dos(dos_data.structure[atom_index]),  # type: ignore
            )

        dos_plotter.get_plot(xlim=D["xlims"], ylim=D["ylims"])
        save_figure_dpi300(D["figure"])

    return D


def s5_6(language: Literal["EN", "CN"]) -> dict:
    """d-带中心分析"""
    if auto_test_cli:
        from dspawpy.io.read import get_dos_data as cli_get_dos_data
        from dspawpy.io.utils import d_band as cli_d_band

        for D in list_ds:
            if D["menu"] == 56:
                dos_data = cli_get_dos_data(D["inf"])
                os.makedirs(
                    os.path.dirname(os.path.abspath(D["outfile"])), exist_ok=True
                )
                with open(D["outfile"], "w") as f:
                    for spin in dos_data.densities:
                        # up, down = (1, -1)
                        if spin.value == 1:
                            s = "up"
                        elif spin.value == -1:
                            s = "down"
                        else:
                            raise ValueError(f"Unknown spin: {spin}")
                        logger.info("spin=", s)
                        f.write(f"spin={s}\n")
                        c = cli_d_band(spin, dos_data)
                        f.write(str(c) + "\n")
                        logger.info(c)
        D = {}
    else:

        def imp():
            global get_dos_data, d_band

            from dspawpy.io.read import get_dos_data
            from dspawpy.io.utils import d_band

        import_thread = threading.Thread(target=imp)
        import_thread.start()
        D = {}
        D["menu"] = 56
        D["inf"] = prompt(Dio[language]["pdos"], completer=pc)
        D["outfile"] = prompt(Dio[language]["txt"], completer=pc)
        import_thread.join()
        logger.info(Dresponse[language][16])

        dos_data = get_dos_data(D["inf"])
        os.makedirs(os.path.dirname(os.path.abspath(D["outfile"])), exist_ok=True)
        with open(D["outfile"], "w") as f:
            for spin in dos_data.densities:
                # up, down = (1, -1)
                if spin.value == 1:
                    s = "up"
                elif spin.value == -1:
                    s = "down"
                else:
                    raise ValueError(f"Unknown spin: {spin}")
                logger.info("spin=", s)
                f.write(f"spin={s}\n")
                c = d_band(spin, dos_data)
                f.write(str(c) + "\n")
                logger.info(c)

    return D
