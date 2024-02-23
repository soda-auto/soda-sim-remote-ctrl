import asyncio

from soda_sim_remote_ctrl.Simulator import Simulator
from soda_sim_remote_ctrl.UE4API import UE4API

if __name__ == "__main__":
    ue4api = UE4API()
    sim = Simulator(ue4api)

    async def main():
        await sim.update_default_objects(ue4api.session)
        active_vehicle = await sim.get_active_vehicle(ue4api.session)
        await active_vehicle.set_position(
            ue4api.session,
            {"X": -679, "Y": 537, "Z": 65},
            {"Yaw": 45, "Pitch": 0, "Roll": 0},
        )
        await ue4api.session.close()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
