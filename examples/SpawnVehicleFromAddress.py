import asyncio

from soda_sim_remote_ctrl.Simulator import *
from soda_sim_remote_ctrl.UE4API import *

if __name__ == "__main__":
    ue4api = UE4API()
    sim = Simulator(ue4api)

    async def main():
        await sim.update_default_objects(ue4api.session)
        await sim.spawn_vehicle(
            ue4api.session, 
            FVechicleSaveAddress("JsonLocal", "123"),
            FVector(500, 0, 50)
        )
        await ue4api.session.close()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
