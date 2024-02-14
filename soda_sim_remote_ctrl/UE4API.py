import json

import aiohttp


class UE4API:
    def __init__(self, url="http://127.0.0.1:30010"):
        self.url = url
        self.session = aiohttp.ClientSession()
        self.print_request = False
        self.print_response = False

    async def req(self, **kwargs):
        if self.print_request:
            print(
                "----------------------Request Begin---------------------------",
                flush=True,
            )
            print(json.dumps(kwargs["body"], indent=2), flush=True)
            print(
                "-----------------------Request End----------------------------",
                flush=True,
            )
        async with self.session.put(
            self.url + "/" + kwargs["endpoint"], json=kwargs["body"]
        ) as response:
            if response.status != 200:
                print(
                    "--------------------HTTP Error Begin------------------------------",
                    flush=True,
                )
                print(
                    "HTTP Error\nStatus: ",
                    response.status,
                    "\nResponse text:",
                    await response.text(),
                    flush=True,
                )
                print(
                    "---------------------HTTP Error End-------------------------------",
                    flush=True,
                )
            response.raise_for_status()
            if self.print_response:
                print(
                    "---------------------Response Begin---------------------------",
                    flush=True,
                )
                print(await response.text(), flush=True)
                print(
                    "----------------------Response End----------------------------",
                    flush=True,
                )
            return await response.json()

    async def req_object_call(self, **kwargs):
        kwargs["endpoint"] = "remote/object/call"
        return await self.req(**kwargs)

    async def req_object_property(self, **kwargs):
        kwargs["endpoint"] = "remote/object/property"
        return await self.req(**kwargs)

    async def req_search_assets(self, **kwargs):
        kwargs["endpoint"] = "remote/search/assets"
        return await self.req(**kwargs)

    async def req_object_describe(self, **kwargs):
        kwargs["endpoint"] = "remote/object/describe"
        return await self.req(**kwargs)

    async def req_remote_batch(self, **kwargs):
        kwargs["endpoint"] = "remote/batch"
        return await self.req(**kwargs)

class FVector:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    def to_json(self):
        return {"X": self.x, "Y": self.y, "Z": self.z}
   
    
class FRotator:
    def __init__(self, pitch, yaw, roll):
        self.pitch = pitch
        self.yaw = yaw
        self.roll = roll
    def to_json(self):
        return {"Pitch": self.pitch, "Yaw": self.yaw, "Roll": self.roll}
        
class FTransform:
    def __init__(self, rotation, translation, scale3D=FVector(1, 1, 1)):
        self.rotation = rotation
        self.translation = translation
        self.scale3D = scale3D
    def to_json(self):
        return {
            "Rotation": self.rotation.to_json(), 
            "Translation": self.translation.to_json(), 
            "Scale3D": self.scale3D.to_json()} 