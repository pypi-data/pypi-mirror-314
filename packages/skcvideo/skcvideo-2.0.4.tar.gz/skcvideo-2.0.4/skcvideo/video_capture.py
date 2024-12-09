import cv2

from skcvideo.controlled_fps_video_capture import ControlledFPSVideoCapture

DEFAULT_WIDTH = 1280
DEFAULT_HEIGHT = 720

SET_READ_TRADEOFF = 20
MAX_STORED = 100
AMONG_FRAMES = 20


class TransformedImageVideoCapture:
    """
    This VideoCapture overlay aims to add operations on the images before
    providing them.

    For instance, the operations are:
        - change channel order to switch from BGR to RGB
        - resize to desired shape

    Additionnaly, you can give an initial frame for the VideoCapture

    Args:
        - min_frame: the initial frame index of the video to start with
        - colormap: the order of the image channels (can be 'rgb' or 'bgr')
        - resize: tuple (width, height) or None: the shape of the outputted
          image. If None, no resize will be applied.
    """

    def __init__(self, *args, **kwargs):
        self.min_frame = kwargs.pop("min_frame", 0)
        self.colormap = kwargs.pop("colormap", "rgb")
        self.resize = kwargs.pop("resize", (DEFAULT_WIDTH, DEFAULT_HEIGHT))
        self.interlaced = kwargs.pop("interlaced", False)

        if self.min_frame < 0:
            self.min_frame = 0

        if self.colormap not in ["rgb", "bgr"]:
            raise NotImplementedError

        self.frame_reader = ControlledFPSVideoCapture(*args, **kwargs)

        resize_log = f"Resize to {self.resize[0]}x{self.resize[1]}" if self.resize is not None else "No resize"
        colormap_log = f"Colormap: {self.colormap}"
        print(f"{resize_log}, {colormap_log}")

        if self.min_frame > 0:
            self.frame_reader.set(cv2.CAP_PROP_POS_FRAMES, self.min_frame)

        # According to our use-case we prefer to have the first frame already read.
        self.read()

    def read(self):
        ret, self.image = self.frame_reader.read()

        if self.interlaced:
            h, w = self.image.shape[:2]
            self.image = cv2.resize(self.image[::2], (w, h))

        self.image_before_resize = self.image
        if self.resize is not None:
            # ffmpeg prefers to save video with 1088 pixels height, thus we
            # add 8 pixels to our 1080p videos. The following removes those
            # pixels before resizing them to 720p images.
            if self.image.shape[0] == 1088:
                self.image = self.image[8:]

            in_height, in_width = self.image.shape[:2]
            out_width, out_height = self.resize
            if in_height != out_height or in_width != out_width:
                in_aspect_ratio = float(in_height) / float(in_width)
                out_aspect_ratio = float(out_height) / float(out_width)
                if in_aspect_ratio != out_aspect_ratio:
                    size_in = f"{in_width}x{in_height}"
                    size_out = f"{out_width}x{out_height}"
                    print("Warning: resizing image with a different aspect ratio")
                    print(f"    {size_in} -> {size_out}")
                self.image = cv2.resize(self.image, self.resize)
        if self.colormap == "rgb":
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)

    def set(self, prop_id, value):
        return self.frame_reader.set(prop_id, value)

    def get(self, prop_id):
        return self.frame_reader.get(prop_id)

    def seek(self, frame):
        """
        This method aims to manage the tradoff between directly setting the
        VideoCapture to the desired frame and reading the successive frames
        up to the desired in order to get the frame in the fastest manner.

        /!\\ Default value was chosen empirically and may not be optimal
        depending on your architecture.
        """
        if not (self.frame_reader.output_frame <= frame < self.frame_reader.output_frame + SET_READ_TRADEOFF):
            self.set(cv2.CAP_PROP_POS_FRAMES, frame)
            self.read()

        while self.frame_reader.output_frame < frame:
            self.read()
        return self.image


class StoredImagesVideoCapture(TransformedImageVideoCapture):
    """
    This VideoCapture overlay stores previously read frames for faster access.

    When setting to a new instant in the video, it prepares the previous
    frames by actually setting several frames back in order to facilitate
    backward reading.

    The accessible frames are bounded as it was designed for the displayer and
    we may want a close up on a sequence (in particular for a better precision
    in the timeline).

    Args:
        - min_frame: the index of the first accessible frame
        - max_frame: the index of the last accessible frame
    """

    def __init__(self, *args, **kwargs):
        self.stored_images = {}
        super().__init__(*args, **kwargs)

    def get_max_frame(self):
        return super().get(cv2.CAP_PROP_FRAME_COUNT)

    def read(self):
        """
        Overrides read() method to store the output
        """
        super().read()
        if self.frame_reader.output_frame - MAX_STORED in self.stored_images:
            del self.stored_images[self.frame_reader.output_frame - MAX_STORED]
        self.stored_images[self.frame_reader.output_frame] = self.image

    def set(self, prop_id, value):
        """
        Overrides set() method to erase all the stored values
        """
        if prop_id == cv2.CAP_PROP_POS_FRAMES:
            self.stored_images = {}
            super().set(prop_id, max(0, value - AMONG_FRAMES))
        else:
            super().set(prop_id, value)

    def seek(self, frame):
        if frame not in self.stored_images:
            super().seek(frame)
        self.frame = frame
        return self.stored_images[frame]
