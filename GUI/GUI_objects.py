import pygame
import pygame_gui
from setup import manager

update_list = []

class HideOnCloseUIWindow(pygame_gui.elements.UIWindow):
    def on_close_window_button_pressed(self):
        self.hide()


class Container:
    def __init__(self, x, y, width, height, title='container', resizable=False, draggable=True):
        self.container = HideOnCloseUIWindow(
            rect=pygame.Rect((x, y), (width, height)),
            manager=None,
            window_display_title=title,
            element_id=str(self),
            resizable=resizable,
            draggable=draggable
        )

class HoriSlider:
    def __init__(self, X, Y, width, height, container=None, label=True, labeltext='Your text here!', startvalue=0,
                 sliderange=(0, 10), clickincrement=1):
        self.slider = pygame_gui.elements.ui_horizontal_slider.UIHorizontalSlider(
            relative_rect=pygame.Rect((X, Y + height), (width, height)),
            start_value=startvalue,
            value_range=sliderange,
            manager=None,
            container=container,
            click_increment=clickincrement
        )

        self.slider_readout = pygame_gui.elements.ui_label.UILabel(
            relative_rect=pygame.Rect((X + width, Y + height), (width / 5, height)),
            text=str(startvalue),
            manager=None,
            container=container
        )
        update_list.append(self)

        if label:
            self.slider_label = pygame_gui.elements.ui_label.UILabel(
                relative_rect=pygame.Rect((X, Y), (width, height)),
                text=labeltext,
                manager=None,
                container=container
            )

    def update_readout(self):
        self.slider_readout.set_text(str(self.slider.get_current_value()))


class button:
    def __init__(self, X, Y, width, height, text='Text', tool_tip_text=None, container=None, ):
        self.button = pygame_gui.elements.ui_button.UIButton(
            relative_rect=pygame.Rect((X, Y), (width, height)),
            text=text,
            manager=None,
            container=container,
            tool_tip_text=tool_tip_text
        )
