import math
import numpy
import pygame
import pygame.gfxdraw

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

def glow(surface, thicc, color):
    b = pygame.Surface(
        (surface.get_width() + (4 * thicc), surface.get_height() + (4 * thicc)),
        flags = pygame.SRCALPHA,
    )
    a = b.copy()
    b.blit(surface, (2 * thicc, 2 * thicc))
    pygame.transform.gaussian_blur()
    a.fill(color, special_flags=pygame.BLEND_RGBA_MIN)
    a.blit(surface, (2 * thicc, 2 * thicc), special_flags=pygame.BLEND_RGBA_ADD)
    return a

def round_corners(surface, radius):
    radius = radius * 3
    #create a copy of the surface BUT it's on alpha pils
    rounded_surface = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
    
    pygame.draw.rect(
        rounded_surface,
        (255, 255, 255),
        (0, 0, surface.get_width(), surface.get_height()),
        border_radius= radius,
    )