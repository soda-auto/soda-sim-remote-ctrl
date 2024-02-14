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
                ActorClass="/SodaSim/Markers/ArUCO_pattern_lenght_77cm.ArUCO_pattern_lenght_77cm_C",
            )
        )["OutActors"]

        # Some other classes of object for search:
        #   "/SodaSim/Markers/ArUCO_pattern_lenght_77cm.ArUCO_pattern_lenght_77cm_C"
        #   "/SodaSim/Markers/Chess_Prattern+_length_120_8cm.Chess_Prattern+_length_120_8cm_C"
        #   "/SodaSim/Markers/Circle_Pattern_step_25cm.Circle_Pattern_step_25cm_C"
        #   "/SodaSim/Markers/TwistCalib.TwistCalib_C"
        #   "/SodaSim/Pedestrians/Worker.Worker_C"
        #   "/SodaSim/Vehicles/B12/B12.B12_C"
        #   "/SodaSim/Vehicles/DevBot/DevBot.DevBot_C"
        #   "/SodaSim/Vehicles/Mustang/Mustang.Mustang_C"
        #   "/SodaSim/Vehicles/P1/P1.P1_C"
        #   "/SodaSim/Vehicles/P6/P6.P6_C"
        #   "/SodaSim/Vehicles/Robocar/Robocar.Robocar_C"
        #   "/SodaSim/Vehicles/T4/T4.T4_C"
        #   "/SodaSim/Vehicles/VANv2/VANv2.VANv2_C"
        #   "/SodaSim/Pedestrians/BoldWalker.BoldWalker_C"
        #   "/SodaSim/Vehicles/SimpleVehicle/SimpleVehicle.SimpleVehicle_C"
        #   "/SodaSim/TrafficVehicle_SpawnPoint.TrafficVehicle_SpawnPoint_C"
        #   "/SodaSim/V2VBox.V2VBox_C"

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
        ue4api.session.close()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
