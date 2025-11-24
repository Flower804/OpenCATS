import os
from json import load
import pygame
from pygame.rect import Rect

base_path = os.path.dirname(__file__)

cwd = os.getcwd()
with open(os.path.join(base_path, "theme.json")) as f:
    theme = load(f)
    primary = tuple(theme["primary"])
    secondary = tuple(theme["secondary"])
    tertiary = tuple(theme["tertiary"])
    fontalias = theme["fontalias"]