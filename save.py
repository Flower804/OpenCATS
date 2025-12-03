import sys
import os
import fileinput

#the utils file will be formated in
#money
#number of small planes

base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))  

def get_money():
    with open(os.path.join(base_path, "util", "utils.txt"), "r") as file:
        return int(file.readline().strip())
    
def get_planes():
    file = open(os.path.join(base_path, "util", "utils.txt"), "r")
    
    content = file.readlines()
    
    file.close()
    return content[1]
    
def save_planes(new_quantity):
    file_path = os.path.join(base_path, "util", "utils.txt")
    
    with open(file_path, "r") as file:
        lines = file.readlines()
    
    lines[1] = str(int(new_quantity)) + "\n"
    
    with open(file_path, "w") as file:
        file.writelines(lines)
    
def update_money(new_quantity):
    #old_value = str(get_money())
    #new_value = str(new_quantity)
    
    file_path = os.path.join(base_path, "util", "utils.txt")
    
    #with fileinput.input(file_path, inplace=True) as file:
    #    for line in file:
    #        #print(line.replace(old_value, new_value), end='')
    #        if line.strip() == old_value:
    #            print(new_value)
    #        else:
    #            print(line, end='')
    
    lines = []
    with open(file_path, "r") as file:
        lines = file.readlines()
    
    lines[0] = str(int(new_quantity)) + "\n"
    
    with open(file_path, "w") as file:
        file.writelines(lines)      
    