import pygame
import pymunk
from pygame import *
import LE_setup
from math import sqrt
import matplotlib.path
import LevelEditorGUI.LevelEditorGUI_manager, LevelEditorGUI.LevelEditorGUI_objects

render_list = []

zoom_power = LE_setup.zoom_power
aspect_ratio = LE_setup.aspect_ratio

def apply_zoom(zoom_input, zoom_level, ball_radius=None, invert=False):
    if ball_radius is None:
        if isinstance(zoom_input, tuple):
            #print(zoom_input)
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
    def __init__(self, x, y, radius, color=(255, 0, 0), density=100, elasticity=0.99):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.density = density
        self.elasticity = elasticity
        self.type = 'Balls'
        render_list.append(self)

        self.properties_window = None
        self.radius_slider = None
        self.density_slider = None
        self.elasticity_slider = None
        self.color_picker = None
        self.color_picker_button = None

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
        save_info_list = ['Ball', self.x, self.y, self.radius, self.color, self.density, self.elasticity]
        return save_info_list

    def create_personal_gui(self):
        self.properties_window = LevelEditorGUI.LevelEditorGUI_objects.Container(
            0, 25, 215, 400,
            title=str(self),
            draggable=True,
            resizable=True,
            manager=LevelEditorGUI.LevelEditorGUI_manager.le_ui_manager,
            hideonclose=False
        )

        self.radius_slider = LevelEditorGUI.LevelEditorGUI_objects.HoriSlider(
            5, 5, 150, 25,
            container=self.properties_window.container,
            label=True,
            labeltext='Radius',
            startvalue=self.radius,
            sliderange=(1, 300),
            clickincrement=1,
            manager=LevelEditorGUI.LevelEditorGUI_manager.le_ui_manager
        )
        self.density_slider = LevelEditorGUI.LevelEditorGUI_objects.HoriSlider(
            5, 55, 150, 25,
            container=self.properties_window.container,
            label=True,
            labeltext='Density',
            startvalue=self.density,
            sliderange=(10, 10000),
            clickincrement=50,
            manager=LevelEditorGUI.LevelEditorGUI_manager.le_ui_manager
        )
        self.elasticity_slider = LevelEditorGUI.LevelEditorGUI_objects.HoriSlider(
            5, 105, 150, 25,
            container=self.properties_window.container,
            label=True,
            labeltext='Elasticity',
            startvalue=self.elasticity,
            sliderange=(0.01, 1.00),
            clickincrement=0.01,
            manager=LevelEditorGUI.LevelEditorGUI_manager.le_ui_manager
        )
        self.color_picker_button = LevelEditorGUI.LevelEditorGUI_objects.Button(
            5, 170, 150, 25,
            text='Change Colour',
            manager=LevelEditorGUI.LevelEditorGUI_manager.le_ui_manager,
            container=self.properties_window.container
        )

    def update_values_from_personal_gui(self):
        if self.radius_slider is not None:
            self.radius = self.radius_slider.slider.get_current_value()
            self.density = self.density_slider.slider.get_current_value()
            self.elasticity = self.elasticity_slider.slider.get_current_value()

    def change_color(self):
        self.color_picker = LevelEditorGUI.LevelEditorGUI_objects.ColorPickerWindow(
            5, 155, 200, 200,
            manager=LevelEditorGUI.LevelEditorGUI_manager.le_ui_manager,
            initial_color=Color(self.color[0], self.color[1], self.color[2], 255),
            title='Colour Selector'
        )


class SaveBouncingCube:
    def __init__(self, a, b, c, d, density, elasticity=0.20, friction=1, color=(255, 0, 255)):
        self.temp_poly = pymunk.Poly(None, [a, b, c, d])
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.density = density
        self.elasticity = elasticity
        self.friction = friction
        self.color = color
        self.type = 'Bouncing Cubes'
        render_list.append(self)

        self.properties_window = None
        self.density_slider = None
        self.elasticity_slider = None
        self.friction_slider = None
        self.color_picker = None
        self.color_picker_button = None

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
        pygame.draw.polygon(LE_setup.le_screen, self.color, [
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
        save_info_list = ['BouncingCube', a, b, c, d, self.density, self.elasticity, self.friction, self.color]
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

    def create_personal_gui(self):
        self.properties_window = LevelEditorGUI.LevelEditorGUI_objects.Container(
            0, 25, 215, 400,
            title=str(self),
            draggable=True,
            resizable=True,
            manager=LevelEditorGUI.LevelEditorGUI_manager.le_ui_manager,
            hideonclose=False
        )
        self.density_slider = LevelEditorGUI.LevelEditorGUI_objects.HoriSlider(
            5, 5, 150, 25,
            container=self.properties_window.container,
            label=True,
            labeltext='Density',
            startvalue=self.density,
            sliderange=(10, 10000),
            clickincrement=50,
            manager=LevelEditorGUI.LevelEditorGUI_manager.le_ui_manager
        )
        self.elasticity_slider = LevelEditorGUI.LevelEditorGUI_objects.HoriSlider(
            5, 55, 150, 25,
            container=self.properties_window.container,
            label=True,
            labeltext='Elasticity',
            startvalue=self.elasticity,
            sliderange=(0.01, 1.00),
            clickincrement=0.01,
            manager=LevelEditorGUI.LevelEditorGUI_manager.le_ui_manager
        )
        self.friction_slider = LevelEditorGUI.LevelEditorGUI_objects.HoriSlider(
            5, 105, 150, 25,
            container=self.properties_window.container,
            label=True,
            labeltext='Friction',
            startvalue=self.friction,
            sliderange=(0.1, 1.9),
            clickincrement=0.1,
            manager=LevelEditorGUI.LevelEditorGUI_manager.le_ui_manager
        )
        self.color_picker_button = LevelEditorGUI.LevelEditorGUI_objects.Button(
            5, 170, 150, 25,
            text='Change Colour',
            manager=LevelEditorGUI.LevelEditorGUI_manager.le_ui_manager,
            container=self.properties_window.container
        )

    def update_values_from_personal_gui(self):
        if self.density_slider is not None:
            self.density = self.density_slider.slider.get_current_value()
            self.elasticity = self.elasticity_slider.slider.get_current_value()
            self.friction = self.friction_slider.slider.get_current_value()

    def change_color(self):
        self.color_picker = LevelEditorGUI.LevelEditorGUI_objects.ColorPickerWindow(
            5, 155, 200, 200,
            manager=LevelEditorGUI.LevelEditorGUI_manager.le_ui_manager,
            initial_color=Color(self.color[0], self.color[1], self.color[2], 255),
            title='Colour Selector'
        )


class SaveWall:
    def __init__(self, a, b, c, d, bounce=0.8):
        self.a = a
        self.b = b
        self.d = c
        self.c = d
        self.temp_poly = pymunk.Poly(None, [a, b, c, d])
        self.bounce = bounce
        self.type = 'Walls'
        render_list.append(self)

        self.properties_window = None
        self.bounce_slider = None
        self.color_picker = None
        self.color_picker_button = None

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
        save_info_list = ['Wall', a, b, c, d, self.bounce]
        return save_info_list

    def create_personal_gui(self):
        self.properties_window = LevelEditorGUI.LevelEditorGUI_objects.Container(
            0, 25, 215, 400,
            title=str(self),
            draggable=True,
            resizable=True,
            manager=LevelEditorGUI.LevelEditorGUI_manager.le_ui_manager,
            hideonclose=False
        )
        self.bounce_slider = LevelEditorGUI.LevelEditorGUI_objects.HoriSlider(
            5, 5, 150, 25,
            container=self.properties_window.container,
            label=True,
            labeltext='Elasticity',
            startvalue=self.bounce,
            sliderange=(0.10, 1.00),
            clickincrement=0.01,
            manager=LevelEditorGUI.LevelEditorGUI_manager.le_ui_manager
        )
        self.color_picker_button = LevelEditorGUI.LevelEditorGUI_objects.Button(
            5, 70, 150, 25,
            text='Change Colour',
            manager=LevelEditorGUI.LevelEditorGUI_manager.le_ui_manager,
            container=self.properties_window.container
        )

    def update_values_from_personal_gui(self):
        if self.bounce_slider is not None:
            self.bounce = self.bounce_slider.slider.get_current_value()

    def change_color(self):
        self.color_picker = LevelEditorGUI.LevelEditorGUI_objects.ColorPickerWindow(
            5, 155, 200, 200,
            manager=LevelEditorGUI.LevelEditorGUI_manager.le_ui_manager,
            initial_color=Color(self.color[0], self.color[1], self.color[2], 255),
            title='Colour Selector'
        )

class SavePreWaterObject:
    def __init__(self, x, y, width, height, dpp, epp, dop, aopphpa, color=(0, 255, 0), custom_collision=True):
        self.width_slide = None
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.density_per_particle = dpp
        self.elasticity_per_particle = epp
        self.density_of_particles = dop
        self.amount_of_particles_per_hundred_pixels_area = aopphpa
        self.collision_type = custom_collision
        self.color = color
        self.type = 'Pre-Water Objects'
        render_list.append(self)

        self.color_picker = None
        self.color_picker_button = None
        self.amount_of_particles_per_hundred_pixels_area_slide = None
        self.density_of_particles_slide = None
        self.elasticity_per_particle_slide = None
        self.density_per_particle_slide = None
        self.properties_window = None

    def draw(self, zoom_level):
        a, b, c, d = (self.x, self.y), (self.x + self.width, self.y), (self.x + self.width, self.y + self.height), (self.x, self.y + self.height)
        a = (a[0] + LE_setup.xPos, a[1] + LE_setup.yPos)
        b = (b[0] + LE_setup.xPos, b[1] + LE_setup.yPos)
        c = (c[0] + LE_setup.xPos, c[1] + LE_setup.yPos)
        d = (d[0] + LE_setup.xPos, d[1] + LE_setup.yPos)
        pygame.draw.polygon(LE_setup.le_screen, self.color, [
            apply_zoom(a, zoom_level),
            apply_zoom(b, zoom_level),
            apply_zoom(c, zoom_level),
            apply_zoom(d, zoom_level)
        ], 5)

    def get_save_info(self):
        save_info_list = ['PreWaterObject', self.x, self.y, self.width, self.height, self.density_per_particle,
                          self.elasticity_per_particle, self.density_of_particles,
                          self.amount_of_particles_per_hundred_pixels_area, self.color, self.collision_type]
        return save_info_list

    def check_mouse_touching(self, zoom_level):

        a, b, c, d = [(self.x, self.y), (self.x + self.width, self.y), (self.x + self.width, self.y + self.height), (self.x, self.y + self.height)]
        a = (a[0] + LE_setup.xPos, a[1] + LE_setup.yPos)
        b = (b[0] + LE_setup.xPos, b[1] + LE_setup.yPos)
        c = (c[0] + LE_setup.xPos, c[1] + LE_setup.yPos)
        d = (d[0] + LE_setup.xPos, d[1] + LE_setup.yPos)

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

    def create_personal_gui(self):
        self.properties_window = LevelEditorGUI.LevelEditorGUI_objects.Container(
            0, 25, 215, 475,
            title=str(self),
            draggable=True,
            resizable=True,
            manager=LevelEditorGUI.LevelEditorGUI_manager.le_ui_manager,
            hideonclose=False
        )
        self.density_per_particle_slide = LevelEditorGUI.LevelEditorGUI_objects.HoriSlider(
            5, 5, 150, 25,
            container=self.properties_window.container,
            label=True,
            labeltext='Density of Particle',
            startvalue=self.density_per_particle,
            sliderange=(1, 1000),
            clickincrement=5,
            manager=LevelEditorGUI.LevelEditorGUI_manager.le_ui_manager
        )
        self.elasticity_per_particle_slide = LevelEditorGUI.LevelEditorGUI_objects.HoriSlider(
            5, 55, 150, 25,
            container=self.properties_window.container,
            label=True,
            labeltext='Elasticity of Particle',
            startvalue=self.elasticity_per_particle,
            sliderange=(0, 1.00),
            clickincrement=0.01,
            manager=LevelEditorGUI.LevelEditorGUI_manager.le_ui_manager
        )
        self.density_of_particles_slide = LevelEditorGUI.LevelEditorGUI_objects.HoriSlider(
            5, 105, 150, 25,
            container=self.properties_window.container,
            label=True,
            labeltext='Particle Density',
            startvalue=self.density_of_particles,
            sliderange=(1, 100),
            clickincrement=1,
            manager=LevelEditorGUI.LevelEditorGUI_manager.le_ui_manager
        )
        self.amount_of_particles_per_hundred_pixels_area_slide = LevelEditorGUI.LevelEditorGUI_objects.HoriSlider(
            5, 155, 150, 25,
            container=self.properties_window.container,
            label=True,
            labeltext='AOPPHPA',
            startvalue=self.amount_of_particles_per_hundred_pixels_area,
            sliderange=(1, 3000),
            clickincrement=1,
            manager=LevelEditorGUI.LevelEditorGUI_manager.le_ui_manager
        )
        self.width_slide = LevelEditorGUI.LevelEditorGUI_objects.HoriSlider(
            5, 205, 150, 25,
            container=self.properties_window.container,
            label=True,
            labeltext='Rect Width',
            startvalue=self.width,
            sliderange=(10, 1000),
            clickincrement=10,
            manager=LevelEditorGUI.LevelEditorGUI_manager.le_ui_manager
        )
        self.height_slide = LevelEditorGUI.LevelEditorGUI_objects.HoriSlider(
            5, 255, 150, 25,
            container=self.properties_window.container,
            label=True,
            labeltext='Rect Height',
            startvalue=self.height,
            sliderange=(10, 1000),
            clickincrement=10,
            manager=LevelEditorGUI.LevelEditorGUI_manager.le_ui_manager
        )
        if self.collision_type is False:
            startvalue = 1
        else:
            startvalue = 0
        self.collision_type_slide = LevelEditorGUI.LevelEditorGUI_objects.HoriSlider(
            5, 305, 150, 25,
            container=self.properties_window.container,
            label=True,
            labeltext='Default Collisions',
            startvalue=startvalue,
            sliderange=(0, 1),
            clickincrement=1,
            manager=LevelEditorGUI.LevelEditorGUI_manager.le_ui_manager
        )
        self.area_readout = LevelEditorGUI.LevelEditorGUI_objects.Readout(
            5, 355, 150, 25,
            labeltext='Area: no data',
            manager=LevelEditorGUI.LevelEditorGUI_manager.le_ui_manager,
            container=self.properties_window.container
        )

        self.particles_readout = LevelEditorGUI.LevelEditorGUI_objects.Readout(
            5, 380, 150, 25,
            labeltext='Particles: no data',
            manager=LevelEditorGUI.LevelEditorGUI_manager.le_ui_manager,
            container=self.properties_window.container
        )
        self.color_picker_button = LevelEditorGUI.LevelEditorGUI_objects.Button(
            5, 405, 150, 25,
            text='Change Colour',
            manager=LevelEditorGUI.LevelEditorGUI_manager.le_ui_manager,
            container=self.properties_window.container
        )

    def update_values_from_personal_gui(self):
        if self.density_per_particle_slide is not None:
            self.elasticity_per_particle = self.elasticity_per_particle_slide.slider.get_current_value()
            self.density_per_particle = self.density_per_particle_slide.slider.get_current_value()
            self.density_of_particles = self.density_of_particles_slide.slider.get_current_value()
            self.amount_of_particles_per_hundred_pixels_area = self.amount_of_particles_per_hundred_pixels_area_slide.slider.get_current_value()
            self.width = self.width_slide.slider.get_current_value()
            self.height = self.height_slide.slider.get_current_value()
            if self.collision_type_slide.slider.get_current_value() == 0:
                self.collision_type = True
            else:
                self.collision_type = False

            self.area_readout.readout.set_text('Area: ' + str(self.width * self.height) + 'px')
            self.particles_readout.readout.set_text('Particles: ' + str(int(((self.width * self.height) / 100) * (self.amount_of_particles_per_hundred_pixels_area / 100))))

    def change_color(self):
        self.color_picker = LevelEditorGUI.LevelEditorGUI_objects.ColorPickerWindow(
            5, 155, 200, 200,
            manager=LevelEditorGUI.LevelEditorGUI_manager.le_ui_manager,
            initial_color=Color(self.color[0], self.color[1], self.color[2], 255),
            title='Colour Selector'
        )


# todo saving the string class needs some work, also LE_setup.x/yPos needs tp be added
class SaveString:
    def __init__(self, body1, attachment, length, identifier="body"):
        self.body1 = body1
        self.attachment = attachment
        self.length = length
        self.identifier = identifier
        self.type = 'Strings'
        render_list.append(self)

    def draw(self, zoom_level):
        pygame.draw.line(LE_setup.le_screen, (0, 0, 255), self.body1.position, self.body2.position, 2)

    def check_mouse_touching(self, zoom_level):
        pass

    def get_save_info(self):
        save_info_list = ['String', 'i\'m a string']
        return save_info_list