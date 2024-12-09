import threading
from typing import Literal

from loguru import logger
from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter

from dspawpy import auto_test_cli
from dspawpy.cli import list_ds, pc
from dspawpy.cli.auxiliary import get_input, get_inputs, save_figure_dpi300
from dspawpy.cli.menu_prompts import Dio, Dresponse, Dselect


def s3_1(language: Literal["EN", "CN"]) -> dict:
    """volumetricData可视化"""
    if auto_test_cli:
        from dspawpy.io.write import write_VESTA as cli_write_VESTA

        for D in list_ds:
            if D["menu"] == 31:
                cli_write_VESTA(
                    in_filename=D["inf"],
                    data_type=D["task"],
                    out_filename=D["outfile"],
                    subtype=D["subtype"],
                )
        D = {}
    else:

        def imp():
            global write_VESTA
            from dspawpy.io.write import write_VESTA

        import_thread = threading.Thread(target=imp)
        import_thread.start()

        D = {}
        D["menu"] = 31
        D["inf"] = prompt(Dio[language]["inf"], completer=pc)
        supported_tasks = ["rho", "potential", "elf", "pcharge", "rhoBound"]
        D["task"] = None
        for task in supported_tasks:
            if task in D["inf"]:
                D["task"] = task
                break
        if not D["task"]:
            D["task"] = get_input(
                f"{supported_tasks}: ",
                supported_tasks,
                completer=WordCompleter(supported_tasks),
            )

        D["subtype"] = None
        if D["task"] == "potential":
            if D["inf"].endswith(".h5"):
                from dspawpy.io.read import load_h5

                data = load_h5(D["inf"])
                keys = [
                    k.split("/")[-1] for k in data.keys() if k.startswith("/Potential")
                ]

                if len(keys) == 0:
                    raise ValueError(f"{Dresponse[language][3]}{D['infile']}")
                elif len(keys) == 1:
                    D["subtype"] = keys[0]
                else:
                    D["subtype"] = get_input(
                        f"{Dselect[language][0]} {keys}: ",
                        keys,
                        completer=WordCompleter(keys),
                    )

            elif D["inf"].endswith(".json"):
                from json import load

                with open(D["inf"]) as fin:
                    data = load(fin)
                    if "Potential" not in data.keys():
                        raise ValueError(f"{Dresponse[language][3]} {D['infile']}")
                    keys = [k for k in data["Potential"].keys()]

                if len(keys) == 1:
                    D["subtype"] = keys[0]
                else:
                    D["subtype"] = get_input(
                        f"{Dselect[language][0]} {keys}",
                        keys,
                        completer=WordCompleter(keys),
                    )
            else:
                raise ValueError(Dresponse[language][2])

        D["outfile"] = prompt(Dio[language]["outf"], completer=pc)

        import_thread.join()
        logger.info(Dresponse[language][16])
        write_VESTA(  # type: ignore
            in_filename=D["inf"],
            data_type=D["task"],
            out_filename=D["outfile"],
            subtype=D["subtype"],
        )
        logger.info(Dresponse[language][5])

    return D


def s3_2(language: Literal["EN", "CN"]) -> dict:
    """差分volumetricData可视化"""

    if auto_test_cli:
        D = {}
        from dspawpy.io.write import write_delta_rho_vesta as cli_write_delta_rho_vesta

        for D in list_ds:
            if D["menu"] == 32:
                cli_write_delta_rho_vesta(
                    total=D["total"],
                    individuals=D["individuals"],
                    output=D["outfile"],
                    data_type=D["task"],
                )
    else:

        def imp():
            global write_delta_rho_vesta
            from dspawpy.io.write import write_delta_rho_vesta

        import_thread = threading.Thread(target=imp)
        import_thread.start()

        D = {}
        D["menu"] = 32
        D["total"] = prompt(Dio[language]["tcharge"], completer=pc)
        D["individuals"] = []
        while True:
            individual = prompt(
                Dio[language]["pcharge"],
                completer=pc,
            )
            if individual == "":
                break
            D["individuals"].append(individual)

        supported_tasks = ["rho", "potential", "elf", "pcharge", "rhoBound"]
        D["task"] = None
        for task in supported_tasks:
            if task in D["total"]:
                D["task"] = task
                break
        if not D["task"]:
            D["task"] = get_input(
                f"{supported_tasks}: ",
                supported_tasks,
                completer=WordCompleter(supported_tasks),
            )
        D["outfile"] = prompt(Dio[language]["outf"], completer=pc)

        import_thread.join()
        logger.info(Dresponse[language][16])
        write_delta_rho_vesta(
            total=D["total"],
            individuals=D["individuals"],
            output=D["outfile"],
            data_type=D["task"],
        )
        logger.info(Dresponse[language][5])

    return D


def s3_3(language: Literal["EN", "CN"]) -> dict:
    """volumetricData面平均"""
    if auto_test_cli:
        import matplotlib.pyplot as cli_plt

        from dspawpy.plot import average_along_axis as cli_average_along_axis

        D = {}
        for D in list_ds:
            if D["menu"] == 33:
                cli_plt = cli_average_along_axis(D["inf"], D["axes"])
                cli_plt.ylim(D["ylims"])
                save_figure_dpi300(D["figure"], cli_plt)
    else:

        def imp():
            global plt, average_along_axis

            import matplotlib.pyplot as plt

            from dspawpy.plot import average_along_axis

        import_thread = threading.Thread(target=imp)
        import_thread.start()

        D = {}
        D["menu"] = 33
        D["inf"] = prompt(Dio[language]["inf"], completer=pc)
        D["axes"] = get_inputs(Dselect[language][1], ["0", "1", "2"])
        _list = ["rho", "potential", "elf", "pcharge", "rhoBound"]
        D["task"] = get_input(
            f"{_list}: ",
            _list,
            completer=WordCompleter(_list),
        )

        D["subtype"] = None
        if D["task"] == "rho":
            k = "TotalCharge"
        elif D["task"] == "potential":
            if D["inf"].endswith(".h5"):
                from dspawpy.io.read import load_h5

                data = load_h5(D["inf"])
                keys = [
                    k.split("/")[-1] for k in data.keys() if k.startswith("/Potential")
                ]

                if len(keys) == 0:
                    raise ValueError(f"{Dresponse[language][3]}{D['infile']}")
                elif len(keys) == 1:
                    D["subtype"] = keys[0]
                else:
                    D["subtype"] = get_input(
                        Dselect[language][0],
                        keys,
                        completer=WordCompleter(keys),
                    )

            elif D["inf"].endswith(".json"):
                from json import load

                with open(D["inf"]) as fin:
                    data = load(fin)
                    if "Potential" not in data.keys():
                        raise ValueError(f"{Dresponse[language][3]}{D['infile']}")
                    keys = [k for k in data["Potential"].keys()]

                if len(keys) == 1:
                    D["subtype"] = keys[0]
                else:
                    D["subtype"] = get_input(
                        Dselect[language][0],
                        keys,
                        completer=WordCompleter(keys),
                    )
            else:
                raise ValueError(Dresponse[language][4])
            k = D["subtype"]
        elif D["task"] == "elf":
            k = "TotalELF"
        elif D["task"] == "pcharge":
            k = "TotalCharge"
        elif D["task"] == "rhoBound":
            k = "Rho"
        else:
            raise ValueError(D["task"])

        ax_indices = [int(a) for a in D["axes"]]
        import_thread.join()
        logger.info(Dresponse[language][16])
        for ai in ax_indices:
            average_along_axis(
                datafile=D["inf"],
                task=D["task"],
                axis=ai,
                subtype=D["subtype"],
                label=f"axis{ai}",
            )
        if len(ax_indices) > 1:
            plt.legend()

        plt.xlabel("Grid Index")
        plt.ylabel(k)
        D["figure"] = prompt(Dio[language]["figure"], completer=pc)

        save_figure_dpi300(D["figure"], plt)

    return D
