#!/usr/bin/env python3
"""Searchs directory for jpg and compresses them"""

#imports
import os
import glob
import re
import filecmp
import sys
import subprocess
from datetime import datetime

BASEDIR='/opt/website/intake'
OUTDIR='/opt/website/transform'



###### Main #######
if __name__ == '__main__':
        print(datetime.now().strftime('%Y-%m-%d %H:%M:%S') + " Start processing")
        os.chdir(BASEDIR)
        #Get all HTML and convert to static pages
        for jpgfile in glob.glob("**/*.jpg", recursive=True):
                print(jpgfile)
                subprocess.call('convert ' + jpgfile + ' -sampling-factor 4:2:0 -strip -quality 80 -interlace JPEG -colorspace sRGB ' + OUTDIR+'/'+jpgfile, shell=True)


