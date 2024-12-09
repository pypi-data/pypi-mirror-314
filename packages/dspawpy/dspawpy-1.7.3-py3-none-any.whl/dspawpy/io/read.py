from typing import TYPE_CHECKING, Optional, Sequence

from loguru import logger

if TYPE_CHECKING:
    from pymatgen.electronic_structure.bandstructure import BandStructureSymmLine


def read_relax_data(
    logfile: str = "DS-PAW.log",
    print_efs: bool = True,
    relative: bool = False,
    write_traj: bool = True,
    xyz_file_name: Optional[str] = "relaxing.xyz",
    write_as: bool = True,
    as_file_name: Optional[str] = "min_force.as",
) -> None:
    """Read relax data from log file, not h5/json, because they lack data.

    Only supports VDW-corrected atom fix now.

    TODO: Support atom and cell fix, Direct and Cartesian.

    Parameters
    ----------
    logfile:
        location of "DS-PAW.log", such as '../another/DS-PAW.log'.
    print_efs:
        whether to print energies and forces table.
    relative:
        whether to print energies and forces relative to the first step value.
    write_traj:
        whether to write traj xyz file
    xyz_file_name:
        location of the traj xyz file, such as '../another/rel.xyz'
    write_as:
        whether to write structure.as file corresponding to the minimal force.
    as_file_name:
        location of the structure.as file, such as '../another/min_force.as'

    Examples
    --------
    >>> from dspawpy.io.read import read_relax_data
    >>> read_relax_data(logfile='dspawpy_proj/dspawpy_tests/inputs/2.1/DS-PAW.log') # doctest: +ELLIPSIS
    shape: (3, 3)
    ┌──────┬─────────────────────┬─────────────┐
    │ step ┆ force (eV/Angstrom) ┆ energy (eV) │
    ╞══════╪═════════════════════╪═════════════╡
    │ 0    ┆ 0.489284            ┆ -216.967842 │
    │ 1    ┆ 0.1096              ┆ -216.976886 │
    │ 2    ┆ 0.024697            ┆ -216.977327 │
    └──────┴─────────────────────┴─────────────┘
    ==> ...relaxing.xyz...
    ==> ...min_force.as...

    >>> read_relax_data(logfile='dspawpy_proj/dspawpy_tests/inputs/2.1/DS-PAW.log', relative=True, write_traj=False, write_as=False)
    shape: (3, 3)
    ┌──────┬─────────────────────┬─────────────┐
    │ step ┆ force (eV/Angstrom) ┆ energy (eV) │
    ╞══════╪═════════════════════╪═════════════╡
    │ 0    ┆ 0.0                 ┆ 0.0         │
    │ 1    ┆ -0.379684           ┆ -0.009044   │
    │ 2    ┆ -0.464587           ┆ -0.009485   │
    └──────┴─────────────────────┴─────────────┘
    """
    import re
    from pathlib import Path

    from pymatgen.core.structure import Structure

    # energy, lattice, coordinate type, atom positions, forces, max force, time
    # p_vdw_energy = r"Total Energy\s+:\s+(.*)eV\n-+\n"
    p_vdw_energy = r"Total Energy\s+:\s+(.*)eV\n"  # SCF may not converge, so that "PAW Warning" will be added here.
    p_LOOP_energy = (
        r"LOOP \d+:\n",
        r"-+\n",
        r"#\s+iter\s+\|\s+Etot\(eV\)\s+dE\(eV\)\s+time\s*\n",
        r"((#\s+\d+\s+\|\s+.*\s+.*\s+.*s\n)+)\n",
        r"-+\n",
    )
    p_structure = (
        r"## STRUCTURE ##\n",
        r"Lattice vectors \(Angstrom\)\n",
        r"((.*\n){3})",
        r"CoordinateType\s+=\s+(.*)\n",
        r"Atom Position and force:\s*\n"
        r"((\s*\w+\s+[-+]?\d+\.\d+\s+[-+]?\d+\.\d+\s+[-+]?\d+\.\d+\s+[-+]?\d+\.\d+\s+[-+]?\d+\.\d+\s+[-+]?\d+\.\d+\s*)+)\n",
        r"-+\n",
        r"Total force.*\n",
        r"Max force:\s+(.*) eV/Angstrom.*\n",
        r"-+\n",
        r"Calculating force and stress.*\n",
        r"Total calculation time\s+:\s+(.*) s\n",
    )
    p_fix_atom = (
        r"CoordinateType\s+=\s+\w+\n",
        r"Atom position Fix_x Fix_y Fix_z:\s*\n",
        r"((\s*\w+\s+-?\d+\.\d+\s+-?\d+\.\d+\s+-?\d+\.\d+\s+[TF]?\s+[TF]?\s+[TF]?\s+)+)\n",
        r"## KPOINTS ##\n",
    )
    p = Path(logfile)
    if p.is_file():
        # Parsing flags and variables
        with p.open() as f:
            logger.info(f"reading {logfile}...")
            from pymatgen.core.structure import Structure

            data = f.read()

            # read atom fix info
            matches = re.findall("".join(p_fix_atom), data)
            if matches:
                atom_fix_info = []
                for jobid in range(len(matches)):
                    atomfix_data_for_this_job = matches[jobid]
                    atomfix_info_for_this_job = []
                    for atomline in atomfix_data_for_this_job[0].strip().split("\n"):
                        f_or_t = atomline.split()[-3:]
                        atomfix_info_for_this_job.append(f_or_t)
                    atom_fix_info.append(atomfix_info_for_this_job)
                # raise warning if atomfix info for each job is not the same
                if len(atom_fix_info) > 1 and not all(
                    a == atom_fix_info[0] for a in atom_fix_info
                ):
                    print(
                        "Warning: Atom fix info is not the same for each job, please check your log file."
                    )

                else:
                    print(f"conbining {len(atom_fix_info)} jobs")
            else:
                pass

            # read total energy of each step
            total_energies = []
            if "## VDW CORRECTION ##" in data:
                logger.info("Detected VDW correction in your log file.")
                matches = re.findall(p_vdw_energy, data)
                if not matches:
                    raise ValueError(
                        "SCF LOOP info not found, please check your log file."
                    )
                for i in range(len(matches)):
                    total_energies.append(float(matches[i]))

            else:
                matches = re.findall("".join(p_LOOP_energy), data)
                if not matches:
                    raise ValueError(
                        "SCF LOOP info not found, please check your log file."
                    )
                for i in range(len(matches)):
                    total_energies.append(
                        float(matches[i][0].split("\n")[-2].split()[3])
                    )

            # read lattice, coordinate type, atom positions, forces, time
            matches = re.findall("".join(p_structure), data)
            if not matches:
                raise ValueError(
                    "Structure info not found, please check your log file."
                )

            max_forces: list[float] = []
            times: list[float] = []
            structures: list[Structure] = []

            # for each ionic step
            for s in range(len(matches)):
                step = matches[s]

                lattice: list[float] = []
                elements: list[str] = []
                xyzs: list[list[float]] = []
                forces: list[float] = []
                for vector in step[0].strip().split("\n"):
                    lattice.extend([float(i) for i in vector.split()])

                coordinate_type = step[2]

                for al in step[3].strip().split("\n"):
                    ele, x, y, z, fx, fy, fz = al.split()
                    elements.append(ele)
                    xyzs.append([float(x), float(y), float(z)])
                    forces.extend([float(fx), float(fy), float(fz)])

                max_forces.append(float(step[5]))
                times.append(float(step[6]))

                s = Structure(
                    lattice=lattice,
                    species=elements,
                    coords=xyzs,
                    coords_are_cartesian=coordinate_type == "Cartesian",
                )
                structures.append(s)

        if not len(total_energies) == len(max_forces) == len(structures) == len(times):
            raise ValueError(
                f"{len(total_energies)=}, {len(max_forces)=}, {len(structures)=}, {len(times)=}"
            )
        min_force_step_index = max_forces.index(min(max_forces))

        if print_efs:
            import polars as pl

            if relative:
                print(
                    pl.DataFrame(
                        {
                            "step": list(range(len(total_energies))),
                            "force (eV/Angstrom)": [
                                f - max_forces[0] for f in max_forces
                            ],
                            "energy (eV)": [
                                e - total_energies[0] for e in total_energies
                            ],
                        }
                    )
                )
            else:
                print(
                    pl.DataFrame(
                        {
                            "step": list(range(len(total_energies))),
                            "force (eV/Angstrom)": max_forces,
                            "energy (eV)": total_energies,
                        }
                    )
                )
        else:
            logger.debug(f"Will not print enegies and forces because {print_efs=}")

        logger.info(
            f"min force {max_forces[min_force_step_index]} eV/Angstrom, with energy: {total_energies[min_force_step_index]} eV at step: {min_force_step_index}"
        )
        if write_traj:
            from .write import _write_xyz_traj

            xyz_file_name = xyz_file_name or "rel.xyz"
            _write_xyz_traj(structures, xyz_file_name)
        else:
            logger.debug(f"Will not write traj because {write_traj=}")

        if write_as:
            from .write import _to_dspaw_as

            min_force_as = as_file_name or "min_force.as"
            _to_dspaw_as(structures[min_force_step_index], min_force_as)
        else:
            logger.debug(f"Will not write min_force.as because {write_as=}")
    else:
        raise FileNotFoundError(logfile)


def get_band_data(
    band_dir: str,
    syst_dir: Optional[str] = None,
    efermi: Optional[float] = None,
    zero_to_efermi: bool = False,
    verbose: bool = False,
) -> "BandStructureSymmLine":
    """读取h5或json文件中的能带数据，构建BandStructureSymmLine对象

    Parameters
    ----------
    band_dir
        - 能带文件路径，band.h5 / band.json 或包含band.h5 / band.json的文件夹
        - 注意，wannier.h5 也可以使用此函数读取，但band_dir不支持文件夹类型
    syst_dir
        system.json 路径，仅为辅助处理 Wannier 数据而准备（从中读取结构和费米能级）
    efermi
        费米能级，如果h5文件中的费米能级不正确，可以通过此参数指定费米能级
    zero_to_efermi
        是否将费米能级移动到0

    Returns
    -------
    BandStructureSymmLine

    Examples
    --------
    >>> from dspawpy.io.read import get_band_data
    >>> band = get_band_data(band_dir='dspawpy_proj/dspawpy_tests/inputs/2.3/band.h5')
    >>> band = get_band_data(band_dir='dspawpy_proj/dspawpy_tests/inputs/2.4/band.h5')
    >>> band = get_band_data(band_dir='dspawpy_proj/dspawpy_tests/inputs/2.4/band.json')

    如果希望通过指定wannier.json来处理瓦尼尔能带，需要额外指定syst_dir参数

    >>> band = get_band_data(band_dir='dspawpy_proj/dspawpy_tests/inputs/2.30/wannier.h5')
    >>> band = get_band_data(band_dir='dspawpy_proj/dspawpy_tests/inputs/2.30/wannier.json', syst_dir='dspawpy_proj/dspawpy_tests/inputs/2.30/system.json')

    """
    if efermi is not None and zero_to_efermi:
        raise ValueError(
            "efermi and zero_to_efermi should not be set at the same time!",
        )

    from dspawpy.io.utils import get_absfile

    absfile = get_absfile(
        band_dir,
        task="band",
        verbose=verbose,
    )  # give wannier.h5 also work, verbose=verboses
    if absfile.endswith(".h5"):
        band = load_h5(absfile)
        from h5py import File

        raw = File(absfile, "r").keys()
        if "/WannBandInfo/NumberOfBand" in raw:
            (
                structure,
                kpoints,
                eigenvals,
                rEf,
                labels_dict,
                projections,
            ) = _get_band_data_h5(band, iwan=True, zero_to_efermi=zero_to_efermi)
        elif "/BandInfo/NumberOfBand" in raw:
            (
                structure,
                kpoints,
                eigenvals,
                rEf,
                labels_dict,
                projections,
            ) = _get_band_data_h5(band, iwan=False, zero_to_efermi=zero_to_efermi)
        else:
            raise KeyError("BandInfo or WannBandInfo key not found in h5file!")
    elif absfile.endswith(".json"):
        with open(absfile) as fin:
            from json import load

            band = load(fin)
        if "WannBandInfo" in band.keys():
            assert (
                syst_dir is not None
            ), "system.json is required for processing wannier band info!"
            with open(syst_dir) as system_json:
                from json import load

                syst = load(system_json)
            (
                structure,
                kpoints,
                eigenvals,
                rEf,
                labels_dict,
                projections,
            ) = _get_band_data_json(
                band,
                syst,
                iwan=True,
                zero_to_efermi=zero_to_efermi,
            )
        elif "BandInfo" in band.keys():
            (
                structure,
                kpoints,
                eigenvals,
                rEf,
                labels_dict,
                projections,
            ) = _get_band_data_json(band, iwan=False, zero_to_efermi=zero_to_efermi)
        else:
            raise ValueError(
                f"BandInfo or WannBandInfo key not found in {absfile} file!",
            )
    else:
        raise TypeError(f"{absfile} must be h5 or json file!")

    if efermi:  # 从h5直接读取的费米能级可能是错的，此时需要用户自行指定
        rEf = efermi  # 这只是个临时解决方案

    from pymatgen.core.lattice import Lattice

    lattice_new = Lattice(structure.lattice.reciprocal_lattice.matrix)

    from pymatgen.electronic_structure.bandstructure import BandStructureSymmLine

    return BandStructureSymmLine(
        kpoints=kpoints,
        eigenvals=eigenvals,
        lattice=lattice_new,
        efermi=rEf,
        labels_dict=labels_dict,
        structure=structure,
        projections=projections,
    )


def get_dos_data(
    dos_dir: str,
    return_dos: bool = False,
    verbose: bool = False,
):
    """读取h5或json文件中的态密度数据，构建CompleteDos或DOS对象

    Parameters
    ----------
    dos_dir:
        态密度文件路径，dos.h5 / dos.json 或包含dos.h5 / dos.json的文件夹
    return_dos : bool, optional
        是否返回DOS对象，如果为False，则统一返回CompleteDos对象（无论计算时是否开了投影）

    Returns
    -------
    CompleteDos or Dos

    Examples
    --------
    >>> from dspawpy.io.read import get_dos_data
    >>> dos = get_dos_data(dos_dir='dspawpy_proj/dspawpy_tests/inputs/2.5/dos.h5')
    >>> dos = get_dos_data(dos_dir='dspawpy_proj/dspawpy_tests/inputs/2.5/dos.h5', return_dos=True)

    """
    from dspawpy.io.utils import get_absfile

    absfile = get_absfile(dos_dir, task="dos", verbose=verbose)
    if absfile.endswith(".h5"):
        dos = load_h5(absfile)
        if return_dos and not dos["/DosInfo/Project"][0]:
            return _get_total_dos(dos)
        else:
            return _get_complete_dos(dos)

    elif absfile.endswith(".json"):
        with open(absfile) as fin:
            from json import load

            dos = load(fin)
        if return_dos and not dos["DosInfo"]["Project"]:
            return _get_total_dos_json(dos)
        else:
            return _get_complete_dos_json(dos)

    else:
        raise TypeError(f"{absfile} must be h5 or json file!")


def get_ele_from_h5(hpath: str = "aimd.h5") -> list:
    """从h5文件中读取元素列表；
    多离子步并不会在每个离子步的Structure中保存元素信息，只能读取初始结构的元素信息

    Parameters
    ----------
    hpath:
        h5文件路径

    Returns
    -------
    ele:
        元素列表, Natom x 1

    Examples
    --------
    >>> from dspawpy.io.read import get_ele_from_h5
    >>> ele = get_ele_from_h5(hpath='dspawpy_proj/dspawpy_tests/inputs/2.18/aimd.h5')
    >>> ele
    ['H', 'H_1', 'O']

    """
    import os

    absh5 = os.path.abspath(hpath)
    from h5py import File

    data = File(absh5)
    import numpy as np

    Elements_bytes = np.asarray(data.get("/AtomInfo/Elements"))
    tempdata = np.asarray([i.decode() for i in Elements_bytes])
    ele = "".join(tempdata).split(";")

    return ele


def get_lines_without_comment(filename: str, comment: str = "#") -> list:
    """读取as文件内容，移除批注后返回行列表

    Examples
    --------
    >>> from dspawpy.io.read import get_lines_without_comment
    >>> lines = get_lines_without_comment(filename='dspawpy_proj/dspawpy_tests/inputs/2.15/01/structure01.as', comment='#')
    >>> lines
    ['Total number of atoms', '13', 'Lattice', '5.60580000 0.00000000 0.00000000', '0.00000000 5.60580000 0.00000000', '0.00000000 0.00000000 16.81740000', 'Cartesian', 'H 2.48700709 3.85367720 6.93461994', 'Pt 1.40145000 1.40145000 1.98192999', 'Pt 4.20434996 1.40145000 1.98192999', 'Pt 1.40145000 4.20434996 1.98192999', 'Pt 4.20434996 4.20434996 1.98192999', 'Pt 0.00843706 0.00042409 3.91500875', 'Pt 0.00881029 2.80247953 3.91551673', 'Pt 2.81216310 -0.00105882 3.91807627', 'Pt 2.81156629 2.80392163 3.91572506', 'Pt 1.41398585 1.39603492 5.85554462', 'Pt 4.22886663 1.39820574 5.84677553', 'Pt 1.40485707 4.20963461 5.89521929', 'Pt 4.23788559 4.20753128 5.88625580']

    """
    lines = []
    import os

    absfile = os.path.abspath(filename)
    import re

    with open(absfile) as file:
        while True:
            line = file.readline()
            if line:
                line = re.sub(comment + r".*$", "", line)  # remove comment
                line = line.strip()
                if line:
                    lines.append(line)
            else:
                break

    return lines


def get_phonon_band_data(
    phonon_band_dir: str,
    verbose: bool = False,
):
    """读取h5或json文件中的声子能带数据，构建PhononBandStructureSymmLine对象

    Parameters
    ----------
    phonon_band_dir:
        能带文件路径，phonon.h5 / phonon.json 或包含这两个文件的文件夹

    Returns
    -------
    PhononBandStructureSymmLine

    Examples
    --------
    >>> from dspawpy.io.read import get_phonon_band_data
    >>> band_data = get_phonon_band_data("dspawpy_proj/dspawpy_tests/inputs/2.16/phonon.h5") # 读取声子能带
    >>> band_data = get_phonon_band_data("dspawpy_proj/dspawpy_tests/inputs/2.16/phonon.json") # 读取声子能带

    """
    from dspawpy.io.utils import get_absfile

    absfile = get_absfile(phonon_band_dir, task="phonon", verbose=verbose)

    if absfile.endswith(".h5"):
        band = load_h5(absfile)
        (
            symmmetry_kpoints,
            symmetry_kPoints_index,
            qpoints,
            structure,
            frequencies,
        ) = _get_phonon_band_data_h5(band)
    elif absfile.endswith(".json"):
        with open(absfile) as fin:
            from json import load

            band = load(fin)
        (
            symmmetry_kpoints,
            symmetry_kPoints_index,
            qpoints,
            structure,
            frequencies,
        ) = _get_phonon_band_data_json(band)
    else:
        raise TypeError(f"{absfile} must be h5 or json file")

    labels_dict = {}
    for i, s in enumerate(symmmetry_kpoints):
        labels_dict[s] = qpoints[symmetry_kPoints_index[i] - 1]
    from pymatgen.core.lattice import Lattice

    lattice_new = Lattice(structure.lattice.reciprocal_lattice.matrix)

    from pymatgen.phonon.bandstructure import PhononBandStructureSymmLine

    return PhononBandStructureSymmLine(
        qpoints=qpoints,  # type: ignore
        frequencies=frequencies,
        lattice=lattice_new,
        has_nac=False,
        labels_dict=labels_dict,
        structure=structure,
    )


def get_phonon_dos_data(
    phonon_dos_dir: str,
    verbose: bool = False,
):
    """读取h5或json文件中的声子态密度数据，构建PhononDos对象

    Parameters
    ----------
    phonon_dos_dir:
        声子态密度文件路径，phonon_dos.h5 / phonon_dos.json 或包含这两个文件的文件夹

    Returns
    -------
    PhononDos

    Examples
    --------
    >>> from dspawpy.io.read import get_phonon_dos_data
    >>> phdos = get_phonon_dos_data(phonon_dos_dir='dspawpy_proj/dspawpy_tests/inputs/2.16.1/phonon.json')
    >>> phdos = get_phonon_dos_data(phonon_dos_dir='dspawpy_proj/dspawpy_tests/inputs/2.16.1/phonon.h5')
    >>> phdos.frequencies
    array([ 0. ,  0.1,  0.2,  0.3,  0.4,  0.5,  0.6,  0.7,  0.8,  0.9,  1. ,
            1.1,  1.2,  1.3,  1.4,  1.5,  1.6,  1.7,  1.8,  1.9,  2. ,  2.1,
            2.2,  2.3,  2.4,  2.5,  2.6,  2.7,  2.8,  2.9,  3. ,  3.1,  3.2,
            3.3,  3.4,  3.5,  3.6,  3.7,  3.8,  3.9,  4. ,  4.1,  4.2,  4.3,
            4.4,  4.5,  4.6,  4.7,  4.8,  4.9,  5. ,  5.1,  5.2,  5.3,  5.4,
            5.5,  5.6,  5.7,  5.8,  5.9,  6. ,  6.1,  6.2,  6.3,  6.4,  6.5,
            6.6,  6.7,  6.8,  6.9,  7. ,  7.1,  7.2,  7.3,  7.4,  7.5,  7.6,
            7.7,  7.8,  7.9,  8. ,  8.1,  8.2,  8.3,  8.4,  8.5,  8.6,  8.7,
            8.8,  8.9,  9. ,  9.1,  9.2,  9.3,  9.4,  9.5,  9.6,  9.7,  9.8,
            9.9, 10. , 10.1, 10.2, 10.3, 10.4, 10.5, 10.6, 10.7, 10.8, 10.9,
           11. , 11.1, 11.2, 11.3, 11.4, 11.5, 11.6, 11.7, 11.8, 11.9, 12. ,
           12.1, 12.2, 12.3, 12.4, 12.5, 12.6, 12.7, 12.8, 12.9, 13. , 13.1,
           13.2, 13.3, 13.4, 13.5, 13.6, 13.7, 13.8, 13.9, 14. , 14.1, 14.2,
           14.3, 14.4, 14.5, 14.6, 14.7, 14.8, 14.9, 15. , 15.1, 15.2, 15.3,
           15.4, 15.5, 15.6, 15.7, 15.8, 15.9, 16. , 16.1, 16.2, 16.3, 16.4,
           16.5, 16.6, 16.7, 16.8, 16.9, 17. , 17.1, 17.2, 17.3, 17.4, 17.5,
           17.6, 17.7, 17.8, 17.9, 18. , 18.1, 18.2, 18.3, 18.4, 18.5, 18.6,
           18.7, 18.8, 18.9, 19. , 19.1, 19.2, 19.3, 19.4, 19.5, 19.6, 19.7,
           19.8, 19.9, 20. ])

    """
    from dspawpy.io.utils import get_absfile

    absfile = get_absfile(phonon_dos_dir, task="phonon_dos", verbose=verbose)
    if absfile.endswith(".h5"):
        dos = load_h5(absfile)
        frequencies = dos["/DosInfo/DosEnergy"]
        densities = dos["/DosInfo/Spin1/Dos"]
    elif absfile.endswith(".json"):
        with open(absfile) as fin:
            from json import load

            dos = load(fin)
        frequencies = dos["DosInfo"]["DosEnergy"]
        densities = dos["DosInfo"]["Spin1"]["Dos"]
    else:
        raise TypeError(f"{absfile} must be h5 or json file")

    from pymatgen.phonon.dos import PhononDos

    return PhononDos(frequencies, densities)


def get_sinfo(
    datafile: str,
    scaled: bool = False,
    si=None,
    ele=None,
    ai=None,
    verbose: bool = False,
):
    r"""从datafile中读取结构信息

    Parameters
    ----------
    datafile:
        h5 / json 文件路径
    scaled : bool, optional
        是否返回分数坐标，默认False
    si : int or list or str, optional
        运动轨迹中的第几步，从1开始计数！
        如果要切片，用字符串写法： '1, 10'
        默认为None，返回所有步
    ele : list, optional
        元素列表, Natom x 1
        默认为None，从h5文件中读取
    ai : int or list or str, optional
        多离子步中的第几个离子步，从1开始计数
        如果要切片，用字符串写法： '1, 10'
        默认为None，返回所有离子步

    Returns
    -------
    Nstep:
        总离子步数（几个构型）
    ele:
        元素列表, Natom x 1
    pos : np.ndarray
        坐标分量数组，Nstep x Natom x 3
    latv : np.ndarray
        晶胞矢量数组，Nstep x 3 x 3
    D_mag_fix:
        磁矩、自由度相关信息

    Examples
    --------
    >>> from dspawpy.io.read import get_sinfo
    >>> Nstep, elements, pos, latv, D_mag_fix = get_sinfo(datafile='dspawpy_proj/dspawpy_tests/inputs/2.18/aimd.h5', scaled=False, si=None, ele=None, ai=None)
    >>> Nstep, elements, pos, latv, D_mag_fix = get_sinfo(datafile='dspawpy_proj/dspawpy_tests/inputs/2.18/aimd.h5', scaled=True, si=[1,10], ele=None, ai=None)
    >>> Nstep, elements, pos, latv, D_mag_fix = get_sinfo(datafile='dspawpy_proj/dspawpy_tests/inputs/2.18/aimd.h5', scaled=True, si=2, ele=None, ai=None)
    >>> Nstep, elements, pos, latv, D_mag_fix = get_sinfo(datafile='dspawpy_proj/dspawpy_tests/inputs/2.18/aimd.h5', scaled=True, si='1:', ele=None, ai=None)
    >>> Nstep, elements, pos, latv, D_mag_fix = get_sinfo(datafile='dspawpy_proj/dspawpy_tests/inputs/2.18/aimd.h5', scaled=True, si=None, ele=['H', 'O'], ai=None)
    >>> Nstep, elements, pos, latv, D_mag_fix = get_sinfo(datafile='dspawpy_proj/dspawpy_tests/inputs/2.18/aimd.h5', scaled=True, si=None, ele='H', ai=None)
    >>> Nstep, elements, pos, latv, D_mag_fix = get_sinfo(datafile='dspawpy_proj/dspawpy_tests/inputs/2.18/aimd.h5', scaled=False, si=None, ele=None, ai=[1,2])
    >>> Nstep, elements, pos, latv, D_mag_fix = get_sinfo(datafile='dspawpy_proj/dspawpy_tests/inputs/2.18/aimd.h5', scaled=False, si=None, ele=None, ai=1)
    >>> Nstep, elements, pos, latv, D_mag_fix = get_sinfo(datafile='dspawpy_proj/dspawpy_tests/inputs/2.18/aimd.h5', scaled=False, si=None, ele=None, ai='1:')
    >>> Nstep, elements, pos, latv, D_mag_fix = get_sinfo(datafile='dspawpy_proj/dspawpy_tests/inputs/2.2/rho.h5', scaled=False)

    >>> Nstep, elements, pos, latv, D_mag_fix = get_sinfo(datafile='dspawpy_proj/dspawpy_tests/inputs/2.18/aimd.json', scaled=False, si=None, ele=None, ai=None)
    >>> Nstep, elements, pos, latv, D_mag_fix = get_sinfo(datafile='dspawpy_proj/dspawpy_tests/inputs/2.18/aimd.json', scaled=True, si=[1,10], ele=None, ai=None)
    >>> Nstep, elements, pos, latv, D_mag_fix = get_sinfo(datafile='dspawpy_proj/dspawpy_tests/inputs/2.18/aimd.json', scaled=True, si=2, ele=None, ai=None)
    >>> Nstep, elements, pos, latv, D_mag_fix = get_sinfo(datafile='dspawpy_proj/dspawpy_tests/inputs/2.18/aimd.json', scaled=True, si='1:', ele=None, ai=None)
    >>> Nstep, elements, pos, latv, D_mag_fix = get_sinfo(datafile='dspawpy_proj/dspawpy_tests/inputs/2.18/aimd.json', scaled=True, si=None, ele=['H', 'O'], ai=None)
    >>> Nstep, elements, pos, latv, D_mag_fix = get_sinfo(datafile='dspawpy_proj/dspawpy_tests/inputs/2.18/aimd.json', scaled=True, si=None, ele='H', ai=None)
    >>> Nstep, elements, pos, latv, D_mag_fix = get_sinfo(datafile='dspawpy_proj/dspawpy_tests/inputs/2.18/aimd.json', scaled=False, si=None, ele=None, ai=[1,2])
    >>> Nstep, elements, pos, latv, D_mag_fix = get_sinfo(datafile='dspawpy_proj/dspawpy_tests/inputs/2.18/aimd.json', scaled=False, si=None, ele=None, ai=1)
    >>> Nstep, elements, pos, latv, D_mag_fix = get_sinfo(datafile='dspawpy_proj/dspawpy_tests/inputs/2.18/aimd.json', scaled=False, si=None, ele=None, ai='1:')
    >>> Nstep, elements, pos, latv, D_mag_fix = get_sinfo(datafile='dspawpy_proj/dspawpy_tests/inputs/2.2/rho.json', scaled=False)

    这些信息可以用于进一步构建Structure对象，
    具体参考 dspawpy.io.structure.build_Structures_from_datafile 函数

    """
    assert (
        ele is None or ai is None
    ), "Cannot select element and atomic number at the same time"

    from dspawpy.io.utils import get_absfile

    absfile = get_absfile(datafile, task="free", verbose=verbose)
    import numpy as np

    D_mag_fix = {}
    if absfile.endswith(".h5"):
        from h5py import File

        hf = File(absfile)  # 加载h5文件

        # decide task type by check the internal key
        if "/Structures" in hf.keys():  # multi-steps
            Total_step = np.asarray(hf.get("/Structures/FinalStep"))[0]  # 总步数
            if f"/Structures/Step-{Total_step}" not in hf.keys():
                Total_step -= 1  # 最后一步可能还没保存

            if si is not None:  # 步数
                if isinstance(si, int):  # 1
                    indices = [si]

                elif isinstance(si, list) or isinstance(ai, np.ndarray):  # [1,2,3]
                    indices = si

                elif isinstance(si, str):  # ':', '1:'
                    indices = __parse_indices(si, Total_step)

                else:
                    raise ValueError("si=%s is invalid" % si)

                Nstep = len(indices)
            else:
                Nstep = Total_step
                indices = list(range(1, Nstep + 1))

            # 读取元素列表，这个列表不会随步数改变，也不会“合并同类项”
            Elements = np.asarray(get_ele_from_h5(absfile), dtype=object)

            # 开始读取晶胞和原子位置
            lattices = np.empty((Nstep, 3, 3))  # Nstep x 3 x 3
            location = []
            if ele is not None:  # 如果用户指定元素
                if isinstance(ele, str):  # 单个元素符号，例如 'Fe'
                    ele_list = np.asarray(ele, dtype=object)
                    location = np.where(Elements == ele_list)[0]
                # 多个元素符号组成的列表，例如 ['Fe', 'O']
                elif isinstance(ele, (list, np.ndarray)):
                    for e in ele:
                        loc = np.where(Elements == e)[0]
                        location.append(loc)
                    location = np.concatenate(location)
                else:
                    raise TypeError("ele=%s is invalid" % ele)
                elements = Elements[location]

            elif ai is not None:  # 如果用户指定原子序号
                if isinstance(ai, int):  # 1
                    ais = [ai]
                elif isinstance(ai, (list, np.ndarray)):  # [1,2,3]
                    ais = ai
                elif isinstance(ai, str):  # ':', '1:'
                    ais = __parse_indices(ai, len(Elements))
                else:
                    raise ValueError("ai=%s is invalid" % ai)
                ais = [i - 1 for i in ais]  # python从0开始计数，但是用户从1开始计数
                elements = Elements[ais]
                location = ais

            else:  # 如果都没指定
                elements = Elements
                location = list(range(len(Elements)))

            elements = elements.tolist()  # for pretty output
            Natom = len(elements)
            poses = np.empty(shape=(len(indices), Natom, 3))
            wrapped_poses = np.empty(shape=(len(indices), Natom, 3))
            for i, ind in enumerate(indices):  # 步数
                lats = np.asarray(hf.get("/Structures/Step-" + str(ind) + "/Lattice"))
                lattices[i] = lats
                # [x1,y1,z1,x2,y2,z2,x3,y3,z3], ...
                # 结构优化时输出的都是分数坐标，不管CoordinateType写的是啥！
                rawpos = np.asarray(
                    hf.get("/Structures/Step-" + str(ind) + "/Position"),
                )  # (3, Natom)
                pos = rawpos[:, location]
                wrapped_pos = pos - np.floor(pos)  # wrap into [0,1)
                wrapped_pos = wrapped_pos.flatten().reshape(-1, 3)
                wrapped_poses[i] = wrapped_pos

            if "/AtomInfo/Fix" in hf.keys():  # fix atom
                atomFixs_raw = np.asarray(hf.get("/AtomInfo/Fix"))
                atomfix = np.asarray(
                    ["True" if _v else "False" for _v in atomFixs_raw],
                ).reshape(-1, 3)
            else:
                atomfix = np.full(shape=(Natom, 3), fill_value="False")

            try:  # fix lattice
                latticeFixs = (
                    np.asarray(hf.get("/AtomInfo/FixLattice")).astype(bool).flatten()
                )
                assert latticeFixs.shape == (9,)
                latticeFixs = latticeFixs.reshape(
                    9,
                )  # (9,)
            except Exception as e:
                if str(e):  # ignore empty AssertionError()
                    print(e)
                latticeFixs = np.full(shape=(9,), fill_value="False")

            # iNoncollinear = False
            try:  # 自旋计算
                if "/MagInfo/TotalMagOnAtom" in hf.keys():  # collinear
                    mag = np.asarray(hf.get("/MagInfo/TotalMagOnAtom"))  # Natom x 1
                    mags = np.repeat(mag[np.newaxis, :], Nstep, axis=0).tolist()
                    D_mag_fix = {
                        "Mag": mags,
                    }
                elif "/MagInfo/TotalMagOnAtomX" in hf.keys():  # noncollinear
                    magx = np.asarray(hf.get("/MagInfo/TotalMagOnAtomX"))  # Natom x 1
                    magy = np.asarray(hf.get("/MagInfo/TotalMagOnAtomY"))  # Natom x 1
                    magz = np.asarray(hf.get("/MagInfo/TotalMagOnAtomZ"))  # Natom x 1
                    # iNoncollinear = True
                    D_mag_fix = {
                        "Mag_x": np.repeat(magx[np.newaxis, :], Nstep, axis=0).tolist(),
                        "Mag_y": np.repeat(magy[np.newaxis, :], Nstep, axis=0).tolist(),
                        "Mag_z": np.repeat(magz[np.newaxis, :], Nstep, axis=0).tolist(),
                    }
                else:
                    mag = np.zeros(shape=(Natom, 1))
                    mags = np.repeat(mag[np.newaxis, :], Nstep, axis=0).tolist()
                    D_mag_fix = {
                        "Mag": mags,
                    }

            except Exception as e:
                if str(e):  # ignore empty AssertionError()
                    print(e)
                mag = np.zeros(shape=(Natom, 1))

            # repeat atomFixs of shape Natom x 3 to Nstep x Natom x 3
            Atomfixs = np.repeat(atomfix[np.newaxis, :], Nstep, axis=0).reshape(
                Nstep,
                Natom,
                3,
            )
            D_mag_fix.update({"Fix_x": Atomfixs[:, :, 0].tolist()})
            D_mag_fix.update({"Fix_y": Atomfixs[:, :, 1].tolist()})
            D_mag_fix.update({"Fix_z": Atomfixs[:, :, 2].tolist()})

            # repeat latticeFixs of shape 9 x 1 to Nstep x Natom x 9
            latticeFixs = (
                np.repeat(latticeFixs[np.newaxis, :], Nstep * Natom, axis=0)
                .reshape(Nstep, Natom, 9)
                .tolist()
            )
            D_mag_fix.update({"FixLattice": latticeFixs})

            if scaled:  # Fractional coordinates
                for k, ind in enumerate(indices):  # 步数
                    poses[k] = wrapped_poses[k]
            else:  # Cartesian coordinates
                for k, ind in enumerate(indices):  # 步数
                    poses[k] = wrapped_poses[k] @ lattices[k]

        elif "/RelaxedStructure" in hf.keys():  # 最新NEB链
            raise NotImplementedError("neb.h5 is not supported yet")
        elif "/UnitAtomInfo" in hf.keys():  # phonon 仅读取单胞信息
            raise NotImplementedError("phonon.h5 is not supported yet")

        else:  # rho, potential, elf, pcharge
            hfDict = load_h5(absfile)
            s = _get_structure(hfDict, "/AtomInfo")
            elements = np.asarray(get_ele_from_h5(absfile), dtype=object)
            poses = [s.cart_coords]
            lattices = [s.lattice.matrix]
            Nstep = 1
            D_mag_fix = None

            logger.warning(
                "--> rho/potential/elf/pcharge.h5 has no mag or fix info,\n  you should manually set it if you are going to start new calculations..",
            )

    elif absfile.endswith(".json"):
        logger.warning(
            "float number in json has precision of 4 digits by default, which may cause inconsistency with h5/log file, you may use io.jsonPrec to adjust the precision",
            category=UserWarning,
        )
        with open(absfile) as f:
            from json import load

            data = load(f)  # 加载json文件

        # decide the task type by checking the internal keys
        if "AtomInfo" in data:  # single-step task
            s = _get_structure_json(data["AtomInfo"])
            elements = [str(i) for i in s.species]
            poses = [s.cart_coords]
            lattices = [s.lattice.matrix]
            Nstep = 1
            D_mag_fix = None

        elif "UnitAtomInfo" in data:  # phonon task
            raise NotImplementedError("Read from phonon.json is not supported yet.")
        elif "IniFin" in data:  # neb.json
            raise NotImplementedError("Read from neb.json is not supported yet.")
        elif "WannierInfo" in data:
            raise NotImplementedError("wannier.json has no structure info!")

        else:  # multi-steps task
            if "Structures" in data:
                Total_step = len(data["Structures"])  # aimd.json
            else:
                Total_step = len(data)  # relax.json, neb01.json

            if ele is not None and ai is not None:
                raise ValueError("Cannot specify both ele and ai")
            # 步数
            if si is not None:
                if isinstance(si, int):  # 1
                    indices = [si]

                elif isinstance(si, list) or isinstance(ai, np.ndarray):  # [1,2,3]
                    indices = si

                elif isinstance(si, str):  # ':', '-3:'
                    indices = __parse_indices(si, Total_step)

                else:
                    raise ValueError("si=%s is invalid" % si)

                Nstep = len(indices)
            else:
                Nstep = Total_step
                indices = list(range(1, Nstep + 1))  # [1,Nstep+1)

            # 预先读取全部元素的总列表，这个列表不会随步数改变，也不会“合并同类项”
            # 这样可以避免在循环内部频繁判断元素是否符合用户需要

            if "Structures" in data:
                Nele = len(data["Structures"][0]["Atoms"])  # relax.json
                total_elements = np.empty(
                    shape=(Nele),
                    dtype=object,
                )  # 未合并的元素列表
                for i in range(Nele):
                    element = data["Structures"][0]["Atoms"][i]["Element"]
                    total_elements[i] = element
            else:
                if "Atoms" not in data[0]:
                    raise NotImplementedError("nebXX.json has no structure info!")
                Nele = len(data[0]["Atoms"])
                total_elements = np.empty(
                    shape=(Nele),
                    dtype=object,
                )  # 未合并的元素列表
                for i in range(Nele):
                    element = data[0]["Atoms"][i]["Element"]
                    total_elements[i] = element

            Natom = len(total_elements)

            # 开始读取晶胞和原子位置
            # 在data['Structures']['%d' % index]['Atoms']中根据元素所在序号选择结构
            if ele is not None:  # 用户指定要某些元素
                location = []
                if isinstance(ele, str):  # 单个元素符号，例如 'Fe'
                    ele_list = list(ele)
                # 多个元素符号组成的列表，例如 ['Fe', 'O']
                elif isinstance(ele, (list, np.ndarray)):
                    ele_list = ele
                else:
                    raise TypeError("ele=%s is invalid" % ele)
                for e in ele_list:
                    location.append(np.where(total_elements == e)[0])
                location = np.concatenate(location)

            elif ai is not None:  # 如果用户指定原子序号，也要据此筛选元素列表
                if isinstance(ai, int):  # 1
                    ais = [ai]
                elif isinstance(ai, (list, np.ndarray)):  # [1,2,3]
                    ais = ai
                elif isinstance(ai, str):  # ':', '-3:'
                    ais = __parse_indices(ai, Natom)
                else:
                    raise ValueError("ai=%s is invalid" % ai)
                ais = [i - 1 for i in ais]  # python从0开始计数，但是用户从1开始计数
                location = ais
                # read lattices and poses

            else:  # 如果都没指定
                location = list(range(Natom))

            # 满足用户需要的elements列表
            elements = total_elements[location]

            # Nstep x Natom x 3, positions are all fractional
            poses = np.empty(shape=(len(indices), len(elements), 3))
            lattices = np.empty(shape=(Nstep, 3, 3))  # Nstep x 3 x 3
            mags = []  # Nstep x Natom x ?
            Atomfixs = []  # Nstep x Natom x 1
            LatFixs = []  # Nstep x Natom x 9

            if "Structures" in data:  # aimd
                for i, ind in enumerate(indices):  # for every ionic step
                    lat = data["Structures"][ind - 1]["Lattice"]
                    lattices[i] = np.asarray(lat).reshape(3, 3)
                    mag_for_each_step = []
                    fix_for_each_step = []
                    if "FixLattice" in data["Structures"][ind - 1]:
                        fixlat_raw = data["Structures"][ind - 1]["FixLattice"]
                    else:
                        fixlat_raw = []
                    if fixlat_raw == []:
                        fixlat_raw = np.full((9, 1), fill_value=False).tolist()
                    fixlat_str = [
                        "True" if _v is True else "False" for _v in fixlat_raw
                    ]
                    fixlat_arr = np.asarray(fixlat_str).reshape(9, 1)
                    # repeat fixlat for each atom
                    fixlat = np.repeat(fixlat_arr, Natom, axis=1).T.tolist()
                    LatFixs.append(fixlat)
                    for j, sli in enumerate(location):
                        ati = data["Structures"][ind - 1]["Atoms"][sli]
                        poses[i, j, :] = ati["Position"][:]

                        mag_for_each_atom = ati["Mag"][:]
                        if mag_for_each_atom == []:
                            mag_for_each_atom = [0.0]
                        mag_for_each_step.append(mag_for_each_atom)

                        fix_for_each_atom = ati["Fix"][:]
                        if fix_for_each_atom == []:
                            fix_for_each_atom = ["False"]
                        fix_for_each_step.append(fix_for_each_atom)

                    mags.append(mag_for_each_step)
                    Atomfixs.append(fix_for_each_step)
                    if not scaled:
                        poses[i] = np.dot(poses[i], lattices[i])

            else:  # relax, neb01
                logger.warning(
                    "mag and fix info are not available for relax.json and nebXX.json yet, trying read info...",
                    category=UserWarning,
                )

                for i, ind in enumerate(indices):  # for every ionic step
                    lat = data[ind - 1]["Lattice"]
                    lattices[i] = np.asarray(lat).reshape(3, 3)
                    mag_for_each_step = []
                    fix_for_each_step = []
                    if "FixLattice" in data[ind - 1]:
                        fixlat_raw = data[ind - 1]["FixLattice"]
                        if fixlat_raw is None:
                            fixlat_raw = np.full((9, 1), fill_value=False).tolist()
                        fixlat_str = [
                            "True" if _v is True else "False" for _v in fixlat_raw
                        ]
                        fixlat_arr = np.asarray(fixlat_str).reshape(9, 1)
                        # repeat fixlat for each atom
                        fixlat = np.repeat(fixlat_arr, Natom, axis=1).T.tolist()
                    else:
                        fixlat = np.full((Natom, 9), fill_value=False).tolist()

                    LatFixs.append(fixlat)
                    for j, sli in enumerate(location):
                        ati = data[ind - 1]["Atoms"][sli]
                        poses[i, j, :] = ati["Position"][:]

                        mag_for_each_atom = ati["Mag"][:]
                        if mag_for_each_atom == []:
                            mag_for_each_atom = [0.0]
                        mag_for_each_step.append(mag_for_each_atom)

                        fix_for_each_atom = ati["Fix"][:]
                        if fix_for_each_atom == []:
                            fix_for_each_atom = ["False"]
                        fix_for_each_step.append(fix_for_each_atom)

                    mags.append(mag_for_each_step)
                    Atomfixs.append(fix_for_each_step)
                    if not scaled:
                        poses[i] = np.dot(poses[i], lattices[i])

            elements = elements.tolist()
            Mags = np.asarray(mags).tolist()  # (Nstep, Natom, ?) or (Nstep, 0,)

            D_mag_fix = {"Mag": Mags, "Fix": Atomfixs, "LatticeFixs": LatFixs}

    else:
        raise ValueError(
            "get_sinfo function only accept datafile of .h5 / .json format!",
        )

    return Nstep, elements, poses, lattices, D_mag_fix


def load_h5(dir_h5: str) -> dict:
    """遍历读取h5文件中的数据，保存为字典格式

    慎用此函数，因为会读取很多不需要的数据，耗时很长。

    Parameters
    ----------
    dir_h5:
        h5文件路径

    Returns
    -------
    data:
        数据字典

    Examples
    --------
    >>> from dspawpy.io.read import load_h5
    >>> data = load_h5(dir_h5='dspawpy_proj/dspawpy_tests/inputs/2.2/scf.h5')
    >>> data.keys()
    dict_keys(['/AtomInfo/CoordinateType', '/AtomInfo/Elements', '/AtomInfo/Grid', '/AtomInfo/Lattice', '/AtomInfo/Position', '/Eigenvalue/CBM/BandIndex', '/Eigenvalue/CBM/Energy', '/Eigenvalue/CBM/Kpoint', '/Eigenvalue/NumberOfBand', '/Eigenvalue/Spin1/BandEnergies', '/Eigenvalue/Spin1/Kpoints/Coordinates', '/Eigenvalue/Spin1/Kpoints/Grid', '/Eigenvalue/Spin1/Kpoints/NumberOfKpoints', '/Eigenvalue/Spin1/Occupation', '/Eigenvalue/VBM/BandIndex', '/Eigenvalue/VBM/Energy', '/Eigenvalue/VBM/Kpoint', '/Electron', '/Energy/EFermi', '/Energy/TotalEnergy', '/Energy/TotalEnergy0', '/Force/ForceOnAtoms', '/Stress/Direction', '/Stress/Pressure', '/Stress/Stress', '/Stress/Total', '/Structures/FinalStep', '/Structures/Step-1/Lattice', '/Structures/Step-1/Position'])

    """

    def get_names(key, h5_object):
        names.append(h5_object.name)

    def is_dataset(name):
        for name_inTheList in names:
            if name_inTheList.find(name + "/") != -1:
                return False
        return True

    import numpy as np

    def get_data(key, h5_object):
        if is_dataset(h5_object.name):
            _data = np.asarray(h5_object)
            if _data.dtype == "|S1":  # 转成字符串 并根据";"分割
                byte2str = [str(bi, "utf-8") for bi in _data]
                string = ""
                for char in byte2str:
                    string += char
                _data = np.asarray([elem for elem in string.strip().split(";")])
            # "/group1/group2/.../groupN/dataset" : value
            data[h5_object.name] = _data.tolist()

    import os

    from h5py import File

    with File(os.path.abspath(dir_h5), "r") as fin:
        names = []
        data = {}
        fin.visititems(get_names)
        fin.visititems(get_data)

        return data


def __parse_indices(index: str, maxIndex: int) -> list:
    """解析用户输入的原子、结构序号字符串

    输入：
        - index: 用户输入的原子序号/元素字符串，例如 '1:3,5,7:10'
        - maxIndex: 最大序号，例如 10
    输出：
        - indices: 解析后的原子序号列表，例如 [1,2,3,4,5,6,7,8,9,10]
    """
    assert (
        ":" in index
    ), "If you don't want to slice the index, please enter an integer or a list"
    blcs = index.split(",")
    indices = []
    for blc in blcs:
        if ":" in blc:  # 切片
            low = blc.split(":")[0]
            if not low:
                low = 1  # 从1开始
            else:
                low = int(low)
                assert low > 0, "Index start at 1!"
            high = blc.split(":")[1]
            if not high:
                high = maxIndex
            else:
                high = int(high)
                assert high <= maxIndex, "Index too large!"

            for i in range(low, high + 1):
                indices.append(i)
        else:  # 单个数字
            indices.append(int(blc))
    return indices


def _get_lammps_non_orthogonal_box(lat: Sequence):
    """计算用于输入lammps的盒子边界参数，用于生成dump结构文件

    Parameters
    ----------
    lat : np.ndarray
        常见的非三角3x3矩阵

    Returns
    -------
    box_bounds:
        用于输入lammps的盒子边界

    """
    # https://docs.lammps.org/Howto_triclinic.html
    A = lat[0]
    B = lat[1]
    C = lat[2]
    import numpy as np

    assert np.cross(A, B).dot(C) > 0, "Lat is not right handed"

    # 将常规3x3矩阵转成标准的上三角矩阵
    alpha = np.arccos(np.dot(B, C) / (np.linalg.norm(B) * np.linalg.norm(C)))
    beta = np.arccos(np.dot(A, C) / (np.linalg.norm(A) * np.linalg.norm(C)))
    gamma = np.arccos(np.dot(A, B) / (np.linalg.norm(A) * np.linalg.norm(B)))

    ax = np.linalg.norm(A)
    a = np.asarray([ax, 0, 0])

    bx = np.linalg.norm(B) * np.cos(gamma)
    by = np.linalg.norm(B) * np.sin(gamma)
    b = np.asarray([bx, by, 0])

    cx = np.linalg.norm(C) * np.cos(beta)
    cy = (np.linalg.norm(B) * np.linalg.norm(C) - bx * cx) / by
    cz = np.sqrt(abs(np.linalg.norm(C) ** 2 - cx**2 - cy**2))
    c = np.asarray([cx, cy, cz])

    # triangluar matrix in lammmps cell format
    # note that in OVITO, it will be down-triangular one
    # lammps_lattice = np.asarray([a,b,c]).T

    # write lammps box parameters
    # https://docs.lammps.org/Howto_triclinic.html#:~:text=The%20inverse%20relationship%20can%20be%20written%20as%20follows
    lx = np.linalg.norm(a)
    xy = np.linalg.norm(b) * np.cos(gamma)
    xz = np.linalg.norm(c) * np.cos(beta)
    ly = np.sqrt(np.linalg.norm(b) ** 2 - xy**2)
    yz = (np.linalg.norm(b) * np.linalg.norm(c) * np.cos(alpha) - xy * xz) / ly
    lz = np.sqrt(np.linalg.norm(c) ** 2 - xz**2 - yz**2)

    # "The parallelepiped has its “origin” at (xlo,ylo,zlo) and is defined by 3 edge vectors starting from the origin given by a = (xhi-xlo,0,0); b = (xy,yhi-ylo,0); c = (xz,yz,zhi-zlo)."
    # 令原点在(0,0,0)，则 xlo = ylo = zlo = 0
    xlo = ylo = zlo = 0
    # https://docs.lammps.org/Howto_triclinic.html#:~:text=the%20LAMMPS%20box%20sizes%20(lx%2Cly%2Clz)%20%3D%20(xhi%2Dxlo%2Cyhi%2Dylo%2Czhi%2Dzlo)
    xhi = lx + xlo
    yhi = ly + ylo
    zhi = lz + zlo
    # https://docs.lammps.org/Howto_triclinic.html#:~:text=This%20bounding%20box%20is%20convenient%20for%20many%20visualization%20programs%20and%20is%20calculated%20from%20the%209%20triclinic%20box%20parameters%20(xlo%2Cxhi%2Cylo%2Cyhi%2Czlo%2Czhi%2Cxy%2Cxz%2Cyz)%20as%20follows%3A
    xlo_bound = xlo + np.min([0, xy, xz, xy + xz])
    xhi_bound = xhi + np.max([0, xy, xz, xy + xz])
    ylo_bound = ylo + np.min([0, yz])
    yhi_bound = yhi + np.max([0, yz])
    zlo_bound = zlo
    zhi_bound = zhi
    box_bounds = np.asarray(
        [
            [xlo_bound, xhi_bound, xy],
            [ylo_bound, yhi_bound, xz],
            [zlo_bound, zhi_bound, yz],
        ],
    )

    return box_bounds


def _get_total_dos(dos: dict):
    # h5 -> Dos Obj
    import numpy as np

    energies = np.asarray(dos["/DosInfo/DosEnergy"])
    from pymatgen.electronic_structure.core import Spin

    if dos["/DosInfo/SpinType"][0] != "collinear":
        densities = {Spin.up: np.asarray(dos["/DosInfo/Spin1/Dos"])}
    else:
        densities = {
            Spin.up: np.asarray(dos["/DosInfo/Spin1/Dos"]),
            Spin.down: np.asarray(dos["/DosInfo/Spin2/Dos"]),
        }

    efermi = dos["/DosInfo/EFermi"][0]

    from pymatgen.electronic_structure.dos import Dos

    return Dos(efermi, energies, densities)


def _get_total_dos_json(dos: dict):
    # json -> Dos Obj
    import numpy as np

    energies = np.asarray(dos["DosInfo"]["DosEnergy"])
    from pymatgen.electronic_structure.core import Spin

    if dos["DosInfo"]["SpinType"] != "collinear":
        densities = {Spin.up: np.asarray(dos["DosInfo"]["Spin1"]["Dos"])}
    else:
        densities = {
            Spin.up: np.asarray(dos["DosInfo"]["Spin1"]["Dos"]),
            Spin.down: np.asarray(dos["DosInfo"]["Spin2"]["Dos"]),
        }
    efermi = dos["DosInfo"]["EFermi"]
    from pymatgen.electronic_structure.dos import Dos

    return Dos(efermi, energies, densities)


def _get_complete_dos(dos: dict):
    # h5 -> CompleteDos Obj
    total_dos = _get_total_dos(dos)
    structure = _get_structure(dos, "/AtomInfo")
    N = len(structure)
    pdos = [{} for i in range(N)]
    number_of_spin = 2 if dos["/DosInfo/SpinType"][0] == "collinear" else 1

    from pymatgen.electronic_structure.core import Orbital, Spin

    for i in range(number_of_spin):
        spin_key = "Spin" + str(i + 1)
        spin = Spin.up if i == 0 else Spin.down
        if dos["/DosInfo/Project"][0]:
            atomindexs = dos["/DosInfo/" + spin_key + "/ProjectDos/AtomIndexs"][0]
            orbitindexs = dos["/DosInfo/" + spin_key + "/ProjectDos/OrbitIndexs"][0]
            for atom_index in range(atomindexs):
                for orbit_index in range(orbitindexs):
                    orbit_name = Orbital(orbit_index)
                    Contribution = dos[
                        "/DosInfo/"
                        + spin_key
                        + "/ProjectDos"
                        + str(atom_index + 1)
                        + "/"
                        + str(orbit_index + 1)
                    ]
                    if orbit_name in pdos[atom_index].keys():
                        pdos[atom_index][orbit_name].update({spin: Contribution})
                    else:
                        pdos[atom_index][orbit_name] = {spin: Contribution}

            pdoss = {structure[i]: pd for i, pd in enumerate(pdos)}
        else:
            pdoss = {}

    from pymatgen.electronic_structure.dos import CompleteDos

    return CompleteDos(structure, total_dos, pdoss)  # type: ignore


def _get_complete_dos_json(dos: dict):
    # json -> CompleteDos Obj
    total_dos = _get_total_dos_json(dos)
    structure = _get_structure_json(dos["AtomInfo"])
    N = len(structure)
    pdos = [{} for i in range(N)]
    number_of_spin = 2 if dos["DosInfo"]["SpinType"] == "collinear" else 1

    from pymatgen.electronic_structure.core import Orbital, Spin

    for i in range(number_of_spin):
        spin_key = "Spin" + str(i + 1)
        spin = Spin.up if i == 0 else Spin.down
        if dos["DosInfo"]["Project"]:
            project = dos["DosInfo"][spin_key]["ProjectDos"]
            for p in project:
                atom_index = p["AtomIndex"] - 1
                o = p["OrbitIndex"] - 1
                orbit_name = Orbital(o)
                if orbit_name in pdos[atom_index].keys():
                    pdos[atom_index][orbit_name].update({spin: p["Contribution"]})
                else:
                    pdos[atom_index][orbit_name] = {spin: p["Contribution"]}
            pdoss = {structure[i]: pd for i, pd in enumerate(pdos)}
        else:
            pdoss = {}

    from pymatgen.electronic_structure.dos import CompleteDos

    return CompleteDos(structure, total_dos, pdoss)  # type: ignore


def _get_structure(hdf5: dict, key: str):
    """For single-step task"""
    # load_h5 -> Structure Obj
    import numpy as np

    lattice = np.asarray(hdf5[key + "/Lattice"]).reshape(3, 3)
    elements = hdf5[key + "/Elements"]
    positions = hdf5[key + "/Position"]
    coords = np.asarray(positions).reshape(-1, 3)
    is_direct = hdf5[key + "/CoordinateType"][0] == "Direct"
    import re

    elements = [re.sub(r"_", "", e) for e in elements]

    from pymatgen.core.structure import Structure

    return Structure(lattice, elements, coords, coords_are_cartesian=(not is_direct))


def _get_structure_json(atominfo: dict):
    """For single-step task"""
    import numpy as np

    lattice = np.asarray(atominfo["Lattice"]).reshape(3, 3)
    elements = []
    positions = []
    for atom in atominfo["Atoms"]:
        elements.append(atom["Element"])
        positions.extend(atom["Position"])

    coords = np.asarray(positions).reshape(-1, 3)
    is_direct = atominfo["CoordinateType"] == "Direct"
    import re

    elements = [re.sub(r"_", "", e) for e in elements]

    from pymatgen.core.structure import Structure

    return Structure(lattice, elements, coords, coords_are_cartesian=(not is_direct))


def _get_band_data_h5(band: dict, iwan: bool = False, zero_to_efermi: bool = False):
    if iwan:
        bd = "WannBandInfo"
    else:
        bd = "BandInfo"
    number_of_band = band[f"/{bd}/NumberOfBand"][0]
    number_of_kpoints = band[f"/{bd}/NumberOfKpoints"][0]
    if band[f"/{bd}/SpinType"][0] != "collinear":
        number_of_spin = 1
    else:
        number_of_spin = 2

    symmetry_kPoints_index = band[f"/{bd}/SymmetryKPointsIndex"]

    efermi = band[f"/{bd}/EFermi"][0]
    eigenvals = {}
    import numpy as np
    from pymatgen.electronic_structure.core import Spin

    for i in range(number_of_spin):
        spin_key = "Spin" + str(i + 1)
        spin = Spin.up if i == 0 else Spin.down

        if f"/{bd}/" + spin_key + "/BandEnergies" in band:
            data = band[f"/{bd}/" + spin_key + "/BandEnergies"]
        elif f"/{bd}/" + spin_key + "/Band" in band:
            data = band[f"/{bd}/" + spin_key + "/Band"]
        else:
            raise KeyError("Band key error")
        band_data = np.asarray(data).reshape((number_of_kpoints, number_of_band)).T

        if zero_to_efermi:
            eigenvals[spin] = band_data - efermi
        else:
            eigenvals[spin] = band_data

    kpoints = np.asarray(band[f"/{bd}/CoordinatesOfKPoints"]).reshape(
        number_of_kpoints,
        3,
    )

    structure = _get_structure(band, "/AtomInfo")
    labels_dict = {}

    for i, s in enumerate(band[f"/{bd}/SymmetryKPoints"]):
        labels_dict[s] = kpoints[symmetry_kPoints_index[i] - 1]

    # read projection data
    projections = None
    if f"/{bd}/IsProject" in band:
        if band[f"/{bd}/IsProject"][0]:
            projections = {}
            number_of_orbit = len(band[f"/{bd}/Orbit"])
            projection = np.zeros(
                (number_of_band, number_of_kpoints, number_of_orbit, len(structure)),
            )

            for i in range(number_of_spin):
                spin_key = "Spin" + str(i + 1)
                spin = Spin.up if i == 0 else Spin.down

                atomindexs = band[f"/{bd}/" + spin_key + "/ProjectBand/AtomIndex"][0]
                orbitindexs = band[f"/{bd}/" + spin_key + "/ProjectBand/OrbitIndexs"][0]
                for atom_index in range(atomindexs):
                    for orbit_index in range(orbitindexs):
                        project_data = band[
                            f"/{bd}/"
                            + spin_key
                            + "/ProjectBand/1/"
                            + str(atom_index + 1)
                            + "/"
                            + str(orbit_index + 1)
                        ]
                        projection[:, :, orbit_index, atom_index] = (
                            np.asarray(project_data)
                            .reshape((number_of_kpoints, number_of_band))
                            .T
                        )
                projections[spin] = projection

    if zero_to_efermi:
        efermi = 0  # set to 0

    return structure, kpoints, eigenvals, efermi, labels_dict, projections


def _get_band_data_json(
    band: dict,
    syst: Optional[dict] = None,
    iwan: bool = False,
    zero_to_efermi: bool = False,
):
    # syst is only required for wannier band structure
    if iwan:
        bd = "WannBandInfo"
        assert syst is not None, "syst is required for wannier band structure"
        efermi = syst["Energy"]["EFermi"]
        structure = _get_structure_json(syst["AtomInfo"])
    else:
        bd = "BandInfo"
        if "EFermi" in band[bd]:
            efermi = band[bd]["EFermi"]
        else:
            logger.warning("EFermi not found in band data, set to 0")
            efermi = 0
        structure = _get_structure_json(band["AtomInfo"])

    number_of_band = band[bd]["NumberOfBand"]
    number_of_kpoints = band[bd]["NumberOfKpoints"]
    # ! wannier.json has no SpinType key
    # if band[bd]["SpinType"][0] != "collinear":
    if "Spin2" not in band[bd]:
        number_of_spin = 1
    else:
        number_of_spin = 2

    symmetry_kPoints_index = band[bd]["SymmetryKPointsIndex"]
    eigenvals = {}
    import numpy as np
    from pymatgen.electronic_structure.core import Spin

    for i in range(number_of_spin):
        spin_key = "Spin" + str(i + 1)
        spin = Spin.up if i == 0 else Spin.down

        if "BandEnergies" in band[bd][spin_key]:
            data = band[bd][spin_key]["BandEnergies"]
        elif "Band" in band[bd][spin_key]:
            data = band[bd][spin_key]["Band"]
        else:
            raise KeyError("Band key error")

        band_data = np.asarray(data).reshape((number_of_kpoints, number_of_band)).T

        if zero_to_efermi:
            eigenvals[spin] = band_data - efermi

        else:
            eigenvals[spin] = band_data

    kpoints = np.asarray(band[bd]["CoordinatesOfKPoints"]).reshape(number_of_kpoints, 3)

    labels_dict = {}

    for i, s in enumerate(band[bd]["SymmetryKPoints"]):
        labels_dict[s] = kpoints[symmetry_kPoints_index[i] - 1]

    # read projection data
    projections = None
    if "IsProject" in band[bd].keys():
        if band[bd]["IsProject"]:
            projections = {}
            number_of_orbit = len(band[bd]["Orbit"])
            projection = np.zeros(
                (number_of_band, number_of_kpoints, number_of_orbit, len(structure)),
            )

            for i in range(number_of_spin):
                spin_key = "Spin" + str(i + 1)
                spin = Spin.up if i == 0 else Spin.down

                data = band[bd][spin_key]["ProjectBand"]
                for d in data:
                    orbit_index = d["OrbitIndex"] - 1
                    atom_index = d["AtomIndex"] - 1
                    project_data = d["Contribution"]
                    projection[:, :, orbit_index, atom_index] = (
                        np.asarray(project_data)
                        .reshape((number_of_kpoints, number_of_band))
                        .T
                    )
                projections[spin] = projection

    if zero_to_efermi:
        logger.warning("Setting efemi to 0 because zero_to_efermi is True")
        efermi = 0  # set to 0

    return structure, kpoints, eigenvals, efermi, labels_dict, projections


def _get_phonon_band_data_h5(band: dict):
    import numpy as np

    number_of_band = band["/BandInfo/NumberOfBand"][0]
    number_of_qpoints = band["/BandInfo/NumberOfQPoints"][0]
    symmmetry_qpoints = band["/BandInfo/SymmetryQPoints"]
    symmetry_qPoints_index = band["/BandInfo/SymmetryQPointsIndex"]
    qpoints = np.asarray(band["/BandInfo/CoordinatesOfQPoints"]).reshape(
        number_of_qpoints,
        3,
    )
    if "/SupercellAtomInfo/CoordinateType" in band:
        structure = _get_structure(band, "/SupercellAtomInfo")
    else:
        structure = _get_structure(band, "/AtomInfo")

    spin_key = "Spin1"
    if "/BandInfo/" + spin_key + "/BandEnergies" in band:
        data = band["/BandInfo/" + spin_key + "/BandEnergies"]
    elif "/BandInfo/" + spin_key + "/Band" in band:
        data = band["/BandInfo/" + spin_key + "/Band"]
    else:
        raise KeyError("Band key error")
    frequencies = np.asarray(data).reshape((number_of_qpoints, number_of_band)).T

    return symmmetry_qpoints, symmetry_qPoints_index, qpoints, structure, frequencies


def _get_phonon_band_data_json(band: dict):
    import numpy as np

    number_of_band = band["BandInfo"]["NumberOfBand"]
    number_of_qpoints = band["BandInfo"]["NumberOfQPoints"]

    symmmetry_qpoints = band["BandInfo"]["SymmetryQPoints"]
    symmetry_qPoints_index = band["BandInfo"]["SymmetryQPointsIndex"]
    qpoints = np.asarray(band["BandInfo"]["CoordinatesOfQPoints"]).reshape(
        number_of_qpoints,
        3,
    )
    if "SupercellAtomInfo" in band:
        structure = _get_structure_json(band["SupercellAtomInfo"])
    else:
        structure = _get_structure_json(band["AtomInfo"])

    spin_key = "Spin1"
    if "BandEnergies" in band["BandInfo"][spin_key]:
        data = band["BandInfo"][spin_key]["BandEnergies"]
    elif "Band" in band["BandInfo"][spin_key]:
        data = band["BandInfo"][spin_key]["Band"]
    else:
        raise KeyError("Band key error")
    frequencies = np.asarray(data).reshape((number_of_qpoints, number_of_band)).T

    return symmmetry_qpoints, symmetry_qPoints_index, qpoints, structure, frequencies
