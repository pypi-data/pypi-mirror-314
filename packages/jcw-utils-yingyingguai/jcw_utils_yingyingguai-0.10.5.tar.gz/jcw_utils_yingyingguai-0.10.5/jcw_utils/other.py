
import time
import os
from copy import deepcopy
from pprint import pprint
import uuid
import sys
import importlib

def clear_print(content,time_sleep=0):
    if os.name=='nt':
        os.system('cls')
    else:
        os.system('clear')
    temp=deepcopy(content)
    def backtrace_cut(dictobj):
        if isinstance(dictobj,dict):
            for k,v in dictobj.items():    
                if isinstance(v,str) and len(v)>100:
                    dictobj[k]=v[:50]+v[-50:]
                elif isinstance(v,dict):
                    backtrace_cut(v)
        return dictobj
    pprint(backtrace_cut(temp))
    time.sleep(time_sleep)
    

def import_if_not_exists(package_names):
    for package_name in package_names:
        if package_name not in sys.modules:
            importlib.import_module(package_name)
            # print(f"{package_name} was imported.")
            pass
        else:
            # print(f"{package_name} is already imported.")
            pass
        
class CustomVector:
    def __init__(self,init_value=[],x_range=None,y_range=None,dim=None):
        if init_value!=[]:
            self.vector=init_value
        elif dim == None:
            self.vector=[0]*2

    def __add__(self,other):
        return [self.vector[i]+other.vector[i] for i in range(len(self.vector))]
    
    def __sub__(self,other):
        return [self.vector[i]-other.vector[i] for i in range(len(self.vector))]
    
    def __mul__(self,scale):
        return [self.vector[i]*scale for i in range(len(self.vector))]
    
    def norm(self):
        return sum([i**2 for i in self.vector])**0.5
    
    def __truediv__(self,scale):
        return [self.vector[i]*(1/scale) for i in range(len(self.vector))]
    
    def __str__(self) -> str:
        return str(self.vector)
    
    def dot(self,other):
        return sum([self.vector[i]*other.vector[i] for i in range(len(self.vector))])
    
    #两个向量之间的欧氏距离
    def euclidean_distance(self,other):
        return sum([(self.vector[i]-other.vector[i])**2 for i in range(len(self.vector))])**0.5
    
# test=CustomVector([1,2])
# print(test)
# print(test.dot(CustomVector([1,0])))
# print(test.norm())
# print(test*2)
# print(test/2)
# print(type(test))

def easy_install(requirement_file_path):
    # import argparse
    import subprocess
    # parser = argparse.ArgumentParser(description="Install packages listed in a file using pip.")
    # parser.add_argument('-r', required=True, help="Path to the requirements file.")
    # args = parser.parse_args()

    # # Get the file name from the -r argument
    # requirements_file = args.r

    with open(requirement_file_path, 'r') as file:
        lines = file.readlines()

    package_install_fail1=[]
    # Loop through each line and install the package using pip
    for line in lines:
        package = line.strip()  # Remove leading/trailing whitespace
        try:
            subprocess.run(['pip', 'install', package], check=True)
        except Exception as e:
            package_install_fail1.append(package)
    print(f'package_install_fail:{package_install_fail1}')
# path=r'E:\高频常用函数\requirements.txt'
# easy_install(path)

import subprocess
import sys
import re
def run_script_with_auto_install(script_path):
    """
    Run a Python script, and automatically install missing modules if a ModuleNotFoundError occurs.

    Args:
        script_path (str): The path to the Python script to run.
    """
    while True:
        try:
            # Attempt to run the script
            result = subprocess.run([sys.executable, script_path], check=True, capture_output=True, text=True)
            print(repr(result.stdout))  # Print script's output if it runs successfully
            break  # Exit loop if script runs successfully
        except subprocess.CalledProcessError as e:
            # Check if the error is a ModuleNotFoundError
            if "ModuleNotFoundError" in e.stderr:
                # Extract the missing module name using regex
                match = re.search(r"No module named '(.*?)'", e.stderr)
                if match:
                    missing_module = match.group(1)
                    print(f"Missing module detected: {missing_module}")
                    print(f"Attempting to install {missing_module}...")

                    # Install the missing module
                    install_result = subprocess.run([sys.executable, "-m", "pip", "install", missing_module])
                    if install_result.returncode != 0:
                        print(f"Failed to install {missing_module}. Exiting.")
                        sys.exit(1)
                else:
                    print("Could not determine the missing module. Exiting.")
                    sys.exit(1)
            else:
                # If it's not a ModuleNotFoundError, re-raise the error
                print("An error occurred:")
                print(e.stderr)
                sys.exit(1)
# script_to_run = r"E:\高频常用函数\jcw_utils\audio_operation.py"
# run_script_with_auto_install(script_to_run)


