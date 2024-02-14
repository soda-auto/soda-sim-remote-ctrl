import asyncio

from soda_sim_remote_ctrl.Simulator import Simulator
from soda_sim_remote_ctrl.UE4API import UE4API

if __name__ == "__main__":
    ue4api = UE4API()
    sim = Simulator(ue4api)

    async def main():
        await sim.update_default_objects(ue4api.session)
        active_vehicle = await sim.get_active_vehicle(ue4api.session)
        component_by_name = await active_vehicle.get_component_by_name(
            ue4api.session, object_name="SimCamera90Front"
        )
        await component_by_name.call.Toggle(ue4api.session)
        ue4api.session.close()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
