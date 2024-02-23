# SODA.Sim Remote Control

The SODA.Sim approach for remote control of the simulator involves the use of the standard UnrealEngine [Remote Control](https://docs.unrealengine.com/5.3/en-US/remote-control-for-unreal-engine/) plugin. To make sure that Remote Control plugin is connected to your UnrealEngine project, see [Quick Start](https://docs.unrealengine.com/5.3/en-US/remote-control-api-websocket-reference-for-unreal-engine/).
This repository is just an HTTP Python client for [Remote Control](https://docs.unrealengine.com/5.3/en-US/remote-control-for-unreal-engine/) implementing [Remote Control API HTTP](https://docs.unrealengine.com/5.3/en-US/remote-control-api-http-reference-for-unreal-engine/) and several convenient classes for quickly starting to work with SODA.Sim through this protocol.

> [!IMPORTANT]  
> If you are using a packaged UnrealEngine project (i.e. without an editor), then to use the Remote Control server you need to run the UnrealEngine project with the **-RCWebControlEnable** flag.

## Pythin API Overview  
Base classes:
  - ``UE4API`` 
  - ``UObject``
  - ``ArrivalVehicle``
  - ``Simulator``
  
### UE4API Class 
The UE4API is a implementation of the [Remote Control API HTTP](https://docs.unrealengine.com/5.3/en-US/remote-control-api-http-reference-for-unreal-engine/) protocol based on the aiohttp library. This is a simple and small class that simply implements all the endpoints according to the protocol:
  - ``UE4API.req_object_call(...)``
  - ``UE4API.req_object_property(...)``
  - ``UE4API.req_search_assets(...)``
  - ``UE4API.req_object_describe(...)``
  - ``UE4API.req_remote_batch(...)`` 

> [!TIP]
> There is a ability to print HTTP requests JSON content for debugging. To do this, set the appropriateoptions of UE4API:
>   - ``UE4API.print_request``
>   - ``UE4API.print_response``

### UObject Class
The python UObject is reflection of the UnrealEngine C++/Blueprint UObject. Allows to read and write properties and call methods of the origin UnrealEngine UObject:
  - To call the UObject method use the ``UObject.call`` property;  
    Example: ``await some_obj.call.TestMethod(session, param1=param1, param2=param2)``;  
  - To read the UObject property use the ``UObject.getter property``;  
    Example: ``test_property = await some_obj.setter.TestProperty(session)``;  
  - To write the UObject property use the ``UObject.setter`` property;  
    Example: ``await some_obj.getter.TestProperty(session, some_value)``;  

### SodaVehicle Class
It based on UObject class and contains several helper and most commonly used methods:
  - ``SodaVehicle.respawn(...)``
  - ``SodaVehicle.respawn_from_class(...)``
  - ``SodaVehicle.respawn_from_slot(...)``
  - ``SodaVehicle.set_position(...)``
  - ``SodaVehicle.get_component_by_class(...)``
  - ``SodaVehicle.get_component_by_name(...)``
  - ``SodaVehicle.get_components_by_class(...)``
  - ...

### Simulator Class
It is a simply container for the most commonly used dynamic and static classes. It also includes a small set of method that are most commonly used: ``open_level()``, ``reset_level()``, etc... 

## Examples
Typical template:
```
import asyncio

from soda_sim_remote_ctrl.Simulator import Simulator
from soda_sim_remote_ctrl.UE4API import UE4API

if __name__ == "__main__":
    ue4api = UE4API()
    sim = Simulator(ue4api)

    async def main():
        await sim.update_default_objects(ue4api.session)
        # Your code here begin
        # ...
        # Your code here end

        await ue4api.session.close()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
```

Open level "Calib":
```
import asyncio

from soda_sim_remote_ctrl.Simulator import Simulator
from soda_sim_remote_ctrl.UE4API import UE4API

if __name__ == "__main__":
    ue4api = UE4API()
    sim = Simulator(ue4api)

    async def main():
        await sim.update_default_objects(ue4api.session)
        await sim.open_level(ue4api.session, "Calib")
        await ue4api.session.close()

    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
```