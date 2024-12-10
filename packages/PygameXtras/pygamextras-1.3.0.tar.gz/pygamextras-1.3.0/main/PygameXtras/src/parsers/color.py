from ..classes.Colors import color_dict


class Color:

    @staticmethod
    def parse(value):
        if isinstance(value, (tuple, list)):
            if len(value) != 3:
                raise ValueError(f"invalid color tuple: {value}")
            if not all((isinstance(v, int) and 0 <= v <= 255) for v in value):
                raise ValueError(f"invalid color tuple: {value}")
            return value
        elif isinstance(value, int):
            if not 0 <= value <= 255:
                raise ValueError(f"invalid color int: {value}")
            return (value, value, value)
        elif isinstance(value, str):
            c = color_dict.get(value, None)
            if c is None:
                raise ValueError(f"invalid color string: {value}")
            return c
        else:
            raise ValueError(f"invalid color: {value}")
