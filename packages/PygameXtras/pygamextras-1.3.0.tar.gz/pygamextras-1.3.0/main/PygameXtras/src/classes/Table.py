import pygame

class Table:
    def __init__(
            self, surface, xy: tuple, columns_rows: tuple, x_distance_y_distance: tuple,
            circle_color=(0, 0, 255),
            circle_radius=10):
        """
        xy centers the table at the given position
        """

        self.surface = surface
        self.columns, self.rows = columns_rows[0], columns_rows[1]
        self.x_distance, self.y_distance = x_distance_y_distance[0], x_distance_y_distance[1]
        self.circle_color = circle_color
        self.circle_radius = circle_radius

        x = xy[0]-((self.columns-1)/2)*self.x_distance
        y = xy[1]-((self.rows-1)/2)*self.y_distance
        self.xy = (x, y)

        if self.rows < 1:
            raise ValueError(
                f"Invalid argument for 'rows': '{self.rows}'.")
        if self.columns < 1:
            raise ValueError(
                f"Invalid argument for 'columns': '{self.columns}'.")
        if self.x_distance < 1:
            raise ValueError(
                f"Invalid argument for 'x_distance': '{self.x_distance}'.")
        if self.y_distance < 1:
            raise ValueError(
                f"Invalid argument for 'y_distance': '{self.y_distance}'.")

        # target: dict["row"]["column"] ("self.tdict")
        self.dict = {}
        for x in range(self.columns):
            temp_d = {}
            for y in range(self.rows):
                temp_d[y] = (self.xy[0]+x*self.x_distance,
                             self.xy[1]+y*self.y_distance)
            self.dict[x] = temp_d

    def draw_dots(self):
        for x in range(self.columns):
            for y in range(self.rows):
                pygame.draw.circle(
                    self.surface, self.circle_color, self.dict[x][y], self.circle_radius)

    def get(self, xy: tuple):
        assert isinstance(xy, (tuple, list)), f"invalid argument for 'xy': {xy}"
        assert len(xy) == 2, f"invalid argument for 'xy': {xy}"
        x, y = xy
        try:
            return self.dict[x][y]
        except KeyError:
            raise Exception(f"x or y out of range (x: {x}, y: {y}, min_x: 0, min_y: 0, max_x: {self.columns-1}, max_y: {self.rows-1}")
