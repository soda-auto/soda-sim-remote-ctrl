import asyncio
import json

from soda_sim_remote_ctrl.Simulator import Simulator
from soda_sim_remote_ctrl.UE4API import UE4API

if __name__ == "__main__":
    ue4api = UE4API()
    sim = Simulator(ue4api)

    async def main():
        await sim.update_default_objects(ue4api.session)
        print(
            "\nVehicle classes:",
            json.dumps(await sim.get_vehicle_classes(ue4api.session), indent=2),
        )
        print(
            "\nVehicle slots:",
            json.dumps(await sim.get_vehicle_slots(ue4api.session), indent=2),
        )
        print(
            "\nVehicle component classes:",
            json.dumps(await sim.get_vehicle_component_classes(ue4api.session), indent=2),
        )
        ue4api.session.close()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
