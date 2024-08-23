import sys

from LevelEditor.LevelEditorGUI import LevelEditorGUI_objects
import pygame_gui
import pygame
import os

le_ui_manager = pygame_gui.UIManager(pygame.display.get_window_size())

'''editing mode switcher'''
editing_mode_dropdown = LevelEditorGUI_objects.DropDownMenu(
    ['Collisions/Object placement', 'Selection and Editing', 'Graphics and Effects'],
    'Collisions/Object placement',
    0, 0, 225, 25,
    manager=le_ui_manager
)

'''filename and file loading'''
filename = LevelEditorGUI_objects.TextEntryLine(
    225, 0, 150, 25,
    manager=le_ui_manager,
    initial_text=os.listdir(os.path.join('..', 'PymunkPhysicsAndLevels', 'LevelData'))[0],
    placeholder_text='Input Name of Level'
)
file_renamer_button = LevelEditorGUI_objects.Button(
    375, 0, 75, 25,
    text='Rename',
    manager=le_ui_manager
)
file_loader_list = LevelEditorGUI_objects.DropDownMenu(
    os.listdir(os.path.join('..', 'PymunkPhysicsAndLevels', 'LevelData')),
    os.listdir(os.path.join('..', 'PymunkPhysicsAndLevels', 'LevelData'))[0],
    450, 0, 175, 25,
    manager=le_ui_manager
)
file_loader_button = LevelEditorGUI_objects.Button(
    625, 0, 100, 25,
    text='Load from File',
    manager=le_ui_manager
)


'''exporting settings'''
x, y = pygame.display.get_window_size()
export_settings_dropdown = LevelEditorGUI_objects.DropDownMenu(
    ['JSON', 'Graphics', 'JSON and Graphics'],
    'JSON and Graphics',
    x - 250, 0, 175, 25,
    manager=le_ui_manager
)
export_button = LevelEditorGUI_objects.Button(
    x - 75, 0, 75, 25,
    text='Export',
    manager=le_ui_manager
)

'''screen settings'''
x, y = pygame.display.get_window_size()
fullscreen_button = LevelEditorGUI_objects.Button(
    x - 25, 25, 25, 25,
    text='FS',
    manager=le_ui_manager
)

zoomer = LevelEditorGUI_objects.VerticalScrollBar(
    x - 25, 50, 25, 250,
    labeltext='+/-',
    visible_percentage=0.2,
    manager=le_ui_manager
)
