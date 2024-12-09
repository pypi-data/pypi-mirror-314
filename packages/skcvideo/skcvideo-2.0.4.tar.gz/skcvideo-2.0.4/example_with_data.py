import json
import os

import click

from get_group_to_color import get_group_to_color
from skcvideo.colors import BLACK, GREEN, WHITE
from skcvideo.minimap import Minimap
from skcvideo.reader import Reader
from skcvideo.timeline import Timeline
from skcvideo.utils import put_text
from skcvideo.video_incrustation import VideoIncrustation


class Visualizator(Reader):
    def __init__(self, video_path, match_data, data, **kwargs):
        self.match_data = match_data
        self.data = data

        self.players = {p["trackable_object"]: p for p in match_data["players"] + match_data["referees"]}
        self.group_to_color = get_group_to_color(self.match_data, order="bgr", kind="jersey")
        self.group_to_text_color = get_group_to_color(self.match_data, order="bgr", kind="number")

        self.video_incrustation = VideoIncrustation(
            box=[0, 575, 720, 575 + 1280],
        )
        self.minimap = Minimap(
            box=[200, 0, 590, 575], pitch_length=match_data["pitch_length"], pitch_width=match_data["pitch_width"]
        )
        self.timeline = Timeline(
            box=[730, 585, 820, 1845],
            parent=self,
            timeline_color=self.timeline_color,
        )

        super().__init__(video_path, **kwargs)

    def info_mapping(self, d):
        trackable_object = d.get("trackable_object", None)
        if trackable_object == 55:
            group = "balls"
        elif "group_name" in d:
            group = d["group_name"]
        else:
            player = self.players[trackable_object]
            if "number" in player:
                if player["team_id"] == self.match_data["home_team"]["id"]:
                    side = "home"
                else:
                    side = "away"

                if player["player_role"]["name"] == "Goalkeeper":
                    kind = "goalkeeper"
                else:
                    kind = "team"

                group = f"{side} {kind}"

            else:
                group = "referee"

        info = {
            "x": d["x"],
            "y": d["y"],
            "radius": 3 if group == "balls" else 7,
            "color": self.group_to_color.get(group, BLACK),
            "second_color": WHITE,
            "text": None,
            "text_color": self.group_to_text_color.get(group, WHITE),
        }
        if trackable_object is not None and trackable_object != 55:
            info["text"] = str(self.players[trackable_object].get("number", "R"))
        return info

    def timeline_color(self, frame):
        if len(self.data[frame]["data"]) > 0:
            return GREEN
        else:
            return BLACK

    def refresh(self):
        put_text(
            img=self.big_image,
            text=f"Frame {self.frame}",
            org=(20, 20),
            align_x="left",
            align_y="top",
        )
        self.timeline.refresh(self.big_image, self.frame)
        self.video_incrustation.refresh(self.big_image, self.image.copy())
        self.minimap.refresh(self.big_image, self.data[self.frame]["data"], self.info_mapping)


@click.command()
@click.option("--data-dir", required=True, help="Path to the data directory")
@click.option("--video-path", default=None, help="Path to the video")
def main(data_dir, video_path):
    match_data_path = os.path.join(data_dir, "match_data.json")
    with open(match_data_path, "rb") as f:
        match_data = json.load(f)
    print("match_id:", match_data["id"])

    data_path = os.path.join(data_dir, "structured_data.json")
    with open(data_path) as f:
        data = json.load(f)

    reader = Visualizator(
        video_path,
        match_data,
        data,
        min_frame=0,
        max_frame=9000,
    )
    reader.start()


if __name__ == "__main__":
    main()
