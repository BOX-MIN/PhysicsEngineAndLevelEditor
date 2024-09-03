import pymunk
from pymunk import constraints
import pygame
from pygame import *

import setup
from setup import space, display

render_list = []

class Ball:
    def __init__(self, x, y, radius, color=(255, 0, 0)):
        self.body = pymunk.Body()
        self.body.position = x, y
        self.shape = pymunk.Circle(self.body, radius)
        self.shape.density = 100
        self.shape.elasticity = 0.99
        self.color = color
        space.add(self.body, self.shape)
        render_list.append(self)

    def draw(self):
        x, y = self.body.position
        x = x + setup.camx
        y = y + setup.camy
        pygame.draw.circle(display, self.color, (int(x), int(y)), self.shape.radius)

class BouncingCube:
    def __init__(self, a, b, c, d, density):
        self.cube_body = pymunk.Body()
        self.cube_shape = pymunk.Poly(self.cube_body, [a, b, c, d])
        self.cube_shape.density = density
        self.cube_shape.elasticity = 0.20
        self.cube_shape.friction = 1
        space.add(self.cube_body, self.cube_shape)
        render_list.append(self)

    def draw(self):
        vertices = []
        for v in self.cube_shape.get_vertices():
            x, y = v.rotated(self.cube_shape.body.angle) + self.cube_shape.body.position
            vertices.append((int(x + setup.camx), int(y + setup.camy)))

        pygame.draw.polygon(display, (255, 0, 255), vertices)


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
