import pygame

pygame.init()
clock = pygame.time.Clock()
fps = 120
window_size = (1280, 720)
le_display = pygame.display.set_mode(window_size)
scroll_position = 0
zoom_power = 1
aspect_ratio = (le_display.width / le_display.height)
le_screen = pygame.Surface(pygame.display.get_window_size())

xPos = 0
yPos = 0
xVel = 0
yVel = 0
friction = 0.9
speed = 1

grid_size = 20

clipboard = []

input_mode = 'collisions/object placement'

show_object_menu = True

show_selection_filters = True

object_menu_width = 200
