import weakref

class Dummy:

    def __init__(self, value):
        self.value = value

weak_dict = weakref.WeakValueDictionary()

var = Dummy(1)

weak_dict["var"] = var

print("var" in weak_dict)

del var

print("var" in weak_dict)