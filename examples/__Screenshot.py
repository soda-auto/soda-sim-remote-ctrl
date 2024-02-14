import asyncio

from soda_sim_remote_ctrl.Simulator import Simulator
from soda_sim_remote_ctrl.UE4API import UE4API
from soda_sim_remote_ctrl.UObject.UObject import UObject

sensor_holder_name = "SensorHolder_0"

if __name__ == "__main__":
    ue4api = UE4API()
    sim = Simulator(ue4api)

    async def main():
        await sim.update_default_objects(ue4api.session)

        sensor_holder = await sim.find_actor_by_name(ue4api.session, sensor_holder_name)
        if not sensor_holder:
            print("Can't find", sensor_holder_name)
            return

        sensor_path_name = (await sensor_holder.call.GetSensor(ue4api.session))[
            "ReturnValue"
        ]

        if not sensor_path_name:
            print("Can't find a sensor in the", sensor_holder_name)
            return

        sensor = UObject(ue4api, sensor_path_name)
        await sensor.call.MakeScreenshot(
            ue4api.session, InFileName="C:\\UnrealProjects\\Test.png"
        )
        ue4api.session.close()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
