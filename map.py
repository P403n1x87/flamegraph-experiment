class Map(dict):
    """Element of a free module over a ring."""

    def __call__(self, x):
        # TODO: 0 is not the generic element of the ring
        return self.get(x, 0)

    def __add__(self, other):
        m = self.__class__(self)
        for k, v in other.items():
            n = m.setdefault(k, v.__class__()) + v
            if not n and k in m:
                del m[k]
                continue
            m[k] = n
        return m

    def __mul__(self, other):
        m = self.__class__(self)
        for k, v in self.items():
            n = v * other
            if not n and k in m:
                del m[k]
                continue
            m[k] = n
        return m

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        return self * (1 / other)

    def __rtruediv__(self, other):
        return self.__div__(other)

    def __sub__(self, other):
        return self + (-other)

    def __neg__(self):
        m = Map(self)
        for k, v in m.items():
            m[k] = -v
        return m

    def supp(self):
        return set(self.keys())


if __name__ == "__main__":
    f = Map({"a": 2, "b": 4})
    g = Map({"b": 4, "c": 4})

    print("f =", f)
    print("g =", g)

    print("f + g = ", f + g)
    print("f - g = ", f - g)
    print("supp(f - g) = ", (f - g).supp())
    print("f * 2 =", f * 2)
    print("2 * f =", 2 * f)
