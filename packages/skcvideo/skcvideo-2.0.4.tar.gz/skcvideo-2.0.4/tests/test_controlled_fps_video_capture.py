import os
import unittest
from unittest.mock import patch

import cv2
from ffmphisdp.utils import create_video, decode_all_frames, expected_frame_color, is_almost_same_color

from skcvideo.controlled_fps_video_capture import ControlledFPSVideoCapture


class FakeCapture:
    def __init__(self, *args, **kwargs):
        self.input_fps = kwargs.get("input_fps")

    def get(self, prop):
        return self.input_fps

    def read(self):
        return True, None


class TestControlledFPSVideoCapture(unittest.TestCase):
    def test_reader_selection(self):
        """This test validate that when setting the frame_selection_version we get the correct reader"""
        from ffmphisdp.pyav_reader import ControlledVideoReader as ControlledFPSVideoCapture_ffmphisdp

        from skcvideo.controlled_fps_video_capture import ControlledFPSVideoCapture_skcvideo

        reader = ControlledFPSVideoCapture()
        self.assertIsInstance(reader, ControlledFPSVideoCapture_skcvideo)
        self.assertEqual(reader.frame_selection_version, ControlledFPSVideoCapture.FRAME_SELECTION_LEGACY)

        reader = ControlledFPSVideoCapture(frame_selection_version=ControlledFPSVideoCapture.FRAME_SELECTION_LEGACY)
        self.assertIsInstance(reader, ControlledFPSVideoCapture_skcvideo)
        self.assertEqual(reader.frame_selection_version, ControlledFPSVideoCapture.FRAME_SELECTION_LEGACY)

        filename = "test.mp4"
        create_video([(filename, 25, 50)], filename)
        all_frames = decode_all_frames(filename, framerate=10, use_gpu=False)
        frame_infos = list(all_frames.keys())
        frame_selection = list(all_frames.values())

        reader = ControlledFPSVideoCapture(
            filename,
            frame_infos=frame_infos,
            frame_selection=frame_selection,
            frame_selection_version=ControlledFPSVideoCapture.FRAME_SELECTION_FFMPHISDP,
        )
        self.assertIsInstance(reader, ControlledFPSVideoCapture_ffmphisdp)
        self.assertEqual(reader.frame_selection_version, ControlledFPSVideoCapture.FRAME_SELECTION_FFMPHISDP)
        os.remove(filename)

    @patch("cv2.VideoCapture", side_effect=FakeCapture)
    def test_controlled_fps_video_capture(self, *args):
        expected_results = {
            10: [0, 1, 2, 3, 4],
            25: [0, 1, 2, 4, 7],
            30: [0, 1, 2, 5, 8],
            50: [0, 1, 4, 9, 14],
            60: [0, 1, 5, 11, 17],
        }
        for input_fps in [10, 25, 30, 50, 60]:
            cap = ControlledFPSVideoCapture(input_fps=input_fps)
            for i in range(5):
                cap.read()
                self.assertEqual(cap.input_frame, expected_results[input_fps][i])

    def test_video_reader_start_frame(self):
        """Test the video reader return the correct frames when starting at a specific frame"""
        # Create the video file
        red_shift = 11
        green_shift = 17
        filename = "test_set_frame_idx.mp4"
        create_video([(filename, 25, 50)], filename, red_shift=red_shift, green_shift=green_shift)

        # Test ControlledFPSVideoCapture at various fps
        fps_test_cases = {
            10: [
                (0, [0, 1, 2, 4, 7, 9, 12, 14, 17, 19, 22, 24, 27, 29, 32]),
                (1, [1, 2, 4, 7, 9, 12, 14, 17, 19, 22, 24, 27, 29, 32]),
                (2, [2, 4, 7, 9, 12, 14, 17, 19, 22, 24, 27, 29, 32]),
                (3, [4, 7, 9, 12, 14, 17, 19, 22, 24, 27, 29, 32]),
                (4, [7, 9, 12, 14, 17, 19, 22, 24, 27, 29, 32]),
                (5, [9, 12, 14, 17, 19, 22, 24, 27, 29, 32]),
            ],
            25: [
                (0, [0, 1, 2, 3, 4, 5]),
                (1, [1, 2, 3, 4, 5, 6]),
                (2, [2, 3, 4, 5, 6, 7]),
                (3, [3, 4, 5, 6, 7, 8]),
            ],
            5: [
                (0, [0, 1, 4, 9, 14, 19, 24]),
                (1, [1, 4, 9, 14, 19, 24]),
                (2, [4, 9, 14, 19, 24]),
                (3, [9, 14, 19, 24]),
                (4, [14, 19, 24]),
                (5, [19, 24]),
            ],
        }
        for fps, test_cases in fps_test_cases.items():
            video_reader = ControlledFPSVideoCapture(filename, fps=fps)
            for frame_idx, expected_frames in test_cases:
                with self.subTest((frame_idx, expected_frames)):
                    video_reader.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
                    # video_reader.set_frame_idx(frame_idx)
                    for expected_frame in expected_frames:
                        ret, frame = video_reader.read()
                        self.assertTrue(ret, msg="reading error")
                        frame_color = frame[0, 0]
                        expected_red, expected_green, _ = expected_frame_color(expected_frame, red_shift, green_shift)
                        self.assertTrue(
                            is_almost_same_color(frame_color[2], expected_red),
                            msg=f"{frame_color[2]} != {expected_red} (Frame_idx {frame_idx}, \
Expected_frame: {expected_frame}, Frame {frame_color}, color: red)",
                        )
                        self.assertTrue(
                            is_almost_same_color(frame_color[1], expected_green),
                            msg=f"{frame_color[1]} != {expected_green} (Frame_idx {frame_idx}, \
Expected_frame: {expected_frame}, Frame {frame_color}, color: green)",
                        )

        # Cleanup
        os.remove(filename)

    def test_set(self):
        # Create the video file
        red_shift = 11
        green_shift = 17
        filename = "test_set_frame_idx.mp4"
        create_video([(filename, 25, 50)], filename, red_shift=red_shift, green_shift=green_shift)
        framerate = 10
        seek_local_frame_idx = 9

        # Test Legacy ControlledFPSVideoCapture at 10 fps
        with self.subTest("Legacy ControlledFPSVideoCapture at 10 fps"):
            video_reader = ControlledFPSVideoCapture(
                filename, fps=framerate, frame_selection_version=ControlledFPSVideoCapture.FRAME_SELECTION_LEGACY
            )
            video_reader.set(cv2.CAP_PROP_POS_FRAMES, seek_local_frame_idx)
            ret, frame = video_reader.read()
            self.assertTrue(ret, msg="reading error")
            frame_color = frame[0, 0]
            expected_global_frame_idx = 19
            expected_red, expected_green, _ = expected_frame_color(expected_global_frame_idx, red_shift, green_shift)
            self.assertTrue(
                is_almost_same_color(frame_color[2], expected_red),
                msg=f"{frame_color[2]} != {expected_red} (Frame_idx {seek_local_frame_idx}, \
Expected_frame: {expected_global_frame_idx}, Frame {frame_color}, color: red)",
            )
            self.assertTrue(
                is_almost_same_color(frame_color[1], expected_green),
                msg=f"{frame_color[1]} != {expected_green} (Frame_idx {seek_local_frame_idx}, \
Expected_frame: {expected_global_frame_idx}, Frame {frame_color}, color: green)",
            )

        # Test ffmphisdp ControlledFPSVideoCapture at 10 fps
        with self.subTest("ffmphisdp ControlledFPSVideoCapture at 10 fps"):
            all_frames = decode_all_frames(filename, framerate=10, use_gpu=False)
            frame_infos = list(all_frames.keys())
            frame_selection = list(all_frames.values())
            print(frame_infos)
            print(frame_selection)
            video_reader = ControlledFPSVideoCapture(
                filename,
                frame_infos=frame_infos,
                frame_selection=frame_selection,
                frame_selection_version=ControlledFPSVideoCapture.FRAME_SELECTION_FFMPHISDP,
            )
            video_reader.set(cv2.CAP_PROP_POS_FRAMES, seek_local_frame_idx)
            ret, frame = video_reader.read()
            self.assertTrue(ret, msg="reading error")
            frame_color = frame[0, 0]
            expected_global_frame_idx = 23
            expected_red, expected_green, _ = expected_frame_color(expected_global_frame_idx, red_shift, green_shift)
            self.assertTrue(
                is_almost_same_color(frame_color[2], expected_red),
                msg=f"{frame_color[2]} != {expected_red} (Frame_idx {seek_local_frame_idx}, \
Expected_frame: {expected_global_frame_idx}, Frame {frame_color}, color: red)",
            )
            self.assertTrue(
                is_almost_same_color(frame_color[1], expected_green),
                msg=f"{frame_color[1]} != {expected_green} (Frame_idx {seek_local_frame_idx}, \
Expected_frame: {expected_global_frame_idx}, Frame {frame_color}, color: green)",
            )

    def test_get_ffmphisdp(self):
        """Test the get method of ControlledFPSVideoCapture_ffmphisdp"""
        # Create the video file
        red_shift = 11
        green_shift = 17
        filename = "test_set_frame_idx.mp4"
        create_video([(filename, 25, 50)], filename, red_shift=red_shift, green_shift=green_shift)
        all_frames = decode_all_frames(filename, framerate=10, use_gpu=False)
        frame_infos = list(all_frames.keys())
        frame_selection = list(all_frames.values())
        print(frame_infos)
        print(frame_selection)
        video_reader = ControlledFPSVideoCapture(
            filename,
            frame_infos=frame_infos,
            frame_selection=frame_selection,
            frame_selection_version=ControlledFPSVideoCapture.FRAME_SELECTION_FFMPHISDP,
        )
        seek_local_frame_idx = 9  # global_idx = 23
        video_reader.set(cv2.CAP_PROP_POS_FRAMES, seek_local_frame_idx)

        # Read a couple frames
        video_reader.read()  # after read: global_idx = 23 , local = 9
        video_reader.read()  # after read: global_idx = 26 , local = 10
        video_reader.read()  # after read: global_idx = 28 , local = 11

        # Get current_frame
        expected_next_local_frame_idx = 11
        expected_global_index = 28
        self.assertEqual(expected_next_local_frame_idx, video_reader.get(cv2.CAP_PROP_POS_FRAMES))
        self.assertEqual(expected_next_local_frame_idx, video_reader.output_frame)
        self.assertEqual(expected_global_index, video_reader.input_frame)

        # Get frame count
        expected_local_frame_count = 20
        self.assertEqual(expected_local_frame_count, video_reader.get(cv2.CAP_PROP_FRAME_COUNT))
