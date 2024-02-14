import asyncio

from soda_sim_remote_ctrl.Simulator import Simulator
from soda_sim_remote_ctrl.UE4API import UE4API

if __name__ == "__main__":
    ue4api = UE4API()
    sim = Simulator(ue4api)

    async def main():
        with open("VAN_test.json") as f:
            print(
                "Result:",
                await sim.soda_statics.call.UploadVehicleJSON(
                    ue4api.session, JSONStr=f.read(), VehicleName="VAN_test"
                ),
            )
            ue4api.session.close()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
