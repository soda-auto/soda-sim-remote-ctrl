from soda_sim_remote_ctrl.UObject.UObject import UObject


class SodaVehicle(UObject):
    def __init__(self, ue4api, object_path, parent=None):
        super().__init__(ue4api, object_path, parent)

    async def respawn(self, session):
        self.object_path = (
            await self.call.RespawnVehcile(session, IsOffset=True, Location={"X": 0, "Y": "0", "Z": 30}))["ReturnValue"]
        assert (len(self.object_path))

    async def respawn_from_class(self, session, class_name):
        self.object_path = (await self.call.RespawnVehcile(session, IsOffset=True, NewVehicleClass=class_name,
                                                           Location={"X": 0, "Y": "0", "Z": 30}))["ReturnValue"]
        assert (len(self.object_path))

    async def respawn_from_slot(self, session, slot_name):
        self.object_path = (await self.call.RespawnVehcileFromSlot(session, IsOffset=True, SlotOrFileName=slot_name,
                                                                   Location={"X": 0, "Y": "0", "Z": 30}))["ReturnValue"]
        assert (len(self.object_path))

    async def set_position(self, session, location, rotation):
        self.object_path = (await
                            self.call.RespawnVehcile(session, Location=location, Rotation=rotation, IsOffset=False)
                            )["ReturnValue"]
        assert (len(self.object_path))

    async def get_component_by_class(self, session, class_name):
        path = (await self.call.GetComponentByClass(session, ComponentClass=class_name))["ReturnValue"]
        return UObject(self.ue4api, path) if len(path) else None

    async def add_component_by_name(self, session, object_class, object_name):
        await self.call.AddVehicleComponent(session, Class=object_class, Name=object_name)

    async def get_component_by_name(self, session, object_name):
        path = (await self.call.FindVehicleComponentByName(session, ComponentName=object_name))["ReturnValue"]
        return UObject(self.ue4api, path) if len(path) else None

    async def get_components_by_class(self, session, class_name):
        paths = (await self.call.K2_GetComponentsByClass(session, ComponentClass=class_name))["ReturnValue"]
        ret = []
        for path in paths:
            ret.append(UObject(self.ue4api, path))
        return ret

    async def get_vehicle_movement(self, session):
        return UObject(self.ue4api, await self.getter.VehicleMovement(session))
