import os
from typing import Literal

from loguru import logger
from prompt_toolkit import prompt

from dspawpy import auto_test_cli
from dspawpy.cli import list_ds, pc_h5
from dspawpy.cli.menu_prompts import Dio, Dresponse, Dselect


def s15_1(language: Literal["EN", "CN"]) -> dict:
    """查看hdf5数据结构.

    h5glance name.h5
    """
    if auto_test_cli:
        for D in list_ds:
            if D["menu"] == 151:
                os.system(f'h5glance {D["h5file"]}')
        D = {}
    else:
        D = {}
        D["menu"] = 151
        D["h5file"] = prompt(Dio[language]["h5file"], completer=pc_h5)
        os.system(f'h5glance {D["h5file"]}')
    return D


def s15_2(language: Literal["EN", "CN"]) -> dict:
    """查看hdf5数据内容.

    支持查看单个key的数据，unix系统也支持查看全部key的数据（用less翻页）
    windows系统没有less，会直接打印出全部内容
    （建议直接使用HDFViewer窗口程序而不是dspawpy查看）

    h5glance name.h5 -
    ptdump -d name.h5
    """
    if auto_test_cli:
        from platform import system as cli_system

        for D in list_ds:
            if D["menu"] == 152:
                if D["is_all"] == "y":
                    if cli_system() == "Windows":
                        cmd = f"ptdump -d {D['h5file']}"
                    else:
                        cmd = f"ptdump -d {D['h5file']} | less"
                    os.system(cmd)
                else:
                    cmd = f'h5glance {D["h5file"]} -'
                    os.system(cmd)
        D = {}
    else:
        D = {}
        D["menu"] = 152
        D["h5file"] = prompt(Dio[language]["h5file"], completer=pc_h5)
        D["is_all"] = prompt(Dselect[language][18])
        if D["is_all"] == "y":
            from platform import system

            # requires PyTables, `pip install tables`
            if system() == "Windows":
                cmd = f"ptdump -d {D['h5file']}"
            else:
                cmd = f"ptdump -d {D['h5file']} | less"

            os.system(cmd)
        else:
            while True:
                logger.info(Dresponse[language][15])
                cmd = f'h5glance {D["h5file"]} -'
                os.system(cmd)
                if prompt(Dselect[language][19]) != "y":
                    break
    return D
