#!/usr/bin/env python3
"""Searchs directory for HTML and replaces any include comments"""

#imports
import os
import glob
import re
import filecmp
from datetime import datetime


#Global Variables
BASEDIR = "/opt/website/intake/"
OUTDIR = "/opt/website/transform/"
TEMPDIR = "/tmp/"

FILEDICT = {}


def convert_html(htmlfile):
    """Processes the file to static content"""
    #print("Processing file " + htmlfile)
    def get_include_file_content(x):
        """Reads the content of all the include files listed in html file"""
        file_to_read =  x.group(2)
        include_file = BASEDIR + file_to_read
        if include_file in FILEDICT.keys():
            return FILEDICT[include_file]
        else:
            if os.path.exists(include_file):
                try:
                    include_content = open(include_file,'r').read()
                except:
                    include_content = open(include_file,'r', encoding="utf8").read()
                FILEDICT[include_file] = include_content
                return include_content
            else:
                print("File Doesn't Exist " + include_file)
    content = open(htmlfile, 'r',errors='ignore').read()
    content = re.sub(r'<!-- *#include *(virtual|file)=[\'"]([^\'"]+)[\'"] *-->', get_include_file_content, content)
    return content

def create_htmlfile(filecontent,filepath):
    """"Creates the files in the output directory"""
    print("Updating file " + filepath)
    if not os.path.exists(os.path.dirname(filepath)):
        os.makedirs(os.path.dirname(filepath))
    output_html_file = open(filepath, 'w')
    output_html_file.writelines(filecontent)
    output_html_file.close()



###### Main #######
if __name__ == '__main__':
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " Start processing")
    os.chdir(BASEDIR)

    #Get all HTML and convert to static pages
    for htmlfile in glob.glob("**/*.html", recursive=True):
        converted = convert_html(htmlfile)
        #create temp file
        tempfile = TEMPDIR+'temp.html'
        tmp_file = open(tempfile, 'w')
        tmp_file.writelines(converted)
        tmp_file.close()
        if os.path.exists(OUTDIR+htmlfile):
            if not filecmp.cmp(OUTDIR+htmlfile, tempfile, shallow=False):
                create_htmlfile(converted, OUTDIR+htmlfile)
            else:
                print("No change to " + OUTDIR+htmlfile)
        else:
             create_htmlfile(converted, OUTDIR+htmlfile)
    print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " End of processing")