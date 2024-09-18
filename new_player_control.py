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

import pymunk
import pygame

import setup


class Leg:
    def __init__(self, target, length_top, length_bottom, pos_on_target=(0, 0)):
        self.top_leg_body = pymunk.Body()
        self.top_leg_poly = pymunk.Segment(self.top_leg_body, target.position, target.position + (0, length_top), 3)
        self.bottom_leg_body = pymunk.Body()
        self.bottom_leg_poly = pymunk.Segment(self.top_leg_body, target.position + (0, length_top),
                                              target.position + (0, length_top) + (0, length_bottom), 3)
        top_muscle = pymunk.DampedRotarySpring(target, self.top_leg_body, 0, 4, 3)
        bottom_muscle = pymunk.DampedRotarySpring(target, self.top_leg_body, 0, 4, 3)



class PlayerBox:
    def __init__(self, a, b, c, d, density, elasticity=0.20, friction=1, color=(255, 0, 255)):
        self.cube_body = pymunk.Body()
        self.cube_shape = pymunk.Poly(self.cube_body, [a, b, c, d])
        self.cube_shape.density = density
        self.cube_shape.elasticity = elasticity
        self.cube_shape.friction = friction
        self.color = color
        setup.space.add(self.cube_body, self.cube_shape)

        self.vx = 0
        self.vy = 0
        self.movement_friction = 0.6

    def draw(self):
        vertices = []
        for v in self.cube_shape.get_vertices():
            x, y = v.rotated(self.cube_shape.body.angle) + self.cube_shape.body.position
            vertices.append((int(x + setup.camx), int(y + setup.camy)))

        pygame.draw.polygon(setup.display, self.color, vertices)

    def move(self, speed):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if keys[pygame.K_RIGHT]:
                self.vx += speed
            if keys[pygame.K_LEFT]:
                self.vx += -speed
            if keys[pygame.K_UP]:
                self.vy += -speed * 2

        self.vx *= self.movement_friction
        self.vy *= self.movement_friction

        self.cube_body.velocity += (self.vx, self.vy)
