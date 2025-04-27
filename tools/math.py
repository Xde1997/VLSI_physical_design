from base.point import Point2D
def manhattan_distance(point1: Point2D, point2: Point2D) -> float:
    return abs(point1.x - point2.x) + abs(point1.y - point2.y)
