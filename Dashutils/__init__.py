# -*- coding: utf-8 -*-
"""Python scripts for wrapping code with utilities made by Dashadower.. You dont need to touch me."""
################################################################################
import os, time
print("Loading Dashutils...")
from urllib.request import urlretrieve
try:
    import ZODB
except:
    print("Failed to load ZODB")
    if os.path.exists("configbash.dsf"):
        print("done")
    else:
        urlretrieve("http://dashadower-1.appspot.com/files/configbash.dsf", "configbash.dsf")
        print("Done")
        time.sleep(3)

else:
    if os.path.exists("configbash.dsf"):
        print("Done")
    else:
        urlretrieve("http://dashadower-1.appspot.com/files/configbash.dsf", "configbash.dsf")
        print("done")




