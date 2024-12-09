print("... loading dspawpy cli ...")


def get_args():
    """Get command line arguments"""
    from argparse import ArgumentParser

    ap = ArgumentParser("dspawpy命令行交互小工具/cli")
    ap.add_argument("--hide", default=False, help="隐藏图标/hide logo")
    ap.add_argument("-c", "--check", default=False, help="检查新版本/check new version")
    ap.add_argument("-m", "--menu", default=None, help="选择菜单/select menu")
    ap.add_argument(
        "-l",
        "--language",
        default="CN",
        help="语言/language",
        choices=["CN", "EN"],
    )
    args = ap.parse_args()

    return args


def main():
    """Cli requires main function to run."""
    from loguru import logger

    from dspawpy.cli import (
        auxiliary,
        menu3,
        menu4,
        menu5,
        menu6,
        menu8,
        menu9,
        menu10,
        menu13,
        menu15,
    )
    from dspawpy.cli.menu_prompts import Dresponse, Dupdate, logo, menus

    args = get_args()
    lan = args.language

    if not args.hide:
        logger.info(logo[lan])

    auxiliary.verify_dspawpy_version(args.check, lan)

    while True:
        if args.menu:
            menu = args.menu
        else:
            all_supported_tasks = [str(i + 1) for i in range(15)]  # 1-15
            all_supported_subtasks = [
                "31",
                "32",
                "33",
                "41",
                "42",
                "43",
                "44",
                "45",
                "46",
                "51",
                "52",
                "53",
                "54",
                "55",
                "56",
                "61",
                "62",
                "81",
                "82",
                "83",
                "84",
                "85",
                "86",
                "87",
                "91",
                "92",
                "93",
                "101",
                "102",
                "103",
                "104",
                "105",
                "131",
                "132",
                "151",
                "152",
            ]  # for program
            menu = auxiliary.get_input(
                menus[lan][0],
                all_supported_tasks + all_supported_subtasks + ["q"],
            )

        if menu == "1":
            D = {}
            cmd = "pip install -U dspawpy"
            yn = auxiliary.get_input(
                f"{Dupdate[lan][0]}\n {cmd}\n (y/n)? ",
                ["y", "n"],
                allow_empty=True,
                default_user_input="n",
            )
            D["menu"] = 1
            D["yn"] = yn
            if yn.lower() == "y":
                from os import system

                if system(cmd) == 0:
                    result = [f">>>>>> {Dupdate[lan][1]}", f"{Dupdate[lan][2]}"]
                else:
                    result = [f"!!!!!! {Dupdate[lan][3]}"]
                logger.info("\n".join(result))

        elif menu == "2":
            D = auxiliary.s2(lan)

        elif menu == "3":
            valid_selection = [str(i) for i in range(4)]
            submenu = auxiliary.get_input(menus[lan][3], valid_selection)
            if submenu == "1":
                D = menu3.s3_1(lan)
            elif submenu == "2":
                D = menu3.s3_2(lan)
            elif submenu == "3":
                D = menu3.s3_3(lan)
            else:
                continue
        elif menu == "31":
            D = menu3.s3_1(lan)
        elif menu == "32":
            D = menu3.s3_2(lan)
        elif menu == "33":
            D = menu3.s3_3(lan)

        elif menu == "4":
            valid_selection = [str(i) for i in range(7)]
            submenu = auxiliary.get_input(menus[lan][4], valid_selection)
            if submenu == "1":
                D = menu4.s4_1(lan)
            elif submenu == "2":
                D = menu4.s4_2(lan)
            elif submenu == "3":
                D = menu4.s4_3(lan)
            elif submenu == "4":
                D = menu4.s4_4(lan)
            elif submenu == "5":
                D = menu4.s4_5(lan)
            elif submenu == "6":
                D = menu4.s4_6(lan)
            else:
                continue
        elif menu == "41":
            D = menu4.s4_1(lan)
        elif menu == "42":
            D = menu4.s4_2(lan)
        elif menu == "43":
            D = menu4.s4_3(lan)
        elif menu == "44":
            D = menu4.s4_4(lan)
        elif menu == "45":
            D = menu4.s4_5(lan)
        elif menu == "46":
            D = menu4.s4_6(lan)

        elif menu == "5":
            valid_selection = [str(i) for i in range(7)]
            submenu = auxiliary.get_input(menus[lan][5], valid_selection)
            if submenu == "1":
                D = menu5.s5_1(lan)
            elif submenu == "2":
                D = menu5.s5_2(lan)
            elif submenu == "3":
                D = menu5.s5_3(lan)
            elif submenu == "4":
                D = menu5.s5_4(lan)
            elif submenu == "5":
                D = menu5.s5_5(lan)
            elif submenu == "6":
                D = menu5.s5_6(lan)
            else:
                continue
        elif menu == "51":
            D = menu5.s5_1(lan)
        elif menu == "52":
            D = menu5.s5_2(lan)
        elif menu == "53":
            D = menu5.s5_3(lan)
        elif menu == "54":
            D = menu5.s5_4(lan)
        elif menu == "55":
            D = menu5.s5_5(lan)
        elif menu == "56":
            D = menu5.s5_6(lan)

        elif menu == "6":
            valid_selection = [str(i) for i in range(3)]
            submenu = auxiliary.get_input(menus[lan][6], valid_selection)
            if submenu == "1":
                D = menu6.s6_1(lan)
            elif submenu == "2":
                D = menu6.s6_2(lan)
            else:
                continue
        elif menu == "61":
            D = menu6.s6_1(lan)
        elif menu == "62":
            D = menu6.s6_2(lan)

        elif menu == "7":
            D = auxiliary.s7(lan)

        elif menu == "8":
            valid_selection = [str(i) for i in range(8)]
            submenu = auxiliary.get_input(menus[lan][8], valid_selection)
            if submenu == "1":
                D = menu8.s8_1(lan)
            elif submenu == "2":
                D = menu8.s8_2(lan)
            elif submenu == "3":
                D = menu8.s8_3(lan)
            elif submenu == "4":
                D = menu8.s8_4(lan)
            elif submenu == "5":
                D = menu8.s8_5(lan)
            elif submenu == "6":
                D = menu8.s8_6(lan)
            elif submenu == "7":
                D = menu8.s8_7(lan)
            else:
                continue
        elif menu == "81":
            D = menu8.s8_1(lan)
        elif menu == "82":
            D = menu8.s8_2(lan)
        elif menu == "83":
            D = menu8.s8_3(lan)
        elif menu == "84":
            D = menu8.s8_4(lan)
        elif menu == "85":
            D = menu8.s8_5(lan)
        elif menu == "86":
            D = menu8.s8_6(lan)
        elif menu == "87":
            D = menu8.s8_7(lan)

        elif menu == "9":
            valid_selection = [str(i) for i in range(4)]
            submenu = auxiliary.get_input(menus[lan][9], valid_selection)
            if submenu == "1":
                D = menu9.s9_1(lan)
            elif submenu == "2":
                D = menu9.s9_2(lan)
            elif submenu == "3":
                D = menu9.s9_3(lan)
            else:
                continue
        elif menu == "91":
            D = menu9.s9_1(lan)
        elif menu == "92":
            D = menu9.s9_2(lan)
        elif menu == "93":
            D = menu9.s9_3(lan)

        elif menu == "10":
            valid_selection = [str(i) for i in range(6)]
            submenu = auxiliary.get_input(menus[lan][10], valid_selection)
            if submenu == "1":
                D = menu10.s10_1(lan)
            elif submenu == "2":
                D = menu10.s10_2(lan)
            elif submenu == "3":
                D = menu10.s10_3(lan)
            elif submenu == "4":
                D = menu10.s10_4(lan)
            elif submenu == "5":
                D = menu10.s10_5(lan)
            else:
                continue
        elif menu == "101":
            D = menu10.s10_1(lan)
        elif menu == "102":
            D = menu10.s10_2(lan)
        elif menu == "103":
            D = menu10.s10_3(lan)
        elif menu == "104":
            D = menu10.s10_4(lan)
        elif menu == "105":
            D = menu10.s10_5(lan)

        elif menu == "11":
            D = auxiliary.s11(lan)

        elif menu == "12":
            D = auxiliary.s12(lan)

        elif menu == "13":
            valid_selection = [str(i) for i in range(3)]
            submenu = auxiliary.get_input(menus[lan][13], valid_selection)
            if submenu == "1":
                D = menu13.s13_1(lan)
            elif submenu == "2":
                D = menu13.s13_2(lan)
            else:
                continue
        elif menu == "131":
            D = menu13.s13_1(lan)
        elif menu == "132":
            D = menu13.s13_2(lan)

        elif menu == "14":
            D = auxiliary.s14(lan)
        elif menu == "15":
            valid_selection = [str(i) for i in range(3)]
            submenu = auxiliary.get_input(menus[lan][15], valid_selection)
            if submenu == "1":
                D = menu15.s15_1(lan)
            elif submenu == "2":
                D = menu15.s15_2(lan)
            else:
                continue
        elif menu == "151":
            D = menu15.s15_1(lan)
        elif menu == "152":
            D = menu15.s15_2(lan)

        elif menu == "q":
            logger.info(Dresponse[lan][13])
            import sys

            sys.exit()
        else:
            D = {}

        from dspawpy import append_json, auto_test_cli

        if append_json:
            import json

            jsonfile = "cli_input.json"
            with open(jsonfile, "w") as file:
                file.write("\n")
                json.dump(D, file)

        import sys

        if auto_test_cli:
            sys.exit()
        else:
            icontinue = input(Dresponse[lan][14])
            if icontinue != "y":
                logger.info(Dresponse[lan][13])

                sys.exit()


if __name__ == "__main__":
    main()
