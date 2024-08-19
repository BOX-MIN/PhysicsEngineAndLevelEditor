import pygame_gui
import pymunk
import pygame

space = pymunk.Space()
space.gravity = (0, 1000)
space.damping = 0.59

pygame.init()
clock = pygame.time.Clock()
fps = 120
screen = pygame.display.set_mode((1280, 720), pygame.OPENGL | pygame.DOUBLEBUF)
display = pygame.Surface(pygame.display.get_window_size())
gui_display = pygame.Surface(pygame.display.get_window_size())

manager = pygame_gui.UIManager(pygame.display.get_window_size())

time = 0        # for shaders



