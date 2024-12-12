from typing import Any


class hybridmethod:
    """
    A decorator that allows for the creation of a method that can be called as a classmethod or an instancemethod.
    See https://stackoverflow.com/questions/28237955/same-name-for-classmethod-and-instancemethod
    """
    def __init__(self, fclass: type, finstance: object = None, doc: str = None):
        self.fclass = fclass
        self.finstance = finstance
        self.__doc__ = doc or fclass.__doc__
        # support use on abstract base classes
        self.__isabstractmethod__ = bool(
            getattr(fclass, '__isabstractmethod__', False)
        )

    def classmethod(self, fclass: type):
        return type(self)(fclass, self.finstance, None)

    def instancemethod(self, finstance: object):
        return type(self)(self.fclass, finstance, self.__doc__)

    def __get__(self, instance: object, cls: type) -> Any:
        if instance is None or self.finstance is None:
            # either bound to the class, or no instance method available
            return self.fclass.__get__(cls, None)
        return self.finstance.__get__(instance, cls)
