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

from GUI import GUI_objects

"""FPS Counter"""
FPSReadout = GUI_objects.Readout(5, 5, 85, 25, 'FPS:')

"""Main menu"""
MainMenuWindow = GUI_objects.Container(400, 400, 195, 150, title='Dev tools')

MainMenuButton1 = GUI_objects.button(10, 10, -1, 25, text='Sine wave effect', container=MainMenuWindow.container)

MainMenuButton2 = GUI_objects.button(10, 45, -1, 25, text='CRT effect', container=MainMenuWindow.container)

MainMenuButton3 = GUI_objects.button(10, 80, -1, 25, text='Temp Lighting Controls', container=MainMenuWindow.container)

MainMenuWindow.container.hide()

"""Lighting control"""
LightingWindow = GUI_objects.Container(400, 400, 200, 250, title='Sine wave effect control')

LightingSlider1 = GUI_objects.HoriSlider(10, 0, 150, 25, container=LightingWindow.container, label=True,
                                         labeltext='Intensity', sliderange=(0.1, 20.0), clickincrement=0.1)

Lightingrcolor = GUI_objects.HoriSlider(10, 50, 150, 25, container=LightingWindow.container, label=True,
                                         labeltext='Red', sliderange=(0, 255), clickincrement=1)

Lightinggcolor = GUI_objects.HoriSlider(10, 100, 150, 25, container=LightingWindow.container, label=True,
                                         labeltext='Green', sliderange=(0, 255), clickincrement=1)

Lightingbcolor = GUI_objects.HoriSlider(10, 150, 150, 25, container=LightingWindow.container, label=True,
                                         labeltext='Blue', sliderange=(0, 255), clickincrement=1)

Lightingrcolor.slider.set_current_value(255)
Lightinggcolor.slider.set_current_value(60)
Lightingbcolor.slider.set_current_value(80)
LightingSlider1.slider.set_current_value(1.9)

LightingWindow.container.hide()


"""Sine wave effect control"""
SineWaveWindow = GUI_objects.Container(400, 400, 195, 150, title='Sine wave effect control')

SineWaveSlider1 = GUI_objects.HoriSlider(10, 0, 150, 25, container=SineWaveWindow.container, label=True,
                                         labeltext='Amplitude', sliderange=(0, 100), clickincrement=5)

SineWaveSlider2 = GUI_objects.HoriSlider(10, 50, 150, 25, container=SineWaveWindow.container, label=True,
                                         labeltext='Rate', sliderange=(0, 150), clickincrement=5)

SineWaveWindow.container.hide()

"""CRT effect control"""
CRTWindow = GUI_objects.Container(400, 400, 195, 250, title='CRT effect control')

CRTSlider1 = GUI_objects.HoriSlider(10, 0, 150, 25, container=CRTWindow.container, label=True,
                                    labeltext='Center X', sliderange=(0.0, 1.0), startvalue=0.5,
                                    clickincrement=0.1)

CRTSlider2 = GUI_objects.HoriSlider(10, 50, 150, 25, container=CRTWindow.container, label=True,
                                    labeltext='Center Y', sliderange=(0.0, 1.0), startvalue=0.5, clickincrement=0.1)

CRTSlider3 = GUI_objects.HoriSlider(10, 100, 150, 25, container=CRTWindow.container, label=True,
                                    labeltext='Warp', sliderange=(1.0, 10.0), startvalue=10, clickincrement=0.1)

CRTButton1 = GUI_objects.button(10, 175, 50, 25, text='Reset', container=CRTWindow.container)

CRTWindow.container.hide()
