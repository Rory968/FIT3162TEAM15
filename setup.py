#!/usr/bin/env python
# Written by Rory Austin, id: 28747194


import database_details as dbd
import subprocess

# This file sets up the python environment on the system


def install_packages():
    '''
    This function takes a list of packages that are specified for the use of the application
    It uses this list to install each package on the system.
    :return: returns nothing.
    '''
    command = 'install'
    for element in dbd.packages:
        cmd = ['pip', command, element]
        subprocess.call(cmd)


def main():
    install_packages()


if __name__ == "__main__":
    main()