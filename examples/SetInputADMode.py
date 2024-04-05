import asyncio

from soda_sim_remote_ctrl.Simulator import Simulator
from soda_sim_remote_ctrl.UE4API import UE4API
from soda_sim_remote_ctrl.UObject.UObject import UObject


if __name__ == "__main__":
    ue4api = UE4API()
    sim = Simulator(ue4api)

    async def main():
        await sim.update_default_objects(ue4api.session)
        active_vehicle = await sim.get_active_vehicle(ue4api.session)
        input_component = UObject(ue4api, (await active_vehicle.call.GetActiveVehicleInput(ue4api.session))["ReturnValue"])
        await input_component.setter.InputState(ue4api.session, {"InputState" : {"bADModeEnbaled" : True}})
        await ue4api.session.close()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())