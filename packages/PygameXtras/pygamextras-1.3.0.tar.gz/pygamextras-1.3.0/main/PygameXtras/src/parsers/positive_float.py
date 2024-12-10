class PositiveFloat:

    @staticmethod
    def parse(value):
        if isinstance(value, (int, float)):
            if value < 0:
                raise ValueError(f"invalid positive float: {value}")
            return float(value)
        else:
            raise ValueError(f"invalid positive float: {value}")
