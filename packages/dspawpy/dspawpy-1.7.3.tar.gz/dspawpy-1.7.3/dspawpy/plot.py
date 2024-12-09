from typing import TYPE_CHECKING, List, Optional, Tuple, cast

from loguru import logger

if TYPE_CHECKING:
    from pymatgen.electronic_structure.bandstructure import BandStructureSymmLine
    from pymatgen.electronic_structure.dos import CompleteDos
    from pymatgen.electronic_structure.plotter import BSDOSPlotter


def average_along_axis(
    datafile: str = "potential.h5",
    task: str = "potential",
    axis: int = 2,
    smooth: bool = False,
    smooth_frac: float = 0.8,
    raw: bool = False,
    subtype: Optional[str] = None,
    verbose: bool = False,
    **kwargs,
):
    r"""绘制沿着某个轴向的物理量平均值曲线

    Parameters
    ----------
    datafile:
        h5或json文件路径或包含任意这些文件的文件夹，默认 'potential.h5'
    task:
        任务类型，可以是 'rho', 'potential', 'elf', 'pcharge', 'rhoBound'
    axis:
        沿着哪个轴向绘制势能曲线, 默认2
    smooth:
        是否平滑, 默认False
    smooth_frac:
        平滑系数, 默认0.8
    raw:
        是否返回绘图数据到csv文件
    subtype:
        用于指定task数据子类，默认None，代表绘制 Potential/TotalElectrostaticPotential
    **kwargs:
        其他参数, 传递给 matplotlib.pyplot.plot

    Returns
    -------
    axes:
        可传递给其他函数进行进一步处理

    Examples
    --------
    >>> from dspawpy.plot import average_along_axis

    读取 potential.h5 文件中的数据，绘图并保存原始绘图数据到csv文件

    >>> plt = average_along_axis(datafile='dspawpy_proj/dspawpy_tests/inputs/3.3/rho.h5', task='rho', axis=2, smooth=True, smooth_frac=0.8) # doctest: +ELLIPSIS
    >>> plt.savefig('dspawpy_proj/dspawpy_tests/outputs/doctest/rho_h5.png')
    >>> plt = average_along_axis(datafile='dspawpy_proj/dspawpy_tests/inputs/3.3/rho.json', task='rho', axis=2, smooth=True, smooth_frac=0.8) # doctest: +ELLIPSIS
    >>> plt.savefig('dspawpy_proj/dspawpy_tests/outputs/doctest/rho_json.png')

    >>> plt = average_along_axis(datafile='dspawpy_proj/dspawpy_tests/inputs/2.7/potential.h5', task='potential', axis=2, smooth=True, smooth_frac=0.8, raw=True) # doctest: +ELLIPSIS
    >>> plt.savefig('dspawpy_proj/dspawpy_tests/outputs/doctest/potential_h5.png')
    >>> plt = average_along_axis(datafile='dspawpy_proj/dspawpy_tests/inputs/2.7/potential.json', task='potential', axis=2, smooth=True, smooth_frac=0.8) # doctest: +ELLIPSIS
    >>> plt.savefig('dspawpy_proj/dspawpy_tests/outputs/doctest/potential_json.png')

    >>> plt = average_along_axis(datafile='dspawpy_proj/dspawpy_tests/inputs/2.8/elf.h5', task='elf', axis=2, smooth=True, smooth_frac=0.8) # doctest: +ELLIPSIS
    >>> plt.savefig('dspawpy_proj/dspawpy_tests/outputs/doctest/elf_h5.png')
    >>> plt = average_along_axis(datafile='dspawpy_proj/dspawpy_tests/inputs/2.8/elf.json', task='elf', axis=2, smooth=True, smooth_frac=0.8) # doctest: +ELLIPSIS
    >>> plt.savefig('dspawpy_proj/dspawpy_tests/outputs/doctest/elf_json.png')

    >>> plt = average_along_axis(datafile='dspawpy_proj/dspawpy_tests/inputs/2.9/pcharge.h5', task='pcharge', axis=2, smooth=True, smooth_frac=0.8) # doctest: +ELLIPSIS
    >>> plt.savefig('dspawpy_proj/dspawpy_tests/outputs/doctest/pcharge_h5.png')
    >>> plt = average_along_axis(datafile='dspawpy_proj/dspawpy_tests/inputs/2.9/pcharge.json', task='pcharge', axis=2, smooth=True, smooth_frac=0.8) # doctest: +ELLIPSIS
    >>> plt.savefig('dspawpy_proj/dspawpy_tests/outputs/doctest/pcharge_json.png')

    >>> plt = average_along_axis(datafile='dspawpy_proj/dspawpy_tests/inputs/2.28/rhoBound.h5', task='rhoBound', axis=2, smooth=True, smooth_frac=0.8) # doctest: +ELLIPSIS
    >>> plt.savefig('dspawpy_proj/dspawpy_tests/outputs/doctest/rhoBound_h5.png')
    >>> plt = average_along_axis(datafile='dspawpy_proj/dspawpy_tests/inputs/2.28/rhoBound.json', task='rhoBound', axis=2, smooth=True, smooth_frac=0.8) # doctest: +ELLIPSIS
    >>> plt.savefig('dspawpy_proj/dspawpy_tests/outputs/doctest/rhoBound_json.png')

    """
    assert task in [
        "rho",
        "potential",
        "elf",
        "pcharge",
        "rhoBound",
    ], "Only support: rho, potential, elf, pcharge, rhoBound"

    # only for compatibility
    import numpy as np

    if isinstance(datafile, (list, np.ndarray)):
        ys = datafile  # expect np.ndarray or list
    else:
        from dspawpy.io.utils import get_absfile

        absfile = get_absfile(datafile, task, verbose=verbose)

        if absfile.endswith(".h5"):
            hfile = absfile
            from dspawpy.io.read import load_h5

            hdict = load_h5(hfile)
            grid = hdict["/AtomInfo/Grid"]

            if task == "rho":
                if subtype is None:
                    subtype = "TotalCharge"
                _key = f"/Rho/{subtype}"
            elif task == "potential":
                if subtype is None:
                    if "/Potential/TotalElectrostaticPotential" in hdict:
                        subtype = "TotalElectrostaticPotential"
                    elif "/Potential/TotalLocalPotential" in hdict:
                        subtype = "TotalLocalPotential"
                    else:
                        raise KeyError(
                            f"Neither TotalElectrostaticPotential nor TotalLocalPotential can be found, please check your {absfile}",
                        )
                _key = f"/Potential/{subtype}"
            elif task == "elf":
                if subtype is None:
                    subtype = "TotalELF"
                _key = f"/ELF/{subtype}"
            elif task == "pcharge":
                if subtype is None:
                    subtype = "TotalCharge"
                _key = f"/Pcharge/1/{subtype}"
            elif task == "rhoBound":
                if subtype is None:
                    subtype = "TotalCharge"
                _key = f"/Rho/{subtype}"
            else:
                raise ValueError("Only support rho, potential, elf, pcharge, rhoBound")

            if _key not in hdict:
                raise KeyError(f"No {_key} key")

            tmp_pot = np.asarray(hdict[_key]).reshape([-1, 1], order="C")
            ys = tmp_pot.reshape(grid, order="F")

        elif absfile.endswith(".json"):
            jfile = absfile
            with open(jfile) as f:
                from json import load

                jdict = load(f)
            grid = jdict["AtomInfo"]["Grid"]

            if task == "rho":
                if subtype is None:
                    subtype = "TotalCharge"
                ys = np.asarray(jdict["Rho"][subtype]).reshape(grid, order="F")
            elif task == "potential":
                if subtype is None:
                    if "TotalElectrostaticPotential" in jdict["Potential"]:
                        subtype = "TotalElectrostaticPotential"
                    elif "TotalLocalPotential" in jdict["Potential"]:
                        subtype = "TotalLocalPotential"
                    else:
                        raise KeyError(
                            f"Neither TotalElectrostaticPotential nor TotalLocalPotential can be found, please check your {absfile}",
                        )

                ys = np.asarray(jdict["Potential"][subtype]).reshape(grid, order="F")
            elif task == "elf":
                if subtype is None:
                    subtype = "TotalELF"
                ys = np.asarray(jdict["ELF"][subtype]).reshape(grid, order="F")
            elif task == "pcharge":
                if subtype is None:
                    subtype = "TotalCharge"
                ys = np.asarray(jdict["Pcharge"][0][subtype]).reshape(grid, order="F")
            else:
                if subtype is None:
                    subtype = "TotalCharge"
                ys = np.asarray(jdict["Rho"][subtype]).reshape(grid, order="F")

        else:
            raise TypeError("Only support h5/json file")

    all_axis = [0, 1, 2]
    all_axis.remove(axis)
    y = np.mean(ys, tuple(all_axis))  # type: ignore
    x = np.arange(len(y))

    import matplotlib.pyplot as plt

    if raw:
        import polars as pl

        pl.DataFrame({"x": x, "y": y}).write_csv(
            f"raw{task}_axis{axis}.csv",
        )
    if smooth:
        import statsmodels.api as sm

        s = sm.nonparametric.lowess(y, x, frac=smooth_frac)
        if raw:
            import polars as pl

            pl.DataFrame({"x": s[:, 0], "y": s[:, 1]}).write_csv(
                f"raw{task}_axis{axis}_smooth.csv",
            )

        plt.plot(s[:, 0], s[:, 1], label="macroscopic average", **kwargs)

    plt.plot(x, y, **kwargs)

    return plt


def plot_aimd(
    datafile: str = "aimd.h5",
    show: bool = True,
    figname: str = "aimd.png",
    flags_str: str = "12345",
    raw: bool = False,
):
    r"""AIMD任务完成后，绘制关键物理量的收敛过程图

    aimd.h5 -> aimd.png

    Parameters
    ----------
    datafile:
        h5文件位置. 例如 'aimd.h5' 或 ['aimd.h5', 'aimd2.h5']
    show:
        是否展示交互界面. 默认 False
    figname:
        保存的图片路径. 默认 'aimd.h5'
    flags_str:
        子图编号.
        1. 动能
        2. 总能
        3. 压力
        4. 温度
        5. 体积
    raw:
        是否输出绘图数据到csv文件

    Returns
    -------
    figname:
        图片路径，默认 'aimd.png'

    Examples
    --------
    >>> from dspawpy.plot import plot_aimd

    读取 aimd.h5 文件内容，画出动能、总能、温度、体积的收敛过程图，并保存相应数据到 rawaimd_*.csv 中

    >>> plot_aimd(datafile='dspawpy_proj/dspawpy_tests/inputs/2.18/aimd.h5', flags_str='1 2 3 4 5', raw=True, show=False, figname="dspawpy_proj/dspawpy_tests/outputs/doctest/aimdconv.png")
    >>> plot_aimd(datafile='dspawpy_proj/dspawpy_tests/inputs/2.18/aimd.json', flags_str='1 2 3 4 5', show=False, figname="dspawpy_proj/dspawpy_tests/outputs/doctest/aimdconv_json.png")

    """
    # 处理用户读取，按顺序去重
    temp = set()
    flags = [x for x in flags_str if x not in temp and (temp.add(x) or True)]
    if " " in flags:  # remove space
        flags.remove(" ")

    for flag in flags:
        assert flag in ["1", "2", "3", "4", "5"], "flag must be in '12345'"

    if datafile.endswith("json"):
        # delete 3 from flags
        flags = [f for f in flags if f != "3"]
        logger.warning(
            "PressureKinetic array is not written in json file, so dspawapy can not read it!\nYou may try aimd.h5 file, which contains that info",
        )

    # 开始画组合图
    N_figs = len(flags)
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(N_figs, 1, sharex=True, figsize=(6, 2 * N_figs))
    if N_figs == 1:  # 'AxesSubplot' object is not subscriptable
        axes = [axes]  # 避免上述类型错误
    fig.suptitle("DSPAW AIMD")

    for i, flag in enumerate(flags):
        # 读取数据
        if i == 0:
            xs, ys = _read_aimd_converge_data(datafile, flag, verbose=True)
        else:
            xs, ys = _read_aimd_converge_data(datafile, flag, verbose=False)
        logger.info("For subfigure " + flag)

        if raw:
            import polars as pl

            pl.DataFrame({"x": xs, "y": ys}).write_csv(
                f"rawaimd_{flag}.csv",
            )

        axes[i].plot(xs, ys)  # 绘制坐标点
        # 子图的y轴标签
        if flag == "1":
            axes[i].set_ylabel("Kinetic Energy (eV)")
        elif flag == "2":
            axes[i].set_ylabel("Energy (eV)")
        elif flag == "3":
            axes[i].set_ylabel("Pressure Kinetic (kbar)")
        elif flag == "4":
            axes[i].set_ylabel("Temperature (K)")
        else:
            axes[i].set_ylabel("Volume (Angstrom^3)")

    plt.tight_layout()
    # save and show
    if figname:
        import os

        absfig = os.path.abspath(figname)
        os.makedirs(os.path.dirname(absfig), exist_ok=True)
        plt.savefig(absfig, dpi=300)
        logger.info(f"==> {absfig}")
    if show:
        plt.show()


def plot_bandunfolding(
    datafile: str = "band.h5",
    ef: Optional[float] = None,
    de: float = 0.05,
    dele: float = 0.06,
    raw: bool = False,
    verbose: bool = False,
):
    r"""能带反折叠任务完成后，读取 h5 或 json 文件数据绘图

    band.h5/band.json -> bandunfolding.png

    Parameters
    ----------
    datafile:
        h5或json文件路径或包含任意这些文件的文件夹，默认 'band.h5'
    ef:
        费米能级，默认从文件中读取 /UnfoldingBandInfo/Efermi 记录的数据
    de:
        能带宽度，默认0.05
    dele:
        能带间隔，默认0.06
    raw:
        是否输出绘图数据到rawbandunfolding.csv

    Returns
    -------
    axes: matplotlib.axes._subplots.AxesSubplot
        可传递给其他函数进行进一步处理

    Examples
    --------
    绘图并保存绘图数据到rawbandunfolding.csv

    >>> from dspawpy.plot import plot_bandunfolding
    >>> plt = plot_bandunfolding("dspawpy_proj/dspawpy_tests/inputs/2.22/band.h5", raw=True)
    >>> plt.savefig('dspawpy_proj/dspawpy_tests/outputs/doctest/bandunfolding_h5.png')
    >>> plt = plot_bandunfolding("dspawpy_proj/dspawpy_tests/inputs/2.22/band.json")
    >>> plt.savefig('dspawpy_proj/dspawpy_tests/outputs/doctest/bandunfolding_json.png')

    """
    from dspawpy.io.utils import get_absfile

    absfile = get_absfile(datafile, task="band", verbose=verbose)
    import numpy as np

    if absfile.endswith(".h5"):
        from h5py import File

        f = File(absfile, "r")
        if ef is None:
            ef = np.asarray(f["/UnfoldingBandInfo/EFermi"])[0]
        number_of_band = np.asarray(f["/BandInfo/NumberOfBand"])[0]
        number_of_kpoints = np.asarray(f["/BandInfo/NumberOfKpoints"])[0]
        data = np.asarray(f["/UnfoldingBandInfo/Spin1/UnfoldingBand"])
        weight = np.asarray(f["/UnfoldingBandInfo/Spin1/Weight"])
    elif absfile.endswith(".json"):
        with open(absfile) as f:
            from json import load

            band = load(f)
        if ef is None:
            ef = band["UnfoldingBandInfo"]["EFermi"]
        number_of_band = band["BandInfo"]["NumberOfBand"]
        number_of_kpoints = band["BandInfo"]["NumberOfKpoints"]
        data = band["UnfoldingBandInfo"]["Spin1"]["UnfoldingBand"]
        weight = band["UnfoldingBandInfo"]["Spin1"]["Weight"]
    else:
        raise TypeError("Only support h5/json file")

    celtot = np.asarray(data).reshape((number_of_kpoints, number_of_band)).T
    proj_wt = np.asarray(weight).reshape((number_of_kpoints, number_of_band)).T
    X2, Y2, Z2, emin = getEwtData(
        number_of_kpoints,
        number_of_band,
        celtot,
        proj_wt,
        ef,
        de,
        dele,
    )

    if raw:
        import polars as pl

        pl.DataFrame({"Y": Y2, "Z": Z2}).write_csv("rawbandunfolding.csv")

    import matplotlib.pyplot as plt

    plt.clf()
    plt.scatter(X2, Y2, c=Z2, cmap="hot")
    plt.xlim(0, 200)
    plt.ylim(emin - 0.5, 15)
    ax = plt.gca()
    plt.colorbar()
    ax.set_facecolor("black")

    return plt


def plot_optical(
    datafile: str = "optical.h5",
    keys: List[str] = [
        "AbsorptionCoefficient",
        "ExtinctionCoefficient",
        "RefractiveIndex",
        "Reflectance",
    ],
    axes: List[str] = ["X", "Y", "Z", "XY", "YZ", "ZX"],
    raw: bool = False,
    prefix: str = "",
    save: bool = True,
    verbose: bool = False,
):
    """光学性质计算任务完成后，读取数据并绘制预览图

    optical.h5/optical.json -> optical.png

    Parameters
    ----------
    datafile:
        h5或json文件路径或包含任意这些文件的文件夹，默认 'optical.h5'
    keys:
        可选 "AbsorptionCoefficient", "ExtinctionCoefficient", "RefractiveIndex", "Reflectance" 中的任意一个，默认 "AbsorptionCoefficient"
    axes:
        序号，默认"X", "Y", "Z", "XY", "YZ", "ZX"
    raw:
        是否保存绘图数据到csv
    prefix:
        保存图片的文件夹路径，若留空则保存在当前目录
    save:
        是否保存图片，默认True

    Examples
    --------
    绘图并保存绘图数据到rawoptical.csv

    >>> from dspawpy.plot import plot_optical
    >>> plot_optical("dspawpy_proj/dspawpy_tests/inputs/2.12/scf.h5", "AbsorptionCoefficient", ['X', 'Y'], prefix='dspawpy_proj/dspawpy_tests/outputs/doctest')
    >>> plot_optical("dspawpy_proj/dspawpy_tests/inputs/2.12/optical.json", ["AbsorptionCoefficient"], ['X', 'Y'], prefix='dspawpy_proj/dspawpy_tests/outputs/doctest', raw=True)

    """
    import matplotlib.pyplot as plt
    import numpy as np
    from scipy.interpolate import interp1d

    from dspawpy.io.utils import get_absfile

    if isinstance(keys, str):
        keys = [keys]

    absfile = get_absfile(datafile, task="optical", verbose=verbose)
    data = {}
    if absfile.endswith("h5"):
        from dspawpy.io.read import load_h5

        data_all = load_h5(absfile)
        energy = data_all["/OpticalInfo/EnergyAxe"]
        for k in keys:
            data[k] = data_all["/OpticalInfo/" + k]
    elif absfile.endswith("json"):
        with open(absfile) as fin:
            from json import load

            data_all = load(fin)
        energy = data_all["OpticalInfo"]["EnergyAxe"]
        for k in keys:
            data[k] = data_all["OpticalInfo"][k]
    else:
        raise TypeError("Only support h5/json file")

    energy_spline = np.linspace(energy[0], energy[-1], 2001)
    dd = {"X": 0, "Y": 1, "Z": 2, "XY": 3, "YZ": 4, "ZX": 5}
    data_spline_dict = {}

    for k, v in data.items():
        if save:
            plt.clf()
            # plt.ylabel(k + r" $\alpha (\omega )(cm^{-1})$", fontsize=14)
            plt.ylabel(k, fontsize=14)
        else:
            plt.ylabel("Properties", fontsize=14)
        plt.xlabel("Photon energy (eV)", fontsize=14)
        # TODO: unit
        for a in axes:
            d = np.asarray(v).reshape(len(energy), 6)[:, dd[a]]
            inter_f = interp1d(energy, d, kind="cubic")
            data_spline = inter_f(energy_spline)
            if save:
                plt.plot(energy_spline, data_spline, label=a)
            else:
                plt.plot(energy_spline, data_spline, label=" ".join([k, a]))
            data_spline_dict.update({k + a: data_spline})
        plt.legend()
        if save:
            if prefix:
                import os

                os.makedirs(prefix, exist_ok=True)
                plt.savefig(f"{prefix}/{k}.png")
            else:
                plt.savefig(f"{k}.png")

    if raw:
        import polars as pl

        for k in data:
            dictOriginal = {"energy": energy}
            dictInterp = {"energy": energy_spline}
            for a in axes:
                dictOriginal.update(
                    {k + a: np.asarray(data[k]).reshape(len(energy), 6)[:, dd[a]]},
                )
                dictInterp.update({k + a: data_spline_dict[k + a]})
            pl.DataFrame(dictOriginal).write_csv(
                f"rawoptical{k}.csv",
            )
            pl.DataFrame(dictInterp).write_csv(
                f"rawoptical_spline{k}.csv",
            )


def plot_phonon_thermal(
    datafile: str = "phonon.h5",
    figname: str = "phonon.png",
    show: bool = True,
    raw: bool = False,
    verbose: bool = False,
):
    """声子热力学计算任务完成后，绘制相关物理量随温度变化曲线

    phonon.h5/phonon.json -> phonon.png

    Parameters
    ----------
    datafile:
        h5或json文件路径或包含任意这些文件的文件夹，默认 'phonon.h5'
    figname:
        保存图片的文件名
    show:
        是否弹出交互界面
    raw:
        是否保存绘图数据到rawphonon.csv文件

    Returns
    -------
    figname:
        图片路径，默认 'phonon.png'

    Examples
    --------
    >>> from dspawpy.plot import plot_phonon_thermal
    >>> plot_phonon_thermal('dspawpy_proj/dspawpy_tests/inputs/2.26/phonon.h5', figname='dspawpy_proj/dspawpy_tests/outputs/doctest/phonon_thermal_h5.png', show=False)
    >>> plot_phonon_thermal('dspawpy_proj/dspawpy_tests/inputs/2.26/phonon.json', figname='dspawpy_proj/dspawpy_tests/outputs/doctest/phonon_thermal_json.png', show=False, raw=True)

    """
    from dspawpy.io.utils import get_absfile

    absfile = get_absfile(datafile, task="phonon", verbose=verbose)

    import numpy as np

    if absfile.endswith(".h5"):
        hfile = absfile
        from h5py import File

        ph = File(hfile, "r")
        if "/ThermalInfo/Temperatures" not in ph:
            raise KeyError(
                f"No thermal info in {absfile}, you probably gave a wrong phonon.h5 file",
            )
        temp = np.asarray(ph["/ThermalInfo/Temperatures"])
        entropy = np.asarray(ph["/ThermalInfo/Entropy"])
        heat_capacity = np.asarray(ph["/ThermalInfo/HeatCapacity"])
        helmholts_free_energy = np.asarray(ph["/ThermalInfo/HelmholtzFreeEnergy"])
    elif absfile.endswith(".json"):
        jfile = absfile
        with open(jfile) as f:
            from json import load

            data = load(f)
        temp = np.asarray(data["ThermalInfo"]["Temperatures"])
        entropy = np.asarray(data["ThermalInfo"]["Entropy"])
        heat_capacity = np.asarray(data["ThermalInfo"]["HeatCapacity"])
        helmholts_free_energy = np.asarray(data["ThermalInfo"]["HelmholtzFreeEnergy"])
    else:
        raise TypeError("Only support h5/json file")

    if raw:
        import polars as pl

        pl.DataFrame(
            {
                "temp": temp,
                "entropy": entropy,
                "heat_capacity": heat_capacity,
                "helmholts_free_energy": helmholts_free_energy,
            },
        ).write_csv(
            "rawphonon.csv",
        )

    import matplotlib.pyplot as plt

    plt.plot(temp, entropy, c="red", label="Entropy (J/K/mol)")
    plt.plot(temp, heat_capacity, c="green", label="Heat Capacity (J/K/mol)")
    plt.plot(
        temp,
        helmholts_free_energy,
        c="blue",
        label="Helmholtz Free Energy (kJ/mol)",
    )
    plt.xlabel("Temperature(K)")
    plt.ylabel("Thermal Properties")
    plt.tick_params(direction="in")  # 刻度线朝内
    plt.grid(alpha=0.2)
    plt.legend()
    plt.title("Thermal")

    plt.tight_layout()
    # save and show
    if figname:
        import os

        absfig = os.path.abspath(figname)
        os.makedirs(os.path.dirname(absfig), exist_ok=True)
        plt.savefig(absfig, dpi=300)
        logger.info(f"==> {absfig}")
    if show:
        plt.show()


def plot_polarization_figure(
    directory: str,
    repetition: int = 2,
    annotation: bool = False,
    annotation_style: int = 1,
    show: bool = True,
    figname: str = "pol.png",
    raw: bool = False,
):
    """绘制铁电极化结果图

    Parameters
    ----------
    directory:
        铁电极化计算任务主目录
    repetition:
        沿上（或下）方向重复绘制的次数, 默认 2
    annotation:
        是否显示首尾构型的铁电极化数值, 默认显示
    show:
        是否交互显示图片, 默认 True
    figname:
        图片保存路径, 默认 'pol.png'
    raw:
        是否将原始数据保存到csv文件

    Returns
    -------
    axes: matplotlib.axes._subplots.AxesSubplot
        可传递给其他函数进行进一步处理

    Examples
    --------
    >>> from dspawpy.plot import plot_polarization_figure
    >>> result = plot_polarization_figure(directory='dspawpy_proj/dspawpy_tests/inputs/2.20', figname='dspawpy_proj/dspawpy_tests/outputs/doctest/pol1.png', show=False, annotation=True, annotation_style=1)
    >>> result = plot_polarization_figure(directory='dspawpy_proj/dspawpy_tests/inputs/2.20', figname='dspawpy_proj/dspawpy_tests/outputs/doctest/pol2.png', show=False, annotation=True, annotation_style=2)

    """
    assert repetition >= 0, "The number of repetitions must be a natural number"
    subfolders, quantum, totals = _get_subfolders_quantum_totals(directory)
    number_sfs = [int(sf) for sf in subfolders]
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 3, sharey=True)
    xyz = ["x", "y", "z"]
    import numpy as np

    for j in range(3):  # x, y, z
        ys = np.empty(shape=(len(subfolders), repetition * 2 + 1))
        for r in range(repetition + 1):
            ys[:, repetition - r] = totals[:, j] - quantum[j] * r
            ys[:, repetition + r] = totals[:, j] + quantum[j] * r

        axes[j].plot(number_sfs, ys, ".")  # plot
        axes[j].set_title("P%s" % xyz[j])
        axes[j].xaxis.set_ticks(number_sfs)  # 设置x轴刻度
        axes[j].set_xticklabels(labels=subfolders, rotation=90)
        axes[j].grid(axis="x", color="gray", linestyle=":", linewidth=0.5)
        axes[j].tick_params(direction="in")
        # set y ticks using the first and last values
        if annotation:
            if annotation_style == 2:
                style = "arc,angleA=-0,angleB=0,armA=-10,armB=0,rad=0"
                for i in range(repetition * 2 + 1):
                    axes[j].annotate(
                        "%.2f" % ys[0, i],
                        xy=(number_sfs[0], ys[0, i]),
                        xycoords="data",
                        xytext=(number_sfs[-1] + 2, ys[0, i] - 8),
                        textcoords="data",
                        arrowprops=dict(
                            arrowstyle="->",
                            color="black",
                            linewidth=0.75,
                            shrinkA=2,
                            shrinkB=1,
                            connectionstyle=style,
                        ),
                    )
                    axes[j].annotate(
                        "%.2f" % ys[-1, i],
                        xy=(number_sfs[-1], ys[-1, i]),
                        xycoords="data",
                        xytext=(number_sfs[-1] + 2, ys[-1, i] + 8),
                        textcoords="data",
                        arrowprops=dict(
                            arrowstyle="->",
                            color="black",
                            linewidth=0.75,
                            shrinkA=2,
                            shrinkB=1,
                            connectionstyle=style,
                        ),
                    )
            elif annotation_style == 1:
                for i in range(repetition * 2 + 1):
                    axes[j].annotate(
                        text="%.2f" % ys[0, i],
                        xy=(0, ys[0, i]),
                        xytext=(0, ys[0, i] - np.max(ys) / repetition / 5),
                    )
                    axes[j].annotate(
                        text="%.2f" % ys[-1, i],
                        xy=(len(subfolders) - 1, ys[-1, i]),
                        xytext=(
                            len(subfolders) - 1,
                            ys[-1, i] - np.max(ys) / repetition / 5,
                        ),
                    )
            else:
                raise ValueError("annotation_style must be 1 or 2")

        if raw:
            import polars as pl

            pl.DataFrame(ys).write_csv(f"pol_{xyz[j]}.csv")

    plt.tight_layout()
    # save and show
    if figname:
        import os

        absfig = os.path.abspath(figname)
        os.makedirs(os.path.dirname(absfig), exist_ok=True)
        plt.savefig(absfig, dpi=300)
        logger.info(f"==> {absfig}")
    if show:
        plt.show()

    return axes


def _get_subfolders_quantum_totals(directory: str):
    """返回铁电极化计算任务的子目录、量子数、极化总量；

    请勿创建其他子目录，否则会被错误读取

    Parameters
    ----------
    directory：str
        铁电极化计算任务主目录

    Returns
    -------
    subfolders:
        子目录列表
    quantum : np.ndarray
        量子数，xyz三个方向, shape=(1, 3)
    totals : np.ndarray
        极化总量，xyz三个方向, shape=(len(subfolders), 3)

    """
    import os

    absdir = os.path.abspath(directory)
    raw_subfolders = next(os.walk(absdir))[1]
    subfolders = []
    for subfolder in raw_subfolders:
        assert (
            0 <= int(subfolder) < 100
        ), f"--> You should rename subfolders to 0~99, but {subfolder} found"
        try:
            assert 0 <= int(subfolder) < 100
            subfolders.append(subfolder)
        except Exception:
            pass
    subfolders.sort()  # 从小到大排序

    # quantum number if constant across the whole calculation, read only once
    absh5 = f"{os.path.join(absdir, subfolders[0])}/scf.h5"
    absjs = f"{os.path.join(absdir, subfolders[0])}/polarization.json"
    import numpy as np
    from h5py import File

    if os.path.isfile(absjs):
        quantum = np.asarray(File(absh5).get("/PolarizationInfo/Quantum"))
    elif os.path.isfile(absjs):
        with open(absjs) as f:
            from json import load

            quantum = np.asarray(load(f)["PolarizationInfo"]["Quantum"])
    else:
        raise FileNotFoundError(f"No {absh5}/{absjs}")

    totals = np.empty(shape=(len(subfolders), 3))
    # the Total number is not constant, read for each subfolder
    for i, fd in enumerate(subfolders):
        absh5 = f"{os.path.join(absdir, fd)}/scf.h5"
        absjs = f"{os.path.join(absdir, fd)}/polarization.json"
        if os.path.isfile(absh5):
            data = File(f"{os.path.join(absdir, fd)}/scf.h5")
            total = np.asarray(data.get("/PolarizationInfo/Total"))
        elif os.path.isfile(absjs):
            with open(absjs) as f:
                from json import load

                data = load(f)
            total = np.asarray(data["PolarizationInfo"]["Total"], dtype=float)
        else:
            raise FileNotFoundError(f"No {absh5}/{absjs}")
        totals[i] = total

    return subfolders, quantum, totals


def getEwtData(nk, nb, celtot, proj_wt, ef, de, dele):
    import numpy as np

    emin = np.min(celtot) - de
    emax = np.max(celtot) - de

    emin = np.floor(emin - 0.2)
    emax = max(np.ceil(emax) * 1.0, 5.0)

    nps = int((emax - emin) / de)

    X = np.zeros((nps + 1, nk))
    Y = np.zeros((nps + 1, nk))

    X2 = []
    Y2 = []
    Z2 = []

    for ik in range(nk):
        for ip in range(nps + 1):
            omega = ip * de + emin + ef
            X[ip][ik] = ik
            Y[ip][ik] = ip * de + emin
            ewts_value = 0
            for ib in range(nb):
                smearing = dele / np.pi / ((omega - celtot[ib][ik]) ** 2 + dele**2)
                ewts_value += smearing * proj_wt[ib][ik]
            if ewts_value > 0.01:
                X2.append(ik)
                Y2.append(ip * de + emin)
                Z2.append(ewts_value)

    Z2_half = max(Z2) / 2

    for i, x in enumerate(Z2):
        if x > Z2_half:
            Z2[i] = Z2_half

    return X2, Y2, Z2, emin


def _read_aimd_converge_data(
    datafile: str,
    index: Optional[str] = None,
    verbose: bool = False,
):
    """从datafile指定的路径读取index指定的数据，返回绘图用的xs和ys两个数组

    Parameters
    ----------
    datafile:
        hdf5文件路径，如 'aimd.h5' 或 ['aimd.h5', 'aimd2.h5']
    index:
        编号, 默认 None

    Returns
    -------
    xs : np.ndarray
        x轴数据
    ys : np.ndarray
        y轴数据

    """
    import numpy as np

    if isinstance(datafile, list):
        xs = []
        ys = []
        for i, df in enumerate(datafile):
            # concentrate returned np.ndarray
            x, y = _read_aimd_converge_data(df, index)
            xs.extend(x)
            ys.extend(y)
        xs = np.linspace(1, len(xs), len(xs))
        return xs, ys

    # search datafile in the given directory
    elif isinstance(datafile, str):
        from dspawpy.io.utils import get_absfile

        absfile = get_absfile(datafile, task="aimd", verbose=verbose)

        if datafile.endswith("h5"):
            from h5py import File

            hf = File(absfile)  # 加载h5文件
            Nstep = (
                len(np.asarray(hf.get("/Structures"))) - 2
            )  # 步数（可能存在未完成的）
            ys = np.full(Nstep, np.nan)  # 准备一个空数组
            # 开始读取
            if index == "5":
                for i in range(1, Nstep + 1):
                    ys[i - 1] = np.linalg.det(
                        np.asarray(hf.get("/Structures/Step-%d/Lattice" % i)),
                    )
            else:
                map = {
                    "1": "IonsKineticEnergy",
                    "2": "TotalEnergy0",
                    "3": "PressureKinetic",
                    "4": "Temperature",
                }
                if index == "3" and "PressureKinetic" not in np.asarray(
                    hf.get("/AimdInfo/Step-1"),
                ):
                    logger.warning(
                        "Ensemble is neither NPT nor NPH, no PressureKinetic found for subfigure 3!",
                    )
                else:
                    for i in range(1, Nstep + 1):
                        assert index is not None
                        try:
                            ys[i - 1] = np.asarray(
                                hf.get("/AimdInfo/Step-%d/%s" % (i, map[index])),
                            )[0]
                        except Exception:
                            ys[i - 1] = 0
                            ys = np.delete(ys, -1)
                            logger.warning(
                                "-> AIMD task stopped at Nstep=%s, failed to read its %s value"
                                % (Nstep, map[index]),
                            )
                            break

            Nstep = len(ys)  # 步数更新为实际完成的步数
        elif datafile.endswith("json"):
            from json import load

            with open(absfile) as f:
                data = load(f)
            Nstep = len(data["Structures"])
            ys = np.zeros(Nstep)

            if index == "5":
                for i in range(Nstep):
                    ys[i] = np.linalg.det(
                        np.asarray(data["Structures"][i]["Lattice"]).reshape(3, 3),
                    )
            else:
                map = {
                    "1": "IonsKineticEnergy",
                    "2": "TotalEnergy0",
                    "3": "PressureKinetic",
                    "4": "Temperature",
                }
                assert index is not None
                if index in ["1", "2"]:
                    ys = data["AimdInfo"]["Energy"][map[index]]

                elif index == "3":
                    raise ValueError(
                        "PressureKinetic array is not written in json file, so dspawapy can not read it!",
                    )
                else:
                    ys = data["AimdInfo"][map[index]]

            Nstep = len(ys)  # 步数更新为实际完成的步数

        # 返回xs，ys两个数组
        return np.linspace(1, Nstep, Nstep), np.asarray(ys)  # type: ignore

    else:
        raise TypeError("datafile must be str or list")


def pltbd(
    bdp: "BSDOSPlotter",
    bs: "BandStructureSymmLine",
    dos: Optional["CompleteDos"] = None,
    demax: float = 0.1,
    ylim: Optional[List[float]] = None,
    alpha: float = 0.3,
    colors: Optional[List[str]] = None,
    filename: str = "banddos.png",
    dpi: int = 300,
):
    """基于BSDOSPlotter类的get_plot()优化而来，可绘制（投影）能带态密度图。

    改进：

    - dos 使用半透明涂抹
    - 费米能级用虚线，左右费米能级保持在同一高度
    - 线条颜色、宽度、类型可自定义
    - 允许设置能带范围
    - 如果没有磁性，不必显示能带图例
    - 在费米能级附近的能带可以突出显示
    - 可使用latex字体
    - 左右图间距减小

    此函数在原函数上有所改进，但仍存在不足，未来可能会开放更多选项，使用时请注意参数设置

    Parameters
    ----------
    bdp:
        BSDOSPlotter 类对象
    bs:
        能带数据
    dos:
        态密度数据
    demax:
        在费米能级附近 demax 范围内的能带将被高亮
    ylim:
        y轴边界
    alpha:
        态密度图的透明度
    colors:
        颜色列表
    filename:
        保存的文件名
    dpi:
        图片dpi

    Examples
    --------
    >>> from dspawpy.io.read import get_band_data, get_dos_data
    >>> from pymatgen.electronic_structure.plotter import BSDOSPlotter
    >>> from dspawpy.plot import pltbd
    >>> bdp = BSDOSPlotter(
    ...     bs_projection=None,  # 能带的投影方式，None表示不投影
    ...     dos_projection="elements")  # 态密度的投影方式，None表示不投影
    >>> band_data = get_band_data(
    ...     band_dir='dspawpy_proj/dspawpy_tests/inputs/supplement/banddos/band.json',  # 能带数据
    ...     zero_to_efermi=True,  # 非金属体系应将零点能移动到费米能级
    ... )
    >>> dos_data = get_dos_data(dos_dir='dspawpy_proj/dspawpy_tests/inputs/supplement/banddos/dos.json')
    >>> pltbd(bdp, band_data, dos_data, ylim=(-2,4), filename='dspawpy_proj/dspawpy_tests/outputs/doctest/newbd.png') # doctest: +ELLIPSIS
    <module 'matplotlib.pyplot' from '...pyplot.py'>

    与之前的版本对比:

    >>> bdp = BSDOSPlotter(bs_projection=None,dos_projection="elements")
    >>> plt = bdp.get_plot(bs=band_data, dos=dos_data)

    for old version pymatgen, it returns plt, otherwise may return axes, ref to userscripts for how to user them.

    """
    import numpy as np
    import palettable

    if colors is None:
        _colors = palettable.colorbrewer.qualitative.Set1_9.mpl_colors  # type: ignore
    else:
        _colors = colors

    # self -> BSDOSPlotter
    bs_projection = bdp.bs_projection
    dos_projection = bdp.dos_projection
    vb_energy_range = bdp.vb_energy_range
    cb_energy_range = bdp.cb_energy_range
    fixed_cb_energy = bdp.fixed_cb_energy
    egrid_interval = bdp.egrid_interval
    axis_fontsize = bdp.axis_fontsize
    tick_fontsize = bdp.tick_fontsize
    legend_fontsize = bdp.legend_fontsize
    bs_legend = bdp.bs_legend
    dos_legend = bdp.dos_legend
    rgb_legend = bdp.rgb_legend
    fig_size = bdp.fig_size

    if dos:
        elements = [e.symbol for e in dos.structure.composition.elements]
    elif bs_projection and bs.structure:
        elements = [e.symbol for e in bs.structure.composition.elements]
    else:
        elements = []

    rgb_legend = (
        rgb_legend
        and bs_projection
        and bs_projection.lower() == "elements"
        and len(elements) in [2, 3, 4]
    )

    if (
        bs_projection
        and bs_projection.lower() == "elements"
        and (len(elements) not in [2, 3, 4] or not bs.get_projection_on_elements())
    ):
        logger.warning(
            "Cannot get element projected data; either the projection data "
            "doesn't exist, or you don't have a compound with exactly 2 "
            "or 3 or 4 unique elements.",
        )
        bs_projection = None

    # specify energy range of plot
    emin = -vb_energy_range
    emax = (
        cb_energy_range
        if fixed_cb_energy
        else cb_energy_range + bs.get_band_gap()["energy"]
    )

    # initialize all the k-point labels and k-point x-distances for bs plot
    xlabels = []  # all symmetry point labels on x-axis
    xlabel_distances = []  # positions of symmetry point x-labels

    x_distances_list = []
    prev_right_klabel = (
        None  # used to determine which branches require a midline separator
    )

    for branch in bs.branches:
        x_distances = []

        # get left and right kpoint labels of this branch
        left_k, right_k = branch["name"].split("-")

        # add $ notation for LaTeX kpoint labels
        if left_k[0] == "\\" or "_" in left_k:
            left_k = "$" + left_k + "$"
        if right_k[0] == "\\" or "_" in right_k:
            right_k = "$" + right_k + "$"

        # add left k label to list of labels
        if prev_right_klabel is None:
            xlabels.append(left_k)
            xlabel_distances.append(0)
        elif prev_right_klabel != left_k:  # used for pipe separator
            xlabels[-1] = xlabels[-1] + "$\\mid$ " + left_k

        # add right k label to list of labels
        xlabels.append(right_k)
        prev_right_klabel = right_k

        # add x-coordinates for labels
        left_kpoint = bs.kpoints[branch["start_index"]].cart_coords
        right_kpoint = bs.kpoints[branch["end_index"]].cart_coords
        distance = np.linalg.norm(right_kpoint - left_kpoint)
        xlabel_distances.append(xlabel_distances[-1] + distance)  # type: ignore

        # add x-coordinates for kpoint data
        npts = branch["end_index"] - branch["start_index"]
        distance_interval = distance / npts
        x_distances.append(xlabel_distances[-2])
        for _ in range(npts):
            x_distances.append(x_distances[-1] + distance_interval)
        x_distances_list.append(x_distances)

    # set up bs and dos plot
    from matplotlib.gridspec import GridSpec

    gs = GridSpec(1, 2, width_ratios=[2, 1], wspace=0) if dos else GridSpec(1, 1)

    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=fig_size)
    fig.patch.set_facecolor("white")
    bs_ax = plt.subplot(gs[0])
    # set basic axes limits for the plot
    bs_ax.set_xlim(0, x_distances_list[-1][-1])
    emin = ylim[0] if ylim else emin
    emax = ylim[1] if ylim else emax
    bs_ax.set_ylim(emin, emax)
    # add BS xticks, labels, etc.
    bs_ax.set_xticks(xlabel_distances)
    bs_ax.set_xticklabels(xlabels, size=tick_fontsize)
    bs_ax.set_xlabel("Wavevector $k$", fontsize=axis_fontsize)
    bs_ax.set_ylabel("$E-E_F$ / eV", fontsize=axis_fontsize)

    # add BS fermi level line at E=0 and gridlines
    bs_ax.hlines(y=0, xmin=0, xmax=x_distances_list[-1][-1], color="k", lw=1, ls="--")
    bs_ax.set_yticks(np.arange(emin, emax + 1e-5, egrid_interval))
    bs_ax.set_yticklabels(
        np.arange(emin, emax + 1e-5, egrid_interval),
        size=tick_fontsize,
    )
    bs_ax.set_axisbelow(True)
    bs_ax.grid(color=[0.5, 0.5, 0.5], linestyle="dotted", linewidth=1)
    # renormalize the band energy to the Fermi level
    band_energies = {}
    spin_count = 0
    from pymatgen.electronic_structure.core import Spin

    for spin in (Spin.up, Spin.down):
        if spin in bs.bands:
            spin_count += 1
            band_energies[spin] = []
            for band in bs.bands[spin]:
                band = cast(List[float], band)
                band_energies[spin].append([e - bs.efermi for e in band])  # type: ignore

    # plot the colored band structure lines
    for spin in (Spin.up, Spin.down):
        if spin in band_energies:
            for band_idx, band in enumerate(band_energies[spin]):
                current_pos = 0
                for x_distances in x_distances_list:
                    sub_band = band[current_pos : current_pos + len(x_distances)]
                    # ! highlight the band close to the Fermi level
                    if np.max(np.abs(sub_band)) < demax:
                        bs_ax.plot(x_distances, sub_band, color=_colors[0], linewidth=3)
                    elif spin == Spin.up:
                        bs_ax.plot(
                            x_distances,
                            sub_band,
                            color=_colors[0],
                            linewidth=1,
                        )
                    elif spin == Spin.down:
                        bs_ax.plot(
                            x_distances,
                            sub_band,
                            color=_colors[1],
                            linewidth=1,
                        )
                    current_pos += len(x_distances)

    # add legend for band structure
    if spin_count == 2:
        if bs_legend and not rgb_legend:
            handles = []

            if bs_projection is None:
                import matplotlib.lines as mlines

                handles = [
                    mlines.Line2D(
                        [],
                        [],
                        linewidth=2,
                        color=_colors[0],
                        label="spin up",
                    ),
                    mlines.Line2D(
                        [],
                        [],
                        linewidth=2,
                        color=_colors[1],
                        label="spin down",
                    ),
                ]

            bs_ax.legend(
                handles=handles,
                fancybox=True,
                prop={"size": legend_fontsize},
                loc=bs_legend,
            )

    # renormalize the DOS energies to Fermi level
    from pymatgen.electronic_structure.core import OrbitalType

    if dos:
        dos_ax = plt.subplot(gs[1])
        dos_ax.set_ylim(emin, emax)
        dos_ax.set_yticks(np.arange(emin, emax + 1e-5, egrid_interval))
        dos_ax.set_yticklabels([])
        dos_ax.grid(color=[0.5, 0.5, 0.5], linestyle="dotted", linewidth=1)

        dos_energies = [e - dos.efermi for e in dos.energies]
        # Plot the DOS and projected DOS
        for spin in (Spin.up, Spin.down):
            if spin in dos.densities:
                # plot the total DOS
                dos_densities = dos.densities[spin] * int(spin)
                label = "total" if spin == Spin.up else None
                dos_ax.plot(dos_densities, dos_energies, color=(0.6, 0.6, 0.6))
                dos_ax.fill_betweenx(
                    dos_energies,
                    0,
                    dos_densities,
                    color=(0.7, 0.7, 0.7),
                    alpha=alpha,
                    # facecolor=(0.7, 0.7, 0.7),
                    label=label,
                )
                if dos_projection is None:
                    pass
                elif dos_projection.lower() == "elements":
                    # plot the atom-projected DOS
                    from pymatgen.core.periodic_table import Element

                    for idx, el in enumerate(elements):
                        if spin_count == 1:
                            el_dos = dos.get_element_dos()
                            dos_densities = el_dos[Element(el)].densities[spin] * int(
                                spin,
                            )
                            label = el if spin == Spin.up else None
                            dos_ax.plot(dos_densities, dos_energies, color=_colors[idx])
                            dos_ax.fill_betweenx(
                                dos_energies,
                                0,
                                dos_densities,
                                color=_colors[idx],
                                alpha=alpha,
                                label=label,
                            )
                        elif spin_count == 2:
                            if el not in ["O", "Cu"]:  # TODO generalize
                                continue
                            el_spd_dos = dos.get_element_spd_dos(el)
                            for idx, orb in enumerate([OrbitalType.p, OrbitalType.d]):
                                if (
                                    orb == OrbitalType.p
                                    and el == "Cu"
                                    or orb == OrbitalType.d
                                    and el == "O"
                                ):
                                    continue
                                if orb in el_spd_dos:
                                    dos_densities = el_spd_dos[orb].densities[
                                        spin
                                    ] * int(spin)
                                    label = f"{el}-{orb}" if spin == Spin.up else None  # type: ignore
                                    dos_ax.plot(
                                        dos_densities,
                                        dos_energies,
                                        color=_colors[idx],
                                    )
                                    dos_ax.fill_betweenx(
                                        dos_energies,
                                        0,
                                        dos_densities,
                                        color=_colors[idx],
                                        alpha=alpha,
                                        label=label,
                                    )

        # get index of lowest and highest energy being plotted, used to help auto-scale DOS x-axis
        emin_idx = next(x[0] for x in enumerate(dos_energies) if x[1] >= emin)
        emax_idx = len(dos_energies) - next(
            x[0] for x in enumerate(reversed(dos_energies)) if x[1] <= emax
        )

        # determine DOS x-axis range
        dos_xmin = (
            0
            if Spin.down not in dos.densities
            else -max(dos.densities[Spin.down][emin_idx : emax_idx + 1] * 1.05)
        )
        dos_xmax = max(
            [max(dos.densities[Spin.up][emin_idx:emax_idx]) * 1.05, abs(dos_xmin)],
        )

        # set up the DOS x-axis and add Fermi level line
        dos_ax.set_xlim(dos_xmin, dos_xmax)
        dos_ax.set_xticklabels([])
        dos_ax.hlines(y=0, xmin=dos_xmin, xmax=dos_xmax, color="k", lw=1, ls="--")
        dos_ax.set_xlabel("DOS", fontsize=axis_fontsize)
        dos_ax.set_ylim(emin, emax)

        # add legend for DOS
        if dos_legend:
            dos_ax.legend(
                fancybox=True,
                prop={"size": legend_fontsize},
                loc=dos_legend,
            )

    plt.subplots_adjust(wspace=0.1)
    import os

    os.makedirs(os.path.dirname(os.path.abspath(filename)), exist_ok=True)
    plt.tight_layout()
    plt.savefig(filename, dpi=dpi)
    # plt.show()

    return plt


def plot_dos(
    dosplotter,
    xlim: Optional[Tuple[float, float]] = None,
    ylim: Optional[Tuple[float, float]] = None,
    invert_axes: bool = False,
    beta_dashed: bool = False,
    ax=None,
    raw: bool = False,
):
    """Get a matplotlib plot showing the DOS.

    Parameters
    ----------
    dosplotter (DosPlotter): A DosPlotter object containing a complete Dos.
    xlim (tuple[float, float]): The energy axis limits. Defaults to None for automatic
        determination.
    ylim (tuple[float, float]): The y-axis limits. Defaults to None for automatic determination.
    invert_axes (bool): Whether to invert the x and y axes. Enables chemist style DOS plotting.
        Defaults to False.
    beta_dashed (bool): Plots the beta spin channel with a dashed line. Defaults to False.
    raw (bool): Whether to save raw data to csv file. Defaults to False.

    Returns
    -------
    plt.Axes: matplotlib Axes object.

    Example
    -------
    >>> from dspawpy.io.read import get_dos_data
    >>> from pymatgen.electronic_structure.plotter import DosPlotter
    >>> from dspawpy.plot import plot_dos

    >>> dos_data = get_dos_data(
    ...    dos_dir="dspawpy_proj/dspawpy_tests/inputs/3.2.4/dos.h5",
    ...    return_dos=False)
    >>> dos_plotter = DosPlotter(
    ... zero_at_efermi=True,
    ... stack=False,
    ... sigma=None)
    >>> dos_plotter.add_dos(label="total dos", dos=dos_data)
    >>> ax = plot_dos(
    ...  dosplotter=dos_plotter,
    ...  xlim=[-10, 5],
    ...  ylim=[-15, 15])
    >>> fig = ax.get_figure()
    >>> fig.savefig("dspawpy_proj/dspawpy_tests/outputs/doctest/plot_dos.png")

    """
    import matplotlib.pyplot as plt
    import palettable

    if not ax:
        from pymatgen.util.plotting import pretty_plot

        ax = pretty_plot(12, 8)  # may be plt for old pmg

    n_colors = min(9, max(3, len(dosplotter._doses)))

    # https://jiffyclub.github.io/palettable/colorbrewer/qualitative/
    colors = palettable.colorbrewer.qualitative.Set1_9.mpl_colors  # type: ignore

    ys = None
    all_densities = []
    all_energies = []
    if isinstance(ax, type(plt)):
        ax = ax.gca()  # type: ignore

    # Note that this complicated processing of energies is to allow for
    # stacked plots in matplotlib.
    import numpy as np
    from pymatgen.electronic_structure.core import Spin

    for dos in dosplotter._doses.values():
        energies = dos["energies"]
        densities = dos["densities"]
        if not ys:
            ys = {
                Spin.up: np.zeros(energies.shape),
                Spin.down: np.zeros(energies.shape),
            }
        new_dens = {}
        for spin in [Spin.up, Spin.down]:
            if spin in densities:
                if dosplotter.stack:
                    ys[spin] += densities[spin]
                    new_dens[spin] = ys[spin].copy()
                else:
                    new_dens[spin] = densities[spin]
        all_energies.append(energies)
        all_densities.append(new_dens)

    keys = list(reversed(dosplotter._doses))
    all_densities.reverse()
    all_energies.reverse()
    all_pts = []

    dd = {}
    for idx, key in enumerate(keys):
        for spin in [Spin.up, Spin.down]:
            if spin in all_densities[idx]:
                energy = all_energies[idx]
                densities = list(int(spin) * all_densities[idx][spin])
                if invert_axes:
                    x = densities
                    y = energy
                else:
                    x = energy
                    y = densities
                all_pts.extend(list(zip(x, y)))
                if dosplotter.stack:
                    ax.fill(x, y, color=colors[idx % n_colors], label=str(key))
                elif spin == Spin.down and beta_dashed:
                    ax.plot(
                        x,
                        y,
                        color=colors[idx % n_colors],
                        label=str(key),
                        linestyle="--",
                        linewidth=3,
                    )
                else:
                    ax.plot(
                        x,
                        y,
                        color=colors[idx % n_colors],
                        label=str(key),
                        linewidth=3,
                    )

                dd[f"key={key}_spin={spin}_x"] = x
                dd[f"key={key}_spin={spin}_y"] = y

    if xlim:
        ax.set_xlim(xlim)
    if ylim:
        ax.set_ylim(ylim)
    elif not invert_axes:
        xlim = ax.get_xlim()
        relevant_y = [p[1] for p in all_pts if xlim[0] < p[0] < xlim[1]]
        ax.set_ylim((min(relevant_y), max(relevant_y)))
    if not xlim and invert_axes:
        ylim = ax.get_ylim()
        relevant_y = [p[0] for p in all_pts if ylim[0] < p[1] < ylim[1]]
        ax.set_xlim((min(relevant_y), max(relevant_y)))

    if dosplotter.zero_at_efermi:
        xlim = ax.get_xlim()
        ylim = ax.get_ylim()
        ax.plot(xlim, [0, 0], "k--", linewidth=2) if invert_axes else ax.plot(
            [0, 0],
            ylim,
            "k--",
            linewidth=2,
        )

    if invert_axes:
        ax.set_ylabel("Energies (eV)")
        # ax.set_xlabel(
        #     f"Density of states (states/eV{'/Å³' if hasattr(dosplotter, 'norm_val') else ''})",
        # )
        ax.set_xlabel("Density of states (states/eV)")
        ax.axvline(x=0, color="k", linestyle="--", linewidth=2)
    else:
        ax.set_xlabel("Energies (eV)")
        ax.set_ylabel("Density of states (states/eV)")
        # if hasattr(dosplotter, "_norm_val"):
        #     # if dosplotter._norm_val:
        #     ax.set_ylabel("Density of states (states/eV/Å³)")
        # else:
        #     ax.set_ylabel("Density of states (states/eV)")
        ax.axhline(y=0, color="k", linestyle="--", linewidth=2)

    # Remove duplicate labels with a dictionary
    handles, labels = ax.get_legend_handles_labels()
    label_dict = dict(zip(labels, handles))
    ax.legend(label_dict.values(), label_dict)
    legend_text = (
        ax.get_legend().get_texts()
    )  # all the text.Text instance in the legend
    plt.setp(legend_text, fontsize=30)
    plt.tight_layout()

    if raw:
        import polars as pl

        df = pl.DataFrame(dd)
        df.write_csv("dos_raw.csv")
    return ax
