import numpy as np

CIRCLE_RADIUS = 9.15
GOAL_SIZE = 7.32
GOAL_AREA_SIZE = 5.5
PENALTY_AREA_SIZE = 16.5
PENALTY_MARK_DISTANCE = 11.0


# This file contains all the information concerning the soccer field model.


def create_field_objects(pitch_length=105.0, pitch_width=68.0):
    arc_angle = np.arccos((PENALTY_AREA_SIZE - PENALTY_MARK_DISTANCE) / CIRCLE_RADIUS)
    field_objects = {
        "Center Circle": {
            "type": "circle",
            "x": 0.0,
            "y": 0.0,
            "radius": CIRCLE_RADIUS,
            "startAngle": 0.0,
            "endAngle": 2.0 * np.pi,
        },
        "Halfway line": {
            "type": "line",
            "start_point": (0.0, -pitch_width / 2.0),
            "end_point": (0.0, pitch_width / 2.0),
        },
    }

    for level, level_sign in zip(["Lower", "Upper"], [-1.0, 1.0]):
        x = pitch_length / 2.0
        y = pitch_width / 2.0
        field_objects[f"{level} touch line"] = {
            "type": "line",
            "start_point": (
                -x,
                level_sign * y,
            ),
            "end_point": (
                x,
                level_sign * y,
            ),
        }

    for side, sign in zip(["Right", "Left"], [1.0, -1.0]):
        x = pitch_length / 2.0
        y = pitch_width / 2.0
        field_objects[f"{side} goal line"] = {
            "type": "line",
            "start_point": (
                sign * x,
                -y,
            ),
            "end_point": (
                sign * x,
                y,
            ),
        }

        x = pitch_length / 2.0 - PENALTY_AREA_SIZE
        y = GOAL_SIZE / 2.0 + PENALTY_AREA_SIZE
        field_objects[f"{side} penalty line"] = {
            "type": "line",
            "start_point": (
                sign * x,
                -y,
            ),
            "end_point": (
                sign * x,
                y,
            ),
        }

        x = pitch_length / 2.0 - GOAL_AREA_SIZE
        y = GOAL_SIZE / 2.0 + GOAL_AREA_SIZE
        field_objects[f"{side} goal area line"] = {
            "type": "line",
            "start_point": (
                sign * x,
                -y,
            ),
            "end_point": (
                sign * x,
                y,
            ),
        }

        field_objects[f"{side} penalty arc"] = {
            "type": "circle",
            "x": sign * (pitch_length / 2.0 - PENALTY_MARK_DISTANCE),
            "y": 0.0,
            "radius": CIRCLE_RADIUS,
            "startAngle": -arc_angle - (sign + 1.0) * np.pi / 2.0,
            "endAngle": arc_angle - (sign + 1.0) * np.pi / 2.0,
        }

        for level, level_sign in zip(["lower", "upper"], [-1.0, 1.0]):
            y = GOAL_SIZE / 2.0 + PENALTY_AREA_SIZE
            field_objects[f"{side} {level} penalty line"] = {
                "type": "line",
                "start_point": (
                    sign * pitch_length / 2.0,
                    level_sign * y,
                ),
                "end_point": (
                    sign * (pitch_length / 2.0 - PENALTY_AREA_SIZE),
                    level_sign * y,
                ),
            }

            y = GOAL_SIZE / 2.0 + GOAL_AREA_SIZE
            field_objects[f"{side} {level} goal area line"] = {
                "type": "line",
                "start_point": (
                    sign * pitch_length / 2.0,
                    level_sign * y,
                ),
                "end_point": (
                    sign * (pitch_length / 2.0 - GOAL_AREA_SIZE),
                    level_sign * y,
                ),
            }
    return field_objects
