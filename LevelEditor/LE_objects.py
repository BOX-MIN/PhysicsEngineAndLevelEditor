import pygame
import pymunk
from pygame import *
import LE_setup
from math import sqrt
import matplotlib.path

render_list = []

zoom_power = LE_setup.zoom_power
aspect_ratio = LE_setup.aspect_ratio

def apply_zoom(zoom_input, zoom_level, ball_radius=None, invert=False):
    if ball_radius is None:
        if isinstance(zoom_input, tuple):
            x, y = zoom_input
            scroll_position = zoom_level
            scroll_position = (int(((scroll_position / 184 * 100) - 50))) / 100
            if not invert is True:
                x = x * ((1 + scroll_position) * zoom_power)
                y = y * ((1 + scroll_position) * zoom_power)
                return tuple((x, y))
            else:
                x = x / ((1 + scroll_position) * zoom_power)
                y = y / ((1 + scroll_position) * zoom_power)
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

    def check_mouse_touching(self, zoom_level):
        mx, my = pygame.mouse.get_pos()
        x, y = apply_zoom((self.x + LE_setup.xPos, self.y + LE_setup.yPos), zoom_level)
        distance = sqrt((mx - x) ** 2 + (my - y) ** 2)
        if distance < apply_zoom(None, zoom_level, ball_radius=self.radius):
            return True
        else:
            return False

    def get_save_info(self):
        save_info_list = ['Ball', self.x, self.y, self.radius]
        return save_info_list

class SaveBouncingCube:
    def __init__(self, a, b, c, d, density):
        self.temp_poly = pymunk.Poly(None, [a, b, c, d])
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.density = density
        render_list.append(self)

    def draw(self, zoom_level):
        try:
            a, b, c, d = self.temp_poly.get_vertices()
            a = a + (LE_setup.xPos, LE_setup.yPos)
            b = b + (LE_setup.xPos, LE_setup.yPos)
            c = c + (LE_setup.xPos, LE_setup.yPos)
            d = d + (LE_setup.xPos, LE_setup.yPos)
        except ValueError:
            a, b, c = self.temp_poly.get_vertices()
            a = a + (LE_setup.xPos, LE_setup.yPos)
            b = b + (LE_setup.xPos, LE_setup.yPos)
            c = c + (LE_setup.xPos, LE_setup.yPos)
            d = c
        pygame.draw.polygon(LE_setup.le_screen, (255, 0, 255), [
            apply_zoom(a, zoom_level),
            apply_zoom(b, zoom_level),
            apply_zoom(c, zoom_level),
            apply_zoom(d, zoom_level)
        ])

    def get_save_info(self):
        try:
            a, b, c, d = self.temp_poly.get_vertices()
        except ValueError:
            a, b, c = self.temp_poly.get_vertices()
            d = c
        save_info_list = ['BouncingCube', a, b, c, d, self.density]
        return save_info_list

    def check_mouse_touching(self, zoom_level):
        try:
            a, b, c, d = self.temp_poly.get_vertices()
            a = a + (LE_setup.xPos, LE_setup.yPos)
            b = b + (LE_setup.xPos, LE_setup.yPos)
            c = c + (LE_setup.xPos, LE_setup.yPos)
            d = d + (LE_setup.xPos, LE_setup.yPos)
        except ValueError:
            a, b, c = self.temp_poly.get_vertices()
            a = a + (LE_setup.xPos, LE_setup.yPos)
            b = b + (LE_setup.xPos, LE_setup.yPos)
            c = c + (LE_setup.xPos, LE_setup.yPos)
            d = c

        a = apply_zoom(a, zoom_level)
        b = apply_zoom(b, zoom_level)
        c = apply_zoom(c, zoom_level)
        d = apply_zoom(d, zoom_level)

        mx, my = pygame.mouse.get_pos()
        path = matplotlib.path.Path([a, b, c, d])
        if path.contains_point((mx, my)):
            return True
        else:
            return False

    def mouse_touching_corner(self, zoom_level):
        try:
            a, b, c, d = self.temp_poly.get_vertices()
            a = a + (LE_setup.xPos, LE_setup.yPos)
            b = b + (LE_setup.xPos, LE_setup.yPos)
            c = c + (LE_setup.xPos, LE_setup.yPos)
            d = d + (LE_setup.xPos, LE_setup.yPos)
        except ValueError:
            a, b, c = self.temp_poly.get_vertices()
            a = a + (LE_setup.xPos, LE_setup.yPos)
            b = b + (LE_setup.xPos, LE_setup.yPos)
            c = c + (LE_setup.xPos, LE_setup.yPos)
            d = c

        a = apply_zoom(a, zoom_level)
        b = apply_zoom(b, zoom_level)
        c = apply_zoom(c, zoom_level)
        d = apply_zoom(d, zoom_level)

        tuple_list = [a, b, c, d]
        mx, my = pygame.mouse.get_pos()
        radius_of_detection = 10
        counter = 0
        while counter < 4:
            x = tuple_list[counter][0]
            y = tuple_list[counter][1]
            distance = sqrt((mx - x) ** 2 + (my - y) ** 2)
            if distance < radius_of_detection:

                return tuple_list[counter]
            counter += 1
        return False


class SaveWall:
    def __init__(self, a, b, c, d, bounce=0.8):
        self.a = a
        self.b = b
        self.d = c
        self.c = d
        self.temp_poly = pymunk.Poly(None, [a, b, c, d])
        self.bounce = bounce
        render_list.append(self)

    def draw(self, zoom_level):
        try:
            a, b, c, d = self.temp_poly.get_vertices()
            a = a + (LE_setup.xPos, LE_setup.yPos)
            b = b + (LE_setup.xPos, LE_setup.yPos)
            c = c + (LE_setup.xPos, LE_setup.yPos)
            d = d + (LE_setup.xPos, LE_setup.yPos)
        except ValueError:
            a, b, c = self.temp_poly.get_vertices()
            a = a + (LE_setup.xPos, LE_setup.yPos)
            b = b + (LE_setup.xPos, LE_setup.yPos)
            c = c + (LE_setup.xPos, LE_setup.yPos)
            d = c
        pygame.draw.polygon(LE_setup.le_screen, (100, 0, 255), [
            apply_zoom(a, zoom_level),
            apply_zoom(b, zoom_level),
            apply_zoom(c, zoom_level),
            apply_zoom(d, zoom_level)
        ])

    def check_mouse_touching(self, zoom_level):
        try:
            a, b, c, d = self.temp_poly.get_vertices()
            a = a + (LE_setup.xPos, LE_setup.yPos)
            b = b + (LE_setup.xPos, LE_setup.yPos)
            c = c + (LE_setup.xPos, LE_setup.yPos)
            d = d + (LE_setup.xPos, LE_setup.yPos)
        except ValueError:
            a, b, c = self.temp_poly.get_vertices()
            a = a + (LE_setup.xPos, LE_setup.yPos)
            b = b + (LE_setup.xPos, LE_setup.yPos)
            c = c + (LE_setup.xPos, LE_setup.yPos)
            d = c

        a = apply_zoom(a, zoom_level)
        b = apply_zoom(b, zoom_level)
        c = apply_zoom(c, zoom_level)
        d = apply_zoom(d, zoom_level)

        mx, my = pygame.mouse.get_pos()
        path = matplotlib.path.Path([a, b, c, d])
        if path.contains_point((mx, my)):
            return True
        else:
            return False

    def mouse_touching_corner(self, zoom_level):
        try:
            a, b, c, d = self.temp_poly.get_vertices()
            a = a + (LE_setup.xPos, LE_setup.yPos)
            b = b + (LE_setup.xPos, LE_setup.yPos)
            c = c + (LE_setup.xPos, LE_setup.yPos)
            d = d + (LE_setup.xPos, LE_setup.yPos)
        except ValueError:
            a, b, c = self.temp_poly.get_vertices()
            a = a + (LE_setup.xPos, LE_setup.yPos)
            b = b + (LE_setup.xPos, LE_setup.yPos)
            c = c + (LE_setup.xPos, LE_setup.yPos)
            d = c

        a = apply_zoom(a, zoom_level)
        b = apply_zoom(b, zoom_level)
        c = apply_zoom(c, zoom_level)
        d = apply_zoom(d, zoom_level)

        tuple_list = [a, b, c, d]
        mx, my = pygame.mouse.get_pos()
        radius_of_detection = 30
        counter = 0
        while counter < 4:
            x = tuple_list[counter][0]
            y = tuple_list[counter][1]
            distance = sqrt((mx - x) ** 2 + (my - y) ** 2)
            if distance < radius_of_detection:
                print('hit')
                return tuple_list[counter]
            counter += 1
        return False

    def get_save_info(self):
        try:
            a, b, c, d = self.temp_poly.get_vertices()
        except ValueError:
            a, b, c = self.temp_poly.get_vertices()
            d = c
        save_info_list = ['Wall', a, b, c, d]
        return save_info_list


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

    def check_mouse_touching(self, zoom_level):
        pass

    def get_save_info(self):
        save_info_list = ['String', 'i\'m a string']
        return save_info_list