import asyncio

from soda_sim_remote_ctrl.Simulator import Simulator
from soda_sim_remote_ctrl.UE4API import UE4API
from soda_sim_remote_ctrl.UObject.UObject import UObject

if __name__ == "__main__":
    ue4api = UE4API()
    sim = Simulator(ue4api)

    async def main():
        await sim.update_default_objects(ue4api.session)

        transform = (
            await sim.math_library.call.MakeTransform(
                ue4api.session,
                Location={"X": 0, "Y": 0, "Z": 100},
                Rotation={"Yaw": 90, "Pitch": 0, "Roll": 0},
                Scale={"X": 1, "Y": 1, "Z": 1},
            )
        )["ReturnValue"]
        new_actor = UObject(
            ue4api,
            (
                await sim.gameplay_statics.call.BeginDeferredActorSpawnFromClass(
                    ue4api.session,
                    WorldContextObject=sim.arrival_game_mode.object_path,
                    ActorClass="/Script/UnrealArrival.DefaultVehicleSpawnPoint",
                    SpawnTransform=transform,
                )
            )["ReturnValue"],
        )
        await sim.gameplay_statics.call.FinishSpawningActor(
            ue4api.session, Actor=new_actor.object_path, SpawnTransform=transform
        )

        # Add actor to the ActorFactory
        level_state = UObject(
            ue4api,
            (await sim.arrival_game_mode.getter.LevelState(ue4api.session))["LevelState"],
        )
        actor_factory = UObject(
            ue4api,
            (await sim.level_state.getter.ActorFactory(ue4api.session))["ActorFactory"],
        )
        await actor_factory.call.AddActor(ue4api.session, Actor=new_actor.object_path)

        # Save Level
        res = (
            await level_state.call.SaveLevel(
                ue4api.session,
                InOverrideSlotIndex=0,
                InOverrideDescription="MySave",
                bCreateNewSlot=False,
            )
        )["ReturnValue"]
        assert res
        ue4api.session.close()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
