class Coordinate:

    @staticmethod
    def parse(value):
        if isinstance(value, (tuple, list)):
            if len(value) != 2:
                raise ValueError(f"invalid coordinate tuple: {value}")
            if isinstance(value[0], (int, float)) and isinstance(
                value[1], (int, float)
            ):
                return value
            elif isinstance(value[0], (list, tuple)) and isinstance(
                value[1], (list, tuple)
            ):
                xy1 = Coordinate.parse(value[0])
                xy2 = Coordinate.parse(value[1])
                return (xy1[0] + xy2[0], xy1[1] + xy2[1])
            else:
                raise ValueError(f"invalid coordinate tuple: {value}")
        else:
            raise ValueError(f"invalid coordinate: {value}")
