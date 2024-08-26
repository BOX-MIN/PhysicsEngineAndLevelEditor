import pygame
import pymunk
from pygame import *
import LE_setup

render_list = []

zoom_power = LE_setup.zoom_power
aspect_ratio = LE_setup.aspect_ratio

def apply_zoom(zoom_input, zoom_level, ball_radius=None):
    if ball_radius is None:
        if isinstance(zoom_input, tuple):
            x, y = zoom_input
            scroll_position = zoom_level
            scroll_position = (int(((scroll_position / 184 * 100) - 50))) / 100
            x = x * ((1 + scroll_position) * zoom_power)
            y = y * ((1 + scroll_position) * zoom_power)
            return tuple((x, y))

        if isinstance(zoom_input, (int, float)):
            raise error('ApplyZoomInputIsn\'tTuple')
    else:
        scroll_position = zoom_level
        scroll_position = (int(((scroll_position / 184 * 100) - 50))) / 100
        radius = ball_radius * ((1 + scroll_position) * zoom_power)
        return radius


class SaveBall:
    def __init__(self, x, y, radius, color=(255, 0, 0)):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        render_list.append(self)

    def draw(self, zoom_level):
        pygame.draw.circle(LE_setup.le_screen, self.color, apply_zoom((int(self.x + LE_setup.xPos), int(self.y + LE_setup.yPos)), zoom_level), apply_zoom(None, zoom_level, ball_radius=self.radius))
        # print(apply_zoom((int(self.x + LE_setup.xPos), int(self.y + LE_setup.yPos))))
class SaveBouncingCube:
    def __init__(self, a, b, c, d, density):
        self.temp_poly = pymunk.Poly(None, [a, b, c, d])
        self.a = None
        self.b = None
        self.c = None
        self.d = None
        self.density = density
        render_list.append(self)

    def draw(self, zoom_level):
        try:
            self.a, self.b, self.c, self.d = self.temp_poly.get_vertices()
            self.a = self.a + (LE_setup.xPos, LE_setup.yPos)
            self.b = self.b + (LE_setup.xPos, LE_setup.yPos)
            self.c = self.c + (LE_setup.xPos, LE_setup.yPos)
            self.d = self.d + (LE_setup.xPos, LE_setup.yPos)
        except ValueError:
            self.a, self.b, self.c = self.temp_poly.get_vertices()
            self.a = self.a + (LE_setup.xPos, LE_setup.yPos)
            self.b = self.b + (LE_setup.xPos, LE_setup.yPos)
            self.c = self.c + (LE_setup.xPos, LE_setup.yPos)
            self.d = self.c
        pygame.draw.polygon(LE_setup.le_screen, (255, 0, 255), [
            apply_zoom(self.a, zoom_level),
            apply_zoom(self.b, zoom_level),
            apply_zoom(self.c, zoom_level),
            apply_zoom(self.d, zoom_level)
        ])


class SaveWall:
    def __init__(self, a, b, c, d, bounce=0.8):
        self.a = None
        self.b = None
        self.d = None
        self.c = None
        self.temp_poly = pymunk.Poly(None, [a, b, c, d])
        self.bounce = bounce
        render_list.append(self)

    def draw(self, zoom_level):
        try:
            self.a, self.b, self.c, self.d = self.temp_poly.get_vertices()
            self.a = self.a + (LE_setup.xPos, LE_setup.yPos)
            self.b = self.b + (LE_setup.xPos, LE_setup.yPos)
            self.c = self.c + (LE_setup.xPos, LE_setup.yPos)
            self.d = self.d + (LE_setup.xPos, LE_setup.yPos)
        except ValueError:
            self.a, self.b, self.c = self.temp_poly.get_vertices()
            self.a = self.a + (LE_setup.xPos, LE_setup.yPos)
            self.b = self.b + (LE_setup.xPos, LE_setup.yPos)
            self.c = self.c + (LE_setup.xPos, LE_setup.yPos)
            self.d = self.c
        pygame.draw.polygon(LE_setup.le_screen, (100, 0, 255), [
            apply_zoom(self.a, zoom_level),
            apply_zoom(self.b, zoom_level),
            apply_zoom(self.c, zoom_level),
            apply_zoom(self.d, zoom_level)
        ])

# todo saving the string class needs some work, also LE_setup.x/yPos needs tp be added
class SaveString:
    def __init__(self, body1, attachment, length, identifier="body"):
        self.body1 = body1
        self.attachment = attachment
        self.length = length
        self.identifier = identifier
        render_list.append(self)

    def draw(self, zoom_level):
        pygame.draw.line(LE_setup.le_screen, (0, 0, 255), self.body1.position, self.body2.position, 2)

