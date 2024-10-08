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

import sys
from statistics import median

from pygame import *

import save_load_system
from PymunkPhysicsAndLevels import objects
import new_player_control as npc

import openGLrendering.openGLrendering as oGL

import setup
from setup import *

from GUI import GUI_objects, GUI_manager


def handle_events():
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
            GUI_manager.MainMenuWindow.container.show()

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
            if GUI_manager.MainMenuButton1.button.check_pressed():
                GUI_manager.SineWaveWindow.container.show()

            if GUI_manager.MainMenuButton2.button.check_pressed():
                GUI_manager.CRTWindow.container.show()

            if GUI_manager.MainMenuButton3.button.check_pressed():
                GUI_manager.LightingWindow.container.show()

            if GUI_manager.CRTButton1.button.check_pressed():
                GUI_manager.CRTSlider1.slider.set_current_value(0.5)
                GUI_manager.CRTSlider2.slider.set_current_value(0.5)
                GUI_manager.CRTSlider3.slider.set_current_value(2.5)

        manager.process_events(event)


def main():
    #waterone = objects.PreWaterObject(200, 0, 100, 100, 500, 0, 2, 100, (0, 255, 0), True)
    save_load_system.load_level('arena.json')
    #save_load_system.load_level('bestroom.json')
    # TODO: when implementing level editor, make sure that objects can reference other objects, so that things like
    #  strings will work
    # stringOne = objects.String(ballTwo.body, ballOne.body, 25)
    # stringTwo = objects.String(ballFour.body, ballOne.body, 40)
    # stringThree = objects.String(ballFour.body, (200, 0), 50, "anchored")

    Mx, My = pygame.mouse.get_pos()
    mouseCursorBall = objects.KinematicObject(Mx, My, 15)
    player = npc.PlayerBox(200, 200,(-20, -20), (20, -20), (20, 20), (-20, 20), 10000, color=(0, 0, 0))
    player2 = npc.PlayerBox(200, 200, (-20, -20), (20, -20), (20, 20), (-20, 20), 10000, color=(0, 0, 0))

    lxvel = 0
    lyvel = 0
    lxpos = 500
    lypos = 500

    while True:
        handle_events()

        mouseCursorBall.follow_cursor(200)
        player.move(2)
        player2.move(2, (30, 120))

        # temporary camera controls
        key = pygame.key.get_pressed()
        if key[K_SPACE]:
            if key[K_RIGHT] or key[K_d]:
                lxvel += camspeed
            elif key[K_LEFT] or key[K_a]:
                lxvel += -camspeed
            elif key[K_UP] or key[K_w]:
                lyvel += -camspeed
            elif key[K_DOWN] or key[K_s]:
                lyvel += camspeed
        elif key[K_RIGHT] or key[K_d]:
            setup.camx += -camspeed
        elif key[K_LEFT] or key[K_a]:
            setup.camx += camspeed
        elif key[K_UP] or key[K_w]:
            setup.camy += camspeed
        elif key[K_DOWN] or key[K_s]:
            setup.camy += -camspeed

        """pygame_GUI stuff"""
        for i in GUI_objects.update_list:
            i.update_readout()

        time_delta = clock.tick(fps)
        manager.update(time_delta / 1000.0)

        """adding Pymunk objects to Pygame surface"""
        display.fill((255, 255, 255))
        empty = Color(0, 0, 0, 0)
        gui_display.fill(empty)

        for i in objects.render_list:
            i.draw()
        player.draw()
        player2.draw()

        # fps counter background
        pygame.draw.rect(gui_display, (0, 0, 1), [(-35, 0), (255, 25)])

        manager.draw_ui(gui_display)

        """openGl rendering code. taking Pygame surface, converting, and passing through shaders"""
        setup.time += 1  # for shaders

        frame_tex1 = oGL.surf_to_texture(display)
        frame_tex1.use(0)
        oGL.program['tex1'] = 0
        frame_tex2 = oGL.surf_to_texture(gui_display)
        frame_tex2.use(1)
        oGL.program['tex2'] = 1
        oGL.program['time'] = setup.time
        oGL.program['amplitude'] = float(GUI_manager.SineWaveSlider1.slider.get_current_value() / 1000)
        oGL.program['rate'] = float(GUI_manager.SineWaveSlider2.slider.get_current_value() / 1000)
        oGL.program['center'] = (GUI_manager.CRTSlider1.slider.get_current_value(),
                                 GUI_manager.CRTSlider2.slider.get_current_value())
        oGL.program['warp'] = GUI_manager.CRTSlider3.slider.get_current_value()
        oGL.program['cam'] = (setup.camx, setup.camy)
        oGL.program['aspect_ratio'] = pygame.display.get_window_size()[0] / pygame.display.get_window_size()[1]
        oGL.program['screen_width'] = pygame.display.get_window_size()[0]
        oGL.program['screen_height'] = pygame.display.get_window_size()[1]
        oGL.program['light_intensity'] = float(GUI_manager.LightingSlider1.slider.get_current_value())
        oGL.program['light_color'] = (GUI_manager.Lightingrcolor.slider.get_current_value(),
                                      GUI_manager.Lightinggcolor.slider.get_current_value(),
                                      GUI_manager.Lightingbcolor.slider.get_current_value())
        lxvel = lxvel * 0.6
        lyvel = lyvel * 0.6
        lxpos = lxpos + lxvel
        lypos = lypos + lyvel
        oGL.program['lightoffset'] = (lxpos, lypos)
        oGL.program['shadow_fade'] = GUI_manager.Lightingshadowfade.slider.get_current_value()
        oGL.render_object.render(mode=oGL.moderngl.TRIANGLE_STRIP)

        """"""
        pygame.display.flip()

        frame_tex1.release()
        frame_tex2.release()

        space.step(1 / fps)

        """FPS limiter and counter"""
        setup.fps_list.append(round(clock.get_fps(), 2))

        if setup.fps_list_counter < 600:
            setup.fps_list_counter += 1
        else:
            setup.fps_list_counter = 0
            setup.fps_list = [120]

        GUI_manager.FPSReadout.readout.set_text(
            f'FPS: {round(clock.get_fps(), 2)}, Average 5s: {round(median(setup.fps_list), 2)}'
        )


main()
