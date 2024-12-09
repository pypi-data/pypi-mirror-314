from typing import TYPE_CHECKING, List, Optional, Union

from loguru import logger

from dspawpy.io.utils import reader

if TYPE_CHECKING:
    from pymatgen.core.structure import Structure


def build_Structures_from_datafile(
    datafile: Union[str, List[str]],
    si=None,
    ele=None,
    ai=None,
    fmt=None,
    task="scf",
):
    """Deprecated alias to read"""
    logger.warning(
        "build_Structures_from_datafile is deprecated; use read instead",
        DeprecationWarning,
    )
    return read(datafile, si=si, ele=ele, ai=ai, fmt=fmt, task=task)


def _get_structure_list(
    df: str,
    si=None,
    ele=None,
    ai=None,
    fmt: Optional[str] = None,
    task: Optional[str] = "scf",
    verbose: bool = True,
):
    """Get pymatgen structures from single datafile

    Parameters
    ----------
    df:
        数据文件路径或包含数据文件的文件夹路径

    Returns
    -------
    List[Structure] : list of pymatgen structures

    """
    if task is None:
        task = "scf"

    import os

    if os.path.isdir(df) or df.endswith(".h5") or df.endswith(".json"):
        from dspawpy.io.utils import get_absfile

        absfile = get_absfile(df, task=task, verbose=verbose)
    else:  # for other type of datafile, such as .as, .hzw, POSCAR
        absfile = os.path.abspath(df)

    if fmt is None:
        fmt = absfile.split(".")[-1]
    else:
        assert isinstance(fmt, str)

    if fmt == "as":
        strs = [_from_dspaw_as(absfile)]
    elif fmt == "hzw":
        logger.warning("build from .hzw may lack mag & fix info!", category=UserWarning)
        strs = [_from_hzw(absfile)]
    elif fmt == "xyz":
        strs = [_from_xyz(absfile)]
    elif fmt == "pdb":
        strs = _from_pdb(absfile)
    elif fmt == "h5":
        from dspawpy.io.read import get_sinfo

        Nstep, elements, positions, lattices, D_mag_fix = get_sinfo(
            datafile=absfile,
            si=si,
            ele=ele,
            ai=ai,
        )  # returned positions, not scaled-positions
        # remove _ from elements
        import re

        elements = [re.sub(r"_", "", e) for e in elements]

        strs = []
        from pymatgen.core import Structure

        for i in range(Nstep):
            if D_mag_fix:
                strs.append(
                    Structure(
                        lattices[i],
                        elements,
                        positions[i],
                        coords_are_cartesian=True,
                        site_properties={k: v[i] for k, v in D_mag_fix.items()},
                    ),
                )
            else:
                strs.append(
                    Structure(
                        lattices[i],
                        elements,
                        positions[i],
                        coords_are_cartesian=True,
                    ),
                )

    elif fmt == "json":
        try:
            from dspawpy.io.read import get_sinfo

            Nstep, elements, positions, lattices, D_mag_fix = get_sinfo(
                datafile=absfile,
                si=si,
                ele=ele,
                ai=ai,
            )  # returned positions, not scaled-positions
            # remove _ from elements

            import re

            elements = [re.sub(r"_", "", e) for e in elements]

            strs = []
            from pymatgen.core import Structure

            for i in range(Nstep):
                if D_mag_fix:
                    strs.append(
                        Structure(
                            lattices[i],
                            elements,
                            positions[i],
                            coords_are_cartesian=True,
                            site_properties={k: v[i] for k, v in D_mag_fix.items()},
                        ),
                    )
                else:
                    strs.append(
                        Structure(
                            lattices[i],
                            elements,
                            positions[i],
                            coords_are_cartesian=True,
                        ),
                    )
        except Exception:  # try parse json with pymatgen
            from pymatgen.core import Structure

            strs = [Structure.from_file(absfile)]

    else:
        from pymatgen.core import Structure

        strs = [Structure.from_file(absfile)]

    return strs


def _from_dspaw_as(as_file: str = "structure.as") -> "Structure":
    """从DSPAW的as结构文件中读取结构信息

    Parameters
    ----------
    as_file:
        DSPAW的as结构文件, 默认'structure.as'

    Returns
    -------
    Structure
        pymatgen的Structure对象

    """
    import os

    absfile = os.path.abspath(as_file)
    from dspawpy.io.read import get_lines_without_comment

    lines = get_lines_without_comment(absfile, "#")
    N = int(lines[1])  # number of atoms

    # parse lattice info
    lattice = []  # lattice matrix
    for line in lines[3:6]:
        vector = line.split()
        lattice.extend([float(vector[0]), float(vector[1]), float(vector[2])])
    import numpy as np

    lattice = np.asarray(lattice).reshape(3, 3)

    lat_fixs = []
    if lines[2].strip() != "Lattice":  # fix lattice
        lattice_fix_info = lines[2].strip().split()[1:]
        if lattice_fix_info == ["Fix_x", "Fix_y", "Fix_z"]:
            # ONLY support xyz fix in sequence, yzx will cause error
            for line in lines[3:6]:
                lfs = line.strip().split()[3:6]
                for lf in lfs:
                    if lf.startswith("T"):
                        lat_fixs.append("True")
                    elif lf.startswith("F"):
                        lat_fixs.append("False")
        elif lattice_fix_info == ["Fix"]:
            for line in lines[3:6]:
                lf = line.strip().split()[3]
                if lf.startswith("T"):
                    lat_fixs.append("True")
                elif lf.startswith("F"):
                    lat_fixs.append("False")
        else:
            raise ValueError("Lattice fix info error!")

    elements = []
    positions = []
    for i in range(N):
        atom = lines[i + 7].strip().split()
        elements.append(atom[0])
        positions.extend([float(atom[1]), float(atom[2]), float(atom[3])])

    mf_info = None
    l6 = lines[6].strip()  # str, 'Cartesian/Direct Mag Fix_x ...'
    if l6.split()[0] == "Direct":
        is_direct = True
    elif l6.split()[0] == "Cartesian":
        is_direct = False
    else:
        raise ValueError("Structure file format error!")

    mf_info = l6.split()[1:]  # ['Mag', 'Fix_x', 'Fix_y', 'Fix_z']
    for item in mf_info:
        assert (
            item
            in [
                "Mag",
                "Mag_x",
                "Mag_y",
                "Mag_z",
                "Fix",
                "Fix_x",
                "Fix_y",
                "Fix_z",
            ]
        ), f"{item} is not a valid flag! Expecting ['Mag', 'Mag_x', 'Mag_y', 'Mag_z', 'Fix', 'Fix_x', 'Fix_y', 'Fix_z']"

    mag_fix_dict = {}
    if mf_info is not None:
        for mf_index, item in enumerate(mf_info):
            values = []
            for i in range(N):
                atom = lines[i + 7].strip().split()
                mf = atom[4:]
                if item == "Fix":  # Fix == Fix_x, Fix_y, Fix_z
                    values.append([mf[mf_index], mf[mf_index + 1], mf[mf_index + 2]])
                else:
                    values.append(mf[mf_index])

            if item.startswith("Fix"):  # F -> False, T -> True
                for value in values:
                    if isinstance(value, str):
                        if value.startswith("T"):
                            values[values.index(value)] = "True"
                        elif value.startswith("F"):
                            values[values.index(value)] = "False"
                    elif isinstance(value, list):
                        for v in value:
                            if v.startswith("T"):
                                value[value.index(v)] = "True"
                            elif v.startswith("F"):
                                value[value.index(v)] = "False"
            mag_fix_dict[item] = values

    if lat_fixs != []:
        # replicate lat_fixs to N atoms
        mag_fix_dict["LatticeFixs"] = [lat_fixs for _ in range(N)]

    coords = np.asarray(positions).reshape(-1, 3)
    # remove _ from elements
    import re

    elements = [re.sub(r"_", "", e) for e in elements]

    from pymatgen.core import Structure

    if mag_fix_dict == {}:
        return Structure(
            lattice,
            elements,
            coords,
            coords_are_cartesian=(not is_direct),
        )
    else:
        return Structure(
            lattice,
            elements,
            coords,
            coords_are_cartesian=(not is_direct),
            site_properties=mag_fix_dict,
        )


def _from_hzw(hzw_file) -> "Structure":
    """从hzw结构文件中读取结构信息

    Parameters
    ----------
    hzw_file:
        hzw结构文件，以 .hzw 结尾

    Returns
    -------
    Structure
        pymatgen的Structure对象

    Examples
    --------
    >>> from dspawpy.io.structure import _from_hzw
    >>> print(_from_hzw('dspawpy_proj/dspawpy_tests/inputs/supplement/Si2.hzw'))
    Full Formula (Si2)
    Reduced Formula: Si
    abc   :   0.678839   0.678839   0.678839
    angles:  90.000000  90.000000  90.000000
    pbc   :       True       True       True
    Sites (2)
      #  SP           a         b         c
    ---  ----  --------  --------  --------
      0  Si    0.999999  0.999999  0.999999
      1  Si    3         3         3

    """
    import os

    from pymatgen.core import Structure

    from dspawpy.io.read import get_lines_without_comment

    absfile = os.path.abspath(hzw_file)

    lines = get_lines_without_comment(absfile, "%")
    number_of_probes = int(lines[0])
    elements = []
    positions = []
    if number_of_probes == 0:  # with lattice
        N = int(lines[4])
        for i in range(N):
            atom = lines[i + 5].strip().split()
            elements.append(atom[0])
            positions.append([float(atom[1]), float(atom[2]), float(atom[3])])

        lattice = []
        for line in lines[1:4]:
            vector = line.split()
            lattice.append([float(vector[0]), float(vector[1]), float(vector[2])])

    elif number_of_probes == -1:  # crystal
        N = int(lines[1])
        for i in range(N):
            atom = lines[i + 2].strip().split()
            elements.append(atom[0])
            positions.append([float(atom[1]), float(atom[2]), float(atom[3])])

        max_a = max(positions[:][0]) + 1e-6
        max_b = max(positions[:][0]) + 1e-6
        max_c = max(positions[:][0]) + 1e-6
        lattice = [max_a, 0, 0, 0, max_b, 0, 0, 0, max_c]

    else:
        raise NotImplementedError("number of probes must be 0 or 1")

    return Structure(lattice, elements, positions, coords_are_cartesian=True)


def _from_xyz(xyzfile: str) -> "Structure":
    """From molecule xyz file, build pmg.structure

    Examples
    --------
    >>> from dspawpy.io.structure import _from_xyz
    >>> print(_from_xyz('dspawpy_proj/dspawpy_tests/inputs/supplement/Si2.xyz'))
    Full Formula (Si2)
    Reduced Formula: Si
    abc   :   4.811495   4.826272   4.826271
    angles:  90.000000  90.000000  90.000000
    pbc   :       True       True       True
    Sites (2)
      #  SP           a         b         c
    ---  ----  --------  --------  --------
      0  Si    0.928452  0.927353  0.927353
      1  Si    0.071548  0.072647  0.072647

    """
    from pymatgen.core.structure import Molecule

    mol = Molecule.from_file(xyzfile)
    assert mol is not None

    a = max(mol.cart_coords[:, 0]) + 1e-6
    b = max(mol.cart_coords[:, 1]) + 1e-6
    c = max(mol.cart_coords[:, 2]) + 1e-6

    return mol.get_boxed_structure(a, b, c, no_cross=True)


def _read_atom_line(line_full):
    """从PDB文件读取 原子名称、xyz坐标、元素符号
    PDB文件中ATOM部分的格式如下（不含磁矩、自由度信息）：
    HETATM    1  H14 ORTE    0       6.301   0.693   1.919  1.00  0.00        H
    固定标记 原子序号 原子名称 残基名称 残基序号 x y z 占有率 温度因子 元素符号

    剔除多余信息，仅保留
        - 原子名称
        - xyz坐标
        - 元素符号
    """
    line = line_full.rstrip("\n")
    type_atm = line[0:6]
    if type_atm == "ATOM  " or type_atm == "HETATM":
        name = line[12:16].strip()  # 原子名称
        # atomic coordinates
        import numpy as np

        try:  # 5.3f表示5位整数，3位小数，单位Angstrom
            coord = np.asarray(
                [float(line[30:38]), float(line[38:46]), float(line[46:54])],
                dtype=np.float64,
            )
        except ValueError:
            raise ValueError("Invalid or missing coordinate(s)")
        symbol = line[76:78].strip().upper()  # 元素符号

    else:
        raise ValueError("Only ATOM and HETATM supported")

    return name, coord, symbol


@reader
def _from_pdb(fileobj):
    """Read PDB files. Modified from ASE"""
    images = []  # 构型列表
    import numpy as np

    orig = np.identity(3)  # 原点
    trans = np.zeros(3)  # 偏移
    symbols = []  # 元素
    positions = []  # 坐标
    cell = None  # 晶胞

    from pymatgen.core.lattice import Lattice

    for line in fileobj.readlines():
        if line.startswith("CRYST1"):
            cellpar = [
                float(line[6:15]),  # a
                float(line[15:24]),  # b
                float(line[24:33]),  # c
                float(line[33:40]),  # alpha
                float(line[40:47]),  # beta
                float(line[47:54]),
            ]  # gamma
            cell = Lattice.from_parameters(
                a=cellpar[0],
                b=cellpar[1],
                c=cellpar[2],
                alpha=cellpar[3],
                beta=cellpar[4],
                gamma=cellpar[5],
            )

        for c in range(3):
            if line.startswith("ORIGX" + "123"[c]):
                orig[c] = [float(line[10:20]), float(line[20:30]), float(line[30:40])]
                trans[c] = float(line[45:55])

        if line.startswith("ATOM") or line.startswith("HETATM"):
            # line_info = name, coord, symbol
            line_info = _read_atom_line(line)

            from dspawpy.io.utils import label_to_symbol

            try:  # 尝试从元素符号转化，失败则使用原子名称
                symbol = label_to_symbol(line_info[2])
            except (KeyError, IndexError):
                symbol = label_to_symbol(line_info[0])
            symbols.append(symbol)

            position = np.dot(orig, line_info[1]) + trans
            positions.append(position)

        if line.startswith("END"):
            atoms = _build_atoms(cell, symbols, positions)
            images.append(atoms)
            symbols = []
            positions = []
            cell = None

    if len(images) == 0:
        atoms = _build_atoms(cell, symbols, positions)
        images.append(atoms)

    return images


def _build_atoms(cell, symbols, positions):
    if cell is None:
        logger.warning(
            "No lattice info in PDB file! The lattice defaults to [[2xmax, 0, 0]; [0, 2ymax, 0]; [0, 0, 2zmax]])",
            category=UserWarning,
        )
        # cell = np.zeros(shape=(3, 3))
        import numpy as np

        max_xyz = np.max(positions, axis=0)
        cell = np.diag(max_xyz * 2)

    from pymatgen.core import Structure

    atoms = Structure(
        lattice=cell,
        species=symbols,
        coords=positions,
        coords_are_cartesian=True,
    )

    return atoms


def read(
    datafile: Union[str, list],
    si=None,
    ele=None,
    ai=None,
    fmt: Optional[str] = None,
    task: Optional[str] = "scf",
):
    r"""读取一/多个h5/json文件，返回pymatgen的Structures列表

    Parameters
    ----------
    datafile:
        - h5/json/as/hzw/cif/poscar/cssr/xsf/mcsqs/prismatic/yaml/fleur-inpgen文件路径;
        - 若给定文件夹路径，可配合task参数读取内部的 {task}.h5/json 文件
        - 若给定字符串列表，将依次读取数据并合并成一个Structures列表
    si: int, list or str
        - 构型编号，从 1 开始

            - si=1, 读取第一个构型
            - si=[1,2], 读取第一个和第二个构型
            - si=':', 读取所有构型
            - si='-3:', 读取最后三个构型
        - 若为空，多构型文件将读取所有构型，单构型文件将读取最新构型
        - 此参数仅对 h5/json 文件有效
    ele:
        - 元素符号，写法参考：'H' 或 ['H','O']
        - 若为空，将读取所有元素的原子信息
        - 此参数仅对 h5/json 文件有效
    ai:
        - 原子编号，从 1 开始
        - 用法同si
        - 若为空，将读取所有原子信息
        - 此参数仅对 h5/json 文件有效
    fmt:
        - 文件格式，包括 'as', 'hzw', 'xyz', 'pdb', 'h5', 'json' 6种，其他值将被忽略。
        - 若为空，文件类型将依据文件名称惯例判断。
    task:
        - 用于当 datafile 为文件夹路径时，寻找内部的 {task}.h5/json 文件。
        - 计算任务类型，包括 'scf', 'relax', 'neb', 'aimd' 四种，其他值将被忽略。

    Returns
    -------
    pymatgen_Structures:
        结构列表

    Examples
    --------
    >>> from dspawpy.io.structure import read

    读取单个文件生成 Structures 列表

    >>> pymatgen_Structures = read(datafile='dspawpy_proj/dspawpy_tests/inputs/supplement/PtH.as')
    >>> len(pymatgen_Structures)
    1
    >>> pymatgen_Structures = read(datafile='dspawpy_proj/dspawpy_tests/inputs/supplement/PtH.hzw')
    >>> len(pymatgen_Structures)
    1
    >>> pymatgen_Structures = read(datafile='dspawpy_proj/dspawpy_tests/inputs/supplement/Si2.xyz')
    >>> len(pymatgen_Structures)
    1
    >>> pymatgen_Structures = read(datafile='dspawpy_proj/dspawpy_tests/inputs/supplement/aimd.pdb')
    >>> len(pymatgen_Structures)
    1000
    >>> pymatgen_Structures = read(datafile='dspawpy_proj/dspawpy_tests/inputs/2.1/relax.h5') # doctest: +ELLIPSIS
    >>> len(pymatgen_Structures)
    3
    >>> pymatgen_Structures = read(datafile='dspawpy_proj/dspawpy_tests/inputs/2.1/relax.json') # doctest: +ELLIPSIS
    >>> len(pymatgen_Structures)
    3

    注意pymatgen_Structures是由多个 Structure 对象组成的列表，每个 Structure 对象分别对应一个构型。如果只有一个构型，也会返回列表，请使用 pymatgen_Structures[0] 获取 Structure 对象

    当datafile为列表时，将依次读取多个文件，合并成一个Structures列表

    >>> pymatgen_Structures = read(datafile=['dspawpy_proj/dspawpy_tests/inputs/supplement/aimd1.h5','dspawpy_proj/dspawpy_tests/inputs/supplement/aimd2.h5']) # doctest: +ELLIPSIS

    """
    dfs = []
    if isinstance(datafile, list):  # 续算模式，给的是多个文件
        dfs = datafile
    else:  # 单次计算模式，处理单个文件
        dfs.append(datafile)

    # 读取结构数据
    pymatgen_Structures = []
    for df in dfs:
        structure_list = _get_structure_list(df, si, ele, ai, fmt, task)
        pymatgen_Structures.extend(structure_list)

    return pymatgen_Structures


def write(
    structure,
    filename: str,
    fmt: Optional[str] = None,
    coords_are_cartesian: bool = True,
):
    r"""往结构文件中写入信息

    Parameters
    ----------
    structure:
        pymatgen的Structure对象
    filename:
        结构文件名
    fmt:
        - 结构文件类型，原生支持 'json', 'as', 'hzw', 'pdb', 'xyz', 'dump' 六种
    coords_are_cartesian:
        - 是否写作笛卡尔坐标，默认为True；否则写成分数坐标形式
        - 此选项暂时仅对 as 和 json 格式有效

    Examples
    --------
    先读取结构信息:

    >>> from dspawpy.io.structure import read
    >>> s = read('dspawpy_proj/dspawpy_tests/inputs/2.15/01/neb01.h5') # doctest: +ELLIPSIS
    >>> len(s)
    17

    将结构信息写入文件：

    >>> from dspawpy.io.structure import write
    >>> write(s, filename='dspawpy_proj/dspawpy_tests/outputs/doctest/PtH.json', coords_are_cartesian=True) # doctest: +ELLIPSIS
    ==> ...PtH.json...
    >>> write(s, filename='dspawpy_proj/dspawpy_tests/outputs/doctest/PtH.as', coords_are_cartesian=True) # doctest: +ELLIPSIS
    ==> ...PtH.as...
    >>> write(s, filename='dspawpy_proj/dspawpy_tests/outputs/doctest/PtH.hzw', coords_are_cartesian=True) # doctest: +ELLIPSIS
    ==> ...PtH.hzw...

    pdb, xyz, dump 三种类型的文件，可以写入多个构型，形成“轨迹”。生成的 xyz 等轨迹文件可使用 OVITO 等可视化软件打开观察。

    >>> write(s, filename='dspawpy_proj/dspawpy_tests/outputs/doctest/PtH.pdb', coords_are_cartesian=True) # doctest: +ELLIPSIS
    ==> ...PtH.pdb...
    >>> write(s, filename='dspawpy_proj/dspawpy_tests/outputs/doctest/PtH.xyz', coords_are_cartesian=True) # doctest: +ELLIPSIS
    ==> ...PtH.xyz...
    >>> write(s, filename='dspawpy_proj/dspawpy_tests/outputs/doctest/PtH.dump', coords_are_cartesian=True) # doctest: +ELLIPSIS
    ==> ...PtH.dump...

    单结构信息推荐使用 as 格式存储，如果 Structure 中有磁矩或自由度信息，将会按最完整的格式统一写入，形如 Fix_x, Fix_y, Fix_z, Mag_x, Mag_y, Mag_z，自由度信息默认为 F，磁矩默认为 0.0。可视情况自行手动删除生成的 as 文件中的这些默认信息。写成其他类型的结构文件，将忽略磁矩和自由度信息

    """
    from pymatgen.core import Structure

    if isinstance(structure, Structure):
        structure = [structure]

    import os

    absfilename = os.path.abspath(filename)
    if fmt is None:
        fmt = absfilename.split(".")[-1]

    if fmt == "pdb":  # 可以是多个构型
        from .write import _to_pdb

        _to_pdb(structure, absfilename)
    elif fmt == "xyz":  # 可以是多个构型
        from .write import _write_xyz_traj

        _write_xyz_traj(structure, absfilename)
    elif fmt == "dump":  # 可以是多个构型
        from .write import _write_dump_traj

        _write_dump_traj(structure, absfilename)

    elif fmt == "json":  # 单个构型
        from .write import _to_dspaw_json

        _to_dspaw_json(structure[-1], absfilename, coords_are_cartesian)
    elif fmt == "as":
        from .write import _to_dspaw_as

        _to_dspaw_as(structure[-1], absfilename, coords_are_cartesian)
    elif fmt == "hzw":
        from .write import _to_hzw

        _to_hzw(structure[-1], absfilename)

    elif fmt in [
        "cif",
        "mcif",
        "poscar",
        "cssr",
        "xsf",
        "mcsqs",
        "yaml",
        "fleur-inpgen",
        "prismatic",
        "res",
    ]:
        structure[-1].to(filename=absfilename, fmt=fmt)  # type: ignore

    else:
        try:
            structure[-1].to(filename=absfilename)
        except Exception as e:
            raise NotImplementedError(
                f"formats other than [pdb, xyz, dump, json, as, hzw] are handled by pymatgen, while it returns: {e}",
            )


def convert(
    infile,
    si=None,
    ele=None,
    ai=None,
    infmt: Optional[str] = None,
    task: str = "scf",
    outfile: str = "temp.xyz",
    outfmt: Optional[str] = None,
    coords_are_cartesian: bool = True,
):
    """从infile中读取结构信息，完成格式转化后写入outfile

    - 多构型 -> 单构型，仅写入最后一个离子步信息
    - 晶体结构 -> 分子结构，将丢失晶胞信息
    - 分子结构 -> 晶体结构，将添加一个2倍最大原子xyz坐标的晶胞
    - pdb 和 dump 格式可能存在浮点数精度损失

    Parameters
    ----------
    infile:
        - h5/json/as/hzw/cif/poscar/cssr/xsf/mcsqs/prismatic/yaml/fleur-inpgen文件路径;
        - 若给定文件夹路径，可配合task参数读取内部的 {task}.h5/json 文件
        - 若给定字符串列表，将依次读取数据并合并成一个Structures列表
    si: int, list or str
        - 构型编号，从 1 开始

            - si=1, 读取第一个构型
            - si=[1,2], 读取第一个和第二个构型
            - si=':', 读取所有构型
            - si='-3:', 读取最后三个构型
        - 若为空，多构型文件将读取所有构型，单构型文件将读取最新构型
        - 此参数仅对 h5/json 文件有效
    ele:
        - 元素符号，写法参考：'H' 或 ['H','O']
        - 若为空，将读取所有元素的原子信息
        - 此参数仅对 h5/json 文件有效
    ai:
        - 原子编号，从 1 开始
        - 用法同si
        - 若为空，将读取所有原子信息
        - 此参数仅对 h5/json 文件有效
    infmt:
        - 输入结构文件类型，例如 'h5'，如果为None，则根据文件后规则判断
    task:
        - 用于当 datafile 为文件夹路径时，寻找内部的 {task}.h5/json 文件。
        - 计算任务类型，包括 'scf', 'relax', 'neb', 'aimd' 四种，其他值将被忽略。
    outfile:
        - 输出文件名
    outfmt:
        - 输出结构文件类型，例如 'xyz'，如果为None，则根据文件后规则判断
    coords_are_cartesian:
        - 是否写作笛卡尔坐标，默认为True；否则写成分数坐标形式
        - 此选项暂时仅对 as 和 json 格式有效

    Examples
    --------
    >>> from dspawpy.io.structure import convert
    >>> convert('dspawpy_proj/dspawpy_tests/inputs/supplement/PtH.as', outfile='dspawpy_proj/dspawpy_tests/outputs/doctest/PtH.hzw') # doctest: +ELLIPSIS
    ==> ...PtH.hzw...

    格式转换批量测试

    >>> for readable in ['relax.h5', 'system.json', 'aimd.pdb', 'latestStructure.as', 'CuO.hzw', 'POSCAR']:
    ...     for writable in ['pdb', 'xyz', 'dump', 'as', 'hzw', 'POSCAR']:
    ...         convert('dspawpy_proj/dspawpy_tests/inputs/supplement/stru/'+readable, outfile=f"dspawpy_proj/dspawpy_tests/outputs/doctest/{readable.split('.')[0]}.{writable}") # doctest: +ELLIPSIS
    ==> ...relax.pdb...
    ==> ...relax.xyz...
    ==> ...relax.dump...
    ==> ...relax.as...
    ==> ...relax.hzw...
    ==> ...system.pdb...
    ==> ...system.xyz...
    ==> ...system.dump...
    ==> ...system.as...
    ==> ...system.hzw...
    ==> ...aimd.pdb...
    ==> ...aimd.xyz...
    ==> ...aimd.dump...
    ==> ...aimd.as...
    ==> ...aimd.hzw...
    ==> ...latestStructure.pdb...
    ==> ...latestStructure.xyz...
    ==> ...latestStructure.dump...
    ==> ...latestStructure.as...
    ==> ...latestStructure.hzw...
    ==> ...CuO.pdb...
    ==> ...CuO.xyz...
    ==> ...CuO.dump...
    ==> ...CuO.as...
    ==> ...CuO.hzw...
    ==> ...POSCAR.pdb...
    ==> ...POSCAR.xyz...
    ==> ...POSCAR.dump...
    ==> ...POSCAR.as...
    ==> ...POSCAR.hzw...

    """
    write(read(infile, si, ele, ai, infmt, task), outfile, outfmt, coords_are_cartesian)
