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

import json
import ast
from math import sqrt

import pygame
import pymunk
from pygame import *
import pygame_gui
import sys
import os
import LE_save_load_system
from LevelEditorGUI import LevelEditorGUI_objects

import LE_setup

from LevelEditorGUI import LevelEditorGUI_manager

import LE_objects

clicked = False         # for mouse_events
corner_clicked = False  # for mouse_events
rect_tuple_to_move = 'none'

def touching_object():
    filter_list = LevelEditorGUI_manager.selection_list.list.get_multi_selection()
    if 'Enable Shape Detection' in filter_list:
        for i in LE_objects.render_list:
            if i.check_mouse_touching(LevelEditorGUI_manager.zoomer.vertical_scroll_bar.scroll_position) is True:
                if i.type in filter_list:
                    return i
                else:
                    pass

        return None

    else:
        return None

def touching_corner_of_polygon():
    filter_list = LevelEditorGUI_manager.selection_list.list.get_multi_selection()
    if 'Enable Corner Detection' in filter_list:
        for i in LE_objects.render_list:
            if i.type in filter_list:
                try:
                    coords = i.mouse_touching_corner(LevelEditorGUI_manager.zoomer.vertical_scroll_bar.scroll_position)
                    if coords is not False:
                        return i, coords  # returns tuple
                except AttributeError:
                    pass

        return None

    else:
        return None


def mouse_events_selection_mode(event):
    if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[2] is True:
        object_touched = touching_object()
        object_touched.create_personal_gui()
    if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[1] is True:
        LE_setup.input_mode = 'collisions/object placement'
        for i in LE_objects.render_list:
            try:
                i.properties_window.container.kill()
            except AttributeError:
                pass

def mouse_events_collisions_mode(event):
    # here is where to check if clicking on an object
    if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0] is True:
        """setup mouse offset code for level dragging and object movement"""
        mx, my = pygame.mouse.get_pos()

        zoom_level = LevelEditorGUI_manager.zoomer.vertical_scroll_bar.scroll_position
        zoom_level = (int(((zoom_level / 184 * 100) - 50))) / 100
        zoom_power = LE_setup.zoom_power

        global mox, moy
        mox = mx - (LE_setup.xPos * ((1 + zoom_level) * zoom_power))
        moy = my - (LE_setup.yPos * ((1 + zoom_level) * zoom_power))

        corner_touched = touching_corner_of_polygon()
        if corner_touched == None:
            object_touched = touching_object()
        else:
            object_touched = None

        global clicked
        global corner_clicked
        # check to see if mouse is in menus, add more arguments as needed
        if my <= 25 or LevelEditorGUI_manager.le_ui_manager.get_hovering_any_element():
            pass
        elif not corner_touched is None:
            clicked = False
            corner_clicked = corner_touched

        elif not object_touched is None:
            clicked = object_touched
            corner_clicked = False
        else:
            clicked = 'panning'
    elif event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[2] is True:
        object_touched = touching_object()
        key = pygame.key.get_pressed()
        if key[K_v]:
            try:
                LE_save_load_system.save_level(LevelEditorGUI_manager.filename.text_entry_line.get_text())
                LE_save_load_system.save_object(
                    LevelEditorGUI_manager.filename.text_entry_line.get_text(),
                    LE_setup.clipboard[-1][0],
                    LE_setup.clipboard[-1][1:]
                )
                LE_objects.render_list = []
                LE_save_load_system.load_level(LevelEditorGUI_manager.filename.text_entry_line.get_text())
            except IndexError:
                pass
        if object_touched is not None:
            if key[K_DELETE] or key[K_d]:
                LE_objects.render_list.remove(object_touched)
            elif key[K_c]:
                LE_setup.clipboard.append(object_touched.get_save_info())
            elif key[K_x]:
                LE_setup.clipboard.append(object_touched.get_save_info())
                LE_objects.render_list.remove(object_touched)
            else:
                object_touched.create_personal_gui()
                LE_setup.input_mode = 'selection and editing'



    if event.type == pygame.MOUSEMOTION:
        """level dragging code"""
        if clicked == 'panning':
            mx, my = pygame.mouse.get_pos()
            
            zoom_level = LevelEditorGUI_manager.zoomer.vertical_scroll_bar.scroll_position
            zoom_level = (int(((zoom_level / 184 * 100) - 50))) / 100
            zoom_power = LE_setup.zoom_power
            LE_setup.xPos = (mx - mox) / ((1 + zoom_level) * zoom_power)
            LE_setup.yPos = (my - moy) / ((1 + zoom_level) * zoom_power)

        if not clicked == False and not clicked == 'panning':
            mx, my = pygame.mouse.get_pos()
            zoom_level = LevelEditorGUI_manager.zoomer.vertical_scroll_bar.scroll_position
            zoom_level = (int(((zoom_level / 184 * 100) - 50))) / 100
            zoom_power = LE_setup.zoom_power
            mx = mx / ((1 + zoom_level) * zoom_power) - LE_setup.xPos
            my = my / ((1 + zoom_level) * zoom_power) - LE_setup.yPos

            clicked.x = mx
            clicked.y = my
            try:
                try:
                    (x1, y1), (x2, y2), (x3, y3), (x4, y4) = clicked.temp_poly.get_vertices()
                except ValueError:
                    (x1, y1), (x2, y2), (x3, y3) = clicked.temp_poly.get_vertices()
                    if not (x3, y3) == (x1, y1) or (x2, y2):
                        x4, y4 = x3, y3
                    else:
                        x4, y4 = x1, y1

                x1 = mx
                x2 = clicked.b[0] - clicked.a[0] + mx
                x3 = clicked.c[0] - clicked.a[0] + mx
                x4 = clicked.d[0] - clicked.a[0] + mx

                y1 = my
                y2 = clicked.b[1] - clicked.a[1] + my
                y3 = clicked.c[1] - clicked.a[1] + my
                y4 = clicked.d[1] - clicked.a[1] + my

                split_distance = 7
                if (x1, y1) == (x2, y2):
                    x2 += split_distance
                    y2 += split_distance
                if (x3, y3) == (x2, y2):
                    x3 += split_distance
                    y3 += split_distance
                if (x3, y3) == (x4, y4):
                    x4 += split_distance
                    y4 += split_distance
                if (x1, y1) == (x4, y4):
                    x1 += split_distance
                    y1 += split_distance

                clicked.temp_poly = pymunk.Poly(None, [(x1, y1), (x2, y2), (x3, y3), (x4, y4)])

            except AttributeError:
                pass

        if clicked is False and corner_clicked is not False:
            mx, my = pygame.mouse.get_pos()
            zoom_level = LevelEditorGUI_manager.zoomer.vertical_scroll_bar.scroll_position
            zoom_level = (int(((zoom_level / 184 * 100) - 50))) / 100
            zoom_power = LE_setup.zoom_power
            mx = mx / ((1 + zoom_level) * zoom_power) - LE_setup.xPos
            my = my / ((1 + zoom_level) * zoom_power) - LE_setup.yPos


            try:
                (x1, y1), (x2, y2), (x3, y3), (x4, y4) = corner_clicked[0].temp_poly.get_vertices()
            except ValueError:
                (x1, y1), (x2, y2), (x3, y3) = corner_clicked[0].temp_poly.get_vertices()
                x4, y4 = x3, y3

            distance = sqrt((mx - x1) ** 2 + (my - y1) ** 2)
            range_limiter = 10
            if distance < range_limiter:
                tempx, tempy = x1, y1
                x1, y1 = mx, my
                corner_clicked[0].temp_poly = pymunk.Poly(None, [(x1, y1), (x2, y2), (x3, y3), (x4, y4)])
                try:
                    a, b, c, d = corner_clicked[0].temp_poly.get_vertices()
                except ValueError:
                    x1, y1 = tempx, tempy
                    corner_clicked[0].temp_poly = pymunk.Poly(None, [(x1, y1), (x2, y2), (x3, y3), (x4, y4)])

            distance = sqrt((mx - x2) ** 2 + (my - y2) ** 2)
            if distance < range_limiter:
                tempx, tempy = x2, y2
                x2, y2 = mx, my
                corner_clicked[0].temp_poly = pymunk.Poly(None, [(x1, y1), (x2, y2), (x3, y3), (x4, y4)])
                try:
                    a, b, c, d = corner_clicked[0].temp_poly.get_vertices()
                except ValueError:
                    x2, y2 = tempx, tempy
                    corner_clicked[0].temp_poly = pymunk.Poly(None, [(x1, y1), (x2, y2), (x3, y3), (x4, y4)])

            distance = sqrt((mx - x3) ** 2 + (my - y3) ** 2)
            if distance < range_limiter:
                tempx, tempy = x3, y3
                x3, y3 = mx, my
                corner_clicked[0].temp_poly = pymunk.Poly(None, [(x1, y1), (x2, y2), (x3, y3), (x4, y4)])
                try:
                    a, b, c, d = corner_clicked[0].temp_poly.get_vertices()
                except ValueError:
                    x3, y3 = tempx, tempy
                    corner_clicked[0].temp_poly = pymunk.Poly(None, [(x1, y1), (x2, y2), (x3, y3), (x4, y4)])

            distance = sqrt((mx - x4) ** 2 + (my - y4) ** 2)
            if distance < range_limiter:
                tempx, tempy = x1, y1
                x4, y4 = mx, my
                corner_clicked[0].temp_poly = pymunk.Poly(None, [(x1, y1), (x2, y2), (x3, y3), (x4, y4)])
                try:
                    a, b, c, d = corner_clicked[0].temp_poly.get_vertices()
                except ValueError:
                    x4, y4 = tempx, tempy
                    corner_clicked[0].temp_poly = pymunk.Poly(None, [(x1, y1), (x2, y2), (x3, y3), (x4, y4)])

    if event.type == pygame.MOUSEBUTTONUP:
        clicked = False
        corner_clicked = False


def le_controls(event):
    if LE_setup.input_mode == 'collisions/object placement':
        mouse_events_collisions_mode(event)
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            try:
                if LevelEditorGUI_manager.ball_object_button.button.check_pressed():
                    LE_save_load_system.save_level(LevelEditorGUI_manager.filename.text_entry_line.get_text())
                    LE_save_load_system.save_object(
                        LevelEditorGUI_manager.filename.text_entry_line.get_text(),
                        'Ball',
                        [300 - LE_setup.xPos, 300 - LE_setup.yPos, 30, (220, 0, 0), 120, 0.99]
                    )
                    LE_objects.render_list = []
                    LE_save_load_system.load_level(LevelEditorGUI_manager.filename.text_entry_line.get_text())

                if LevelEditorGUI_manager.wall_object_button.button.check_pressed():
                    LE_save_load_system.save_level(LevelEditorGUI_manager.filename.text_entry_line.get_text())
                    LE_save_load_system.save_object(
                        LevelEditorGUI_manager.filename.text_entry_line.get_text(),
                        'Wall',
                        [[300 - LE_setup.xPos, 300 - LE_setup.yPos],
                         [300 - LE_setup.xPos, 400 - LE_setup.yPos],
                         [400 - LE_setup.xPos, 400 - LE_setup.yPos],
                         [400 - LE_setup.xPos, 300 - LE_setup.yPos]]
                    )
                    LE_objects.render_list = []
                    LE_save_load_system.load_level(LevelEditorGUI_manager.filename.text_entry_line.get_text())

                if LevelEditorGUI_manager.bouncingcube_object_button.button.check_pressed():
                    LE_save_load_system.save_level(LevelEditorGUI_manager.filename.text_entry_line.get_text())
                    LE_save_load_system.save_object(
                        LevelEditorGUI_manager.filename.text_entry_line.get_text(),
                        'BouncingCube',
                        [[300 - LE_setup.xPos, 300 - LE_setup.yPos],
                         [300 - LE_setup.xPos, 350 - LE_setup.yPos],
                         [350 - LE_setup.xPos, 350 - LE_setup.yPos],
                         [350 - LE_setup.xPos, 300 - LE_setup.yPos], 10000]
                    )
                    LE_objects.render_list = []
                    LE_save_load_system.load_level(LevelEditorGUI_manager.filename.text_entry_line.get_text())

                if LevelEditorGUI_manager.prewaterobject_object_button.button.check_pressed():
                    LE_save_load_system.save_level(LevelEditorGUI_manager.filename.text_entry_line.get_text())
                    LE_save_load_system.save_object(
                        LevelEditorGUI_manager.filename.text_entry_line.get_text(),
                        'PreWaterObject',
                        [300 - LE_setup.xPos, 300 - LE_setup.yPos, 100, 100, 500, 0, 2, 100, (0, 255, 0), True]
                    )
                    LE_objects.render_list = []
                    LE_save_load_system.load_level(LevelEditorGUI_manager.filename.text_entry_line.get_text())

                if LevelEditorGUI_manager.string_object_button.button.check_pressed():
                    raise Exception('object hasn\'t yet been implemented in the save/load system')

            except AttributeError:
                pass

    elif LE_setup.input_mode == 'selection and editing':
        mouse_events_selection_mode(event)
        for i in LE_objects.render_list:
            try:
                i.update_values_from_personal_gui()
            except AttributeError as a:
                print(a)
                pass

    if event.type == QUIT:
        pygame.quit()
        sys.exit()

    key = pygame.key.get_pressed()
    if key[K_ESCAPE] and key[K_LCTRL] or key[K_ESCAPE] and key[K_RCTRL]:
        pygame.quit()
        sys.exit()
    if key[K_o]:
        print(LE_objects.render_list)

    if event.type == pygame_gui.UI_BUTTON_PRESSED:
        if LevelEditorGUI_manager.export_button.button.check_pressed():
            LE_save_load_system.save_level(LevelEditorGUI_manager.filename.text_entry_line.get_text())
        try:
            if LevelEditorGUI_manager.json_window_save_button.button.check_pressed():
                string = ast.literal_eval(LevelEditorGUI_manager.json_window.text_box.get_text())
                open(os.path.join('..', 'PymunkPhysicsAndLevels', 'LevelData',
                                  str(LevelEditorGUI_manager.json_window.window.window_display_title)), 'w').close()
                with open(os.path.join('..', 'PymunkPhysicsAndLevels', 'LevelData',
                                       str(LevelEditorGUI_manager.json_window.window.window_display_title)), 'r+') as file:
                    file.seek(0)
                    json.dump(string, file)
                print(str(LevelEditorGUI_manager.json_window.window.window_display_title))
                LE_objects.render_list = []
                LE_save_load_system.load_level(str(LevelEditorGUI_manager.json_window.window.window_display_title))
                LevelEditorGUI_manager.filename.text_entry_line.set_text(
                    str(LevelEditorGUI_manager.json_window.window.window_display_title))
        except AttributeError:
            pass

        if LevelEditorGUI_manager.json_display_button.button.check_pressed():
            LevelEditorGUI_manager.load_json_window()

        if LevelEditorGUI_manager.file_renamer_button.button.check_pressed():
            os.rename(
                os.path.join('..', 'PymunkPhysicsAndLevels', 'LevelData', LevelEditorGUI_manager.file_loader_list.menu.selected_option[0]),
                os.path.join('..', 'PymunkPhysicsAndLevels', 'LevelData', LevelEditorGUI_manager.filename.text_entry_line.get_text())
            )
            LevelEditorGUI_manager.kill_file_loader_dropdown()
            LevelEditorGUI_manager.load_file_loader_dropdown()

        if LevelEditorGUI_manager.file_loader_button.button.check_pressed():
            print(LevelEditorGUI_manager.file_loader_list.menu.selected_option[0])
            LE_objects.render_list = []
            LE_save_load_system.load_level(LevelEditorGUI_manager.file_loader_list.menu.selected_option[0])
            LevelEditorGUI_manager.filename.text_entry_line.set_text(str(LevelEditorGUI_manager.file_loader_list.menu.selected_option[0]))

        if LevelEditorGUI_manager.fullscreen_button.button.check_pressed():
            if not pygame.display.is_fullscreen():
                LE_setup.le_display = pygame.display.set_mode((0, 0))
                LE_setup.le_screen = pygame.Surface(pygame.display.get_window_size())
                LevelEditorGUI_manager.le_ui_manager.set_window_resolution(pygame.display.get_window_size())
                pygame.display.toggle_fullscreen()
                LevelEditorGUI_manager.killRightHandElements()
                LevelEditorGUI_manager.rightHandElements(pygame.display.get_window_size())
            else:
                pygame.display.toggle_fullscreen()
                LE_setup.le_display = pygame.display.set_mode(LE_setup.window_size)
                LE_setup.le_screen = pygame.Surface(pygame.display.get_window_size())
                LevelEditorGUI_manager.le_ui_manager.set_window_resolution(pygame.display.get_window_size())
                LevelEditorGUI_manager.killRightHandElements()
                LevelEditorGUI_manager.rightHandElements(pygame.display.get_window_size())


def LEMain():
    while True:
        """filling the screen before rendering"""
        LE_setup.le_screen.fill((255, 255, 255))
        LE_setup.le_display.fill((255, 255, 255))

        time_delta = LE_setup.clock.tick(LE_setup.fps) / 1000.0
        # print(time_delta * 1000)

        """arrow key panning"""
        key = pygame.key.get_pressed()
        if key[K_RIGHT]:
            LE_setup.xVel += -1 * LE_setup.speed
        if key[K_LEFT]:
            LE_setup.xVel += 1 * LE_setup.speed
        if key[K_UP]:
            LE_setup.yVel += 1 * LE_setup.speed
        if key[K_DOWN]:
            LE_setup.yVel += -1 * LE_setup.speed

        LE_setup.xVel = LE_setup.xVel * LE_setup.friction
        LE_setup.yVel = LE_setup.yVel * LE_setup.friction

        LE_setup.xPos = LE_setup.xPos + LE_setup.xVel
        LE_setup.yPos = LE_setup.yPos + LE_setup.yVel

        """all inputs in level editor"""
        for event in pygame.event.get():
            le_controls(event)

            LevelEditorGUI_manager.le_ui_manager.process_events(event)

        """for any GUI objects that might need to update every frame"""
        LevelEditorGUI_manager.le_ui_manager.update(time_delta)
        for i in LevelEditorGUI_objects.le_update_list:
            i.update_readout()

        """rendering objects to a Surface"""
        scroll_position = LevelEditorGUI_manager.zoomer.vertical_scroll_bar.scroll_position

        for i in LE_objects.render_list:
            i.draw(scroll_position)

        """rendering to the screen"""
        LE_setup.le_display.blit(LE_setup.le_screen)

        LE_setup.le_display.fill((189, 189, 189), ((0, 0), (LE_setup.le_display.width, 25)))
        if LE_setup.show_object_menu is True:
            LE_setup.le_display.fill((189, 189, 189), ((LE_setup.le_display.width - 25 - LE_setup.object_menu_width, 0), (25, LE_setup.le_display.height)))
            LE_setup.le_display.fill((90, 90, 90), ((LE_setup.le_display.width - 25 - LE_setup.object_menu_width, 50), (25, 275)))
        else:
            LE_setup.le_display.fill((189, 189, 189), ((LE_setup.le_display.width - 25, 0), (25, LE_setup.le_display.height)))
            LE_setup.le_display.fill((90, 90, 90), ((LE_setup.le_display.width - 25, 50), (25, 275)))

        LevelEditorGUI_manager.le_ui_manager.draw_ui(LE_setup.le_display)

        pygame.display.flip()


LEMain()
