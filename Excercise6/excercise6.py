"""
This script searches the directory, finds the files, merges their contents and
write them to new file named according to the current date and time.
"""
#importing OS related functions from os library
from os import listdir
from os.path import isfile, join

mypath="C:/Users/hzoghi/Documents/Python Projects/Excercise6/folder/"

#importin datetime library to use as merged files name
import datetime
now=datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f")
mergedfilepath="C:/Users/hzoghi/Documents/Python Projects/Excercise6/"

mergedfile=mergedfilepath+now+".txt"

#list only the file names in the path (no directories)
filenames=[]
filenames = [item for item in listdir(mypath) if isfile(join(mypath,item))]
#Open the destination file in write mode
fwhandle=open(mergedfile,'w')
#Loops through the files in the path
for instance in filenames:
    frhandle=open(join(mypath,instance),'r') #Open each file in the read mode
    #writes the content of the file to the end of the destination file
    fwhandle.write("from file name:"+ instance +"\n"+ frhandle.read()+"\n\n")

#close all the files
frhandle.close()
fwhandle.close()
