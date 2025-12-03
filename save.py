import sys
import os
import fileinput

#the utils file will be formated in
#money
#number of small planes

base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))  

def get_money():
    file = open(os.path.join(base_path, "util", "utils.txt"), "r")
    
    content = file.readlines()
    
    file.close()
    return content[0]
    
def get_planes():
    file = open(os.path.join(base_path, "util", "utils.txt"), "r")
    
    content = file.readlines()
    
    file.close()
    return content[1]
    
def update_money(new_quantity):
    old_value = str(get_money())
    new_value = str(new_quantity)
    
    file_path = os.path.join(base_path, "util", "utils.txt")
    
    with fileinput.input(file_path, inplace=True) as file:
        for line in file:
            print(line.replace(old_value, new_value), end='')
    file.close()        
    