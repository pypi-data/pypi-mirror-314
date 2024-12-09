import os
import unittest

from ffmphisdp.utils import create_video, decode_all_frames

from skcvideo.controlled_fps_video_capture import ControlledFPSVideoCapture
from skcvideo.video_capture import TransformedImageVideoCapture
from skcvideo.video_incrustation import VideoIncrustation


class TestTransformedImageVideoCapture(unittest.TestCase):
    def test_reader_selection(self):
        """This test validate that when setting the frame_selection_version we get the correct reader"""
        from ffmphisdp.pyav_reader import ControlledVideoReader as ControlledFPSVideoCapture_ffmphisdp

        from skcvideo.controlled_fps_video_capture import ControlledFPSVideoCapture_skcvideo

        filename = "test.mp4"
        create_video([(filename, 25, 50)], filename)
        all_frames = decode_all_frames(filename, framerate=10, use_gpu=False)
        frame_infos = list(all_frames.keys())
        frame_selection = list(all_frames.values())

        reader = TransformedImageVideoCapture(filename)
        self.assertIsInstance(reader.frame_reader, ControlledFPSVideoCapture_skcvideo)
        self.assertEqual(reader.frame_reader.frame_selection_version, ControlledFPSVideoCapture.FRAME_SELECTION_LEGACY)

        reader = TransformedImageVideoCapture(
            filename, frame_selection_version=ControlledFPSVideoCapture.FRAME_SELECTION_LEGACY
        )
        self.assertIsInstance(reader.frame_reader, ControlledFPSVideoCapture_skcvideo)
        self.assertEqual(reader.frame_reader.frame_selection_version, ControlledFPSVideoCapture.FRAME_SELECTION_LEGACY)

        reader = TransformedImageVideoCapture(
            filename,
            frame_infos=frame_infos,
            frame_selection=frame_selection,
            frame_selection_version=ControlledFPSVideoCapture.FRAME_SELECTION_FFMPHISDP,
        )
        self.assertIsInstance(reader.frame_reader, ControlledFPSVideoCapture_ffmphisdp)
        self.assertEqual(
            reader.frame_reader.frame_selection_version, ControlledFPSVideoCapture.FRAME_SELECTION_FFMPHISDP
        )

        VideoIncrustation(filename, box=[0, 575, 720, 575 + 1280])

        os.remove(filename)
