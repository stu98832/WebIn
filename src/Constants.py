import sys
import os

if getattr(sys, 'frozen', False):
    ROOT_DIR = os.path.abspath(os.path.dirname(sys.executable))
else:
    # For Develop
    ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]), '..'))