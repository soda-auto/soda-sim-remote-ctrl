class UObjectMethod:
    def __init__(self, uobject):
        self.uobject = uobject

    def __getattr__(self, name):
        return lambda session, **kwargs: self.uobject.object_call(
            **{"function_name": name, "parameters": kwargs}
        )
