import asyncio

from soda_sim_remote_ctrl.SodaVehicle import *
from soda_sim_remote_ctrl.UObject.UObject import *
from soda_sim_remote_ctrl.UE4API import *

class FVechicleSaveAddress:
    def __init__(self, source, location):
        self.source = source
        self.location = location
    def to_json(self):
        return {"Source": self.source, "Location": self.location}
        
class Simulator():
    def __init__(self, ue4api):
        self.ue4api = ue4api

        # Base soda static objects
        self.soda_statics = UObject(ue4api, "/Script/UnrealSoda.Default__SodaStatics")
        self.level_state_static = UObject(ue4api, "/Script/UnrealSoda.Default__LevelState")
        self.vehicle_static = UObject(ue4api, "/Script/UnrealSoda.Default__SodaVehicle")
        self.game_mode_static = UObject(ue4api, "/Script/UnrealSoda.Default__SodaGameModeComponent")

        # Base UE static objects
        self.game_user_settings = UObject(ue4api, "/Script/Engine.Default__GameUserSettings")
        self.gameplay_statics = UObject(ue4api, "/Script/Engine.Default__GameplayStatics")

        # Base soda gameplay objects
        self.soda_game_mode = None
        self.soda_user_settings = None
        self.level_state = None
        self.actor_factory = None

    #########################
    ##   Common
    #########################
    
    def paths_to_uobjects(self, paths, only_first=False):
        if only_first:
            return UObject(self.ue4api, paths[0]) if len(paths) else None
        else:
            ret = []
            for path in paths:
                ret.append(UObject(self.ue4api, path))
            return ret

    async def update_default_objects(self, session):
        self.soda_game_mode = None
        self.level_state = None
        self.actor_factory = None
        resp1 = asyncio.create_task(self.soda_statics.call.FindAllObjectsByClass(session, Class="/Script/UnrealSoda.SodaGameModeComponent"))
        resp2 = asyncio.create_task(self.soda_statics.call.FindAllObjectsByClass(session, Class="/Script/UnrealSoda.LevelState"))
        resp3 = asyncio.create_task(self.soda_statics.call.GetSodaUserSettings(session))
        done, pending = await asyncio.wait({resp1, resp2, resp3})
        assert (len(pending) == 0)
        self.soda_game_mode = self.paths_to_uobjects(resp1.result()["ReturnValue"], only_first=True)
        self.level_state = self.paths_to_uobjects(resp2.result()["ReturnValue"], only_first=True)
        self.soda_user_settings = UObject(self.ue4api, resp3.result()["ReturnValue"])
        self.actor_factory = UObject(self.ue4api, (await self.level_state.getter.ActorFactory(session))["ActorFactory"])
       
    async def find_actor_by_name(self, session, name):
        actor_path_name = (await self.soda_statics.call.FindActoByName(session, Name=name))["ReturnValue"]
        if actor_path_name:
            return UObject(self.ue4api, actor_path_name)
        else:
            return None

    async def app_quit(self, session, force=True):
        await self.soda_game_mode.call.RequestQuit(session, bForce=force)
        
    async def restart_level(self, session, force=True):
        await self.soda_game_mode.call.RequestRestartLevel(session, bForce=force)
        
    async def scenario_play(self, session):
        await self.soda_game_mode.call.ScenarioPlay(session)    
        
    async def scenario_stop(self, session):
        await self.soda_game_mode.call.ScenarioStop(session, Reason="UserRequest")  
        
    async def spawn_actor(self, session, class_path, transform):
        new_actor = UObject(
            self.ue4api, (
                await self.gameplay_statics.call.BeginDeferredActorSpawnFromClass(
                    session,
                    WorldContextObject=self.soda_game_mode.object_path,
                    ActorClass=class_path,
                    SpawnTransform=transform.to_json()
                ))["ReturnValue"]
        )
        await self.gameplay_statics.call.FinishSpawningActor(
            self.ue4api.session, Actor=new_actor.object_path, SpawnTransform=transform.to_json()
        )
        await self.actor_factory.call.AddActor(session, Actor=new_actor.object_path)
        return new_actor
        
    #########################
    ##    Work with level
    #########################
    
    async def get_levels(self, session):
        return (await self.soda_statics.call.GetAllMapPaths(session))["ReturnValue"]
        
    async def get_current_level(self, session):
        return (await self.soda_statics.call.GetLevelName(session))["ReturnValue"]
        
    async def open_level(self, session, level_path):
        return (await self.soda_statics.call.OpenLevel(session, LevelPath=level_path))
    
    async def open_level_from_local_slot(self, session, slot_index):
        return (await self.level_state_static.call.ReloadLevelFromSlotLocally(session, SlotIndex=slot_index))["ReturnValue"]
        
    async def open_level_from_remote_slot(self, session, slot_index):
        return (await self.level_state_static.call.ReloadLevelFromSlotRemotly(session, ScenarioID=slot_index))["ReturnValue"]
        
    async def open_level_from_local_slot_by_desc(self, session, desc):
        slots = await self.get_level_local_slots(session)
        for index, item in enumerate(slots):
            if item["Description"] == desc :
                return await self.open_level_from_local_slot(session, item["SlotIndex"]);
        return False
        
    async def get_level_local_slots(self, session, sort_by_dateyime=True):
        return (await self.level_state_static.call.GetLevelSlotsLocally(session, bSortByDateTime=sort_by_dateyime))["Slots"]
        
    async def get_level_remote_slots(self, session, sort_by_dateyime=True):
        return (await self.level_state_static.call.GetLevelSlotsRemotly(session, bSortByDateTime=sort_by_dateyime))["Slots"] 
        
    async def get_curren_level_slot(self, session):
        return (await self.level_state.getter.Slot)

        
    ###############################
    ##    Work with SODA vehicle
    ###############################
    
    async def get_all_soda_vehicles(self, session):
        paths = (await self.soda_statics.call.FindAllObjectsByClass(session, Class="/Script/UnrealSoda.SodaVehicle"))["ReturnValue"]
        ret = []
        for path in paths:
            ret.append(SodaVehicle(self.ue4api, path))
        return ret

    async def get_active_vehicle(self, session):
        path = (await self.soda_game_mode.call.GetActiveVehicle(session))["ReturnValue"]
        return SodaVehicle(self.ue4api, path) if len(path) else None

    async def spawn_vehicle(self, session, address, location=FVector(0,0,0), rotation=FRotator(0,0,0), posses=True, desire_name=""):
        self.object_path = (
            await self.vehicle_static.call.SpawnVehicleFormAddress(
                session, 
                Address=address.to_json(), 
                Location=location.to_json(),
                Rotation=rotation.to_json(), 
                Posses=posses,
                DesireName=desire_name))["ReturnValue"]
        assert (len(self.object_path))


    async def get_vehicle_classes(self, session):
        return (await self.soda_statics.call.GetAllSubclassOfClass(session, Class="/Script/UnrealSoda.SodaVehicle"))["SubClasses"]

    async def get_vehicle_slots(self, session):
        return (await self.vehicle_static.call.GetSavedVehicles(session, bJson=True))["FilePaths"]

    async def get_vehicle_component_classes(self, session):
        return (await self.soda_statics.call.GetAllSubclassOfClass(session,Class="/Script/UnrealSoda.VehicleComponent"))["SubClasses"]


