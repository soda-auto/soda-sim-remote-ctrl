class UObjectPropertySetter:
    def __init__(self, uobject):
        self.uobject = uobject

    def __getattr__(self, name):
        return lambda session, val: self.uobject.object_write_property(
            property_name=name, property_value=val
        )
