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

def le_controls(event):
    if event.type == QUIT:
        pygame.quit()
        sys.exit()

    key = pygame.key.get_pressed()
    if key[K_ESCAPE] and key[K_LCTRL] or key[K_ESCAPE] and key[K_RCTRL]:
        pygame.quit()
        sys.exit()

    if event.type == pygame_gui.UI_BUTTON_PRESSED:
        if LevelEditorGUI_manager.file_loader_button.button.check_pressed():
            print(LevelEditorGUI_manager.file_loader_list.menu.selected_option[0])
            LE_objects.render_list = []
            LE_save_load_system.load_level(LevelEditorGUI_manager.file_loader_list.menu.selected_option[0])

        if LevelEditorGUI_manager.fullscreen_button.button.check_pressed():
            pygame.display.toggle_fullscreen()

def LEMain():
    while True:
        time_delta = LE_setup.clock.tick(LE_setup.fps) / 1000.0

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

        for i in LE_objects.render_list:
            i.draw()

        LE_setup.le_display.blit(LE_setup.le_screen)

        LE_setup.le_display.fill((189, 189, 189), ((0, 0), (LE_setup.le_screen.width, 25)))
        LE_setup.le_display.fill((189, 189, 189), ((LE_setup.le_screen.width - 25, 0), (25, LE_setup.le_screen.height)))
        LE_setup.le_display.fill((90, 90, 90), ((LE_setup.le_screen.width - 25, 50), (25, 275)))

        LevelEditorGUI_manager.le_ui_manager.draw_ui(LE_setup.le_display)

        pygame.display.flip()


LEMain()
