import pandas as pd
import os
def result_files(topdir):
    flist=[]
    for dirpath, dirnames, files in os.walk(topdir):
        for name in files:
            flist.append(os.path.join(dirpath, name))
    return flist
