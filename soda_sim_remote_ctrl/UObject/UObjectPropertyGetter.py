class UObjectPropertyGetter:
    def __init__(self, uobject):
        self.uobject = uobject

    def __getattr__(self, name):
        return lambda session: self.uobject.object_read_property(
            property_name=name
        )
