import threading
from typing import Literal

from loguru import logger
from prompt_toolkit import prompt

from dspawpy import auto_test_cli
from dspawpy.cli import list_ds, pc
from dspawpy.cli.auxiliary import get_input, get_lims
from dspawpy.cli.menu_prompts import Dio, Dparameter, Dresponse, Dselect


def s10_1(language: Literal["EN", "CN"]) -> dict:
    """轨迹文件转换格式为.xyz或.dump"""
    if auto_test_cli:
        from dspawpy.io.structure import convert as cli_convert

        for D in list_ds:
            if D["menu"] == 101:
                cli_convert(D["inf"], outfile=D["outf"])
        D = {}
    else:

        def imp():
            global convert
            from dspawpy.io.structure import convert

        import_thread = threading.Thread(target=imp)
        import_thread.start()
        D = {}
        D["menu"] = 101
        D["inf"] = prompt(Dio[language]["inf"], completer=pc)
        D["outf"] = prompt(Dio[language]["outf"], completer=pc)
        import_thread.join()
        logger.info(Dresponse[language][16])
        convert(D["inf"], outfile=D["outf"])
    return D


def s10_2(language: Literal["EN", "CN"]) -> dict:
    """动力学过程中能量、温度等变化曲线"""
    if auto_test_cli:
        from dspawpy.plot import plot_aimd as cli_plot_aimd

        for D in list_ds:
            if D["menu"] == 102:
                cli_plot_aimd(D["inf"], show=False, figname=D["figure"])
        D = {}

    else:

        def imp():
            global plot_aimd
            from dspawpy.plot import plot_aimd

        import_thread = threading.Thread(target=imp)
        import_thread.start()
        D = {}
        D["menu"] = 102
        D["inf"] = prompt(Dio[language]["inf"], completer=pc)
        D["figure"] = prompt(Dio[language]["figure"], completer=pc)
        import_thread.join()
        logger.info(Dresponse[language][16])
        plot_aimd(D["inf"], show=False, figname=D["figure"])

    return D


def s10_3(language: Literal["EN", "CN"]) -> dict:
    """均方位移（MSD）"""
    if auto_test_cli:
        import numpy as cli_np

        from dspawpy.analysis.aimdtools import (
            MSD as cli_MSD,
        )
        from dspawpy.analysis.aimdtools import (
            plot_msd as cli_plot_msd,
        )
        from dspawpy.io.structure import read as cli_read

        for D in list_ds:
            if D["menu"] == 103:
                structures = cli_read(D["inf"])
                msd_calculator = cli_MSD(structures, D["select"], D["msdtype"])
                msd = msd_calculator.run()

                ts = float(D["timestep"]) if D["timestep"] else 1.0
                xs = cli_np.arange(msd_calculator.n_frames) * ts
                cli_plot_msd(
                    xs, msd, D["xlims"], D["ylims"], figname=D["figure"], show=False
                )

        D = {}

    else:

        def imp():
            global MSD, _get_time_step, plot_msd, read, np
            import numpy as np

            from dspawpy.analysis.aimdtools import MSD, _get_time_step, plot_msd
            from dspawpy.io.structure import read

        import_thread = threading.Thread(target=imp)
        import_thread.start()
        D = {}
        D["menu"] = 103
        D["inf"] = prompt(Dio[language]["inf"], completer=pc)
        D["figure"] = prompt(Dio[language]["figure"], completer=pc)
        D["msdtype"] = (
            get_input(
                Dselect[language][12], ["xyz", "xy", "xz", "yz", "x", "y", "z", ""]
            )
            or "xyz"
        )
        if D["msdtype"] == "":
            D["msdtype"] = "xyz"

        D["timestep"] = input(Dparameter[language][0])
        D["xlims"] = get_lims(Dparameter[language][9], language)
        D["ylims"] = get_lims(Dparameter[language][10], language)

        import_thread.join()
        logger.info(Dresponse[language][16])
        structures = read(D["inf"])
        initial_structure = structures[0]
        logger.info(initial_structure)
        unique_elements = list(set(str(s) for s in initial_structure.species))
        unique_atomic_numbers = [str(i) for i in range(len(initial_structure.sites))]
        select_str = get_input(
            Dselect[language][8],
            unique_elements + unique_atomic_numbers + [""],
        )
        if select_str == "":
            D["select"] = "all"
        elif ":" in select_str:  # slice, '1:3', '1:3:2'
            D["select"] = select_str
        elif " " in select_str:  # list of symbols or atom indices, '1 2 3', 'H He Li'
            raw_list = select_str.split()
            if all([i.isdigit() for i in raw_list]):
                D["select"] = [int(i) for i in raw_list]
            elif all([i in unique_elements for i in raw_list]):
                D["select"] = raw_list
            else:
                raise ValueError(select_str)
        elif select_str in unique_elements:
            D["select"] = select_str  # symbol
        elif select_str.isdigit():
            D["select"] = int(select_str)  # atom index
        else:
            raise ValueError(select_str)

        logger.info(D["select"])

        if D["timestep"] == "":
            if isinstance(D["inf"], str) or len(D["inf"]) == 1:
                ts = _get_time_step(D["inf"])
            else:
                logger.warning(Dresponse[language][12])
                ts = 1.0
        else:
            ts = float(D["timestep"])

        msd_calculator = MSD(structures, D["select"], D["msdtype"])
        msd = msd_calculator.run()

        xs = np.arange(msd_calculator.n_frames) * ts
        plot_msd(xs, msd, D["xlims"], D["ylims"], figname=D["figure"], show=False)

    return D


def s10_4(language: Literal["EN", "CN"]) -> dict:
    """均方根偏差（RMSD）"""
    if auto_test_cli:
        from dspawpy.analysis.aimdtools import (
            get_lagtime_rmsd as cli_get_lagtime_rmsd,
        )
        from dspawpy.analysis.aimdtools import (
            plot_rmsd as cli_plot_rmsd,
        )

        for D in list_ds:
            if D["menu"] == 104:
                lagtime, rmsd = cli_get_lagtime_rmsd(D["inf"], D["timestep"] or None)
                cli_plot_rmsd(
                    lagtime,
                    rmsd,
                    D["xlims"],
                    D["ylims"],
                    figname=D["figure"],
                    show=False,
                )

        D = {}
    else:

        def imp():
            global get_lagtime_rmsd, plot_rmsd
            from dspawpy.analysis.aimdtools import get_lagtime_rmsd, plot_rmsd

        import_thread = threading.Thread(target=imp)
        import_thread.start()
        D = {}
        D["menu"] = 104
        D["inf"] = prompt(Dio[language]["inf"], completer=pc)
        D["figure"] = prompt(Dio[language]["figure"], completer=pc)
        D["timestep"] = input(Dparameter[language][0])
        if D["timestep"] == "":
            D["timestep"] = None
        else:
            D["timestep"] = float(D["timestep"])
        D["xlims"] = get_lims(Dparameter[language][9], language)
        D["ylims"] = get_lims(Dparameter[language][10], language)
        import_thread.join()
        logger.info(Dresponse[language][16])

        lagtime, rmsd = get_lagtime_rmsd(D["inf"], D["timestep"])
        plot_rmsd(lagtime, rmsd, D["xlims"], D["ylims"], D["figure"], False)
    return D


def s10_5(language: Literal["EN", "CN"]) -> dict:
    """径向分布函数（RDF）"""

    if auto_test_cli:
        from dspawpy.analysis.aimdtools import (
            get_rs_rdfs as cli_get_rs_rdfs,
        )
        from dspawpy.analysis.aimdtools import (
            plot_rdf as cli_plot_rdf,
        )

        for D in list_ds:
            if D["menu"] == 105:
                rs, rdfs = cli_get_rs_rdfs(
                    D["inf"],
                    D["ele1"],
                    D["ele2"],
                    D["rmin"],
                    D["rmax"],
                    D["ngrid"],
                    D["sigma"],
                )
                cli_plot_rdf(
                    rs,
                    rdfs,
                    D["ele1"],
                    D["ele2"],
                    D["xlims"],
                    D["ylims"],
                    figname=D["figure"],
                    show=False,
                )

        D = {}

    else:

        def imp():
            global get_rs_rdfs, plot_rdf, read
            from dspawpy.analysis.aimdtools import get_rs_rdfs, plot_rdf
            from dspawpy.io.structure import read

        import_thread = threading.Thread(target=imp)
        import_thread.start()
        D = {}
        D["menu"] = 105
        D["inf"] = prompt(Dio[language]["inf"], completer=pc)
        D["figure"] = prompt(Dio[language]["figure"], completer=pc)
        D["rmin"] = float(input(Dparameter[language][1]) or 0)
        D["rmax"] = float(input(Dparameter[language][2]) or 10)
        D["ngrid"] = int(input(Dparameter[language][3]) or 101)
        D["sigma"] = float(input(Dparameter[language][4]) or 0)
        D["xlims"] = [D["rmin"], D["rmax"]]
        D["ylims"] = get_lims(Dparameter[language][10], language)

        import_thread.join()
        logger.info(Dresponse[language][16])
        strs = read(datafile=D["inf"])
        logger.info(f"{strs[0]}")
        unique_elements = list(set([str(i) for i in strs[0].species]))
        ele1 = get_input(Dselect[language][13], unique_elements)
        ele2 = get_input(Dselect[language][14], unique_elements)
        rs, rdfs = get_rs_rdfs(
            D["inf"],
            ele1,
            ele2,
            D["rmin"],
            D["rmax"],
            D["ngrid"],
            D["sigma"],
        )
        plot_rdf(rs, rdfs, ele1, ele2, D["xlims"], D["ylims"], D["figure"], False)
    return D
