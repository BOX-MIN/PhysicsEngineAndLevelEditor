# PhysicsEngineAndLevelEditor is a 2D physics engine and level editor
# in python, using pygame and pymunk, and rendering through openGL

# Copyright (C) 2024  Emmet Schell

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# any later version.

# this program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# To contact the author of this program, Email them at
# emmetschell@gmail.com.

import pygame_gui
import pymunk
import pygame
import math
import os

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



