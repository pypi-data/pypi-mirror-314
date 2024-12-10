import math

class C:
    def __init__(self, *values, mo=False):
        """
        vector class - works very similar to c(...) in the language R
        automatically turns into a list if <mo> (="more_operations") is False,
        if True returns another C-class for further mathematical operations

        NOTE:
        if operations like +=, -=, ... are used, the object will
        always stay a C-class!
        """
        assert len(values) > 0, f"list of values can not be empty"

        if len(values) == 1 and isinstance(values[0], (tuple, list)):
            self.__value = list(values[0])
        else:
            for value in values:
                assert (isinstance(value, (int, float))), \
                    f"values have to be int or float, received: '{value}' (type: {type(value)})"
            self.__value = list(values)
            
        self.__more_operations = bool(mo)

    def __repr__(self):
        return self.__value

    def __round__(self, ndigits=0):
        self.round(ndigits)
        return self

    def round(self, decimals=0):
        assert isinstance(decimals, int), f"invalid argument for 'decimals': {decimals}"
        multiplier = 10 ** decimals
        if decimals == 0:
            for i in range(len(self.__value)):
                self.__value[i] = int(math.floor(self.__value[i]*multiplier + 0.5) / multiplier)
        else:
            for i in range(len(self.__value)):
                self.__value[i] = math.floor(self.__value[i]*multiplier + 0.5) / multiplier

    def __add__(self, other):
        if isinstance(other, C):
            assert len(self.__value) == len(other), f"C-objects must have same length ({len(self.__value)} != {len(other)})"
            if self.__more_operations:
                return C(*[v1+v2 for v1, v2 in zip(self.__value, other)])
            else:
                return [v1+v2 for v1, v2 in zip(self.__value, other)]
        else:
            if self.__more_operations:
                return C(*[v + other for v in self.__value])
            else:
                return [v + other for v in self.__value]

    def __iadd__(self, other):
        self.__value = [v + other for v in self.__value]
        return self

    def __sub__(self, other):
        if isinstance(other, C):
            assert len(self.__value) == len(other), f"C-objects must have same length ({len(self.__value)} != {len(other)})"
            if self.__more_operations:
                return C(*[v1-v2 for v1, v2 in zip(self.__value, other)])
            else:
                return [v1-v2 for v1, v2 in zip(self.__value, other)]
        else:
            if self.__more_operations:
                return C(*[v - other for v in self.__value])
            else:
                return [v - other for v in self.__value]

    def __isub__(self, other):
        self.__value = [v - other for v in self.__value]
        return self

    def __mul__(self, other):
        if isinstance(other, C):
            assert len(self.__value) == len(other), f"C-objects must have same length ({len(self.__value)} != {len(other)})"
            if self.__more_operations:
                return C(*[v1*v2 for v1, v2 in zip(self.__value, other)])
            else:
                return [v1*v2 for v1, v2 in zip(self.__value, other)]
        else:
            if self.__more_operations:
                return C(*[v * other for v in self.__value])
            else:
                return [v * other for v in self.__value]

    def __imul__(self, other):
        self.__value = [v * other for v in self.__value]
        return self

    def __truediv__(self, other):
        if isinstance(other, C):
            assert len(self.__value) == len(other), f"C-objects must have same length ({len(self.__value)} != {len(other)})"
            if self.__more_operations:
                return C(*[v1/v2 for v1, v2 in zip(self.__value, other)])
            else:
                return [v1/v2 for v1, v2 in zip(self.__value, other)]
        else:
            if self.__more_operations:
                return C(*[v / other for v in self.__value])
            else:
                return [v / other for v in self.__value]

    def __itruediv__(self, other):
        self.__value = [v / other for v in self.__value]
        return self

    def __floordiv__(self, other):
        if isinstance(other, C):
            assert len(self.__value) == len(other), f"C-objects must have same length ({len(self.__value)} != {len(other)})"
            if self.__more_operations:
                return C(*[v1//v2 for v1, v2 in zip(self.__value, other)])
            else:
                return [v1//v2 for v1, v2 in zip(self.__value, other)]
        else:
            if self.__more_operations:
                return C(*[v // other for v in self.__value])
            else:
                return [v // other for v in self.__value]

    def __ifloordiv__(self, other):
        self.__value = [v // other for v in self.__value]
        return self

    def __iter__(self):
        self.__count = 0
        self.__max = len(self.__value)
        return self

    def __next__(self):
        if self.__count < self.__max:
            v = self.__value[self.__count]
            self.__count += 1
            return v
        else:
            raise StopIteration

    def __len__(self):
        return len(self.__value)

    def __getitem__(self, key):
        return self.__value[key]

    def value(self):
        return self.__value