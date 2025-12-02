import pygame
import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.dropdown import Dropdown
import os
import sys
from enum import Enum, auto, IntEnum
from airplanes import Iventory, ItemType
from plane import Plane
#*************************************************************************#
#                                                                         #
#                                                                         #
# main.py                                                      _____      #
#                                                             _|___ /     #  
# By: Flower :3 <gabrielmoita34@gmail.com                    (_) |_ \     #  
# GitHub: Flower804                                           _ ___) |    #  
# Created: 2025/11/09 17:44:32 by Flower:3                   (_)____/     #                  
#                                                                         #
#                                                                         #
#*************************************************************************#

def load_image_map():
    img = pygame.image.load(os.path.join(base_path, "ui", "Portugal-map-withpoints.jpg")).convert()
    width, height = img.get_size()
    
    map_data = []
    special_points = {
        "Humberto Delgado Airport ": [],
        "Francisco Sa Carneiro Airport ": [],
        "AI Gago Coutinho": []
    }
    
    for i in range(height):
        row = []
        #print("In loop")
        for j in range(width):
            color = img.get_at((j, i))[:3]
            row.append(color)
            
            if color == (255, 0, 1):
                special_points["Humberto Delgado Airport "] = (j, i)
                print("special point on ")
                print((i, j))
            elif color == (255, 0, 2):
                special_points["AI Gago Coutinho"] = (j, i)
                print("special point on ")
                print((i, j))
            elif color == (255, 0, 3):
                special_points["Francisco Sa Carneiro Airport "] = (j, i)
                print("special point on ")
                print((i, j))
        map_data.append(row)
    return map_data, special_points

def coords_with_zoom(wx, wy, camera_zoom, camera_x, camera_y):
    sx = wx * camera_zoom + camera_x
    sy = wy * camera_zoom + camera_y
    
    return sx, sy
       
def draw_iventory(surface, x, y, inventory, font):
    offset_y = 0
    
    for slot in inventory.slots:
        if slot.type == None:
            continue
        
        #draw the icons
        surface.blit(slot.type.icon, (x, y + offset_y))
        
        #draw name
        label = font.render(slot.type.name, True, (255, 255, 255))
        surface.blit(label, (x + 40, y + offset_y + 5))
        
        #draw amount
        amount_label = font.render(f"x{slot.amount}", True, (200, 200, 200))
        surface.blit(amount_label, (x + 40, y + offset_y + 30))
        
        offset_y = offset_y + 60
             
class Menu(Enum):
    MAIN_MENU = auto()
    SETTINGS = auto()
    GAME = auto()
    SHOP = auto()
    ESCAPEMENU = auto()
    
base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))    

#main menu things

planes = pygame.sprite.Group()

def main():
    pygame.display.set_caption("OpenCATS")
    icon = pygame.image.load(os.path.join(base_path, "ui", "HOMOkisssssssssss.png"))
    pygame.display.set_icon(icon)
    
    name = "openCATS"
    
    pygame.init()
    screen = pygame.display.set_mode((1068, 768))
    
    clock = pygame.time.Clock()
    #main menu things
    menubg = pygame.image.load(os.path.join(base_path, "ui", "menu.png")).convert_alpha()
    font = pygame.font.Font(os.path.join(base_path, "ui", "font.ttf"))
    
    gamebg = pygame.image.load(os.path.join(base_path, "ui", "Portugal-map.jpg")).convert_alpha()
    
    title = font.render(name, True, (255, 255, 255))

    Map = pygame.image.load(os.path.join(base_path, "ui", "Portugal-map.jpg")).convert_alpha()
    
    #iventory stuff
    airplane_small = ItemType("Small Plane", "icon_small.png", stack_size=10)
    airplane_big = ItemType("Big Plane", "icon_big.png", stack_size=5)
    
    player_iventory = Iventory(20)
    
    player_iventory.add(airplane_small, 3)
    player_iventory.add(airplane_big, 1)
    
    
    map_pixels, points = load_image_map()
    
    selected_airport = "Humberto Delgado Airport "
    
    #dropdown menus
    airport_names = list(points.keys())
    
    dropdown = Dropdown(
        screen,
        -9999, 100,
        200, 40,
        name = 'Select airport',
        choices= airport_names,
        borderRadius = 3,
        colour = pygame.Color('green'),
        values = airport_names,
        direction = 'down',
        textHAlign = 'left'
    )
    
    def print_values():
        #airport_to_go = dropdown.getSelected()
        #
        #print(selected_airport)
        #print(" to go to ")
        #print(airport_to_go)
        
        airport_from = selected_airport
        airport_to = dropdown.getSelected()
        
        start = points[airport_from]
        end = points[airport_to]
        
        start_screen = coords_with_zoom(start[0], start[1], camera_zoom, camera_x, camera_y)
        end_screen = coords_with_zoom(end[0], end[1], camera_zoom, camera_x, camera_y)
        
        plane = Plane(
            os.path.join(base_path, "airplanes", "icon_small.png"),
            start_screen,
            end_screen,
            speed = 2
        )
        
        planes.add(plane)
        
    sidebar_button = Button(
        screen,
        -9999, 150,
        180, 40,
        text = 'calculate rout',
        fontSize = 18,
        margin = 5,
        inactiveColour = (255, 0, 0),
        pressedColour = (0, 255, 0),
        radius = 5,
        onClick = lambda: print_values(), #lambda prevents the function of running imidealtly
        font = pygame.font.SysFont('calibri', 20)
    ) 
    
    #camera things
    camera_x = 0
    camera_y = 0
    scroll_speed = 5
    camera_zoom = 1.0
    zoom_speed = 0.1
    
    speed = 0
    
    #menus
    sidebar_open = False
    sidebar_x = -300
    SIDEBAR_WIDTH = 300
    SIDEBAR_SPEED = 20
    selected_airport = None
    
    #debug things
    current_menu = Menu.MAIN_MENU
    tick = 0
    
    global_run = True
    while global_run:
        events = pygame.event.get()
        for event in events:
            match event.type:
                case pygame.QUIT:
                    global_run = False
                    
                case pygame.KEYDOWN:
                    match event.key:
                        case pygame.K_F4:
                            pygame.display.toggle_fullscreen()
                        case pygame.K_ESCAPE:
                            if current_menu == Menu.GAME:
                                current_menu = Menu.ESCAPEMENU
                                
            if(event.type == pygame.MOUSEWHEEL):
                if(event.y > 0):
                    camera_zoom = camera_zoom + zoom_speed
                else:
                    camera_zoom = camera_zoom - zoom_speed
                    
            camera_zoom = max(0.3, min(3.0, camera_zoom))    #cap the zoom bethwenm 3 amd 0.3                
        keys = pygame.key.get_pressed()
        
        if(keys[pygame.K_w]):
            camera_y = camera_y + scroll_speed
        if(keys[pygame.K_s]):
            camera_y = camera_y - scroll_speed
        if(keys[pygame.K_a]):
            camera_x = camera_x + scroll_speed
        if(keys[pygame.K_d]):
            camera_x = camera_x - scroll_speed
        
        screen.fill((0, 0, 0)) #clear the screen
        match current_menu:
            case Menu.MAIN_MENU:
                Button1 = pygame.Rect(380, 250, 300, 100)
                Button2 = pygame.Rect(380, 375, 300, 100)
                Button3 = pygame.Rect(380, 500, 300, 100)
                
                screen.blit(menubg, (0, 0))
                screen.blit(title, (150, 75))
                
                #TODO: make buttons grayscale
                pygame.draw.rect(screen, (0, 0, 0), Button1, border_radius= 10) #screen, color, identity, border
                pygame.draw.rect(screen, (0, 0, 0), Button2, border_radius= 10) 
                pygame.draw.rect(screen, (0, 0, 0), Button3, border_radius= 10)
                
                play = font.render("Play", True, (245, 222, 179))
                settings = font.render("Settings", True, (245, 222, 179))
                leave = font.render("Leave", True, (245, 222, 179))
                
                screen.blit(play, (Button1.x + 85, Button1.y + 15))
                screen.blit(settings, (Button2.x + 70, Button2.y + 15))
                screen.blit(leave, (Button3.x + 55, Button3.y + 15))
                
                mouse_pos = pygame.mouse.get_pos()
                
                if(Button1.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]):
                    print("going to menu game")
                    current_menu = Menu.GAME
                elif(Button2.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]):
                    print("going to menu settings")
                    current_menu = Menu.SETTINGS
                elif(Button3.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]):
                    print("exiting")
                    global_run = False
                
                print("in main menu")
                
            case Menu.GAME:
                #---------------------Buttons and things for airports-------------------------
                
                #coordinates from converter 
                hx, hy = points["Humberto Delgado Airport "]
                ax, ay = points["AI Gago Coutinho"]
                fx, fy = points["Francisco Sa Carneiro Airport "]

                #transformed with zoom
                hx_s, hy_s = coords_with_zoom(hx, hy, camera_zoom, camera_x, camera_y)
                ax_s, ay_s = coords_with_zoom(ax, ay, camera_zoom, camera_x, camera_y)
                fx_s, fy_s = coords_with_zoom(fx, fy, camera_zoom, camera_x, camera_y)
                
                button_w = int(180 * camera_zoom)
                button_h = int(180 * camera_zoom)
                
                Button_humberto =  pygame.Rect(hx_s, hy_s, button_w, button_h)
                Button_Faro = pygame.Rect(ax_s, ay_s, button_w, button_h)
                Button_Francisco = pygame.Rect(fx_s, fy_s, button_w, button_h)
                
                #screen.blit(gamebg, (camera_x, camera_y)) --> no scale
                scaled_map = pygame.transform.smoothscale(
                    gamebg,
                    (int(gamebg.get_width() * camera_zoom),
                     int(gamebg.get_height() * camera_zoom))
                )
                
                screen.blit(scaled_map, (camera_x, camera_y))
                
                pygame.draw.rect(screen, (0, 0, 0), Button_humberto, border_radius = 10)
                pygame.draw.rect(screen, (0, 0, 0), Button_Faro, border_radius = 10)
                pygame.draw.rect(screen, (0, 0, 0), Button_Francisco, border_radius = 10)
                 
                humberto = font.render("Humberto Delgado", True, (245, 222, 179))
                Faro = font.render("AI Gago Coutinho", True, (245, 222, 179))
                Francisco = font.render("Francisco Sa Carneiro", True, (245, 222, 179))
                
                #--------------------- Buttons on the side bar--------------------------------------
                
                Button_Airplanes_x = sidebar_x + 20
                Button_Airplanes_y = 240
                
                Button_Airplanes = pygame.Rect(Button_Airplanes_x, Button_Airplanes_y, 180, 40)
                pygame.draw.rect(screen, (0, 0, 0), Button_Airplanes, border_radius = 10)
                Airplanes = font.render("Buy Airplanes", True, (245, 222, 179))
                
                title = font.render("Your frot", True, (255, 255, 255))
                
                screen.blit(humberto, (hx_s, hy_s))
                screen.blit(Faro, (ax_s, ay_s))
                screen.blit(Francisco, (fx_s, fy_s))                
                
                mouse_pos = pygame.mouse.get_pos()
                hover_humberto = Button_humberto.collidepoint(mouse_pos)
                hover_Faro = Button_Faro.collidepoint(mouse_pos)
                hover_Francisco = Button_Francisco.collidepoint(mouse_pos)
                
                if(pygame.mouse.get_pressed()[0]):
                    if(hover_humberto):
                        #print("clicked humberto")
                        selected_airport = "Humberto Delgado Airport "
                        sidebar_open = True
                    if(hover_Faro):
                        #print("clicked Faro")
                        selected_airport = "AI Gago Coutinho"
                        sidebar_open = True
                    if(hover_Francisco):
                        #rint("clicked Francisco")
                        selected_airport = "Francisco Sa Carneiro Airport "
                        sidebar_open = True
                    #TODO: fix this so that the buttons on the sidebar are still usable
                    #if((not hover_humberto) and (not hover_Faro) and (not hover_Francisco)):
                    #    sidebar_open = False
                if(sidebar_open and sidebar_x < 0):
                    sidebar_x = sidebar_x + SIDEBAR_SPEED
                elif(not sidebar_open and sidebar_x):
                    sidebar_x = sidebar_x - SIDEBAR_SPEED 
                    
                sidebar_rect = pygame.Rect(sidebar_x, 0, SIDEBAR_WIDTH, screen.get_height())
                pygame.draw.rect(screen, (30, 30, 30), sidebar_rect)
                
                if sidebar_open and selected_airport:
                    title = font.render(selected_airport, True, (255, 255, 255))
                    screen.blit(title, (sidebar_x + 20, 20))
                    
                    info_label = font.render("Airport Information ", True, (200, 200, 200))
                    screen.blit(info_label, (sidebar_x + 20, 80))
                    
                    dropdown.setX(sidebar_x + 20)
                    dropdown.setY(120)
                    
                    DROPDOWN_WIDTH = 200
                    SPACING = 20
                    
                    sidebar_button.setX(sidebar_x + 20)
                    sidebar_button.setY(180)
                    
                    text_x = dropdown.getX() + dropdown.getWidth() + 10
                    text_y = dropdown.getY()
                    
                    current_selected = font.render(selected_airport, True, (255, 255, 255))
                    screen.blit(current_selected, (text_x, text_y))
                else:
                    dropdown.setX(-9999)
                    sidebar_button.setX(-9999)
                    
                    screen.blit(title, (sidebar_x + 20, 20))
                    screen.blit(Airplanes, (Button_Airplanes_x + 10, Button_Airplanes_y + 10))
                    
                    draw_iventory(
                        screen,
                        sidebar_x + 20,
                        Button_Airplanes_y + 80,
                        player_iventory,
                        font
                    )
                    
                    hover_shop = Button_Airplanes.collidepoint(mouse_pos)
                    
                    if(pygame.mouse.get_pressed()[0]):
                        if(hover_shop):
                            current_menu = Menu.SHOP
                            print("going to shop")
                    
                    
                close_button = pygame.Rect(sidebar_x + SIDEBAR_WIDTH - 40, 10, 30, 30)
                pygame.draw.rect(screen, (120,0,0), close_button)
                x_label = font.render("X", True, (255, 255, 255))
                screen.blit(x_label, (sidebar_x + SIDEBAR_WIDTH - 35, 12))
                
                if(pygame.mouse.get_pressed()[0]):
                    if(close_button.collidepoint(mouse_pos)):
                        sidebar_open = False
                        
                planes.update()
                planes.draw(screen)
                #print("on game")
                #print(points)
            case Menu.SHOP:
                for event in events:
                    match event.type:
                        case pygame.KEYDOWN:
                            match event.key:
                                case pygame.K_ESCAPE:
                                    current_menu = Menu.GAME
                #Button_exit = pygame.rect()
            case Menu.SETTINGS:
                print("on Settings")
        pygame_widgets.update(events)
        pygame.display.update()

main()