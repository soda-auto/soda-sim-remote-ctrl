import asyncio

from soda_sim_remote_ctrl.Simulator import Simulator
from soda_sim_remote_ctrl.UE4API import UE4API

if __name__ == "__main__":
    ue4api = UE4API()
    sim = Simulator(ue4api)

    async def main():
        await sim.update_default_objects(ue4api.session)

        actor = await sim.find_actor_by_name(ue4api.session, "SensorHolder_0")
        if actor:
            print("Actor was found, object path:", actor.object_path)
        else:
            print("Can't find actor")
        await ue4api.session.close()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
