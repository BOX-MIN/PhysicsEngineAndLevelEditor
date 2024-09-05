import pygame_gui
import pymunk
import pygame
import math

space = pymunk.Space()
space.gravity = (0, 1000)
space.damping = 0.59

def fluid_sim_collide(arbiter, space, data):
    fluid_sim_force = 100
    body1 = arbiter.shapes[0].body
    body2 = arbiter.shapes[1].body

    distance = math.sqrt((body1.position[0] - body2.position[0]) ** 2 + (body1.position[1] - body2.position[1]) ** 2)

    if distance == 0:
        distance += 0.1

    body1.apply_impulse_at_local_point((0, fluid_sim_force))
    body2.apply_impulse_at_local_point((0, fluid_sim_force))
    return True

fluid_sim_collision_handler = space.add_collision_handler(3, 3)
fluid_sim_collision_handler.pre_solve = fluid_sim_collide

pygame.init()
clock = pygame.time.Clock()
fps = 120
screen = pygame.display.set_mode((1280, 720), pygame.OPENGL | pygame.DOUBLEBUF)
display = pygame.Surface(pygame.display.get_window_size())
gui_display = pygame.Surface(pygame.display.get_window_size())

manager = pygame_gui.UIManager(pygame.display.get_window_size())

time = 0        # for shaders

camx = 0
camy = 0
camspeed = 4



