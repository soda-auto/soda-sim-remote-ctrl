import asyncio
import json

from soda_sim_remote_ctrl.Simulator import Simulator
from soda_sim_remote_ctrl.UE4API import UE4API

if __name__ == "__main__":
    ue4api = UE4API()
    sim = Simulator(ue4api)

    async def main():
        await sim.update_default_objects(ue4api.session)
        print("\nLevels:", json.dumps(await sim.get_levels(ue4api.session), indent=2))
        print("\nCurrent Level:", await sim.get_current_level(ue4api.session))
        print("\Level Slots:", json.dumps(await sim.get_level_local_slots(ue4api.session), indent=2))
        
        await ue4api.session.close()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
