class Collisions:
    @staticmethod
    def circle_circle(c1_center: tuple, c1_radius: float, c2_center: tuple, c2_radius: float) -> bool:
        return (c2_center[0] - c1_center[0]) ** 2 + (c2_center[1] - c1_center[1]) ** 2 <= (c1_radius + c2_radius) ** 2

    @staticmethod
    def rect_rect(rect1: tuple, rect2: tuple) -> bool:
        """ expects rects in the form of (x, y, width, height) """
        x1, y1, w1, h1 = rect1
        x2, y2, w2, h2 = rect2
        if x1 + w1 < x2 or x2 + w2 < x1:
            return False
        if y1 + h1 < y2 or y2 + h2 < y1:
            return False
        return True

    @staticmethod
    def circle_rect(circle_center: tuple, circle_radius: float, rect: tuple) -> bool:
        cx, cy = circle_center
        rx, ry, rw, rh = rect

        # Find the closest point to the circle within the rectangle
        closest_x = min(max(cx, rx), rx + rw)
        closest_y = min(max(cy, ry), ry + rh)

        # Calculate the distance between the circle's center and this closest point
        distance_x = cx - closest_x
        distance_y = cy - closest_y

        # If the distance is less than or equal to the circle's radius, there's an intersection
        return distance_x ** 2 + distance_y ** 2 <= circle_radius ** 2

    @staticmethod
    def line_circle(line_pos1: tuple, line_pos2: tuple, circle_center: tuple, circle_radius: float) -> bool:
        x1, y1 = line_pos1
        x2, y2 = line_pos2
        cx, cy = circle_center

        # Compute the vector from line start to circle center
        ac = (cx - x1, cy - y1)
        ab = (x2 - x1, y2 - y1)
        ab_len_squared = ab[0] ** 2 + ab[1] ** 2

        # Project ac onto ab, computing the point on ab closest to circle center
        projection = (ac[0] * ab[0] + ac[1] * ab[1]) / ab_len_squared
        closest_x = x1 + projection * ab[0]
        closest_y = y1 + projection * ab[1]

        # Clamp closest point to the segment
        if projection < 0:
            closest_x, closest_y = x1, y1
        elif projection > 1:
            closest_x, closest_y = x2, y2

        # Calculate the distance from the closest point to the circle center
        distance_x = closest_x - cx
        distance_y = closest_y - cy

        # Check if the distance is less than or equal to the circle's radius
        return distance_x ** 2 + distance_y ** 2 <= circle_radius ** 2

    @staticmethod
    def line_rect(line_pos1: tuple, line_pos2: tuple, rect: tuple) -> bool:
        rx, ry, rw, rh = rect
        rect_lines = [
            ((rx, ry), (rx + rw, ry)),
            ((rx + rw, ry), (rx + rw, ry + rh)),
            ((rx + rw, ry + rh), (rx, ry + rh)),
            ((rx, ry + rh), (rx, ry)),
        ]

        for rl1, rl2 in rect_lines:
            if Collisions.line_line(line_pos1, line_pos2, rl1, rl2):
                return True

        # Check if the line starts or ends inside the rectangle
        x1, y1 = line_pos1
        x2, y2 = line_pos2
        if (rx <= x1 <= rx + rw and ry <= y1 <= ry + rh) or (rx <= x2 <= rx + rw and ry <= y2 <= ry + rh):
            return True

        return False

    @staticmethod
    def polygon_circle(polygon: tuple, circle_center: tuple, circle_radius: float) -> bool:
        cx, cy = circle_center

        # Check if any of the polygon's vertices are within the circle
        for px, py in polygon:
            if (px - cx) ** 2 + (py - cy) ** 2 <= circle_radius ** 2:
                return True

        # Check if any of the polygon's edges intersect the circle
        for i in range(len(polygon)):
            p1 = polygon[i]
            p2 = polygon[(i + 1) % len(polygon)]
            if Collisions.line_circle(p1, p2, circle_center, circle_radius):
                return True

        return False

    @staticmethod
    def polygon_rect(polygon: tuple, rect: tuple) -> bool:
        rx, ry, rw, rh = rect

        # Check if any of the polygon's vertices are within the rectangle
        for px, py in polygon:
            if rx <= px <= rx + rw and ry <= py <= ry + rh:
                return True

        # Check if any of the polygon's edges intersect the rectangle
        for i in range(len(polygon)):
            p1 = polygon[i]
            p2 = polygon[(i + 1) % len(polygon)]
            if Collisions.line_rect(p1, p2, rect):
                return True

        return False

    @staticmethod
    def polygon_line(polygon: tuple, line_pos1: tuple, line_pos2: tuple) -> bool:
        for i in range(len(polygon)):
            p1 = polygon[i]
            p2 = polygon[(i + 1) % len(polygon)]
            if Collisions.line_line(p1, p2, line_pos1, line_pos2):
                return True
        return False

    @staticmethod
    def polygon_polygon(polygon1: tuple, polygon2: tuple) -> bool:
        # Check if any of the edges of polygon1 intersect any of the edges of polygon2
        for i in range(len(polygon1)):
            p1 = polygon1[i]
            p2 = polygon1[(i + 1) % len(polygon1)]
            if Collisions.polygon_line(polygon2, p1, p2):
                return True

        # Check if polygon2 is entirely inside polygon1 or vice versa
        if Collisions._point_in_polygon(polygon1[0], polygon2) or Collisions._point_in_polygon(polygon2[0], polygon1):
            return True

        return False

    @staticmethod
    def _point_in_polygon(point: tuple, polygon: tuple) -> bool:
        x, y = point
        inside = False
        for i in range(len(polygon)):
            xi, yi = polygon[i]
            xj, yj = polygon[(i + 1) % len(polygon)]
            intersect = ((yi > y) != (yj > y)) and (x < (xj - xi) * (y - yi) / (yj - yi) + xi)
            if intersect:
                inside = not inside
        return inside

    @staticmethod
    def line_line(line1_pos1: tuple, line1_pos2: tuple, line2_pos1: tuple, line2_pos2: tuple) -> bool:
        def ccw(A, B, C):
            return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])

        A, B = line1_pos1, line1_pos2
        C, D = line2_pos1, line2_pos2
        return ccw(A, C, D) != ccw(B, C, D) and ccw(A, B, C) != ccw(A, B, D)
