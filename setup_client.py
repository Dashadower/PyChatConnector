import sys, re,sre_compile,sre_constants,sre_parse
from cx_Freeze import setup, Executable

setup(
    name = "Chatclient",
    version = "1.3",
    description = "chatting program - Dashadower dashadower.blog.me",
    executables = [Executable("chatclient.py", base = "Win32GUI")])