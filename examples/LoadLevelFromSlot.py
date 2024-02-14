import asyncio

from soda_sim_remote_ctrl.Simulator import Simulator
from soda_sim_remote_ctrl.UE4API import UE4API

if __name__ == "__main__":
    ue4api = UE4API()
    sim = Simulator(ue4api)

    async def main():
        await sim.update_default_objects(ue4api.session)

        ret = (await sim.open_level_from_local_slot_by_desc(ue4api.session, "Sample Vehicles"))
        
        print(ret)
        
        await ue4api.session.close()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
