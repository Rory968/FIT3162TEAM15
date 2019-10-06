import database_details as dbd
import subprocess
import os
from pathlib import Path


def find_path(name):
    '''
    Small function to find the path of a given filename within a system.

    :param name: name of the file.
    :return: returns the path as a string.
    '''
    print("[+] Searching for " + name)
    for root, dirs, files in os.walk(str(Path.home())):

        if name in files:
            print("[+] Found at " + os.path.join(root, name))
            return os.path.join(root, name)


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

    rpath = find_path('setup.R')
    cmd = ['Rscript', rpath]
    subprocess.call(cmd)


def main():
    install_packages()


if __name__ == "__main__":
    main()