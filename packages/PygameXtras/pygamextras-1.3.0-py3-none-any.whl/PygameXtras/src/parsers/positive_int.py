class PositiveInt:

    @staticmethod
    def parse(value):
        if isinstance(value, int):
            if value < 0:
                raise ValueError(f"invalid positive int: {value}")
            return int(value)
        else:
            raise ValueError(f"invalid positive int: {value}")
