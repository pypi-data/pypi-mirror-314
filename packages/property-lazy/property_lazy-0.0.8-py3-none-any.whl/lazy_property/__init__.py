__version__ = "0.0.8"
from functools import update_wrapper


class LazyProperty(property):
    def __init__(self, method, fget=None, fset=None, fdel=None, doc=None):
        self.method = method
        self._cache_name = "__cache_{}".format(self.method.__name__)

        doc = doc or method.__doc__
        super(LazyProperty, self).__init__(fget=fget, fset=fset, fdel=fdel, doc=doc)

        update_wrapper(self, method)

    def __get__(self, instance, owner):
        if instance is None:
            return self

        if hasattr(instance, self._cache_name):
            result = getattr(instance, self._cache_name)
        else:
            if self.fget is not None:
                result = self.fget(instance)
            else:
                result = self.method(instance)

            setattr(instance, self._cache_name, result)

        return result


class LazyWritableProperty(LazyProperty):
    def __set__(self, instance, value):
        if instance is None:
            raise AttributeError

        if self.fset is None:
            setattr(instance, self._cache_name, value)
        else:
            self.fset(instance, value)

    def __delete__(self, instance):
        if instance is None:
            raise AttributeError

        if self.fdel is None:
            delattr(instance, self._cache_name)
        else:
            self.fdel(self._cache_name)


class classproperty:
    """
    Decorator that converts a method with a single cls argument into a property
    that can be accessed directly from the class.
    """

    def __init__(self, method=None):
        self.fget = method

    def __get__(self, instance, cls=None):
        return self.fget(cls)

    def getter(self, method):
        self.fget = method
        return self


def lazy_property_reset(instance, *names):
    for name in names:
        cache_name = f"__cache_{name}"
        if hasattr(instance, cache_name):
            delattr(instance, cache_name)
