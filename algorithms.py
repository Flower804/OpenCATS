import math
import numpy
import pygame

def deg2rad(deg):
    return deg * (math.pi/180)

def calculate_distance_LatLon(cords1, cords2):
    #for cords to be defined as an float array of [lat, lon]
    radios = 6372 #radios of the earth

    dlat = deg2rad(cords1[1] - cords2[1])
    dlon = deg2rad(cords1[2] - cords2[2])

    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(deg2rad(cords1[1])) * math.cos(deg2rad(cords2[1])) * math.sin(dlon/2) * math.sin(dlon/2)

    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = radios * c #distance in km
    return distance