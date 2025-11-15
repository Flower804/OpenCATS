import os
import random
from pygame import image, transform
from algorithms import round_corners
from json import load
import itertools

base_path = os.path.dirname(__file__)

class Countries:
    def __init__(self, data):
        self.countryData = data
        self.colorsToCountries = {tuple(v[0]): k for k, v in self.countryData.items()}
        self.countriesToFlags = {}
        self.Characters = {}
        
        for k in self.countryData:
            try:
                flag_path = os.path.join(base_path, "flags", f"{k.lower()}_flag.png")
                raw_flag = image.load(flag_path)
            except FileNotFoundError:
                raw_flag = image.load(os.path.join(base_path, "unknown.path.jpg")) #ups
                
            scaled = transform.scale_by(raw_flag, 475 / raw_flag.get_width())
            rounded = round_corners(scaled, 16)
            self.countriesToFlags[k] = rounded