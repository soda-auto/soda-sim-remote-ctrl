from .UObjectMethod import UObjectMethod
from .UObjectPropertyGetter import UObjectPropertyGetter
from .UObjectPropertySetter import UObjectPropertySetter


class UObject:
    """
        The python UObject is reflection of the UE4 C++ UObject.
    To call the UObject method use the UObject.call property
    (example: await some_obj.call.TestMethod(param1=param1, param2=param2))
    To read the UObject property use the UObject.setter property
    (example: test_property = await some_obj.setter.TestProperty())
    To write the UObject property use the UObject.getter property
    (example: await some_obj.getter.TestProperty(some_value))
    """

    def __init__(self, ue4api, object_path, parent=None):
        assert len(object_path)
        self.ue4api = ue4api
        self.object_path = object_path
        self.call = UObjectMethod(self)
        self.setter = UObjectPropertySetter(self)
        self.getter = UObjectPropertyGetter(self)
        self.parent = parent

    async def object_call(self, **kwargs):
        if "body" not in kwargs:
            kwargs["body"] = {}
        if "function_name" in kwargs:
            kwargs["body"]["functionName"] = kwargs["function_name"]
        if "parameters" in kwargs:
            kwargs["body"]["parameters"] = kwargs["parameters"]
        kwargs["body"]["objectPath"] = self.object_path
        return await self.ue4api.req_object_call(**kwargs)

    async def object_read_property(self, **kwargs):
        if "body" not in kwargs:
            kwargs["body"] = {}
        if "property_name" in kwargs:
            kwargs["body"]["propertyName"] = kwargs["property_name"]
        kwargs["body"]["access"] = "READ_ACCESS"
        kwargs["body"]["objectPath"] = self.object_path
        return await self.ue4api.req_object_property(**kwargs)

    async def object_write_property(self, **kwargs):
        if "body" not in kwargs:
            kwargs["body"] = {}
        if "property_name" in kwargs:
            property_name = kwargs["property_name"]
            kwargs["body"]["propertyName"] = property_name
            property_value = None
            if "property_value" in kwargs:
                property_value = kwargs["property_value"]
                if not isinstance(property_value, dict):
                    property_value = {property_name: property_value}
            kwargs["body"]["propertyValue"] = property_value
        if "isTransactionAccess" in kwargs and kwargs["isTransactionAccess"] is True:
            kwargs["body"]["access"] = "WRITE_TRANSACTION_ACCESS"
        else:
            kwargs["body"]["access"] = "WRITE_ACCESS"
        kwargs["body"]["objectPath"] = self.object_path
        return await self.ue4api.req_object_property(**kwargs)

    async def object_describe(self, **kwargs):
        if "body" not in kwargs:
            kwargs["body"] = {}
        kwargs["body"]["objectPath"] = self.object_path
        return await self.ue4api.req_object_describe(**kwargs)
