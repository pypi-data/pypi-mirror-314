import os
import threading
from typing import Literal

from loguru import logger
from prompt_toolkit import prompt

from dspawpy import auto_test_cli
from dspawpy.cli import list_ds, pc
from dspawpy.cli.auxiliary import get_input
from dspawpy.cli.menu_prompts import Dio, Dparameter, Dresponse, Dselect


def s8_1(language: Literal["EN", "CN"]) -> dict:
    """输入文件之生成中间构型"""

    if auto_test_cli:
        from dspawpy.diffusion.neb import (
            NEB as cli_NEB,
        )
        from dspawpy.diffusion.neb import (
            write_neb_structures as cli_write_neb_structures,
        )
        from dspawpy.io.structure import read as cli_read

        for D in list_ds:
            if D["menu"] == 81:
                init_struct = cli_read(D["inits"])[0]
                final_struct = cli_read(D["fins"])[0]

                neb = cli_NEB(init_struct, final_struct, D["nmiddle"] + 2)
                pbc = True if D["pbc"] == "y" else False
                if D["method"] == "Linear":
                    structures = neb.linear_interpolate(pbc)
                else:
                    try:
                        structures = neb.idpp_interpolate(pbc)
                    except Exception:
                        logger.error(Dresponse[language][7])
                        structures = neb.linear_interpolate(pbc)
                        logger.warning(Dresponse[language][8])

                absdir = os.path.abspath(D["outd"])
                os.makedirs(os.path.dirname(absdir), exist_ok=True)
                cli_write_neb_structures(structures, fmt="as", path=absdir)
                logger.info(f"{Dresponse[language][9]} {D['outd']}")

                yn = get_input(Dselect[language][10], ["y", "n"])
                if yn.lower().startswith("y"):
                    from dspawpy.diffusion.nebtools import (
                        write_json_chain as cli_write_json_chain,
                    )
                    from dspawpy.diffusion.nebtools import (
                        write_xyz_chain as cli_write_xyz_chain,
                    )

                    cli_write_xyz_chain(preview=True, directory=absdir)
                    cli_write_json_chain(preview=True, directory=absdir)
        D = {}
    else:

        def imp():
            global NEB, write_neb_structures, read

            from dspawpy.diffusion.neb import NEB, write_neb_structures
            from dspawpy.io.structure import read

        import_thread = threading.Thread(target=imp)
        import_thread.start()

        D = {}
        D["menu"] = 81
        D["inits"] = prompt(Dio[language]["inits"], completer=pc)
        D["fins"] = prompt(Dio[language]["fins"], completer=pc)
        D["nmiddle"] = int(input(Dparameter[language][8]))
        D["method"] = get_input(Dselect[language][9], ["IDPP", "Linear"])
        D["pbc"] = get_input(Dselect[language][24], ["y", "n"])
        pbc = True if D["pbc"] == "y" else False
        D["outd"] = prompt(Dio[language]["outd"], completer=pc)

        if D["outd"] == "":
            D["outd"] = "."

        import_thread.join()
        logger.info(Dresponse[language][16])
        init_struct = read(D["inits"])[0]
        final_struct = read(D["fins"])[0]

        neb = NEB(init_struct, final_struct, D["nmiddle"] + 2)
        if D["method"] == "Linear":
            structures = neb.linear_interpolate(pbc)
        else:
            try:
                structures = neb.idpp_interpolate(pbc)
            except Exception:
                logger.error(Dresponse[language][7])
                structures = neb.linear_interpolate(pbc)
                logger.warning(Dresponse[language][8])

        absdir = os.path.abspath(D["outd"])
        os.makedirs(os.path.dirname(absdir), exist_ok=True)
        write_neb_structures(structures, fmt="as", path=absdir)
        logger.info(f"{Dresponse[language][9]} {D['outd']}")

        yn = get_input(Dselect[language][10], ["y", "n"])
        if yn.lower().startswith("y"):
            from dspawpy.diffusion.nebtools import write_json_chain, write_xyz_chain

            write_xyz_chain(preview=True, directory=absdir)
            write_json_chain(preview=True, directory=absdir)

    return D


def s8_2(language: Literal["EN", "CN"]) -> dict:
    """绘制能垒图"""
    if auto_test_cli:
        from dspawpy.diffusion.nebtools import plot_barrier as cli_plot_barrier

        for D in list_ds:
            if D["menu"] == 82:
                if os.path.isdir(D["ind"]):
                    cli_plot_barrier(
                        directory=D["ind"], figname=D["figure"], show=False
                    )
                elif os.path.isfile(D["ind"]):
                    cli_plot_barrier(datafile=D["ind"], figname=D["figure"], show=False)
                else:
                    raise TypeError(D["inf"])
        D = {}
    else:

        def imp():
            global plot_barrier

            from dspawpy.diffusion.nebtools import plot_barrier

        import_thread = threading.Thread(target=imp)
        import_thread.start()
        D = {}
        D["menu"] = 82
        D["ind"] = prompt(Dio[language]["neb"], completer=pc)
        D["figure"] = prompt(Dio[language]["figure"], completer=pc)
        logger.info(Dresponse[language][10])
        import_thread.join()
        logger.info(Dresponse[language][16])

        if os.path.isdir(D["ind"]):
            plot_barrier(directory=D["ind"], figname=D["figure"], show=False)
        elif os.path.isfile(D["ind"]):
            plot_barrier(datafile=D["ind"], figname=D["figure"], show=False)
        else:
            raise TypeError(D["inf"])
    return D


def s8_3(language: Literal["EN", "CN"]) -> dict:
    """过渡态计算概览"""

    if auto_test_cli:
        from dspawpy.diffusion.nebtools import summary as cli_summary

        for D in list_ds:
            if D["menu"] == 83:
                absdir = os.path.abspath(D["outd"])
                os.makedirs(os.path.dirname(absdir), exist_ok=True)
                cli_summary(
                    directory=D["ind"],
                    outdir=absdir,
                    figname=f"{absdir}/neb_summary.png",
                    show=False,
                )

        D = {}
    else:

        def imp():
            global summary

            from dspawpy.diffusion.nebtools import summary

        import_thread = threading.Thread(target=imp)
        import_thread.start()
        D = {}
        D["menu"] = 82
        D["ind"] = prompt(Dio[language]["nebdir"], completer=pc)
        D["outd"] = prompt(Dio[language]["outd"], completer=pc)
        import_thread.join()
        logger.info(Dresponse[language][16])

        assert os.path.isdir(D["ind"])
        absdir = os.path.abspath(D["outd"])
        os.makedirs(os.path.dirname(absdir), exist_ok=True)
        summary(
            directory=D["ind"],
            outdir=absdir,
            figname=f"{absdir}/neb_summary.png",
            show=False,
        )
    return D


def s8_4(language: Literal["EN", "CN"]) -> dict:
    """NEB链可视化"""

    if auto_test_cli:
        from dspawpy.diffusion.nebtools import (
            write_json_chain as cli_write_json_chain,
        )
        from dspawpy.diffusion.nebtools import (
            write_xyz_chain as cli_write_xyz_chain,
        )

        for D in list_ds:
            if D["menu"] == 84:
                if D["yn"] == "y":
                    step = 0
                else:
                    step = int(input(Dselect[language][11]))
                cli_write_xyz_chain(False, D["ind"], step, D["dst"])
                cli_write_json_chain(False, D["ind"], step, D["dst"])
        D = {}
    else:

        def imp():
            global write_json_chain, write_xyz_chain
            from dspawpy.diffusion.nebtools import write_json_chain, write_xyz_chain

        import_thread = threading.Thread(target=imp)
        import_thread.start()
        D = {}
        D["menu"] = 84
        D["yn"] = get_input(Dselect[language][10], ["y", "n"])
        D["ind"] = prompt(Dio[language]["nebdir"], completer=pc)
        if D["yn"] == "y":
            step = 0
        else:
            step = int(input(Dselect[language][11]))
        D["dst"] = prompt(Dio[language]["outd"], completer=pc)
        import_thread.join()
        logger.info(Dresponse[language][16])

        write_xyz_chain(False, D["ind"], step, D["dst"])
        write_json_chain(False, D["ind"], step, D["dst"])
    return D


def s8_5(language: Literal["EN", "CN"]) -> dict:
    """计算构型间距"""
    if auto_test_cli:
        from dspawpy.diffusion.nebtools import get_distance as cli_get_distance
        from dspawpy.io.structure import read as cli_read

        for D in list_ds:
            if D["menu"] == 85:
                s1 = cli_read(D["infile1"])[0]
                s2 = cli_read(D["infile2"])[0]
                result = cli_get_distance(
                    s1.frac_coords,
                    s2.frac_coords,
                    s1.lattice.matrix,
                    s2.lattice.matrix,
                )
                logger.info(str(result))
        D = {}
    else:

        def imp():
            global read, get_distance
            from dspawpy.diffusion.nebtools import get_distance
            from dspawpy.io.structure import read

        import_thread = threading.Thread(target=imp)
        import_thread.start()
        D = {}
        D["menu"] = 85
        D["infile1"] = prompt(Dparameter[language][12], completer=pc)
        D["infile2"] = prompt(Dparameter[language][13], completer=pc)
        import_thread.join()
        logger.info(Dresponse[language][16])
        s1 = read(D["infile1"])[0]
        s2 = read(D["infile2"])[0]
        result = get_distance(
            s1.frac_coords,
            s2.frac_coords,
            s1.lattice.matrix,
            s2.lattice.matrix,
        )
        logger.info(str(result))
    return D


def s8_6(language: Literal["EN", "CN"]) -> dict:
    """neb续算"""

    if auto_test_cli:
        from dspawpy.diffusion.nebtools import restart as cli_restart

        for D in list_ds:
            if D["menu"] == 86:
                cli_restart(D["ind"], D["outd"])
        D = {}
    else:

        def imp():
            global restart
            from dspawpy.diffusion.nebtools import restart

        import_thread = threading.Thread(target=imp)
        import_thread.start()
        D = {}
        D["menu"] = 86
        D["ind"] = prompt(Dio[language]["neb"], completer=pc)
        D["outd"] = prompt(Dio[language]["outd"], completer=pc)
        import_thread.join()
        logger.info(Dresponse[language][16])
        restart(D["ind"], D["outd"])
    return D


def s8_7(language: Literal["EN", "CN"]) -> dict:
    """neb计算过程中受力和能量的收敛趋势图"""
    if auto_test_cli:
        from dspawpy.diffusion.nebtools import (
            monitor_force_energy as cli_monitor_force_energy,
        )

        for D in list_ds:
            if D["menu"] == 87:
                cli_monitor_force_energy(D["ind"], D["fig_dir"])
        D = {}
    else:

        def imp():
            global monitor_force_energy
            from dspawpy.diffusion.nebtools import monitor_force_energy

        import_thread = threading.Thread(target=imp)
        import_thread.start()
        D = {}
        D["menu"] = 87
        D["ind"] = prompt(Dio[language]["neb_can_be_unfinished"], completer=pc)
        D["fig_dir"] = prompt(Dio[language]["fig_dir"], completer=pc)
        import_thread.join()
        logger.info(Dresponse[language][16])
        monitor_force_energy(D["ind"], D["fig_dir"])

    return D
