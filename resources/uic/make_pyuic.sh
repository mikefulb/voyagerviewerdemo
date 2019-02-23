#!/bin/bash
echo "Making uic python files for voyagerviewer"

# set this to the location of pyuic5.bat on your system
PYUIC5="/c/Users/msf/Anaconda3/Library/bin/pyuic5.bat"

echo "imagearea_infi.ui"
$PYUIC5 imagearea_info.ui > ../../voyagerviewerdemo/uic/imagearea_info_uic.py

