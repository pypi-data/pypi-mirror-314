import cv2

from skcvideo.colors import WHITE
from skcvideo.core import Button
from skcvideo.utils import put_text


class ButtonWidget:
    def __init__(self, box, text, callback, data=None, color=WHITE, pressed_color=None):
        self.box = box
        self.text = text
        self._callback = callback
        self._is_pressed = False
        self.default_color = color
        if pressed_color is None:
            self.pressed_color = color
        else:
            self.pressed_color = pressed_color
        self.buttons = [Button(box, callback, data=data)]

    @property
    def is_pressed(self):
        return self._is_pressed

    def build(self, im):
        x1, y1, x2, y2 = self.box
        xc, yc = (x1 + x2) // 2, (y1 + y2) // 2

        if self.is_pressed:
            color = self.pressed_color
            thickness = 2
        else:
            color = self.default_color
            thickness = 1

        im = cv2.rectangle(im, (x1, y1), (x2, y2), color, thickness)
        put_text(im, self.text, (xc, yc), color=color)
        return im

    def refresh(self, image, frame):
        pass

    def callback(self, *args, **kwargs):
        self._is_pressed = not self._is_pressed
        return self._callback(*args, **kwargs)
