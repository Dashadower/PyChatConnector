import sys
from cx_Freeze import setup, Executable
includes = []
packages = ["dbm","pickle"]
eggsac = Executable(
    script = "chatserver.py",
    initScript = None,

    icon = None)

setup(
    name = "chatserver",
    version = "3.1",
    author = "Dashadower",
    description = "Chat server launcher",
    options = {"build_exe":{"includes":includes,"packages":packages}},
    executables = [Executable("chatserver.py")]
    )