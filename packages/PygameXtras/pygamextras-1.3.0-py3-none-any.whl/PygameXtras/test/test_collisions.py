import unittest

from ..src.classes.Collisions import Collisions


class TestCollisions(unittest.TestCase):
    def test_circle_circle(self):
        # Positive test: circles touching
        self.assertTrue(Collisions.circle_circle((0, 0), 5, (10, 0), 5))
        # Negative test: circles not touching
        self.assertFalse(Collisions.circle_circle((0, 0), 5, (11, 0), 5))

    def test_rect_rect(self):
        # Positive test: rectangles touching
        self.assertTrue(Collisions.rect_rect((0, 0, 10, 10), (10, 0, 10, 10)))
        # Negative test: rectangles not touching
        self.assertFalse(Collisions.rect_rect((0, 0, 10, 10), (11, 0, 10, 10)))

    def test_circle_rect(self):
        # Positive test: circle touching rectangle
        self.assertTrue(Collisions.circle_rect((5, 5), 5, (0, 0, 10, 10)))
        # Negative test: circle not touching rectangle
        self.assertFalse(Collisions.circle_rect((20, 20), 5, (0, 0, 10, 10)))

    def test_line_circle(self):
        # Positive test: line touching circle
        self.assertTrue(Collisions.line_circle((0, 0), (10, 0), (5, 5), 5))
        # Negative test: line not touching circle
        self.assertFalse(Collisions.line_circle((0, 0), (10, 0), (20, 20), 5))

    def test_line_rect(self):
        # Positive test: line intersecting rectangle
        self.assertTrue(Collisions.line_rect((0, 5), (10, 5), (2, 2, 6, 6)))
        # Negative test: line not intersecting rectangle
        self.assertFalse(Collisions.line_rect((0, 0), (1, 1), (2, 2, 6, 6)))

    def test_polygon_circle(self):
        # Positive test: polygon touching circle
        self.assertTrue(
            Collisions.polygon_circle(((0, 0), (10, 0), (5, 10)), (5, 5), 5)
        )
        # Negative test: polygon not touching circle
        self.assertFalse(
            Collisions.polygon_circle(((0, 0), (10, 0), (5, 10)), (20, 20), 5)
        )

    def test_polygon_rect(self):
        # Positive test: polygon touching rectangle
        self.assertTrue(
            Collisions.polygon_rect(((0, 0), (10, 0), (5, 10)), (2, 2, 6, 6))
        )
        # Negative test: polygon not touching rectangle
        self.assertFalse(
            Collisions.polygon_rect(((0, 0), (10, 0), (5, 10)), (20, 20, 6, 6))
        )

    def test_polygon_line(self):
        # Positive test: polygon edge intersecting line
        self.assertTrue(
            Collisions.polygon_line(((0, 0), (10, 0), (5, 10)), (5, 5), (15, 5))
        )
        # Negative test: polygon edge not intersecting line
        self.assertFalse(
            Collisions.polygon_line(((0, 0), (10, 0), (5, 10)), (20, 20), (25, 25))
        )

    def test_polygon_polygon(self):
        # Positive test: polygons touching
        self.assertTrue(
            Collisions.polygon_polygon(
                ((0, 0), (10, 0), (5, 10)), ((5, 5), (15, 5), (10, 15))
            )
        )
        # Negative test: polygons not touching
        self.assertFalse(
            Collisions.polygon_polygon(
                ((0, 0), (10, 0), (5, 10)), ((20, 20), (30, 20), (25, 30))
            )
        )

    def test_line_line(self):
        # Positive test: lines intersecting
        self.assertTrue(Collisions.line_line((0, 0), (10, 10), (0, 10), (10, 0)))
        # Negative test: lines not intersecting
        self.assertFalse(Collisions.line_line((0, 0), (10, 0), (0, 10), (10, 10)))


if __name__ == "__main__":
    unittest.main()
