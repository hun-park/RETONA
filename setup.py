import os, subprocess, apt_pkg

apt_pkg.init()

BIN = os.listdir("/usr/bin")
VER = subprocess.check_output(["python3","-V"]).decode()[7:11]
APT = apt_pkg.Cache().__getitem__("python{}-venv".format(VER))

if ("pip3" in BIN):
    pass
else:
    os.system("sudo apt update")
    os.system("sudo apt upgrade")
    os.system("sudo apt install python3-pip")

if (APT):
    CWD = os.getcwd()
    DIR = os.listdir(CWD)
    if (".venv" in DIR):
        os.system("source .venv/bin/activate")
    else:
        os.system("python3 -m venv .venv")
        os.system("source .venv/bin/activate")
        os.system("pip install pandas")
        os.system("pip install numpy")
else:
    os.system("sudo apt install python{}-venv".format(VER))