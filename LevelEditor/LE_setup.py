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

import pygame
import os

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

# path to save files location
# if encountering 'FileNotFoundError: [WinError 3] The system cannot find the path specified:',
# try to change this and see if that fixes it
filepath = os.path.join('PymunkPhysicsAndLevels', 'LevelData')
