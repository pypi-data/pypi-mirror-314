class Size2:

    @staticmethod
    def parse(value):
        if isinstance(value, (tuple, list)):
            if len(value) != 2:
                raise ValueError(f"invalid size2 tuple: {value}")
            if isinstance(value[0], (int, float)) and isinstance(
                value[1], (int, float)
            ):
                return value
            else:
                raise ValueError(f"invalid size2 tuple: {value}")
        else:
            raise ValueError(f"invalid size2: {value}")
