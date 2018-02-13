#includes the function files
import pandas as pd
import os
from distutils.dir_util import copy_tree
import psutil
import re
from decimal import Decimal
import fileinput
import sys
import subprocess


#read paths
def find_path(whichpath):
    pathholderpath="C:/Users/hzoghi/Documents/PythonProjects/Springback_automation/Paths.csv"
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
    subprocess.call(r"C:\Hamed\backup\test\Springback_Experiment\filleted\do.bat", shell=True)
    return

def how_many_rows_in_doe():
    doePath="C:/Users/hzoghi/Documents/PythonProjects/Springback_automation/DOE.csv"
    df=pd.read_csv(doePath)
    number_of_rows=len(df.index)
    return number_of_rows
#reads the DOE data and returns the specific parameter value along with the
#simulation ID in the form of a dictionary {'simID': ID, 'p':value}
def get_parameter(index):
    doePath="C:/Users/hzoghi/Documents/PythonProjects/Springback_automation/DOE.csv"
    df=pd.read_csv(doePath)
    values=df.to_dict('index')[index]
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
    p_character_loc={"ro":20,"e":30,"pr":40, "sigy":50, "etan":60,"r":70 }
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
#reads the nodout file and passes a dataframe containing the displacements
#and node ids
def read_nodout_to_df(path):
    phrase1= "n o d a l   p r i n t   o u t"
    phrase2= "at time 1.0000000E+00"
    phrase3= "x-disp"
    phrase4="x-rot"
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
            if phrase4 in line:
                b2=False
            if len(line.strip()) == 0:
                continue
            if b1 and b2 and b3 and phrase1 in line:
                break
            if b1 and b2 and b3:
                point_list=list(line)[0:9]
                point="".join(point_list)
                point=point.strip()
                xdisp_list=list(line)[10+0*12:22+0*12]
                xdisp="".join(xdisp_list)
                xdisp=xdisp.strip()
                ydisp_list=list(line)[10+1*12:22+1*12]
                ydisp="".join(ydisp_list)
                ydisp=ydisp.strip()
                zdisp_list=list(line)[10+2*12:22+2*12]
                zdisp="".join(zdisp_list)
                zdisp=zdisp.strip()
                xcoord_list=list(line)[10+9*12:22+9*12]
                xcoord="".join(xcoord_list)
                xcoord=xcoord.strip()
                ycoord_list=list(line)[10+10*12:22+10*12]
                ycoord="".join(ycoord_list)
                ycoord=ycoord.strip()
                zcoord_list=list(line)[10+11*12:22+11*12]
                zcoord="".join(zcoord_list)
                zcoord=zcoord.strip()
                row=[point,xdisp,ydisp,zdisp,xcoord,ycoord,zcoord]
                l.append(row)
                row=[]
    df=pd.DataFrame(l,columns=[header[0],header[1],header[2],header[3],
    header[10],header[11],header[12]])
    return df

#returns a pandas DataFrame for stress strain values
def gen_stress_strain(s0,k,n):
    rows=21
    l=[]
    max_strain=0.8
    strain=0
    for i in range(rows):
        if strain == max_strain:
            break
        strain_step=max_strain/rows
        l.append([strain,s0+k*(strain**n)])
        strain+=strain_step
    df=pd.DataFrame(l, columns=['strain','stress'])
    return df
#returns a list of string lines containing stress and strain values in the
#right DYNA character locations
def format_stress_strain_lines_DYNA(df):
    #generate a list of 40 characters with spaces
    l=[]
    lines=[]
    for i in range(40):
        l.append(' ')
    DYNA_character_loc={'strain':20,'stress':40}
    num_format='%.4E'
    for index, row in df.iterrows():
        strain=list(num_format %Decimal(row['strain']))
        stress=list(num_format %Decimal(row['stress']))
        for i in range(len(strain)):
            l[DYNA_character_loc['strain']-(i+1)]=strain[-(i+1)]
            l[DYNA_character_loc['stress']-(i+1)]=stress[-(i+1)]
            line=''.join(l)
            line=line+'\n'
        lines.append(line)
    return lines

#updates the stress strain curve in the blank material files
def update_stress_strain_curve(path,replacement_lines):
    read_curve_keyword=False
    curve_data_finished = False
    exception=True
    i=-1
    phrase1='DEFINE_CURVE'
    newLines=[]
    with open(path) as f:
        for oldLine in f:
            c = oldLine[0]
            if phrase1 in oldLine and not read_curve_keyword:
                read_curve_keyword = True
                newLines.append(oldLine)
                continue
            elif c == '*' and read_curve_keyword:
                curve_data_finished = True
                newLines.append(oldLine)
                continue
            elif read_curve_keyword and not curve_data_finished:
                #skip the first line including numerical values after the define curve keyword
                if oldLine.split()[0][0].isnumeric() and exception:
                    newLines.append(oldLine)
                    exception=False
                    continue
                if oldLine.split()[0][0].isnumeric() and not exception:
                    i+=1
                    print(i,':',oldLine)
                    newLines.append(replacement_lines[i])
                else:
                    newLines.append(oldLine)
                continue
            else:
                newLines.append(oldLine)
                continue
    with open(path,'w') as f:
        for line in newLines:
            f.write(line)
    return newLines
