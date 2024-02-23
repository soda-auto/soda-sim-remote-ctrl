import asyncio

from soda_sim_remote_ctrl.Simulator import Simulator
from soda_sim_remote_ctrl.UE4API import UE4API
from soda_sim_remote_ctrl.UObject.UObject import UObject

if __name__ == "__main__":
    ue4api = UE4API()
    sim = Simulator(ue4api)

    async def main():
        await sim.update_default_objects(ue4api.session)

        # print(await sim.soda_statics.call.GetAllSubclassOfClass(session, Class="/Script/Engine.Actor"))

        pattern_actors_paths = (
            await sim.gameplay_statics.call.GetAllActorsOfClass(
                ue4api.session,
                WorldContextObject=sim.soda_game_mode.object_path,
                ActorClass="/SodaSim/ActorsLibrery/Markers/ArUCO_pattern_dict8.ArUCO_pattern_dict8_C",
            )
        )["OutActors"]

        if len(pattern_actors_paths) == 0:
            print("Can't find any class")
            return

        for path_name in pattern_actors_paths:
            print("Found Patternt Actor:", path_name)

        pattern_actor = UObject(
            ue4api, pattern_actors_paths[0]
        )

        print(
            "Current location:",
            (await pattern_actor.call.K2_GetActorLocation(ue4api.session))["ReturnValue"],
        )

        await pattern_actor.call.K2_SetActorLocation(
            ue4api.session,
            NewLocation={"X": 0, "Y": 0, "Z": 300},
            bSweep=False,
            bTeleport=True,
        )

        print(
            "New location:",
            (await pattern_actor.call.K2_GetActorLocation(ue4api.session))["ReturnValue"],
        )

        print(
            "Current rotation:",
            (await pattern_actor.call.K2_GetActorRotation(ue4api.session))["ReturnValue"],
        )

        await pattern_actor.call.K2_SetActorRotation(
            ue4api.session, NewRotation={"Yaw": 0, "Pitch": 0, "Roll": 300}, bTeleport=True
        )

        print(
            "New rotation:",
            (await pattern_actor.call.K2_GetActorRotation(ue4api.session))["ReturnValue"],
        )
        await ue4api.session.close()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
