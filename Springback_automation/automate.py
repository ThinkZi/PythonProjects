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

from functions import *
import time
#Workflow

#2. create the destination folders
results_folder=find_path('results')
archive_folder=find_path('ArchivedDynaOutputs')
ensure_dir(results_folder)
ensure_dir(archive_folder)

#get the material file
material_file=find_path('blank')+"/"+"blank_material.k"

for i in range(how_many_rows_in_doe()):
    #iterating the rows of the DOE table
    #Get the parameter set at each row of the DOE table
    test_vals=get_parameter(i)
    for key in test_vals:
        simID=str(int(test_vals["simID"]))
        if key == "simID":
            continue
        new_line=update_material_parameter_line(material_file, key, test_vals[key])
        old_line=get_mat_card(material_file)[2]
        write_new_material_line(material_file,old_line,new_line)
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
    clean_folder('2_stage2_springback')


#3. copy and move the files to the destination folder


#4. get the variables that need to be changed and the values
#(process variables excluding geometry)



#5. Geometry variations (to be done later)



#6. Run the simulation loop
#6.1 Apply the changes to the input files (material identified in step 4)
#6.2 Generate simulation ID
#6.3 Submit the simulation
#6.4 check if the simulation has ended
#6.4.1. Read the ASCII results and
#6.4.2. Save to the dataframe
#6.4.3. Backup the results
#6. Run the simulation loop

#7. Visualize the results
