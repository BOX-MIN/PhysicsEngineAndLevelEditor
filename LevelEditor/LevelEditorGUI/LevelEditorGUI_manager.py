import json
import sys
import LevelEditor.LE_setup
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
def load_file_loader_dropdown():
    file_to_set = filename.text_entry_line.get_text()
    global file_loader_list
    file_loader_list = LevelEditorGUI_objects.DropDownMenu(
        os.listdir(os.path.join('..', 'PymunkPhysicsAndLevels', 'LevelData')),
        file_to_set,
        450, 0, 175, 25,
        manager=le_ui_manager
    )


def kill_file_loader_dropdown():
    file_loader_list.menu.kill()


load_file_loader_dropdown()

file_loader_button = LevelEditorGUI_objects.Button(
    625, 0, 100, 25,
    text='Load from File',
    manager=le_ui_manager
)

def load_json_window():
    file_to_load = file_loader_list.menu.selected_option[0]
    with open(os.path.join('..', 'PymunkPhysicsAndLevels', 'LevelData', str(file_to_load)), 'r+') as file:
        text_to_display = str(json.load(file))

    window_height = 600
    global json_window
    json_window = LevelEditorGUI_objects.TextEntryBoxWithWindow(
        LevelEditor.LE_setup.le_display.width - 425, 25, 400, window_height,
        title=str(file_to_load),
        manager=le_ui_manager,
        text=str(text_to_display),
    )
    global json_window_save_button
    json_window_save_button = LevelEditorGUI_objects.Button(
        5, window_height - 58, 210, 25,
        text='Save changes to file and load',
        container=json_window.window,
        manager=le_ui_manager
    )

'''right hand side elements'''
def rightHandElements(window_size):
    """exporting settings"""
    x, y = window_size
    global export_settings_dropdown
    export_settings_dropdown = LevelEditorGUI_objects.DropDownMenu(
        ['JSON', 'Graphics', 'JSON and Graphics'],
        'JSON and Graphics',
        x - 250, 0, 175, 25,
        manager=le_ui_manager
    )

    global export_button
    export_button = LevelEditorGUI_objects.Button(
        x - 75, 0, 75, 25,
        text='Export',
        manager=le_ui_manager
    )

    '''screen settings'''
    global fullscreen_button
    fullscreen_button = LevelEditorGUI_objects.Button(
        x - 25, 25, 25, 25,
        text='FS',
        manager=le_ui_manager
    )
    global zoomer
    zoomer = LevelEditorGUI_objects.VerticalScrollBar(
        x - 25, 50, 25, 250,
        labeltext='+/-',
        visible_percentage=0.1,
        manager=le_ui_manager,
        start_percentage=0.45
    )
    global json_display_button
    json_display_button = LevelEditorGUI_objects.Button(
        x - 325, 0, 75, 25,
        text='View JSON',
        manager=le_ui_manager
    )


rightHandElements(pygame.display.get_window_size())


def killRightHandElements():
    zoomer.vertical_scroll_bar.kill()
    zoomer.scroll_top_label.kill()
    fullscreen_button.button.kill()
    export_button.button.kill()
    export_settings_dropdown.menu.kill()
    json_display_button.button.kill()

