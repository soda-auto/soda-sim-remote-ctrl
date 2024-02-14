import asyncio

from soda_sim_remote_ctrl.Simulator import Simulator
from soda_sim_remote_ctrl.UE4API import UE4API

if __name__ == "__main__":
    ue4api = UE4API()
    sim = Simulator(ue4api)

    async def main():
        await sim.update_default_objects(ue4api.session)
        await sim.soda_user_settings.setter.ThrottleKeyInput(
            ue4api.session, {"ThrottleKeyInput": {"KeyName": "B"}}
        )
        print(await sim.soda_user_settings.getter.ThrottleJoyInput(ue4api.session))
        await ue4api.session.close()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
