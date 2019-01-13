#!/usr/bin/python
# _*_ coding: utf-8 _*_

"""
Credits go to https://unix.stackexchange.com/a/67398 (and comments below!)
"""

import subprocess


def main():
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

    for line in outputs:
        print(line[0], line[1])


if __name__ == "__main__":
    main()
