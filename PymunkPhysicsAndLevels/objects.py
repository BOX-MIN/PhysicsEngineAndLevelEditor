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

import math
import random

import pymunk
from pymunk import constraints
import pygame
from pygame import *

import setup
from setup import space, display

render_list = []

class Ball:
    def __init__(self, x, y, radius, color=(255, 0, 0), density=100, elasticity=0.99):
        self.body = pymunk.Body()
        self.body.position = x, y
        self.shape = pymunk.Circle(self.body, radius)
        self.shape.density = density
        self.shape.elasticity = elasticity
        self.color = color
        space.add(self.body, self.shape)
        render_list.append(self)

    def draw(self):
        x, y = self.body.position
        x = x + setup.camx
        y = y + setup.camy
        pygame.draw.circle(display, self.color, (int(x), int(y)), self.shape.radius)

class BouncingCube:
    def __init__(self, a, b, c, d, density, elasticity=0.20, friction=1, color=(255, 0, 255)):
        self.cube_body = pymunk.Body()
        self.cube_shape = pymunk.Poly(self.cube_body, [a, b, c, d])
        self.cube_shape.density = density
        self.cube_shape.elasticity = elasticity
        self.cube_shape.friction = friction
        self.color = color
        space.add(self.cube_body, self.cube_shape)
        render_list.append(self)

    def draw(self):
        vertices = []
        for v in self.cube_shape.get_vertices():
            x, y = v.rotated(self.cube_shape.body.angle) + self.cube_shape.body.position
            vertices.append((int(x + setup.camx), int(y + setup.camy)))

        pygame.draw.polygon(display, self.color, vertices)


class Wall:
    def __init__(self, a, b, c, d, bounce=0.8):
        self.rect_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        self.rect_shape = pymunk.Poly(self.rect_body, [a, b, c, d])
        self.rect_shape.elasticity = bounce
        self.rect_shape.friction = 1
        space.add(self.rect_body, self.rect_shape)
        render_list.append(self)

    def draw(self):
        vertices = []
        for v in self.rect_shape.get_vertices():
            x, y = v
            vertices.append((int(x + setup.camx), int(y + setup.camy)))

        pygame.draw.polygon(display, (100, 0, 255), vertices)

class String:
    def __init__(self, body1, attachment, length, identifier="body"):
        self.body1 = body1
        if identifier == "body":
            self.body2 = attachment
        elif identifier == "anchored":
            self.body2 = pymunk.Body(body_type=pymunk.Body.STATIC)
            self.body2.position = attachment
        joint = pymunk.SlideJoint(self.body1, self.body2, (0, 0), (0, 0), min=0, max=length)
        joint.distance = length
        space.add(joint)
        render_list.append(self)

    def draw(self):
        pygame.draw.line(display, (0, 0, 255), self.body1.position, self.body2.position, 2)

class KinematicObject:
    def __init__(self, x, y, radius):
        self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.body.position = x, y
        self.shape = pymunk.Circle(self.body, radius)
        self.shape.elasticity = 0
        space.add(self.body, self.shape)
        render_list.append(self)

    def draw(self):
        x, y = self.body.position
        x = x + setup.camx
        y = y + setup.camy
        pygame.draw.circle(display, (0, 255, 0), (int(x), int(y)), self.shape.radius)

    def move(self, speed=80):
        x, y = self.body.position
        x = x + setup.camx
        y = y + setup.camy
        x2, y2 = pygame.mouse.get_pos()
        key = pygame.key.get_pressed()
        if not key[K_SPACE]:
            self.body.velocity = (x2 - x) * speed, (y2 - y) * speed
        elif key[K_RIGHT]:
            self.body.velocity = speed, 0
        elif key[K_LEFT]:
            self.body.velocity = -speed, 0
        elif key[K_UP]:
            self.body.velocity = 0, -speed
        elif key[K_DOWN]:
            self.body.velocity = 0, speed
        else:
            self.body.velocity = 0, 0

class WaterParticle:
    def __init__(self, x, y, radius, density, elasticity, custom_collision, radius_overflow=4, color=(0, 255, 0)):
        self.body = pymunk.Body()
        self.body.position = x, y
        self.shape = pymunk.Circle(self.body, radius)
        self.shape.density = density
        self.shape.elasticity = elasticity
        self.particle_density = 0
        self.color = color
        self.radius_overflow = radius_overflow
        self.collision_type = custom_collision
        if custom_collision is True:
            self.shape.collision_type = 3
        space.add(self.body, self.shape)
        render_list.append(self)

    def draw(self):
        x, y = self.body.position
        x = x + setup.camx
        y = y + setup.camy
        if self.collision_type is True:
            radius_number = self.shape.radius + (self.radius_overflow - abs(self.body.velocity / 500))
        else:
            radius_number = self.shape.radius
        pygame.draw.circle(display, self.color, (int(x), int(y)), radius_number)

class PreWaterObject:
    def __init__(self, x, y, width, height, dpp, epp, dop, aopphpa, color=(0, 255,0), custom_collision=False):
        self.rect = [(x, y), (x + width, y), (x + width, y + height), (x, y + height)]
        self.rect_area = width * height
        self.rect_ratio = width/height
        self.density_per_particle = dpp
        self.elasticity_per_particle = epp
        self.density_of_particles = dop
        self.amount_of_particles_per_hundred_pixels_area = aopphpa
        self.amount_of_particles = (self.rect_area / 100) * (self.amount_of_particles_per_hundred_pixels_area / 100)
        for i in range(int(self.amount_of_particles)):
            WaterParticle(random.randint(int(x), int(x + width)), random.randint(int(y), int(y + height)),
                          self.density_of_particles,
                          self.density_per_particle,
                          self.elasticity_per_particle,
                          custom_collision,
                          color=color
                          )

























