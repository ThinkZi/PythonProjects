#includes the function files

import pandas as pd
import os
from distutils.dir_util import copy_tree

#read paths
def find_path(whichpath):
    #the followings can be passed to this function
    #blank, 1_stage1_forming, 2_stage2_springback, results, ArchivedDynaOutputs
    pathholderpath="C:/Users/hzoghi/Documents/PythonProjects/Springback_automation/Paths.csv"
    df=pd.read_csv(pathholderpath)
    path_string=df.loc[df['folderID'] == whichpath]['path'].values[0]
    path_string=path_string.replace('\\','/')
    return path_string

#Create a directoy
def ensure_dir(directory_path):
    if not os.path.isdir(directory_path):
        os.makedirs(directory_path)
    return

#function to copy a specific folder and its contents to destiantion folder in
#a folder with the name of simulation ID
def copy_folder_to(host_folder_name,destination_folder_name, simulation_ID):
    host_folder_path = find_path(host_folder_name)
    container="/" + simulation_ID + "/" + host_folder_name
    destination_folder_path=find_path(destination_folder_name)+container
    copy_tree(host_folder_path, destination_folder_path)
    return

def clean_folder(to_be_deleted_folder_name):
    exception=".k"
    path=find_path(to_be_deleted_folder_name)
    filenames = os.listdir(path)
    for filename in filenames:
        if not filename.endswith(exception):
            os.remove(path+"/"+filename)
    return

def submit():
    os.system(r"C:\Hamed\backup\test\Springback_Experiment\filleted\test.bat")
    return
submit()
