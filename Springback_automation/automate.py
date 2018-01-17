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
from functions import *
#Workflow
#1. read the path holder files


#2. create the destination folder
results_folder=find_path('results')
archive_folder=find_path('ArchivedDynaOutputs')
ensure_dir(results_folder)
ensure_dir(archive_folder)
material_file=find_path('blank')+"/"+"blank_material.k"

for i in range(how_many_rows_in_doe()):
    test_vals=get_parameter(i)
    for key in test_vals:
        simID=str(int(test_vals["simID"]))
        if key == "simID":
            continue
        new_line=update_material_parameter_line(material_file, key, test_vals[key])
        old_line=get_mat_card(material_file)[2]
        print(old_line)
        print(new_line)
        write_new_material_line(material_file,old_line,new_line)
    submit()
    copy_folder_to('blank','ArchivedDynaOutputs',simID)
    copy_folder_to('11_stage1_forming','ArchivedDynaOutputs',simID)
    copy_folder_to('22_stage2_springback','ArchivedDynaOutputs',simID)


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
