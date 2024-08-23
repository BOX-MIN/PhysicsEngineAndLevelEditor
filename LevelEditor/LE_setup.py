import pygame

pygame.init()
clock = pygame.time.Clock()
fps = 120
le_display = pygame.display.set_mode((1280, 720))
le_screen = pygame.Surface(pygame.display.get_window_size())

xPos = 0
yPos = 0
xVel = 0
yVel = 0
friction = 0.9
speed = 1
