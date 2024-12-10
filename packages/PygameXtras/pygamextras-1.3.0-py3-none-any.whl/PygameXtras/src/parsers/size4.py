class Size4:

    @staticmethod
    def parse(value):
        if isinstance(value, (tuple, list)):
            if len(value) != 4:
                raise ValueError(f"invalid size4 tuple: {value}")
            if (
                isinstance(value[0], (int, float))
                and isinstance(value[1], (int, float))
                and isinstance(value[2], (int, float))
                and isinstance(value[3], (int, float))
            ):
                return value
            else:
                raise ValueError(f"invalid size4 tuple: {value}")
        else:
            raise ValueError(f"invalid size4: {value}")
