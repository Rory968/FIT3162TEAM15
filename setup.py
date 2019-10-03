import database_details as dbd
import subprocess


def install_packages():
    command = 'install'
    for element in dbd.packages:
        cmd = ['pip', command, element]
        subprocess.call(cmd)


def main():
    install_packages()


if __name__ == "__main__":
    main()