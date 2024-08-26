import json
import ast

import pygame
from pygame import *
import pygame_gui
import sys
import os
import LE_save_load_system
from LevelEditorGUI import LevelEditorGUI_objects

import LE_setup

from LevelEditorGUI import LevelEditorGUI_manager

import LE_objects

clicked = False  # for mouse_events

def mouse_events(event):
    # here is where to check if clicking on an object
    if event.type == pygame.MOUSEBUTTONDOWN:
        mx, my = pygame.mouse.get_pos()
        # check to see if mouse is in menus, add more arguments as needed
        if my <= 25 or LevelEditorGUI_manager.le_ui_manager.get_hovering_any_element():
            pass

        elif True == False:
            pass
        else:
            """setup mouse offset code for level dragging"""
            zoom_level = LevelEditorGUI_manager.zoomer.vertical_scroll_bar.scroll_position
            zoom_level = (int(((zoom_level / 184 * 100) - 50))) / 100
            zoom_power = LE_setup.zoom_power
            global mox, moy
            mox = mx - (LE_setup.xPos * ((1 + zoom_level) * zoom_power))
            moy = my - (LE_setup.yPos * ((1 + zoom_level) * zoom_power))

            global clicked
            clicked = True
    if event.type == pygame.MOUSEMOTION and clicked == True:
        """level dragging code"""
        mx, my = pygame.mouse.get_pos()
        zoom_level = LevelEditorGUI_manager.zoomer.vertical_scroll_bar.scroll_position
        zoom_level = (int(((zoom_level / 184 * 100) - 50))) / 100
        zoom_power = LE_setup.zoom_power
        LE_setup.xPos = (mx - mox) / ((1 + zoom_level) * zoom_power)
        LE_setup.yPos = (my - moy) / ((1 + zoom_level) * zoom_power)
    if event.type == pygame.MOUSEBUTTONUP:
        clicked = False




def le_controls(event):
    mouse_events(event)

    if event.type == QUIT:
        pygame.quit()
        sys.exit()

    key = pygame.key.get_pressed()
    if key[K_ESCAPE] and key[K_LCTRL] or key[K_ESCAPE] and key[K_RCTRL]:
        pygame.quit()
        sys.exit()

    if event.type == pygame_gui.UI_BUTTON_PRESSED:
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
                LE_setup.xPos = 0
                LE_setup.yPos = 25
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
            LE_setup.xPos = 0
            LE_setup.yPos = 25

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
        time_delta = LE_setup.clock.tick(LE_setup.fps) / 1000.0
        # print(time_delta * 1000)

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

        for event in pygame.event.get():
            le_controls(event)

            LevelEditorGUI_manager.le_ui_manager.process_events(event)

        LevelEditorGUI_manager.le_ui_manager.update(time_delta)
        for i in LevelEditorGUI_objects.le_update_list:
            i.update_readout()

        LE_setup.le_screen.fill((255, 255, 255))
        LE_setup.le_display.fill((255, 255, 255))

        scroll_position = LevelEditorGUI_manager.zoomer.vertical_scroll_bar.scroll_position

        for i in LE_objects.render_list:
            i.draw(scroll_position)

        LE_setup.le_display.blit(LE_setup.le_screen)

        LE_setup.le_display.fill((189, 189, 189), ((0, 0), (LE_setup.le_display.width, 25)))
        LE_setup.le_display.fill((189, 189, 189), ((LE_setup.le_display.width - 25, 0), (25, LE_setup.le_display.height)))
        LE_setup.le_display.fill((90, 90, 90), ((LE_setup.le_display.width - 25, 50), (25, 275)))

        LevelEditorGUI_manager.le_ui_manager.draw_ui(LE_setup.le_display)

        pygame.display.flip()




LEMain()
