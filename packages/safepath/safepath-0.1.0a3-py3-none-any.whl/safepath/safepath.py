"""SafePath implementation."""

class SafePath:
    """
    A null-safe wrapper that allows chaining of attribute and key accesses
    on potentially None or missing data. At the end of the chain,
    calling the wrapper (i.e. adding `()`) returns the resolved value or None.
    """

    __slots__ = ("_value",)

    def __init__(self, value):
        object.__setattr__(self, "_value", value)

    def __getattr__(self, name):
        # If current value is None or does not have the attribute, return NullSafe(None)
        val = object.__getattribute__(self, "_value")
        if val is None:
            return SafePath(None)
        try:
            return SafePath(getattr(val, name))
        except AttributeError:
            return SafePath(None)

    def __getitem__(self, key):
        val = object.__getattribute__(self, "_value")
        if val is None:
            return SafePath(None)
        try:
            return SafePath(val[key])
        except (KeyError, IndexError, TypeError):
            return SafePath(None)

    def __call__(self):
        # End of the chain, return the underlying value
        return object.__getattribute__(self, "_value")

    def __setattr__(self, name, value):
        # Disallow setting attributes on this proxy
        raise AttributeError("SafePath object is immutable")

    def __repr__(self):
        val = object.__getattribute__(self, "_value")
        return f"SafePath({val!r})"


def sp(value):
    """Return a SafePath wrapper around the given value."""
    return SafePath(value)

