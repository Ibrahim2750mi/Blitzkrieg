import string
from typing import Optional

import arcade
import arcade.gui
from arcade.gui import UIEvent, UIMouseDragEvent, UIMouseEvent, UIMousePressEvent, UIMouseScrollEvent, \
    UITextEvent, UITextMotionEvent, UITextMotionSelectEvent
from pyglet.event import EVENT_HANDLED, EVENT_UNHANDLED


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


class LabelList(list):
    def __init__(self):
        super(LabelList, self).__init__()

    def draw(self):
        for i in self:
            i.draw()
