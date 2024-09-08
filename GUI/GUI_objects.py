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

import pygame
import pygame_gui
from setup import manager

update_list = []


class HideOnCloseUIWindow(pygame_gui.elements.UIWindow):
    def on_close_window_button_pressed(self):
        self.hide()


class Container:
    def __init__(self, x, y, width, height, title='container', resizable=False, draggable=True, manager=None):
        self.container = HideOnCloseUIWindow(
            rect=pygame.Rect((x, y), (width, height)),
            manager=manager,
            window_display_title=title,
            element_id=str(self),
            resizable=resizable,
            draggable=draggable
        )
        print('hi')


class HoriSlider:
    def __init__(self, X, Y, width, height, container=None, label=True, labeltext='Your text here!', startvalue=0,
                 sliderange=(0, 10), clickincrement=1, created_from_LE=False, manager=None):
        self.slider = pygame_gui.elements.ui_horizontal_slider.UIHorizontalSlider(
            relative_rect=pygame.Rect((X, Y + height), (width, height)),
            start_value=startvalue,
            value_range=sliderange,
            manager=manager,
            container=container,
            click_increment=clickincrement
        )

        self.slider_readout = pygame_gui.elements.ui_label.UILabel(
            relative_rect=pygame.Rect((X + width, Y + height), (width / 5, height)),
            text=str(startvalue),
            manager=manager,
            container=container
        )

        update_list.append(self)

        if label:
            self.slider_label = pygame_gui.elements.ui_label.UILabel(
                relative_rect=pygame.Rect((X, Y), (width, height)),
                text=labeltext,
                manager=manager,
                container=container
            )

    def update_readout(self):
        self.slider_readout.set_text(str(self.slider.get_current_value()))


class button:
    def __init__(self, X, Y, width, height, text='Text', tool_tip_text=None, container=None, manager=None):
        self.button = pygame_gui.elements.ui_button.UIButton(
            relative_rect=pygame.Rect((X, Y), (width, height)),
            text=text,
            manager=manager,
            container=container,
            tool_tip_text=tool_tip_text
        )

class ColorPickerWindow:
    def __init__(self, x, y, width, height, manager=None, initial_color=pygame.Color(0, 0, 0, 0), title='Colour Selector'):
        self.picker_window = pygame_gui.windows.ui_colour_picker_dialog.UIColourPickerDialog(
            rect=pygame.Rect((x, y), (width, height)),
            manager=manager,
            initial_colour=initial_color,
            window_title=title,
        )
