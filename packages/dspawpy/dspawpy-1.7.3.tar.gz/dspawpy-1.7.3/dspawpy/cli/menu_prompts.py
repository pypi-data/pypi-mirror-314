menus = {
    "CN": {
        0: """
======================================
|  1: update更新
|  2: structure结构转化
|  3: volumetricData数据处理
|  4: band能带数据处理
|  5: dos态密度数据处理
|  6: bandDos能带和态密度共同显示
|  7: optical光学性质数据处理
|  8: neb过渡态计算数据处理
|  9: phonon声子计算数据处理
|  10: aimd分子动力学模拟数据处理
|  11: Polarization铁电极化数据处理
|  12: ZPE零点振动能数据处理
|  13: TS的热校正能
|  14: relaxation结构优化日志分析
|  15: hdf5文件探索
|
|  q: 退出
======================================
--> 输入数字后回车选择功能：""",
        3: """
=== 3 volumetricData数据处理 ===

1: volumetricData可视化
2: 差分volumetricData可视化
3: volumetricData面平均

0: 返回主菜单
--> 输入数字后回车选择功能：""",
        4: """
=== 4 band能带数据处理 ===

1: 普通能带
2: 将能带投影到每一种元素分别作图，数据点大小表示该元素对该轨道的贡献
3: 能带投影到不同元素的不同轨道
4: 将能带投影到不同原子的不同轨道
5: 能带反折叠处理
6. band-compare能带对比图处理

0: 返回主菜单
--> 输入数字后回车选择功能：""",
        5: """
=== 5 dos态密度数据处理 ===

1: 总的态密度
2: 将态密度投影到不同的轨道上
3: 将态密度投影到不同的元素上
4: 将态密度投影到不同原子的不同轨道上
5: 将态密度投影到不同原子的分裂d轨道(t2g, eg)上
6: d-带中心分析

0: 返回主菜单
--> 输入数字后回车选择功能：""",
        6: """
=== 6 bandDos能带和态密度共同显示 ===

1: 将能带和态密度显示在一张图上
2: 将能带和投影态密度显示在一张图上

0: 返回主菜单
--> 输入数字后回车选择功能：""",
        8: """
=== 8 neb过渡态计算数据处理 ===

1: 输入文件之生成中间构型
2: 绘制能垒图
3: 过渡态计算概览
4: NEB链可视化
5: 计算构型间距
6: neb续算
7: neb计算过程中能量、受力等变化曲线

0: 返回主菜单
--> 输入数字后回车选择功能：""",
        9: """
=== 9 phonon声子计算数据处理 ===

1: 声子能带数据处理
2: 声子态密度数据处理
3: 声子热力学数据处理

0: 返回主菜单
--> 输入数字后回车选择功能：""",
        10: """
=== 10 aimd分子动力学模拟数据处理 ===

1: 轨迹文件转换格式为.xyz或.dump
2: 动力学过程中能量、温度等变化曲线
3: 均方位移（MSD）
4. 均方根偏差（RMSD）
5. 径向分布函数（RDF）

0: 返回主菜单
--> 输入数字后回车选择功能：""",
        13: """
=== 13 TS的热校正能 ===

1: 吸附质
2: 理想气体

0: 返回主菜单
--> 输入数字后回车选择功能：""",
        15: """
=== 15 hdf5文件探索 ===

1. 数据结构
2. 数据查看

0: 返回主菜单
--> 输入数字后回车选择功能：""",
    },
    "EN": {
        0: """
====================================
|  1: dspawpy upgrading
|  2: structure file transforming
|  3: volumetric data processing
|  4: band plotting
|  5: dos plotting
|  6: bandDos aligned plotting
|  7: optical data processing
|  8: neb pre&post processing
|  9: phonon data processing
|  10: aimd data processing
|  11: polarization data processing
|  12: ZPE correction
|  13: entropy correction
|  14: relaxtion log file analysis
|  15: hdf5 file exploration
|
|  q: quit
====================================

--> enter a number and press 'Enter' to select corresponding action: """,
        3: """
=== 3 volumetric data processing ===

1: volumetricData visualization
2: volumetricData difference visualization
3: planer averaged volumetricData

0: return to main menu
--> enter a number and press 'Enter' to select corresponding action: """,
        4: """
=== 4 band plotting ===

1: regular band plotting
2: element projected band plotting (contributions are represented by point size)
3: element's orbital projected band plotting (contributions are represented by point size)
4: atom's orbital projected band plotting (contributions are represented by point size)
5: band unfolding plotting
6. band-compare plotting

0: return to main menu
--> enter a number and press 'Enter' to select corresponding action: """,
        5: """
=== 5 dos plotting ===

1: total dos plotting
2: orbital projected dos plotting
3: element projected dos plotting
4: atom's orbital projected dos plotting
5: atom's split d orbital (t2g, eg) projected dos plotting
6: d-band center analysis

0: return to main menu
--> enter a number and press 'Enter' to select corresponding action: """,
        6: """
=== 6 bandDos aligned plotting ===

1: regular band and total dos aligned plotting
2: regular band and projected dos aligned plotting

0: return to main menu
--> enter a number and press 'Enter' to select corresponding action: """,
        8: """
=== 8 neb calculation pre&post processing ===

1: input structure file preparing : structure interpolation
2: barrier plotting
3: NEB calculation inspecting
4: NEB movie
5: root mean square displacement between structures calculating
6: neb restarting
7: neb calculation monitoring: energy, force...

0: return to main menu
--> enter a number and press 'Enter' to select corresponding action: """,
        9: """
=== 9 phonon calculation post processing ===

1: phonon band plotting
2: phonon dos plotting
3: thermo data from phonon

0: return to main menu
--> enter a number and press 'Enter' to select corresponding action: """,
        10: """
=== 10 aimd calculation post processing ===

1: trajectory file transforming
2: calculation monitoring: energy, temperature, volume...
3: MSD deriving
4. RMSD deriving
5. RDF deriving

0: return to main menu
--> enter a number and press 'Enter' to select corresponding action: """,
        13: """
=== 13 entropy thermal correction ===

1: adsorption entropy correction
2: ideal gas entropy correction

0: return to main menu
--> enter a number and press 'Enter' to select corresponding action: """,
        15: """
=== 15 hdf5 file exploration ===

1. data structure
2. data viewing

0: return to main menu
--> enter a number and press 'Enter' to select corresponding action: """,
    },
}

logo = {
    "CN": r"""
********这是dspawpy命令行交互小工具，预祝您使用愉快********
    ( )
   _| |  ___  _ _      _ _  _   _   _  _ _    _   _
 /'_` |/',__)( '_`\  /'_` )( ) ( ) ( )( '_`\ ( ) ( )
( (_| |\__, \| (_) )( (_| || \_/ \_/ || (_) )| (_) |
 \__,_)(____/| ,__/'`\__,_) \___x___/ | ,__/  \__, |
             | |                      | |    ( )_| |
             (_)                      (_)     \___/
""",
    "EN": r"""
This is a command line interactive tool based on dspawpy, enjoy
    ( )
   _| |  ___  _ _      _ _  _   _   _  _ _    _   _
 /'_` |/',__)( '_`\  /'_` )( ) ( ) ( )( '_`\ ( ) ( )
( (_| |\__, \| (_) )( (_| || \_/ \_/ || (_) )| (_) |
`\__,_)(____/| ,__/'`\__,_)`\___x___/'| ,__/'`\__, |
             | |                      | |    ( )_| |
             (_)                      (_)    `\___/'
""",
}

Dupdate = {
    "CN": [
        "更新dspawpy将执行",
        "执行成功",
        "请重新运行程序，使安装生效",
        "执行失败",
    ],
    "EN": [
        "To update dspawpy, will run",
        "Success",
        "Please re-run this cli to use new version",
        "Failed",
    ],
}


Dcheck = {
    "CN": [
        "正在联网检查dspawpy版本... 使用 -s True 启动可跳过",
        "无法导入 requests 库",
        "requests联网检查dspawpy版本超时",
        "requests联网检查dspawpy版本时出现异常: ",
        "联网检查dspawpy版本失败: ",
        "最新版本号 > 当前导入的，可使用功能1升级",
        "最新版本号 = 当前导入的",
        "联网检查失败，请确认网络连接是否正常",
    ],
    "EN": [
        "Checking dspawpy version online... Use -s True to skip",
        "Unable to import requests library",
        "Online check for dspawpy version timed out via requests",
        "Exception occurred while checking dspawpy version online with requests: ",
        "Failed to check dspawpy version online: ",
        "Latest version number > current imported one, feature 1 can be used to upgrade",
        "Latest version number = current imported one",
        "Online check failed, please check if the network connection is normal",
    ],
}


Dio = {
    "CN": {
        "ins": "输入结构(例如*.h5/*.json/*.pdb/*.as/*.hzw/*.xyz/*.cif/*POSCAR*/*CHGCAR*/vasprun*.xml*/...): ",
        "outs": "输出结构(例如*.json/*.pdb/*.as/*.hzw/*.xyz/*.dump/*.cif*/*.mcif*/*POSCAR*/...): ",
        "tcharge": "体系总电荷密度(例如rho.h5/json): ",
        "pcharge": "体系各组分电荷密度(例如rho.h5/json直接回车表示跳过): ",
        "inits": "初态构型(例如initial_structure.as): ",
        "fins": "末态构型(例如final_structure.as): ",
        "band": "电子能带(例如band.h5/json): ",
        "pband": "电子投影能带(例如pband.h5/json): ",
        "phband": "声子能带(例如phonon.h5/json): ",
        "wband": "瓦尼尔能带(例如wannier.h5/json): ",
        "dos": "电子态密度(例如dos.h5/json): ",
        "pdos": "电子投影态密度(例如pdos.h5/json): ",
        "phdos": "声子投影态密度(例如phonon.h5/json): ",
        "optical": "光学性质数据(例如optical.h5/json): ",
        "sysjson": "体系数据(例如sys.json): ",
        "polarization": "铁电极化计算文件夹(例如./polar): ",
        "neb": "过渡态数据(例如neb.h5/json)或整个过渡态计算文件夹(例如./neb): ",
        "neb_can_be_unfinished": "过渡态计算文件夹: ",
        "txt": "文本文件: ",
        "inf": "文件路径（包含文件名和后缀，直接回车表示跳过）: ",
        "outf": "文件输出路径（包含文件名和后缀，直接回车表示跳过）: ",
        "ind": "文件夹路径（直接回车表示当前路径）: ",
        "outd": "文件夹输出路径（直接回车表示当前路径）: ",
        "figure": "图片保存路径（包含文件名和后缀）: ",
        "nebdir": "过渡态文件夹: ",
        "datafile": "h5/json数据文件路径（包含文件名和后缀）: ",
        "logfile": "DS-PAW.log文件路径（包含文件名和后缀）: ",
        "xyzfilename": "xyz轨迹文件路径：",
        "asfilename": "as结构文件路径：",
        "h5file": "hdf5数据文件(../a/b.h5)：",
        "fig_dir": "图片保存到什么文件夹中（即将打印表格到命令行并保存图片到此文件夹中）：",
    },
    "EN": {
        "ins": "Input structure file, asterisk in parentheses stands for any character(*.h5/*.json/*.pdb/*.as/*.hzw/*.xyz/*.cif/*POSCAR*/*CHGCAR*/vasprun*.xml*/...): ",
        "outs": "Output structure file, asterisk in parentheses stands for any character(*.json/*.pdb/*.as/*.hzw/*.xyz/*.dump/*.cif*/*.mcif*/*POSCAR*/...): ",
        "tcharge": "Total charge density (e.g. rho.h5/json): ",
        "pcharge": "Charge density of individuals (e.g. rho.h5/json): ",
        "inits": "Initial structure (e.g. initial_structure.as): ",
        "fins": "Final structure (e.g. final_structure.as): ",
        "band": "Electronic band (e.g. band.h5/json): ",
        "pband": "Projected electronic band (e.g. pband.h5/json): ",
        "phband": "Phonon band (e.g. phonon.h5/json): ",
        "wband": "Wannier band (e.g. wannier.h5/json): ",
        "dos": "Electronic density of states (e.g. dos.h5/json): ",
        "pdos": "Projected electronic density of states (e.g. pdos.h5/json): ",
        "phdos": "Projected phonon density of states (e.g. phonon.h5/json): ",
        "optical": "Optical properties data (e.g. optical.h5/json): ",
        "sysjson": "System data (e.g. sys.json): ",
        "polarization": "polarization: ",
        "neb": "NEB data file (e.g. neb.h5/json) or whole neb folder: ",
        "neb_unfinished": "(Unfinished) NEB calculation folder: ",
        "txt": ".txt file: ",
        "inf": "File path (including file name and suffix, press Enter to skip): ",
        "outf": "File output path (including file name and suffix, press Enter to skip): ",
        "ind": "Folder path (press Enter to use current path): ",
        "outd": "Folder output path (press Enter to use current path): ",
        "figure": "Figure (including file name and suffix): ",
        "nebdir": "NEB folder: ",
        "datafile": "h5/json data file path (including file name and suffix): ",
        "logfile": "DS-PAW.log file path (including file name and suffix): ",
        "xyzfilename": "xyz trajectory file path: ",
        "asfilename": "as structure file path: ",
        "h5file": "hdf5 data file path(../a/b.h5): ",
        "fig_dir": "Figure output directory (will print table to the terminal and save figs here):",
    },
}
prefix = {"CN": "-> 请指定", "EN": "-> Please specify"}
for language in Dio:
    for k, v in Dio[language].items():
        Dio[language][k] = prefix[language] + v

Dresponse = {
    "CN": [
        "没有以空格分隔，请重试",
        "参数长度不为2",
        "不全是数字，请重试",
        "未检测到数据集，请检查文件",
        "仅支持h5和json格式",
        "可使用VESTA软件打开",
        "未能成功读取能带数据！请检查数据文件",
        "IDPP插值失败，请检查构型是否合理",
        "已成功自动转为线性插值",
        "已将插值后的构型保存到",
        "插值方法默认使用pchip，如果要用其他方法，请参考官网的示例脚本",
        "版本过老",
        "对于多个文件，必须手动指定timestep",
        "**************** 感谢使用dspawpy ****************",
        "-> 上一个任务已结束，是否开始下一个任务？(y/n): ",
        "用Tab键可以自动补全数据组名称",
        "成功导入依赖库，dspawpy现在开始处理数据...",
    ],
    "EN": [
        "Not separated by space, please retry",
        "Parameter length is not 2",
        "Not all are numbers, please retry",
        "No data set detected, please check file",
        "Only support h5 and json format",
        "Can be opened by VESTA software",
        "Failed to read wannier band data! Please check the data file",
        "IDPP interpolation failed, please check if the structure is reasonable",
        "Successfully converted to linear interpolation",
        "The interpolated configuration has been saved to",
        "The interpolation method defaults to pchip, if you want to use other methods, please refer to the example script on the official website",
        "Version is too old",
        "For multiple datafiles, you must manually specify the timestep. It will default to 1.0fs.",
        "******** thanks for using dspawpy ********",
        "-> The previous task was finished, do you want to start the next task? (y/n): ",
        "You may Tab to auto-complete the data group name",
        "Successfully imported dependencies, dspawpy is now processing data...",
    ],
}

Dselect = {
    "CN": [
        "下列数据集其中之一（按Tab键查看可选项，直接回车表示选择结束）: ",
        "沿着哪个或哪些轴平均（按Tab键查看可选项，以空格分隔): ",
        "输出格式： ",
        "是否平移费米能级？(y/n): ",
        "一种元素（按Tab键查看可选项，直接回车表示选择结束）: ",
        "该元素的原子轨道（按Tab键查看可选项，用空格分隔）: ",
        "一个原子序号（按Tab键查看可选项，直接回车表示选择结束）: ",
        "该原子的多个原子轨道（注意，pymatgen暂不支持单个轨道；按Tab键查看可选项，用空格分隔）: ",
        "原子或元素（按Tab键查看可选项，以空格隔开，直接回车表示选择结束）: ",
        "插值方法（按Tab键查看可选项，直接回车表示选择结束）: ",
        "是否将初始插值链另外保存成xyz或者json文件（用于可视化）？ (y/n): ",
        "第几个离子步（从1开始计数，-1表示最新构型）: ",
        "计算MSD的类型（按Tab键查看可选项，直接回车等同于'xyz'，表示计算所有分量）: ",
        "一个中心元素（按Tab键查看可选项，直接回车表示选择结束）: ",
        "一个对象元素（按Tab键查看可选项，直接回车表示选择结束）: ",
        "一个物理量（按Tab键查看可选项，直接回车表示全选）",
        "一个轴（按Tab键查看可选项，直接回车表示全选）",
        "投影方式（按Tab键查看可选项，直接回车表示选择结束）: ",
        "是否查看全部数据（数据可能会非常多，不利于定位）(y/n): ",
        "是否继续查看其他数据？(y/n): ",
        "是否打印能量和最小原子受力变化过程表格(y/n): ",
        "是否将上述表格中的数值设置成相对于初态(y/n): ",
        "是否将结构优化过程原子变化轨迹写入xyz文件(y/n): ",
        "是否将结构优化过程原子受力最小的构型写入as文件(y/n): ",
        "是否考虑周期性边界条件(y/n)：",
    ],
    "EN": [
        "one of the following data sets: ",
        "average along which axis or axes (separated by space): ",
        "output format: ",
        "whether to shift the Fermi level to 0 (y/n): ",
        "one element (press Enter to finish): ",
        "atomic orbitals of this element (separated by space): ",
        "an atomic index (press Enter to finish): ",
        "orbital of this atom (separated by space): ",
        "atom or element (separated by space, press Enter to finish): ",
        "interpolation method: ",
        "whether to save the interpolated chain as a separate xyz or json file for visualization? (y/n): ",
        "which ionic step (counting from 1, -1 indicates the latest configuration): ",
        "type of MSD calculation, optional xyz, xy, xz, yz, x, y, z, (press Enter is equivalent to 'xyz', indicating calculation of all components): ",
        "a center element: ",
        "an object element: ",
        "a physical quantity: ",
        "an axis: ",
        "projection method: ",
        "whether to view all data (data may be very large, not suitable for locating) (y/n): ",
        "whether to continue viewing other data (y/n): ",
        "whether to print energy and minimum atom force change table(y/n):  ",
        "whether to print energy and minimum atom force change table in relative terms(y/n):  ",
        "whether to write structure optimization trajectory to xyz file(y/n):  ",
        "whether to write structure optimization minimized structure to as file(y/n):  ",
        "whether to consider periodic boundary conditions(y/n):  ",
    ],
}
prefix = {"CN": "-> 请选择", "EN": "-> Please select"}
for language in Dselect:
    Dselect[language] = [prefix[language] + i for i in Dselect[language]]

Dparameter = {
    "CN": [
        "时间步长（fs），直接回车将尝试从文件中自动读取，失败则此数值将设为1.0: ",
        "最小半径, 单位埃（默认0）: ",
        "最大半径, 单位埃（默认10）: ",
        "格点数（默认101）: ",
        "sigma值（用于一维高斯函数平滑处理，默认0，不处理）: ",
        "数据点绘图时重复次数（默认2）: ",
        "温度(K, 默认298.15): ",
        "压强(Pa, 默认101325.0): ",
        "初末态之间插入几个构型: ",
        "x轴范围（先小后大，以空格分隔，直接回车可跳过设置）: ",
        "y轴范围（先小后大，以空格分隔，直接回车可跳过设置）: ",
        "备份文件夹: ",
        "第1个构型路径（包含文件名）: ",
        "第2个构型路径（包含文件名）: ",
    ],
    "EN": [
        "Time step (fs), press Enter to try to read automatically from the file, if failed, this value will be set to 1.0: ",
        "Minimum radius, in Å (default 0): ",
        "Maximum radius, in Å (default 10): ",
        "Number of grid points (default 101): ",
        "Sigma value (used for one-dimensional Gaussian function smoothing, default 0, no processing): ",
        "Y-axis lower and upper limits, separated by space (default not specified): ",
        "Number of repetitions when plotting data points (default 2): ",
        "Temperature (K, default 298.15): ",
        "Pressure (Pa, default 101325.0): ",
        "Number of configurations inserted between initial and final states: ",
        "X-axis range (small to large, separated by space, press Enter to skip setting): ",
        "Y-axis range (small to large, separated by space, press Enter to skip setting): ",
        "1st structure path: ",
        "2nd structure path: ",
    ],
}
prefix = {"CN": "-> 请输入", "EN": "-> Please input"}
for language in Dparameter:
    Dparameter[language] = [prefix[language] + i for i in Dparameter[language]]
