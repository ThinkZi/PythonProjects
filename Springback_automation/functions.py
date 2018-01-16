#includes the function files
import pandas as pd
import os
from distutils.dir_util import copy_tree
import psutil
import re
from decimal import Decimal
import fileinput
import sys

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
    if not ((solver_smp_s in pnames_list) or (solver_smp_s in pnames_list)):
        b=True
    return b

#get the material card in a specific content
#Got this from stackoverflow
#https://stackoverflow.com/questions/4595197/how-to-grab-the-lines-after-a-matched-line-in-python
def get_mat_card(path):
    b= False
    card=[]
    with open(path) as f:
        for line in f:
            if line.startswith( "*MAT" ):
                b=True
            elif line.startswith("*") and not line.startswith("*MAT"):
                b=False
            elif b:
                card.append(line)
    return card

#change the parameter p's value to v in the material card of the DYNA input
def update_material_parameter_line(file_path,p,v):
    #contains the last character location of the parameter in DYNA format
    p_character_loc={"RO":20,"E":30,"PR":40, "SIGY":50, "ETAN":60,"r":70, "hlcid":80 }
    with open(file_path) as f:
        DYNA_P_length=10
        card=get_mat_card(file_path)
        val_formatted=('%.4E' %Decimal(v))
        vals_line=list(card[2])
        vals_line[p_character_loc[p]-DYNA_P_length:p_character_loc[p]]=list(val_formatted)
        new_vals_line="".join(vals_line)
    return new_vals_line

def write_new_material_line(path,oldLine,newLine):
    for line in fileinput.input(path, inplace=1):
        if line == oldLine:
            line = newLine
        sys.stdout.write(line)
    return

def read_nodout_to_df(path):
    phrase1= "n o d a l   p r i n t   o u t"
    phrase2= "at time 1.0000000E+00"
    phrase3= "x-disp"
    b1=False
    b2=False
    b3=True
    l=[]
    row=[]
    with open(path) as f:
        for line in f:
            if phrase1 in line and phrase2 in line:
                b1=True
                continue
            if phrase3 in line:
                header=line.split()
                del header[0]
                b2=True
                continue
            if b1 and b2 and phrase1 in line:
                b3=False
            if b1 and b2 and b3:
                point_list=list(line)[0:9]
                point="".join(point_list)
                point=point.strip()
                xdisp_list=list(line)[10:22]
                xdisp="".join(xdisp_list)
                xdisp=xdisp.strip()
                row.append(xdisp)
                ydisp_list=list(line)[22:34]
                ydisp="".join(ydisp_list)
                ydisp=ydisp.strip()
                row.append(ydisp)
                zdisp_list=list(line)[34:46]
                zdisp="".join(zdisp_list)
                zdisp=zdisp.strip()
                row=[point,xdisp,ydisp,zdisp]
                l.append(row)
                row=[]
    df=pd.DataFrame(l,columns=header[0:4])
    df.set_index=df['point']
    return df

#folderID="blank"
#fname="blank_material.k"
#folder_path=find_path(folderID)
#path=folder_path+"/"+fname
#card=get_mat_card(path)
#newLine=update_material_parameter_line(path,"E",210000)
#write_new_material_line(path,card[2],newLine)

path=r"C:\Hamed\backup\test\Springback_Experiment\filleted\2_stage2_springback\2_stage2_springback.nodout"
print(read_nodout_to_df(path))
