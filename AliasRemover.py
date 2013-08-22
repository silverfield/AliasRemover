'''
Created on 21. aug. 2013

@author: Fero Hajnovic

Recursively searches for all .cs files in the current directory and inside 
them replaces all C# aliases for their formal equivalents. A report is made
both in a console and stored in the the directory of the script. A backup of 
all the .cs files is made here as well.

Location of the report file: given by REP_FILE
Location of the backups: given by BCK_DIR
'''

#############################################
# Imports
#############################################

import fnmatch
import os
import re
import shutil
import sys

#############################################
# Constants
#############################################

REP_FILE = './AliasRemoverReport.txt'
BCK_DIR = './AliasRemoverBackups'
TMP_FILE = './AliasRemoverTempFile.cs'

#############################################
# Functions
#############################################

"""
Replaces C# aliases with their formal equivalents
"""
def changeline(line):
    # ignore enum declarations - there have to be an alias used
    if (re.search(r'\benum\b', line) != None):
        return line
    
    # ignore comments
    if (re.match(r'//', line.lstrip()) != None):
        return line
    if (re.match(r'/\*', line.lstrip()) != None):
        return line
    if (re.match(r'\*', line.lstrip()) != None):
        return line
    
    line = re.sub(r'\bbool\b', "Boolean", line)
    line = re.sub(r'\bbyte\b', "Byte", line)
    line = re.sub(r'\bsbyte\b', "SByte", line)
    line = re.sub(r'\bchar\b', "Char", line)
    
    line = re.sub(r'\bdecimal\b', "Decimal", line)
    line = re.sub(r'\bdouble\b', "Double", line)
    line = re.sub(r'\bfloat\b', "Single", line)
    line = re.sub(r'\bint\b', "Int32", line)
    line = re.sub(r'\buint\b', "UInt32", line)
    
    line = re.sub(r'\blong\b', "Int64", line)
    line = re.sub(r'\bulong\b', "Int64", line)
    line = re.sub(r'\bobject\b', "Object", line)
    line = re.sub(r'\bshort\b', "Int16", line)
    line = re.sub(r'\bushort\b', "UInt16", line)
    
    line = re.sub(r'\bstring\b', "String", line)
    
    return line

def logstr(msg):
    print(msg)
    repfile.write(msg + "\n")

#############################################
# Main
#############################################

# go the directory where this script is located
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# get the C# files
csfiles = []
for root, dirnames, filenames in os.walk('.'):
    if (os.path.basename(root) == os.path.basename(BCK_DIR)):
        continue
    for filename in fnmatch.filter(filenames, '*.cs'):
        csfiles.append(os.path.join(root, filename))

# make backup for all of them
if not os.path.exists(BCK_DIR):
    os.makedirs(BCK_DIR)
for fname in csfiles:
    shutil.copyfile(fname, os.path.join(BCK_DIR, os.path.basename(fname)))

# make sure the temporary file is not present
try:
    os.remove(TMP_FILE)
except Exception:
    pass

#create a report file
repfile = open(REP_FILE, 'w')

# process each .cs file
for fname in csfiles:
    logstr("Checking file :" + fname)
    
    file = open(fname, "r")
    lines = file.readlines()
    
    newfile = open(TMP_FILE, "w")
    
    cntr = 1
    for line in lines:
        newline = changeline(line)
        newfile.write(newline)
        if (line != newline):
            report = ("    Changed line " + str(cntr) + "\n" 
                      "    Old line: '" + line.rstrip() + "'\n"
                      "    New line: '" + newline.rstrip() + "'")
            logstr(report)
        
        cntr += 1
        
    file.close()
    newfile.close()
    
    shutil.copyfile(TMP_FILE, fname)
    
# remove the temporary file
os.remove(TMP_FILE)

# get the user a chance to see the output
print("Press any key to finish")
sys.stdin.read(1)    
