import pygame
import os
import sys

#*************************************************************************#
#                                                                         #
#                                                                         #
# airplanes.py                                                 _____      #
#                                                             _|___ /     #  
# By: Flower :3 <gabrielmoita34@gmail.com                    (_) |_ \     #  
# GitHub: Flower804                                           _ ___) |    #  
# Created: 2025/12/02 14:34:57 by Flower:3                   (_)____/     #                  
#                                                                         #
#                                                                         #
#*************************************************************************#
#TODO: Simplify all , creating this on a whim so things will be messy
#all of this was kinda based on Alexander Farrel's pygame invenotry system
#https://youtu.be/1q_0l71Ln7I?si=Zrl7QKst3h7ONtkh
base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))  
image_path = os.path.join(base_path, "airplanes")

class ItemType:
    def __init__(self, name, icon, stack_size=1):
        self.name = name
        self.icon_name = icon
        self.icon = pygame.image.load(image_path + "/" + icon)
        self.value = 0
        self.weight = 0
        self.stack_size = stack_size

class ItemSlot:
    def __init__(self):
        self.type = None
        self.amount = 0

class Iventory:
    #creates a new inventory
    def __init__(self, capacity):
        self.capacity = capacity
        self.taken_slots = 0
        self.slots = []
        for _ in range(self.capacity):
            self.slots.append(ItemSlot())
        self.listener = None
    
    def notify(self):
        if self.listener is not None:
            self.listener.refresh()
    
    #Atempt to add a certain amount of an item to the iventory
    def add(self, item_type, amount=1):
        if item_type.stack_size > 1:
            for slot in self.slots:
                if slot.type == item_type:
                    add_amount = amount
                    if add_amount > item_type.stack_size - slot.amount:
                        add_amount = item_type.stack_size - slot.amount
                    slot.amount = slot.amount + add_amount
                    amount = amount - add_amount
                    if amount <= 0:
                        self.notify()
                        return 0 
        for slot in self.slots:
            if slot.type == None:
                slot.type = item_type
                if item_type.stack_size < amount:
                    slot.amount = item_type.stack_size
                    self.notify()
                    return self.add(item_type, amount - item_type.stack_size)
                else:
                    slot.amount = amount
                    self.notify()
                    return 0
        return amount
                
    
    #atempt to remove a certain amount of an item to the iventory
    def remove(self, item_type, amount=1):
        found = 0
        for slot in self.slots:
            if slot.type == item_type:
                if slot.amount < amount:
                    found = found + slot.amount
                    continue
                elif slot.amount == amount:
                    found = found + amount
                    slot.amount = 0
                    slot.type = None
                    self.notify()
                    return found
                else:
                    found = found + amount
                    slot.amount = slot.amount - amount
                    slot.type = None
                    self.notify()
                    return found
        return found 
    
    def has(self, item_type, quantity=1):
        #found = 0
        #for slot in self.slots:
        #    if slot.type == item_type:
        #        found = found + slot.amount
        #        if found >= amount:
        #            True
        #return False
        for slot in self.slots:
            if slot.type is not None and slot.type.name == item_type.name:
                if slot.amount >= quantity:
                    return True
        return False 
        


    