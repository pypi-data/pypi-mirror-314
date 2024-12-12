from typing import List, Dict

def bbox_to_corners(bbox: List[float]) -> List[float]:
    """ Transform a list of point representing a bbox to the four points of a rectangle"""

    [top_left_x, top_left_y, bottom_right_x, bottom_right_y] = bbox

    return [
        top_left_x,
        top_left_y,
        bottom_right_x,
        top_left_y,
        bottom_right_x,
        bottom_right_y,
        top_left_x,
        bottom_right_y
    ]

def corners_to_bbox(vertices: List[float]) -> List[float]:
    """ Transform a list of point representing a bbox to the four points of a rectangle"""

    [top_left_x, top_left_y, top_right_x, top_right_y, bottom_right_x, bottom_right_y, bottom_left_x, bottom_left_y] = vertices

    return [
        top_left_x,
        top_left_y,
        bottom_right_x,
        bottom_right_y
    ]

def vertices_to_points(vertices: List[float]) -> List[Dict]:
    """Transform vertices [float,float,float,float,...] to points [{ x: float, y: float },{ x: float, y: float },...]"""

    points = []

    for i, v in enumerate(vertices):
        if i % 2 == 0:
            points.append({ "x" : vertices[i], "y" : vertices[i + 1]})

    return points

def points_to_vertices(points):
    """Transform points [{ x: float, y: float },{ x: float, y: float },...] to vertices [float,float,float,float,...] """
    vertices = []
    for p in points:
        vertices.append(p['x'])
        vertices.append(p['y'])
    return vertices

def denormalize_points(points: List[Dict], dimension : Dict, round_decimal : int = None) -> List[float]:
    """Transform relative points to absolute points"""

    denormalized_points = []

    for p in points:
        x = p['x'] * float(dimension['width'])
        y = p['y'] * float(dimension['height'])
        if round_decimal != None:
            x = round(x, round_decimal)
            y = round(y, round_decimal)
        denormalized_points.append({"x" : x, "y": y})

    return denormalized_points

def normalize_points(points: List[Dict], dimension : Dict, round_decimal : int = None) -> List[float]:
    """Transform relative points to absolute points"""

    normalized_points = []

    for p in points:
        x = p['x'] / float(dimension['width'])
        y = p['y'] / float(dimension['height'])
        if round_decimal != None:
            x = round(x, round_decimal)
            y = round(y, round_decimal)
        normalized_points.append({"x" : x, "y": y})

    return normalized_points