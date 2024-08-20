import sys

from pygame import *

from PymunkPhysicsAndLevels import objects

import openGLrendering.openGLrendering as oGL

import os.path
import json

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

            if GUI_manager.CRTButton1.button.check_pressed():
                GUI_manager.CRTSlider1.slider.set_current_value(0.5)
                GUI_manager.CRTSlider2.slider.set_current_value(0.5)
                GUI_manager.CRTSlider3.slider.set_current_value(2.5)

        manager.process_events(event)

def save_to_json(room, key, list):
    with open(os.path.join('PymunkPhysicsAndLevels', 'LevelData', str(room) + '.json'), 'r+') as file:
        try:
            data = json.load(file)
            data.update({key: list})
            file.seek(0)
            json.dump(data, file)
        except json.decoder.JSONDecodeError:
            data = {key: list}
            json.dump(data, file)

def load_from_json(room):
    with open(os.path.join('PymunkPhysicsAndLevels', 'LevelData', str(room) + '.json'), 'r+') as file:
        level_dict = json.load(file)
        return level_dict

room = 'testRoom'
save_to_json(room, with open(os.path.join('PymunkPhysicsAndLevels', 'LevelData', str(room) + '.json'), 'r+') as file: len(str(file)), [str(Ball), 111, -123, 12])
print(load_from_json('testRoom'))

def main():


    Mx, My = pygame.mouse.get_pos()
    mouseCursorBall = objects.KinematicObject(Mx, My, 15)

    while True:
        handle_events()

        mouseCursorBall.move(200)

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
        oGL.render_object.render(mode=oGL.moderngl.TRIANGLE_STRIP)

        """"""
        pygame.display.flip()

        frame_tex1.release()
        frame_tex2.release()

        space.step(1/fps)


#main()
