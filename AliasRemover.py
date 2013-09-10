'''
Created on 21. aug. 2013

@author: Fero Hajnovic

Recursively searches for all .cs files in the current directory and inside 
them tries to detect use of C# aliases. A report is made
both in a console and stored in the the directory of the script. 

Please note that the removing (replacing) functionality is not yet present

Location of the report file: given by REP_FILE
'''

#############################################
# Imports
#############################################

import fnmatch
import os
import re
import sys
import getopt

#############################################
# Constants
#############################################

REP_FILE = './AliasRemoverReport.txt'
SEP_SIZE = 120
LONGEST_ALIAS = 20

#############################################
# Functions
#############################################

"""
Returns True if the last characters of allchars match the word
"""
def match(allchars, word):
    if (len(allchars) < len(word)):
        return False
    
    for i in range(1, 1 + len(word)):
        if (allchars[-i] != word[-i]):
            return False
        
    return True

"""
Returns Match object if the alias matches at the end of allchars.
None otherwise
"""
def matchalias(allchars, alias):
    strallchars = ''.join(allchars[-LONGEST_ALIAS:])
    if (allchars[-1] == '\n'):
        strallchars += '\n'
    pattern = r'\b(' + alias + r')\b.$'
    m = re.search(pattern, strallchars, re.DOTALL)
            
    return m

"""
Returns Match object of an alias that matches the end of allchars
None - if no alias matches
"""
def matchaliases(allchars):
    strallchars = ''.join(allchars[-LONGEST_ALIAS:])
    if (allchars[-1] == '\n'):
        strallchars += '\n'
    pattern = r'\b(bool|byte|sbyte|char|decimal|double|float|int|unit|long|ulong|object|short|ushort|string)\b.$'
    m = re.search(pattern, strallchars, re.DOTALL)
            
    return m

"""
Returns a list of triples (alias, row, col) of detected aliases along
with their line number (row) and column (col)
"""
def getaliases(lines):
    aliases = []
    
    allchars = []
    
    incmt = False
    instr = False
    inmacro = False
    
    lncnt = len(lines)
    lnfrac = lncnt / 100
    perc = 0;
    
    ln = 0;
    for line in lines:
        if (ln > perc * lnfrac):
            perc += 1
            print(str(perc) + '%')
        ln += 1
        
        chn = 0
        for char in line:
            chn += 1
            allchars.append(char)
            
            # we're processing code where int is really int
            if (incmt == False and instr == False and inmacro == False):
                if match(allchars, r'//'):
                    break
                if match(allchars, r'#'):
                    break
                if match(allchars, r'/*'):
                    incmt = True
                    continue
                if match(allchars, r'"'):
                    instr = True
                    continue
                
                aliasmatch = matchaliases(allchars)
                if (aliasmatch != None):
                    alias = aliasmatch.group(1)
                    row = ln
                    col = chn - len(alias)
                    aliases.append([alias, row, col])
               
            # in comment     
            if (incmt):
                if match(allchars, r'*/'):
                    incmt = False
                    continue
            
            # in string literal
            if (instr):
                if (match(allchars, r'"') and not match(allchars, r'\"')):
                    instr = False
                    continue
                
            # in macro preprocessing
            if (inmacro):
                pass
    
    return aliases

"""
Returns the lines where tabs are expanded
"""
def expandtabs(lines):
    newlines = []
    for line in lines:
        newlines.append(line.expandtabs(4))
        
    return newlines

"""
Looks for C# aliases in the document
"""
def analysedoc(lines):
    lines = expandtabs(lines)
    aliases = getaliases(lines)
    
    if (len(aliases) > 0):
        logstr('*' * SEP_SIZE)
    
    for alias in aliases:
        al = alias[0]
        row = alias[1]
        col = alias[2]
        
        logstr('Alias "{0}" found at {1}:{2}'.format(al, row, col))
        logstr('-' * SEP_SIZE)
        logstr(lines[row - 1].rstrip())
        logstr(' ' * (col - 1) + '^')
        logstr('*' * SEP_SIZE)
        
    return
    
"""
Log a string into the report file and console
"""
def logstr(msg):
    print(msg)
    repfile.write(msg + "\n")

def printhelp():
    print("""
A script to check C# files for use of aliases. So far the aliases are only 
detected. A report of found aliases is made both in a console and in a file
{0}

Usage: AliasRemover.py [options]

Options:
-h|--help: displays this help
-p|--pattern <pattern>: determines the pattern which the paths of the .cs 
files have to match in order to be checked. Full path of the file is checked 
with the re.search function of Python.
        """.format(REP_FILE))

#############################################
# Main
#############################################
          
#create a report file
repfile = open(REP_FILE, 'w')
          
def main(argv):
    # parse command line args
    filpat = r'.*'
    try:
        opts, args = getopt.getopt(argv,"hp:",["help", "pattern="])
    except getopt.GetoptError:
        printhelp()
        sys.exit()         
        
    for opt, arg in opts:
        if opt == '-h':
            printhelp()
            sys.exit()
        elif opt in ("-p", "--pattern"):
            filpat = arg
            
    # go the directory where this script is located
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # get the C# files
    csfiles = []
    for root, dirnames, filenames in os.walk('.'):
        for filename in fnmatch.filter(filenames, '*.cs'):
            fullpath = os.path.join(root, filename)
            if (re.search(filpat, fullpath)):
                csfiles.append(fullpath)
    
    # process each .cs file
    for fname in csfiles:
        logstr('\n\n' + '|' * SEP_SIZE)
        logstr("Checking file :" + fname)
        logstr('|' * SEP_SIZE + '\n\n')
        
        file = open(fname, "r")
        lines = file.readlines()
        file.close()
            
        analysedoc(lines)
        
    repfile.close()
        
    # get the user a chance to see the output
    print("Press any key to finish")
    sys.stdin.read(1)    
            
if __name__ == "__main__":
    main(sys.argv[1:])
