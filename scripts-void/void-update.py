#!/usr/bin/python
# _*_ coding: utf-8 _*_

"""
# Author: Piotr Miller
# e-mail: nwg.piotr@gmail.com
# Website: http://nwg.pl
# Project: https://github.com/nwg-piotr/t2ec
# License: GPL3

Arguments [-C] | [-U<aur_helper> <terminal>] | [menu] | -[O] [-N] | [-M<custom_name>]

[-C] - check updates
[-U<terminal>] - your terminal name
[-O] - display pending updates with notify-send
[-N] - name instead of icon
[menu] - show context jgmenu

"""

import sys
import os
import subprocess


def main():
    name = None
    terminal_name, helper_cmd, updates = "", "", ""
    do_check, do_update, do_notify = False, False, False

    tmp_file = os.getenv("HOME") + "/.void-updates"

    check_command = "xbps-install -Suvn | grep ' update ' | awk '{print $1}' > " + tmp_file

    if len(sys.argv) > 1:
        for i in range(1, len(sys.argv)):

            if sys.argv[i].upper() == '-O':
                do_check = False
                do_update = False
                do_notify = True
                break

            elif sys.argv[1].upper() == "MENU":
                show_menu()
                break

            if sys.argv[i].upper().startswith('-C'):
                do_check = True
                do_update = False
                do_notify = False

            if sys.argv[i].upper().startswith('-U'):
                tools = sys.argv[i][2::].split(":")
                terminal_name = tools[0]
                do_check = False
                do_update = True
                do_notify = False

            if sys.argv[i].upper() == '-N':
                name = "Upd:"

            if sys.argv[i].upper().startswith('-M'):
                name = sys.argv[i][2::]

            if sys.argv[i].upper() == '-H' or sys.argv[i].upper() == '-HELP':
                print("\nt2ec --update -C | -U<terminal> | [-O] [-N] | [-M<custom_name>]\n")
                print("-C - (C)heck updates with xbps-install -Suvn")
                print("-U<terminal> - (U)pdate in the <terminal> you use")
                print(" example: t2ec --update -Uxfce4-terminal\n")
                print("-O - display saved pending updates as n(O)tification")
                print("-N - print (N)ame instead of icon")
                print("-M<custom_name> - print custom na(M)e instead of icon\n")

    if do_check:
        if name is not None:
            os.system("echo Checking...")
        else:
            os.system("echo /usr/share/t2ec/refresh.svg")
            os.system("echo ''")

        subprocess.call(check_command, shell=True)
        updates = open(tmp_file, 'r').read().rstrip()
        num_upd = len(updates.splitlines())

        if name is not None:
            if num_upd > 0:
                print(name + " " + str(num_upd))
            else:
                print("Up-to-date")
        else:
            if num_upd > 0:
                os.system("echo ~/PycharmProjects/t2ec/images/void-update-notify.svg")
                os.system("echo " + str(num_upd))
            else:
                os.system("echo ~/PycharmProjects/t2ec/images/void-update.svg")
                os.system("echo ''")

    if do_update:
        command = terminal_name + ' -e \'sh -c \"sudo xbps-install -Suv; echo Press enter to exit; read; killall -SIGUSR1 tint2\"\''
        subprocess.call(command, shell=True)

    if do_notify:
        updates = open(tmp_file, 'r').read().rstrip()
        notify(updates)


def notify(updates):
    subprocess.call(
        ['notify-send', "Pending updates:", "--icon=~/PycharmProjects/t2ec/images/void-update-notify.svg", "--expire-time=5000", updates])


def show_menu():
    try:
        subprocess.check_output("which jgmenu", shell=True)
    except subprocess.CalledProcessError:
        print("\nInstall jgmenu package, run `jgmenu init`\n")
        return

    t2ec_dir = os.getenv("HOME") + "/.t2ecol"
    if not os.path.isdir(t2ec_dir):
        os.makedirs(t2ec_dir)
    if not os.path.isfile(t2ec_dir + "/menu-update.sh"):
        subprocess.call(["cp /usr/lib/t2ec/menu-update.sh "+ t2ec_dir + "/menu-update.sh"], shell=True)
    subprocess.call([t2ec_dir + '/menu-update.sh'], shell=True)


if __name__ == "__main__":
    main()
