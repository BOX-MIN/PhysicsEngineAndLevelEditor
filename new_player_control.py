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


class Dangler:
    def __init__(self, attachbody, position, a, b, c, d, connect_pos, dangle_connect_pos):
        self.danglebody = pymunk.Body()
        self.danglebody.position = position
        self.dangleshape = pymunk.Poly(self.danglebody, [a, b, c, d])
        self.dangleshape.density = 1000
        self.dangleshape.friction = 1
        self.dangleshape.filter = pymunk.ShapeFilter(group=2)

        self.pin = pymunk.constraints.PinJoint(attachbody, self.danglebody, connect_pos, dangle_connect_pos)
        self.pin.distance = 0
        # self.pin.collide_bodies = False
        setup.space.add(self.danglebody, self.dangleshape, self.pin)

    def draw(self):
        vertices = []
        for v in self.dangleshape.get_vertices():
            x, y = v.rotated(self.dangleshape.body.angle) + self.dangleshape.body.position
            vertices.append((int(x + setup.camx), int(y + setup.camy)))

        pygame.draw.polygon(setup.display, (200, 150, 5), vertices)

class PlayerBox:
    def __init__(self, center_x, center_y, a, b, c, d, density, elasticity=0.20, friction=1, color=(255, 0, 255)):
        self.cube_body = pymunk.Body()
        self.cube_body.position = (center_x, center_y)
        self.cube_shape = pymunk.Poly(self.cube_body, [a, b, c, d])
        self.cube_shape.density = density
        self.cube_shape.elasticity = elasticity
        self.cube_shape.friction = friction
        self.color = color
        setup.space.add(self.cube_body, self.cube_shape)

        self.limb1 = Dangler(self.cube_shape.body, (center_x, center_y), (-5, 0), (5, 0), (-5, 25), (5, 25), (10, 25), (0, 0))
        self.limb2 = Dangler(self.cube_shape.body, (center_x, center_y), (-5, 0), (5, 0), (-5, 25), (5, 25), (-10, 25),
                             (0, 0))

        self.vx = 0
        self.vy = 0
        self.movement_friction = 0.6

    def draw(self):
        vertices = []
        for v in self.cube_shape.get_vertices():
            x, y = v.rotated(self.cube_shape.body.angle) + self.cube_shape.body.position
            vertices.append((int(x + setup.camx), int(y + setup.camy)))

        pygame.draw.polygon(setup.display, self.color, vertices)

        self.limb1.draw()
        self.limb2.draw()

    def move(self, speed, offset=(0, 55)):
        x, y = self.cube_body.position
        x = x + setup.camx
        y = y + setup.camy
        x2, y2 = pygame.mouse.get_pos()
        ox, oy = offset  # mouse offset

        self.cube_body.velocity = (x2 + ox - x) * speed, (y2 + oy - y) * speed


