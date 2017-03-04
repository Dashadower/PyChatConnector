# -*- coding: utf-8 -*-
"""Installtools to fetch pip and other modules"""
from urllib.request import urlretrieve
import os, time
def getpip(install=True, debug=True):
    b1 = time.time()
    print("Downloading pip...")
    urlretrieve("https://pypi.python.org/packages/source/p/pip/pip-1.5.6.tar.gz#md5=01026f87978932060cc86c1dc527903e","pip-1.5.6.tar.gz")
    import tarfile
    print("Extracting pip...")
    piptar = tarfile.open("pip-1.5.6.tar.gz","r:gz")
    piptar.extractall(os.getcwd())
    b2 = time.time()
    print("Done!!(%ds)"%(b2-b1))
    if install == True:
        installpip()
    else:
        return True

def installpip():
    os.chdir("pip-1.5.6")
    os.system("setup.py build")
    os.system("setup.py install")
    os.chdir("C:/Python33/Scripts")
    cmdline = os.popen("pip").read()
    if cmdline == "'pip' is not recognized as an internal or external command,operable program or batch file.":
        return False
    else:
        return True

def runpip(pipargv):
    os.chdir("C:/Python33/Scripts")
    os.system("pip %s"%(pipargv))


