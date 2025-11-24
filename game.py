import pygame
import random
from Countries import Countries
from algorithms import glow
from json import load, dump
from enum import Enum, auto, IntEnum
import settings
import os
import sys
import datetime
from dataclasses import dataclass, field
from typing import Optional, Any
from classes import (
    fontalias,
    primary,
    secondary,
    tertiary
)


#check if sys is good
if(getattr(sys, "frozen", False)): 
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
else:
    base_path = os.path.dirname(os.path.abspath(__file__))

THICCMAX = 5

@dataclass
class Vectoi:
    x: int = 0
    y: int = 0
    
    def to_tuple(self) -> tuple[int, int]:
        return(self.x, self.y)

@dataclass
class ButtonConfig:
    string: str = ""
    thiccccc: int = 0
    image: Optional[pygame.Surface] = None

@dataclass #how I hate you javascript
class ButtonDraw:
    pos: Vectoi = field(default_factory=Vectoi)
    size: Vectoi = field(default_factory=Vectoi)
    button: ButtonConfig = field(default_factory=ButtonConfig)
    text: Optional[str] = None
    text_font: Optional[pygame.font.Font] = None

def draw_button(screen: pygame.Surface, mouse_pos: tuple[int, int], button_draw: ButtonDraw) -> bool:
    pos = button_draw.pos.to_tuple()
    size = button_draw.size.to_tuple()
    button = button_draw.button
    text = button_draw.text or button.string
    text_font = button_draw.text_font
    
    rect = pygame.Rect(pos, size)
    
    hovered = pygame.Rect.collidepoint(rect, mouse_pos)
    
    if(hovered):
        if button.thiccccc < THICCMAX:
            button.thiccccc = button.thiccccc + 1
        else:
            button.thiccccc = max(button.thiccccc - 1, 0)
    
    scaled_thicc = button.thiccccc * settings.ui_scale
    
    if scaled_thicc:
        pygame.draw.rect(
            screen,
            secondary,
            pygame.Rect(
                rect.x - scaled_thicc,
                rect.y - scaled_thicc,
                rect.width + scaled_thicc * 2,
                rect.height + scaled_thicc * 2,    
            ),
            border_radius= rect.height * scaled_thicc // 2,
        )
        
        pygame.draw.rect(screen, tertiary, rect, border_radius=rect.height)
        
        if(button.image):
            screen.blit(
                button.image,
                (
                    rect.centerx - button.image.get_width() / 2,
                    rect.y,
                ),
            )
            
        if(text and text_font):
            text_color = secondary if hovered else primary
            text_surface: pygame.Surface = text_font.render(text, fontalias, text_color)
            screen.blit(
                text_surface,
                (
                    rect.centerx - text_surface.get_width() / 2,
                    rect.y + (THICCMAX * settings.ui_scale),
                ),
            )
            
    return hovered

class Menu(Enum): #create a unique constant value for each menu
    MAIN_MENU = auto()
    COUNTRY_SELECT = auto()
    SETTINGS = auto()
    CREDITS = auto()
    GAME = auto()
    ESCAPEMENU = auto()


def compare_cords(mouse_pos, object):
        if(mouse_pos == object):
            return True 
        else:
            return False


#class Game:
#    def __init__(self, screen, clock):
#        self.screen = screen
#        self.clock = clock
#        self.width, self.height = self.screen.get_size()
#        
#        self.world = World(10, 10, self.width, self.height)
#        
#        map = Map("Modern World", (0, 0), 1)
        
def main():
    pygame.display.set_caption("OpenCATS")
    icon = pygame.image.load(os.path.join(base_path, "ui", "HOMOkisssssssssss.png"))
    #make icon
    
    speed = 0
    sidebar_tab = ""
    sidebar_pos = -625
    
    #TODO: add musics
    music_tracks = ["", ""]
    music_index = 0
    
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080), pygame.DOUBLEBUF | pygame.SCALED, vsync=1)
    
    pygame.mixer.init()
    
    #NOTE: keep this for debugg reasons
    
    current_menu = Menu.MAIN_MENU
    tick = 0
    mouse_just_pressed = False
    mouse_scroll = 0
    
    settings_json: dict[str, Any] = {
        "Scroll Invert": 1,
        "UI Size": 14,
        "FPS": 60,
        "Sound Volume": 50,
        "Music Volume": 50,
        "Music Track": "Some song" #TODO" change this to default song
    }
    
    try:
        with open(os.path.join(base_path, "settings.json")) as f:
            settings_json = load(f)
    except FileNotFoundError:
        with open(os.path.join(base_path, "settings.json"), "w") as f:
            dump(settings_json, f)
    
    with open(os.path.join(base_path, "province-centers.json")) as f:
       province_centers = load(f)
    
    pygame.font.init()
    smol_font = pygame.font.Font(os.path.join(base_path, "ui", "font.ttf"), 12 * settings.ui_scale)
    ui_font = pygame.font.Font(os.path.join(base_path, "ui", "font.ttf"), 12 * settings.ui_scale)
    title_font = pygame.font.Font(os.path.join(base_path, "ui", "font.ttf"), 12 * settings.ui_scale)
    
    game_title = glow(title_font.render("OpenCATS", fontalias, primary), 5, primary)
    game_logo = glow(pygame.image.load(os.path.join(base_path, "ui", "logo.png")).convert_alpha(), 5, primary)
    
    menubg = pygame.image.load(os.path.join(base_path, "ui", "HOMOkisssssssssss.png"))    
    
    clock = pygame.time.Clock()
    
    division_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    division_path = {}
    division_time_second = 1.0
    
    camera_pos = pygame.Vector2
    
    main_menu_buttons = [
        ButtonConfig("Start Game"),
        ButtonConfig("Continue Game"),        
        ButtonConfig("Settings"),        
        ButtonConfig("Credits"),        
        ButtonConfig("Exit")        
    ]
    
    global_run = True
    while global_run:
        mouse_rel = pygame.mouse.get_rel()
        mouse_pos = pygame.mouse.get_pos()
        mouse_scroll = 0
        mouse_just_pressed = False

        
        for event in pygame.event.get():
            match event.type:
                case pygame.QUIT:
                    global_run = False
        screen.fill((0, 0, 0)) #clear the screen
        
        if(current_menu != Menu.GAME):
            screen.blit(menubg, (0, 0))
        
        match current_menu:
            case Menu.ESCAPEMENU:
                #TODO: escapemenu
                print("on escape")
            case Menu.MAIN_MENU:
                screen.blit(game_title, (400, 160))
                screen.blit(game_logo, (30, 30))

                button_draw = ButtonDraw(
                    size = Vectoi(160, 40),
                    text_font = ui_font,
                    pos = Vectoi(120, game_logo.get_height() + 30)
                )

                padding: int = 60

                for button in main_menu_buttons:
                    button_draw.button = button

                    hovered = draw_button(screen, mouse_pos, button_draw)
                    button_draw.pos.y += padding + button_draw.size.y

                    if not mouse_just_pressed or not hovered:
                        continue
                    
                    match button.string:
                        case "Start Game":
                            current_menu = Menu.COUNTRY_SELECT
                        case "Settings":
                            current_menu = Menu.SETTINGS
                        case "Credits":
                            current_menu = Menu.CREDITS
                        case "Exit":
                            global_run = False
            case Menu.SETTINGS:
                #TODO: do setings
                print("on settings")
            case Menu.COUNTRY_SELECT:
                print("on country select")
            case Menu.CREDITS:
                print("on credits")
            case Menu.GAME:
                print("on game")

        tick = tick + 1
        
        division_time_second = division_time_second - clock.tick(settings_json["FPS"])/1000.0
        
        if division_time_second <= 0: #somethings is going super wrong
            print("wait")
            division_time_second = 1.0
            if len(division_path) > 0:
                r, g, b = division_path.pop(0)
                division_pos = pygame.Vector2(province_centers[f])

        pygame.display.update()
main()