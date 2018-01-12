#includes the function files

import pandas as pd
import os
from distutils.dir_util import copy_tree
import psutil
import re
from decimal import Decimal

pathholderpath="C:/Users/hzoghi/Documents/PythonProjects/Springback_automation/Paths.csv"
doePath="C:/Users/hzoghi/Documents/PythonProjects/Springback_automation/DOE.csv"
#read paths
def find_path(whichpath):
    #the followings can be passed to this function
    #blank, 1_stage1_forming, 2_stage2_springback, results, ArchivedDynaOutputs
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

#removing dyna output files from the main folder
def clean_folder(to_be_deleted_folder_name):
    exception=".k"
    path=find_path(to_be_deleted_folder_name)
    filenames = os.listdir(path)
    for filename in filenames:
        if not filename.endswith(exception):
            os.remove(path+"/"+filename)
    return

#run the .bat file including dyna commands
def submit():
    os.system(r"C:\Hamed\backup\test\Springback_Experiment\filleted\test.bat")
    return

#reads the DOE data and returns the specific parameter value along with the
#simulation ID in the form of a dictionary {'simID': ID, 'p':value}
def get_parameter(index,p):
    ID_label='simID'
    df=pd.read_csv(doePath)
    value=df.get_value(index,p)
    ID=df.get_value(index, ID_label)
    values={ID_label:ID, p:value}
    return values

#check for the solver #ls-dyna_smp process instance
#return True if the process is not running
def is_finished():
    solver_smp_s="ls-dyna_smp_s_R901_winx64_ifort131.exe"
    solver_smp_d="ls-dyna_smp_d_R901_winx64_ifort131.exe"
    pnames_list=[p.info['name'] for p in psutil.process_iter(attrs=['name'])]
    b=False
    if not ((solver_smp_s in pnames_list) and (solver_smp_s in pnames_list)):
        b=True
    return b

#get the material card in a specific content
#Got this from stackoverflow
#https://stackoverflow.com/questions/4595197/how-to-grab-the-lines-after-a-matched-line-in-python
def get_mat_card(content):
    b= False
    card=[]
    for line in content:
        if line.startswith( "*MAT" ):
            b=True
        elif line.startswith("*") and not line.startswith("*MAT"):
            b=False
        elif b:
            card.append(line)
    return card

#change the parameter p's value to v in the material card of the dyna input
def change_material_parameter(p,v):
    folderID="blank"
    fname="blank_material.k"
    folder_path=find_path(folderID)
    path=folder_path+"/"+fname
    p_character_loc={"RO":20,"E":30,"PR":40, "SIGY":50, "ETAN":60,"r":70, "hlcid":80 }
    with open(path) as f:
        card=get_mat_card(f)
        val_formatted=('%.4E' %Decimal(v))
        vals_line=list(card[2])
        print(val_formatted)
        print(vals_line[p_character_loc[p]-len(val_formatted):p_character_loc[p]])
    return card



change_material_parameter("E",20.0)
