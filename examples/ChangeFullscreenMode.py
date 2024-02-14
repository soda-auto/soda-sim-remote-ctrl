import asyncio

from soda_sim_remote_ctrl.Simulator import Simulator
from soda_sim_remote_ctrl.UE4API import UE4API
from soda_sim_remote_ctrl.UObject.UObject import UObject

if __name__ == "__main__":
    ue4api = UE4API()
    sim = Simulator(ue4api)

    async def main():
        await sim.update_default_objects(ue4api.session)
        user_settings = UObject(
            ue4api,
            (await sim.game_user_settings.call.GetGameUserSettings(ue4api.session))[
                "ReturnValue"
            ],
        )
        await user_settings.call.SetFullscreenMode(
            ue4api.session, InFullscreenMode="WindowedFullscreen"
        )
        await user_settings.call.ApplyResolutionSettings(ue4api.session)
        await ue4api.session.close()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
