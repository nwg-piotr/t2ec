#!/usr/bin/python
# _*_ coding: utf-8 _*_

"""
Credits go to https://unix.stackexchange.com/a/67398 (and comments below!)
"""

import sys
import os
import subprocess


def main():
    if len(sys.argv) > 1 and sys.argv[1].upper() == 'SWITCH':
        try:
            # convert just to check if number given
            number = int(sys.argv[2])
            switch_output(str(number))

        except ValueError:
            print("Number expected")
            exit(0)
    else:

        # get sink numbers
        sinks = subprocess.check_output("pactl list short sinks", shell=True).decode("utf-8").splitlines()

        # get output descriptions
        names = subprocess.check_output("pacmd list-sinks | grep device.description | awk -F '=' '{print $2}'",
                                        shell=True).decode("utf-8").splitlines()
        outputs = []

        # Tuples ("sink_number", "output_description")
        for line in range(len(sinks)):
            output = sinks[line].split()[0], names[line].strip()[1:-1]
            outputs.append(output)

        # Create jgmenu
        jgmenu = []
        jgmenu.append("#!/bin/sh\n")

        jgmenu.append("config_file=$(mktemp)")
        jgmenu.append("menu_file=$(mktemp)")
        jgmenu.append("trap \"rm -f ${config_file} ${menu_file}\" EXIT\n")
        jgmenu.append("cat << 'EOF' >${config_file}")
        jgmenu.append("stay_alive           = 0")
        jgmenu.append("tint2_look           = 1")
        jgmenu.append("menu_width           = 40")
        jgmenu.append("menu_border          = 1")
        jgmenu.append("item_height          = 20")
        jgmenu.append("font                 = Sans 10")
        jgmenu.append("icon_size            = 0")
        jgmenu.append("color_norm_fg        =  # eeeeee 100")
        jgmenu.append("color_sel_fg         =  # eeeeee 100")
        jgmenu.append("EOF\n")

        jgmenu.append("cat <<'EOF' >${menu_file}")
        for line in outputs:
            jgmenu.append(line[1] + "," + "python /home/piotr/PycharmProjects/t2ec/scripts/arch/pa-switch-output.py switch " + line[0])
        jgmenu.append("EOF")

        jgmenu.append("jgmenu --config-file=${config_file} --csv-file=${menu_file}")

        print(jgmenu)

        # Check if jgmenu installed, exit if not
        try:
            subprocess.check_output("which jgmenu", shell=True)
        except subprocess.CalledProcessError:
            print("\nInstall jgmenu package, run `jgmenu init`\n")
            exit(0)

        # Check it t2ec folder exists
        t2ec_dir = os.getenv("HOME") + "/.t2ecol"
        if not os.path.isdir(t2ec_dir):
            os.makedirs(t2ec_dir)

        with open(t2ec_dir + '/pulseaudio-menu.sh', 'w') as f:
            for item in jgmenu:
                f.write("%s\n" % item)

        os.system("chmod u+x " + t2ec_dir + "/pulseaudio-menu.sh")

        subprocess.call(t2ec_dir + "/pulseaudio-menu.sh", shell=True)


def switch_output(output):
    streams = subprocess.check_output("pactl list short sink-inputs", shell=True).decode("utf-8").splitlines()
    subprocess.call("pacmd set-default-sink " + output, shell=True)
    for stream in streams:
        print(stream.split()[0])
        subprocess.call("pactl move-sink-input " + stream.split()[0] + " " + output, shell=True)
    #print(output)


if __name__ == "__main__":
    main()
