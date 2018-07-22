# main piece of code to automate the
#function and library imports
import pandas as pd
import os
from distutils.dir_util import copy_tree
import psutil
import re
from decimal import Decimal
import fileinput
import sys
import subprocess
import time

from functions import *

#Workflow

#2. create the destination folders

archive_folder=find_path('ArchivedDynaOutputs')
results_folder=find_path('results')
ensure_dir(archive_folder)
ensure_dir(results_folder)

#get the material file
material_file=find_path('blank')+"/"+"blank_material.k"
forming_parameter_file=find_path('1_stage1_forming')+"/"+"do.k"
sb_parameter_file=find_path('2_stage2_springback')+"/"+"do.k"

for i in range(how_many_rows_in_doe()):
    #iterating the rows of the DOE table
    #Get the parameter set at each row of the DOE table
    test_vals=get_parameter(i)
    for key in test_vals:
        simID=str(int(test_vals["simID"]))
        if key == "simID":
            continue
        if key in ["ro","e","pr","sigy","etan","r"]:
            new_line=update_material_parameter_line(material_file, key, test_vals[key])
            old_line=get_mat_card(material_file)[2]
            write_new_material_line(material_file,old_line,new_line)
    keys=list(test_vals.keys())
    if 's0' in keys and 'k' in keys and 'n' in keys:
        s0=test_vals['s0']
        k=test_vals['k']
        n=test_vals['n']
        curve_df=gen_stress_strain(s0,k,n)
        curve_list_formatted=format_stress_strain_lines_DYNA(curve_df)
        update_stress_strain_curve(material_file,curve_list_formatted)
    if 't' in keys:
        update_thickness(forming_parameter_file,test_vals['t'])
        update_thickness(sb_parameter_file,test_vals['t'])
    submit()
    b_loop=True
    while b_loop:
        time.sleep(5)
        print("Simulation in progress")
        if is_finished:
            print("Simulation Finished")
            b_loop = False
        else:
            continue
    copy_folder_to('blank','ArchivedDynaOutputs',simID)
    copy_folder_to('1_stage1_forming','ArchivedDynaOutputs',simID)
    clean_folder('1_stage1_forming')
    copy_folder_to('2_stage2_springback','ArchivedDynaOutputs',simID)
    raw_SB_results_folder=find_path('2_stage2_springback')
    nodout_file_path=raw_SB_results_folder+"/"+"2_stage2_springback.nodout"
    read_nodout_to_df(nodout_file_path).to_csv(results_folder+"/"+simID+".csv")
    clean_folder('2_stage2_springback')
