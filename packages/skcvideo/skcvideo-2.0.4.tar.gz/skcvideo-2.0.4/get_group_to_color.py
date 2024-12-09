import numpy as np

REFEREE_GOAL_COLORS = [
    (237, 237, 237),
    (20, 20, 20),
    (16, 16, 188),
    (211, 211, 0),
    (9, 239, 239),
    (99, 205, 255),
    (22, 201, 16),
]


def dist_between_colors(c1, c2):
    return np.linalg.norm(np.array(c1) - np.array(c2))


def choose_compatible_colors(color_options, home_team_color, away_team_color):
    """
    Take the three colors from color_options that are farest from teams colors
    """

    def key(color):
        dist_home = dist_between_colors(color, home_team_color)
        dist_away = dist_between_colors(color, away_team_color)
        return dist_home + dist_away

    return sorted(color_options, key=key)[-3:]


def hex_to_bgr(hex_color):
    return tuple(int(hex_color.lstrip("#")[i : i + 2], 16) for i in (4, 2, 0))


def get_team_colors(match, order="bgr"):
    """
    Args:
        * match: match data (usually from the api/database)
        * order: order of the colors, should be either 'bgr' or 'rgb'
    Returns:
        * team_colors: dict of colors (in BGR) of teams jersey and short
    """
    if order not in {"bgr", "rgb"}:
        raise ValueError('order should be either "bgr" or "rgb"')
    team_colors = {}
    for side in ["home", "away"]:
        kit = match[f"{side}_team_kit"]
        for kind in ["jersey", "number"]:
            color = hex_to_bgr(kit[f"{kind}_color"])
            team_colors[f"{side}_{kind}"] = color
    if order == "rgb":
        team_colors = {key: value[::-1] for key, value in team_colors.items()}
    return team_colors


def get_group_to_color(match, order="bgr", kind="jersey"):
    """
    Same function as in frontend
    Args:
        * match: dict from the database or saved match.json
    Returns:
        * dict linking group to their color in bgr
    """
    # See readme for integer labels meaning.
    team_colors = get_team_colors(match, order=order)
    home_team_color = team_colors[f"home_{kind}"]
    away_team_color = team_colors[f"away_{kind}"]
    sorted_colors = choose_compatible_colors(
        REFEREE_GOAL_COLORS,
        home_team_color,
        away_team_color,
    )
    group_to_color = {
        "home team": home_team_color,
        "away team": away_team_color,
        "home goalkeeper": sorted_colors[0],
        "away goalkeeper": sorted_colors[1],
        "referee": sorted_colors[2],
        "balls": (255, 255, 255),
    }
    return group_to_color
