import asyncio
import keyboard

from soda_sim_remote_ctrl.Simulator import Simulator
from soda_sim_remote_ctrl.UE4API import UE4API

if __name__ == "__main__":
    ue4api = UE4API()
    sim = Simulator(ue4api)

    async def main():
        print("Press 'q' button to exit", flush=True)
        await sim.soda_statics.call.SetSynchronousMode(
            ue4api.session, bEnable=True, DeltaSeconds=0.003
        )
        while not keyboard.is_pressed("q"):
            print(await sim.soda_statics.call.SynchTick(ue4api.session), flush=True)
        await sim.soda_statics.call.SetSynchronousMode(
            ue4api.session, bEnable=False, DeltaSeconds=0.003
        )
        ue4api.session.close()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
