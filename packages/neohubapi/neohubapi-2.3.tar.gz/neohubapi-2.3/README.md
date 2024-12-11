<!--
    SPDX-FileCopyrightText: 2020 Andrius Štikonas <andrius@stikonas.eu>
    SPDX-License-Identifier: CC-BY-4.0
-->

# NeoHubAPI

This is a simple python wrapper around Heatmiser's Neohub API. Up-to-date
documentation for the API can be obtained from the [Heatmiser Developer
Portal](https://dev.heatmiser.com). You will need to sign up for a free account.

The primary purpose of this module is to help with [Home
Assistant](https://www.home-assistant.io) integration but it can also be used as
a standalone library for other projects.

## Connection methods

The API provides two connection methods. The so-called "legacy" method is by way of an unencrypted connection to port 4242 of the Neohub. The newer method uses an encrypted websocket on port 4243, but only works on a second generation hub (look for the sticker on the back).

To use the websocket connection, you need to obtain a token from the Heatmiser Neo app. Go to `Settings > API > +` in the app and create one.

On newer hubs, the legacy connection may be disabled by default. If you want to use it, go to `Settings > API` in the app, and enable it from there.

## Usage example

```python
import asyncio
import neohubapi.neohub as neohub


async def run():
    # Legacy connection
    hub = neohub.NeoHub()
    # Or, for a websocket connection:
    # hub = neohub.Neohub(port=4243, token='xxx-xxxxxxx')
    system = await hub.get_system()
    hub_data = await hub.get_devices_data()
    devices = hub_data['neo_devices']
    for device in devices:
        print(f"Temperature in zone {device.name}: {device.temperature}")
        await device.identify()


asyncio.run(run())
```

## neohub_cli.py

This package includes a CLI for performing common tasks.

```
$ neohub_cli.py help  # Shows all commands
$ neohub_cli.py help set_time  # Displays help for the set_time function
$ neohub_cli.py --hub_ip=myneohub set_time "2021-01-31 15:43:00"  # Specify times like this
$ neohub_cli.py --hub_ip=myneohub set_lock 1234 "Living Room"  # Name NeoStats like this.
$ neohub_cli.py --hub_ip=myneohub --hub_token=XXX get_system  # Get system variables with websocket connection
```
