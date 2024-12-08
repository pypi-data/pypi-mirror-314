# Python Elmax API client

![Elmax Logo](docs/elmax-logo.png?raw=true "Elmax Logo")

Asynchronous Python API client for interacting with the Elmax Cloud services, via HTTP apis.

![Release Build Status](https://github.com/albertogeniola/elmax-api/workflows/Release/badge.svg?branch=main)
![Testing Status](https://github.com/albertogeniola/elmax-api/workflows/Testing/badge.svg?branch=main)
![Documentation](https://github.com/albertogeniola/elmax-api/workflows/Publish%20Documentation/badge.svg?branch=main)

## Installation

Use the package manager pip to install Python Elmax API client:

```bash
$ pip3 install elmax-api --user
```

or, to install it globally, use the following command

```bash
$ pip3 install elmax-api
```

## Usage

```python
import asyncio

from elmax_api.http import Elmax
from elmax_api.model.command import SwitchCommand

MY_USERNAME = 'TYPE_HERE_YOUR_ELMAX_EMAIL'
MY_PASSWORD = 'TYPE_HERE_YOUR_ELMAX_PASSWORD'


async def main():
    # Instantiate the Elmax API client
    client = Elmax(username=MY_USERNAME, password=MY_PASSWORD)

    # List panels for your user
    panels = await client.list_control_panels()
    print(f"Found {len(panels)} panels for user {client.get_authenticated_username()}")

    # Get online panels only
    online_panels = []
    for p in panels:
        status = 'ONLINE' if p.online else 'OFFLINE'
        print(f"+ {p.hash}: {status}")
        if p.online:
            online_panels.append(p)

    if len(online_panels) == 0:
        print("Sorry, no panel to work with. Exiting.")
        exit(0)

    # Fetch status of first panel
    p = online_panels[0]
    panel_status = await client.get_panel_status(control_panel_id=p.hash)

    # Print some zone status
    for z in panel_status.zones:
        print(f"Zone '{z.name}' open: {z.opened}")

    # Toggle some actuator
    actuator = panel_status.actuators[0]
    old_status = actuator.opened
    print(f"Actuator {actuator.name} was {'ON' if old_status else 'OFF'}")
    print(f"Switching {'OFF' if old_status else 'ON'} actuator {actuator.name}")
    await client.execute_command(endpoint_id=actuator.endpoint_id, command=SwitchCommand.TURN_ON if not old_status else SwitchCommand.TURN_OFF)

    print("Waiting a bit...")
    await asyncio.sleep(5)

    print("Reverting back original actuator status")
    await client.execute_command(endpoint_id=actuator.endpoint_id,
                                 command=SwitchCommand.TURN_ON if old_status else SwitchCommand.TURN_OFF)
    print("Done!")

if __name__ == '__main__':
    asyncio.run(main())
```

## Documentation
Full API documentation is available on GitHub pages, [here](https://albertogeniola.github.io/elmax-api/).