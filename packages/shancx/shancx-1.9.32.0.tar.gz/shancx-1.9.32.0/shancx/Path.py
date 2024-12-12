
    
import os 
def CurPath():
    current_file_path = os.path.abspath(__file__) 
    current_folder_path = os.path.dirname(current_file_path)
    return current_folder_path

import sys
def CurPathplus():
    # 获取当前执行文件的绝对路径
    current_file_path = os.path.abspath(sys.argv[0])
    current_folder_path = os.path.dirname(current_file_path)
    return current_folder_path

from pathlib import Path 
def RootFilePaths(root_path=None):
    root_dir = Path(f'{root_path}')
    npy_files = list(root_dir.rglob('*.*'))
    return npy_files
""" 
import gzip
with gzip.open(file_path=None, 'rt') as file:
    first_line = file.readline()
"""

"""
CSV

import gzip
import csv

with gzip.open(file_path, 'rt') as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)

XML

import gzip
import xml.etree.ElementTree as ET

with gzip.open(file_path, 'rt') as file:
    tree = ET.parse(file)
    root = tree.getroot()
    for child in root:
        print(child.tag, child.attrib)

YAML        

import gzip
import yaml
with gzip.open(file_path, 'rt') as file:
    data = yaml.safe_load(file)
    print(data)

TEXT

import gzip

with gzip.open(file_path, 'rt') as file:
    for line in file:
        print(line.strip())

"""
