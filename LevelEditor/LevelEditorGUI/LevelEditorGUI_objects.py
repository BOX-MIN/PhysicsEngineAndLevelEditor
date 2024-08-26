import pygame
import pygame_gui

le_update_list = []


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


class HoriSlider:
    def __init__(self, X, Y, width, height, container=None, label=True, labeltext='Your text here!', startvalue=0,
                 sliderange=(0, 10), clickincrement=1, manager=None):
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

        le_update_list.append(self)

        if label:
            self.slider_label = pygame_gui.elements.ui_label.UILabel(
                relative_rect=pygame.Rect((X, Y), (width, height)),
                text=labeltext,
                manager=manager,
                container=container
            )

    def update_readout(self):
        self.slider_readout.set_text(str(self.slider.get_current_value()))


class Button:
    def __init__(self, X, Y, width, height, text='Text', tool_tip_text=None, container=None, manager=None):
        self.button = pygame_gui.elements.ui_button.UIButton(
            relative_rect=pygame.Rect((X, Y), (width, height)),
            text=text,
            manager=manager,
            container=container,
            tool_tip_text=tool_tip_text
        )

class DropDownMenu:
    def __init__(self, options_list, starting_option, x, y, width, height, manager=None, container=None):
        self.menu = pygame_gui.elements.ui_drop_down_menu.UIDropDownMenu(
            options_list=options_list,
            starting_option=starting_option,
            relative_rect=pygame.Rect((x, y), (width, height)),
            manager=manager,
            container=container
        )

class TextEntryLine:
    def __init__(self, x, y, width, height, manager=None, container=None, initial_text=None, placeholder_text=None):
        self.text_entry_line = pygame_gui.elements.ui_text_entry_line.UITextEntryLine(
            relative_rect=pygame.Rect((x, y), (width, height)),
            manager=manager,
            container=container,
            initial_text=initial_text,
            placeholder_text=placeholder_text
        )

class VerticalScrollBar:
    def __init__(self, x, y, width, height, start_percentage, visible_percentage, labeltext, manager=None, container=None):
        self.scroll_top_label = pygame_gui.elements.ui_label.UILabel(
            relative_rect=pygame.Rect((x, y), (width, 25)),
            text=labeltext,
            manager=manager,
            container=container
        )

        self.vertical_scroll_bar = pygame_gui.elements.ui_vertical_scroll_bar.UIVerticalScrollBar(
            relative_rect=pygame.Rect((x, y + 25), (width, height)),
            visible_percentage=visible_percentage,
            manager=manager,
            container=container
        )
        self.vertical_scroll_bar.set_scroll_from_start_percentage(start_percentage)

class TextEntryBoxWithWindow:
    def __init__(self, x, y, width, height, title, text, resizable=False, draggable=True, manager=None, container=None):
        self.window = pygame_gui.elements.ui_window.UIWindow(
            rect=pygame.Rect((x, y), (width, height)),
            manager=manager,
            window_display_title=str(title),
            resizable=resizable,
            draggable=draggable,
        )

        self.text_box = pygame_gui.elements.ui_text_entry_box.UITextEntryBox(
            relative_rect=pygame.Rect((0, 0), (width, height - 60)),
            initial_text=text,
            manager=manager,
            container=self.window
        )