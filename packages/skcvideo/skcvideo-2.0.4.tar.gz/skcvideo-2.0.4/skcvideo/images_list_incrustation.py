import os

import cv2
import numpy as np


class ImagesListIncrustation:
    def __init__(self, box=None, images_paths=None, shuffle=False, maximum_length=None):
        if box is None:
            box = [0, 575, 720, 575 + 1280]
        self.box = box
        self.images_paths = images_paths

        if shuffle:
            indices = np.random.permutation(len(self.images_paths))
            if maximum_length is not None:
                indices = indices[:maximum_length]
            self.images_paths = [self.images_paths[i] for i in indices]
        elif maximum_length is not None:
            self.images_paths = self.images_paths[:maximum_length]

        self.image_name_to_i = {}
        for i, image_path in enumerate(self.images_paths):
            image_name = os.path.splitext(os.path.basename(image_path))[0]
            self.image_name_to_i[image_name] = i

        self.images_list = []
        for image_path in self.images_paths:
            image = cv2.imread(image_path)
            self.images_list.append(image)

    @property
    def max_frame(self):
        return len(self.images_list) - 1

    def build(self, *args, **kwargs):
        pass

    def get_display_box(self, image):
        y1, x1, y2, x2 = self.box
        box_height, box_width = y2 - y1, x2 - x1
        im_height, im_width = image.shape[:2]

        ratio = min(box_height / im_height, box_width / im_width)
        new_im_height, new_im_width = int(im_height * ratio), int(im_width * ratio)
        y_offset, x_offset = y1 + int((box_height - new_im_height) / 2), x1 + int((box_width - new_im_width) / 2)
        return y_offset, x_offset, y_offset + new_im_height, x_offset + new_im_width

    def incrust_image(self, big_image, image, frame):
        im_height, im_width = image.shape[:2]
        y1, x1, y2, x2 = self.get_display_box(image)

        if im_height != (y2 - y1) or im_width != (x2 - x1):
            image = cv2.resize(image, (x2 - x1, y2 - y1))
        image = self.process_displayed_image(image, frame)
        big_image[y1:y2, x1:x2, :] = image

    def process_original_image(self, image, frame):
        return image

    def process_displayed_image(self, image, frame):
        return image

    def refresh(self, big_image, frame):
        image = self.images_list[frame].copy()
        image = self.process_original_image(image, frame)
        self.incrust_image(big_image, image, frame)

    def get_image_path(self, frame):
        return self.images_paths[frame]

    def get_frame(self, image_name):
        return self.image_name_to_i.get(image_name, None)

    def convert_to_original_coordinates(self, x, y, frame):
        image = self.images_list[frame]
        y1, x1, y2, x2 = self.get_display_box(image)
        h, w = image.shape[:2]
        x = int(np.round((x - x1) / (x2 - x1) * w))
        y = int(np.round((y - y1) / (y2 - y1) * h))
        x = min(max(x, 0), w - 1)
        y = min(max(y, 0), h - 1)
        return x, y

    def convert_to_display_coordinates(self, x, y, frame):
        image = self.images_list[frame]
        y1, x1, y2, x2 = self.get_display_box(image)
        h, w = image.shape[:2]
        x = int(np.round(x / w * (x2 - x1) + x1))
        y = int(np.round(y / h * (y2 - y1) + y1))
        return x, y
