import os
import string
from typing import Optional

import arcade
import arcade.gui
from arcade.gui import UIEvent, UIMouseDragEvent, UIMouseEvent, UIMousePressEvent, UIMouseScrollEvent, \
    UITextEvent, UITextMotionEvent, UITextMotionSelectEvent
from pyglet.event import EVENT_HANDLED, EVENT_UNHANDLED

from config import PATH


class AdvancedUiCheckButton(arcade.gui.UIFlatButton):
    def __init__(self, name):
        super(AdvancedUiCheckButton, self).__init__(text="Select", width=250, style={"bg_color": (0, 200, 0),
                                                                                     "bg_color_pressed": arcade.color.SKY_BLUE})
        self.file_name = name
        self.clicked = False

    def on_click(self, _: arcade.gui.UIOnClickEvent):
        self.text = "SELECTED"
        self.clicked = True


class AdvancedUiManager(arcade.gui.UIManager):
    def __init__(self, *args):
        super(AdvancedUiManager, self).__init__(*args)

    def clear(self):
        for widget in self.walk_widgets():
            self.remove(widget)


class AdvanceUiInputText(arcade.gui.UIInputText):
    def __init__(self,
                 x: float = 0,
                 y: float = 0,
                 width: float = 100,
                 height: float = 50,
                 text: str = "",
                 font_name=('Arial',),
                 font_size: float = 12,
                 text_color: arcade.Color = (0, 0, 0, 255),
                 multiline=False,
                 size_hint=None,
                 size_hint_min=None,
                 size_hint_max=None,
                 style=None,
                 only_numeric_values=False,
                 **kwargs):
        super(AdvanceUiInputText, self).__init__(
            x=x, y=y, width=width, height=height, text=text, font_name=font_name, font_size=font_size,
            text_color=text_color, multiline=multiline, size_hint=size_hint, size_hint_min=size_hint_min,
            size_hint_max=size_hint_max, style=style, **kwargs
        )
        self.only_numeric_values = only_numeric_values

    def on_event(self, event: UIEvent) -> Optional[bool]:
        # if not active, check to activate, return
        if not self._active and isinstance(event, UIMousePressEvent):
            if self.rect.collide_with_point(event.x, event.y):
                self._active = True
                self.trigger_full_render()
                self.caret.on_activate()
                self.caret.position = len(self.doc.text)
                return EVENT_UNHANDLED

        # if active check to deactivate
        if self._active and isinstance(event, UIMousePressEvent):
            if self.rect.collide_with_point(event.x, event.y):
                x, y = event.x - self.x, event.y - self.y
                self.caret.on_mouse_press(x, y, event.button, event.modifiers)
            else:
                self._active = False
                self.trigger_full_render()
                self.caret.on_deactivate()
                return EVENT_UNHANDLED

        # if active pass all non press events to caret
        if self._active:
            # Act on events if active
            if isinstance(event, UITextEvent):
                # if the user want to only accept digits
                if self.only_numeric_values:
                    if event.text not in string.printable[10:]:
                        self.caret.on_text(event.text)
                        self.trigger_full_render()
                else:
                    self.caret.on_text(event.text)
                    self.trigger_full_render()

            elif isinstance(event, UITextMotionEvent):
                self.caret.on_text_motion(event.motion)
                self.trigger_full_render()
            elif isinstance(event, UITextMotionSelectEvent):
                self.caret.on_text_motion_select(event.selection)
                self.trigger_full_render()

            if isinstance(event, UIMouseEvent) and self.rect.collide_with_point(event.x, event.y):
                x, y = event.x - self.x, event.y - self.y
                if isinstance(event, UIMouseDragEvent):
                    self.caret.on_mouse_drag(x, y, event.dx, event.dy, event.buttons, event.modifiers)
                    self.trigger_full_render()
                elif isinstance(event, UIMouseScrollEvent):
                    self.caret.on_mouse_scroll(x, y, event.scroll_x, event.scroll_y)
                    self.trigger_full_render()

        if super(arcade.gui.UIInputText, self).on_event(event):
            return EVENT_HANDLED

        return EVENT_UNHANDLED

    @property
    def text(self):
        if self.only_numeric_values:
            return int(self.doc.text)
        else:
            return self.doc.text


class AdvancedUiFileDialogOpen(arcade.View):
    def __init__(self, main_window, main_view):
        super().__init__()

        self.save_file_icon_list = None
        self.save_file_names_list = None

        self.widget_manager = None

        self.v_box = None

        self.button_list = None

        self.main_window = main_window
        self.main_view = main_view

        arcade.set_background_color(arcade.color.SMOKY_BLACK)

    def setup(self) -> None:
        self.save_file_icon_list = arcade.SpriteList()
        self.save_file_names_list = LabelList()

        self.button_list = []

        self.widget_manager = AdvancedUiManager()
        self.widget_manager.enable()

        self.v_box = arcade.gui.UIBoxLayout(space_between=9)

        save_file_icon = arcade.load_texture(f"{PATH}/../assets/misc/save.png")
        last_y = 0
        save_file_names = [file for file in os.listdir(f"{PATH}/../data/") if 'Turn_' in file and '.' not in file]
        for i, name in enumerate(save_file_names):
            icon = arcade.Sprite(texture=save_file_icon, center_x=30, center_y=600 - (i * 60))
            name_text = arcade.Text(text=name, width=250, start_x=90, start_y=600 - (i * 60))
            button = AdvancedUiCheckButton(name)
            self.save_file_icon_list.append(icon)
            self.save_file_names_list.append(name_text)
            self.v_box.add(button)
            self.button_list.append(button)
            last_y = 600 - (i * 60)

        self.widget_manager.add(
            arcade.gui.UIAnchorWidget(
                anchor_x="right",
                anchor_y="bottom",
                align_x=-100,
                align_y=last_y - 25,
                child=self.v_box
            )
        )

    def on_update(self, delta_time: float):
        for button in self.button_list:
            if button.clicked:
                self.main_view.player.switched_view(button.file_name)
                self.main_window.show_view(self.main_view)

    def on_draw(self) -> None:
        self.clear()

        self.save_file_icon_list.draw()
        self.save_file_names_list.draw()
        self.widget_manager.draw()


class LabelList(list):
    def __init__(self):
        super(LabelList, self).__init__()

    def draw(self):
        for i in self:
            i.draw()
