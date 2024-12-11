# SPDX-FileCopyrightText: 2020-2021 Andrius Štikonas <andrius@stikonas.eu>
# SPDX-FileCopyrightText: 2021 Dave O'Connor <daveoc@google.com>
# SPDX-License-Identifier: LGPL-3.0-or-later
"""NeoHub main class."""

import asyncio
import datetime
import json
import logging
import socket
import ssl
from types import SimpleNamespace

from async_property import async_cached_property
import websockets

from .enums import (
    ATTR_DEVICES,
    ATTR_LIVE,
    ATTR_PROFILES,
    ATTR_PROFILES_0,
    ATTR_SYSTEM,
    ATTR_TIMER_PROFILES,
    ATTR_TIMER_PROFILES_0,
    HCMode,
    ScheduleFormat,
    schedule_format_int_to_enum,
)
from .neostat import NeoStat


class Error(Exception):
    """Generic NeoHubApi error."""


class NeoHubUsageError(Error):
    """NeoHubApi usage error."""


class NeoHubConnectionError(Error):
    """NeoHubApi connection error."""


class NeoHub:
    """Class representing NeoHub."""

    _logger = logging.getLogger("neohub")

    def __init__(
        self,
        host="Neo-Hub",
        port=4242,
        request_timeout=60,
        request_attempts=1,
        token=None,
    ):
        """Initialize NeoHub."""
        self._host = host
        self._port = int(port)
        self._request_timeout = request_timeout
        self._request_attempts = request_attempts
        self._token = token
        # Sanity checks.
        if port not in (4242, 4243):
            raise NeoHubConnectionError(
                f"Invalid port number ({port}): use 4242 or 4243 instead"
            )
        if port == 4243 and token is None:
            raise NeoHubConnectionError(
                "You must provide a token for a connection on port 4243, or use a legacy connection on port 4242"
            )
        if port == 4242 and token is not None:
            raise NeoHubConnectionError(
                "You have provided a token, so you must use port=4243"
            )
        self._websocket = None
        self._update_timestamps = {
            "TIMESTAMP_DEVICE_LISTS": 0,
            "TIMESTAMP_ENGINEERS": 0,
            "TIMESTAMP_PROFILE_0": 0,
            "TIMESTAMP_PROFILE_COMFORT_LEVELS": 0,
            "TIMESTAMP_PROFILE_TIMERS": 0,
            "TIMESTAMP_PROFILE_TIMERS_0": 0,
            "TIMESTAMP_RECIPES": 0,
            "TIMESTAMP_SYSTEM": 0,
        }
        self._eng_hub_data = None
        self._system_data = None
        self._profiles = None
        self._timer_profiles = None
        self._profiles_0 = None
        self._timer_profiles_0 = None
        self._profile_names = None
        self._device_sns = None

    async def _send_message(
        self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter, message: str
    ):
        encoded_message = bytearray(json.dumps(message) + "\0\r", "utf-8")
        self._logger.debug("Sending message: %s", encoded_message)
        writer.write(encoded_message)
        await writer.drain()

        data = await reader.readuntil(b"\0")

        writer.close()
        await writer.wait_closed()

        return data.strip(b"\0")

    async def _send(self, message, expected_reply=None):
        last_exception = None
        writer = None
        for attempt in range(1, self._request_attempts + 1):
            try:
                if self._token is not None:
                    # Websocket connection on port 4243, introduced in v3 of the API on 12/12/21
                    if self._websocket is None or self._websocket.closed:
                        # The hub uses a locally generated certificate, so
                        # we must disable hostname checking
                        context = ssl.SSLContext(check_hostname=False)
                        uri = f"wss://{self._host}:{self._port}"
                        self._websocket = await websockets.connect(
                            uri, ssl=context, open_timeout=self._request_timeout
                        )
                        self._logger.debug("Websocket connected")
                    # The message format includes json nested within json nested within json!
                    # All that appears to matter is the toker and the command
                    encoded_message = (
                        r"""{"message_type":"hm_get_command_queue","message":"{\"token\":\""""
                        + self._token
                        + r"""\",\"COMMANDS\":[{\"COMMAND\":\""""
                        + str(message)
                        + r"""\",\"COMMANDID\":1}]}"}"""
                    )
                    self._logger.debug("Sending message: %s", encoded_message)
                    await self._websocket.send(encoded_message)
                    # There appears to be no obvious way to detect an invalid token.
                    # At present, the hub just seems to forcibly close the connection
                    # with a 1002 error
                    result = await asyncio.wait_for(
                        self._websocket.recv(), timeout=self._request_timeout
                    )
                    json_string = json.loads(result)["response"]
                else:
                    # Legacy connection, on port 4242
                    self._logger.debug("Using legacy connection")
                    reader, writer = await asyncio.open_connection(
                        self._host, self._port
                    )
                    data = await asyncio.wait_for(
                        self._send_message(reader, writer, message),
                        timeout=self._request_timeout,
                    )
                    json_string = data.decode("utf-8")

                self._logger.debug("Received message: %s", json_string)
                reply = json.loads(
                    json_string, object_hook=lambda d: SimpleNamespace(**d)
                )

                if expected_reply is None:
                    return reply
                if reply.__dict__ == expected_reply:
                    return True
                self._logger.error(
                    "[%s] Unexpected reply:%s for message: %s", attempt, reply, message
                )
            except (
                socket.gaierror,
                ConnectionRefusedError,
                websockets.InvalidHandshake,
            ) as e:
                last_exception = NeoHubConnectionError(e)
                self._logger.exception(
                    "[%s] Could not connect to NeoHub at %s", attempt, self._host
                )
            except TimeoutError as e:
                last_exception = e
                self._logger.exception(
                    "[%s] Timed out while sending a message to %s", attempt, self._host
                )
                if self._websocket is not None:
                    self._websocket.close()
                if writer is not None:
                    writer.close()
            except websockets.exceptions.ConnectionClosedError as e:
                last_exception = NeoHubConnectionError(e)
                self._logger.exception(
                    "[%s] Connection forcibly closed - maybe a bad token?", attempt
                )
            except json.decoder.JSONDecodeError as e:
                last_exception = e
                self._logger.exception("[%s] Could not decode JSON"), attempt
            # Wait for 1/2 of the timeout value before retrying.
            if self._request_attempts > 1 and attempt < self._request_attempts:
                await asyncio.sleep(self._request_timeout / 2)

        if expected_reply is None and last_exception is not None:
            raise last_exception
        return False

    def _devices_to_device_ids(self, devices: [NeoStat]):
        """Return the list of device ids."""
        try:
            return [x.device_id for x in devices]
        except (TypeError, AttributeError) as err:
            raise NeoHubUsageError("devices must be a list of NeoStat objects") from err

    def _devices_to_names(self, devices: [NeoStat]):
        """Return the list of device names."""
        try:
            return [x.name for x in devices]
        except (TypeError, AttributeError) as err:
            raise NeoHubUsageError("devices must be a list of NeoStat objects") from err

    async def firmware(self):
        """NeoHub firmware version."""

        message = {"FIRMWARE": 0}

        result = await self._send(message)
        return int(getattr(result, "firmware version"))

    async def get_system(self):
        """Get system wide variables."""
        message = {"GET_SYSTEM": 0}

        data = await self._send(message)
        data.FORMAT = schedule_format_int_to_enum(data.FORMAT)
        data.ALT_TIMER_FORMAT = schedule_format_int_to_enum(data.ALT_TIMER_FORMAT)
        return data

    @async_cached_property
    async def target_temperature_step(self):
        """Return Neohub's target temperature step."""

        firmware_version = await self.firmware()
        if firmware_version >= 2135:
            return 0.5
        return 1

    async def reset(self):
        """Reboot neohub.

        Returns True if Restart is initiated
        """

        message = {"RESET": 0}
        reply = {"Restarting": 1}

        firmware_version = await self.firmware()
        if firmware_version >= 2027:
            return await self._send(message, reply)
        return False

    async def set_channel(self, channel: int):
        """Set ZigBee channel.

        Only channels 11, 14, 15, 19, 20, 24, 25 are allowed.
        """

        try:
            message = {"SET_CHANNEL": int(channel)}
        except ValueError as err:
            raise NeoHubUsageError("channel must be a number") from err

        reply = {"result": "Trying to change channel"}

        return await self._send(message, reply)

    async def set_temp_format(self, temp_format: str):
        """Set temperature format to C or F."""

        message = {"SET_TEMP_FORMAT": temp_format}
        reply = {"result": f"Temperature format set to {temp_format}"}

        return await self._send(message, reply)

    async def set_hc_mode(self, hc_mode: HCMode, devices: [NeoStat]):
        """Set hc_mode to AUTO or..."""
        names = self._devices_to_names(devices)
        message = {"SET_HC_MODE": [hc_mode.value, names]}
        reply = {"result": "HC_MODE was set"}

        return await self._send(message, reply)

    async def set_format(self, sched_format: ScheduleFormat):
        """Set schedule format.

        Format is specified using ScheduleFormat enum:
        """
        if not isinstance(sched_format, ScheduleFormat):
            raise NeoHubUsageError("sched_format must be a ScheduleFormat")

        message = {"SET_FORMAT": sched_format.value}
        reply = {"result": "Format was set"}

        return await self._send(message, reply)

    async def set_away(self, state: bool):
        """Enable away mode for all devices.

        Puts thermostats into frost mode and timeclocks are set to off.
        Instead of this function it is recommended to use frost on/off commands

        List of affected devices can be restricted using GLOBAL_DEV_LIST command
        """

        message = {"AWAY_ON" if state else "AWAY_OFF": 0}
        reply = {"result": "away on" if state else "away off"}

        return await self._send(message, reply)

    async def set_holiday(self, start: datetime.datetime, end: datetime.datetime):
        """Set holiday mode.

        start: beginning of holiday
        end: end of holiday
        """
        for datetime_arg in (start, end):
            if not isinstance(datetime_arg, datetime.datetime):
                raise NeoHubUsageError(
                    "start and end must be datetime.datetime objects"
                )

        message = {
            "HOLIDAY": [start.strftime("%H%M%S%d%m%Y"), end.strftime("%H%M%S%d%m%Y")]
        }

        return await self._send(message)

    async def get_holiday(self):
        """Get list of holidays.

        start end end times are converted to datetimes
        """
        message = {"GET_HOLIDAY": 0}

        result = await self._send(message)
        result.start = (
            datetime.datetime.strptime(result.start.strip(), "%a %b %d %H:%M:%S %Y")
            if result.start
            else None
        )
        result.end = (
            datetime.datetime.strptime(result.end.strip(), "%a %b %d %H:%M:%S %Y")
            if result.end
            else None
        )
        return result

    async def cancel_holiday(self):
        """Cancel holidays and returns to normal schedule."""

        message = {"CANCEL_HOLIDAY": 0}
        reply = {"result": "holiday cancelled"}

        return await self._send(message, reply)

    async def get_devices(self):
        """Return list of devices.

        {"result": ["device1"]}
        """

        message = {"GET_DEVICES": 0}

        return await self._send(message)

    async def get_device_list(self, zone: str):
        """Return list of devices associated with zone."""

        message = {"GET_DEVICE_LIST": zone}

        result = await self._send(message)
        if "error" in result:
            return False
        return result[zone]

    async def devices_sn(self):
        """Return serial numbers of attached devices.

        {'name': [id, 'serial', 1], ...}
        """

        message = {"DEVICES_SN": 0}

        return await self._send(message)

    async def set_ntp(self, state: bool):
        """Enable NTP client on Neohub."""

        message = {"NTP_ON" if state else "NTP_OFF": 0}
        reply = {"result": "ntp client started" if state else "ntp client stopped"}

        return await self._send(message, reply)

    async def set_date(self, date: datetime.datetime = datetime.datetime.today()):
        """Set current date.

        By default, set to current date. Can be optionally passed datetime.datetime object
        """

        message = {"SET_DATE": [date.year, date.month, date.day]}
        reply = {"result": "Date is set"}

        return await self._send(message, reply)

    async def set_time(self, time: datetime.datetime = datetime.datetime.now()):
        """Set current time.

        By default, set to current time. Can be optionally passed datetime.datetime object
        """
        message = {"SET_TIME": [time.hour, time.minute]}
        reply = {"result": "time set"}

        return await self._send(message, reply)

    async def set_datetime(
        self, date_time: datetime.datetime = datetime.datetime.now()
    ):
        """Set both date and time."""

        result = await self.set_date(date_time)
        if result:
            result = await self.set_time(date_time)
        return result

    async def manual_dst(self, state: bool):
        """Manually enables/disables daylight saving time."""

        message = {"MANUAL_DST": int(state)}
        reply = {"result": "Updated time"}

        return await self._send(message, reply)

    async def set_dst(self, state: bool, region: str | None = None):
        """Enables/disables automatic DST handling.

        By default it uses UK dates for turning DST on/off.
        Available options for region are UK, EU, NZ.
        """

        message = {"DST_ON" if state else "DST_OFF": 0 if region is None else region}
        reply = {"result": "dst on" if state else "dst off"}

        valid_timezones = ["UK", "EU", "NZ"]
        if state and region not in valid_timezones:
            raise NeoHubUsageError(f"region must be in {valid_timezones}")

        return await self._send(message, reply)

    async def set_timezone(self, tz: float):
        """Set time zone."""

        message = {"TIME_ZONE": tz}
        reply = {"result": "timezone set"}

        return await self._send(message, reply)

    async def identify(self):
        """Flashes red LED light."""

        message = {"IDENTIFY": 0}
        reply = {"result": "flashing led"}

        return await self._send(message, reply)

    async def get_live_data(self):
        """Return live data from hub and all devices."""

        message = {"GET_LIVE_DATA": 0}
        return await self._send(message)

    async def permit_join(self, name, timeout_s: int = 120):
        """Permit new thermostat to join network.

        name: new zone will be added with this name
        timeout: duration of discovery mode in seconds

        To actually join network you need to select 01
        from the thermostat's setup menu.
        """

        message = {"PERMIT_JOIN": [timeout_s, name]}
        reply = {"result": "network allows joining"}

        return await self._send(message, reply)

    async def permit_repeater_join(self, timeout_s: int = 120):
        """Permit new repeaters to join network."""

        message = {"PERMIT_JOIN": ["repeater", timeout_s]}

        return await self._send(message)

    async def remove_repeater(self, repeater_name: str):
        """Handle repeater removal."""
        message = {"REMOVE_REPEATER": repeater_name}

        return await self._send(message)

    async def set_lock(self, pin: int, devices: [NeoStat]):
        """PIN locks thermostats.

        PIN is a four digit number
        """

        try:
            if pin < 0 or pin > 9999:
                return False
        except TypeError as err:
            raise NeoHubUsageError("pin must be a number") from err

        pins = []
        for _ in range(4):
            pins.append(pin % 10)
            pin = pin // 10
        pins.reverse()

        names = self._devices_to_names(devices)
        message = {"LOCK": [pins, names]}
        reply = {"result": "locked"}

        return await self._send(message, reply)

    async def unlock(self, devices: [NeoStat]):
        """Unlock PIN locked thermostats."""

        names = self._devices_to_names(devices)
        message = {"UNLOCK": names}
        reply = {"result": "unlocked"}

        return await self._send(message, reply)

    async def set_frost(self, state: bool, devices: [NeoStat]):
        """Enable or disable Frost mode."""

        names = self._devices_to_names(devices)
        message = {"FROST_ON" if state else "FROST_OFF": names}
        reply = {"result": "frost on" if state else "frost off"}

        return await self._send(message, reply)

    async def set_frost_temp(self, temperature: float, devices: [NeoStat]):
        """Set frost temperature."""

        names = self._devices_to_names(devices)
        message = {"SET_FROST": [temperature, names]}
        reply = {"result": "temperature was set"}

        result = await self._send(message, reply)
        self._update_timestamps["TIMESTAMP_ENGINEERS"] = 0
        return result

    async def set_cool_temp(self, temperature: int, devices: [NeoStat]):
        """Set the thermostat's cooling temperature.

        i.e. the temperature that will
        trigger the thermostat if exceeded. Note that this is only supported on
        the HC (Heating/Cooling) thermostats.

        The temperature will be reset once next comfort level is reached
        """

        names = self._devices_to_names(devices)
        message = {"SET_COOL_TEMP": [temperature, names]}
        reply = {"result": "temperature was set"}

        return await self._send(message, reply)

    async def set_target_temperature(self, temperature: int, devices: [NeoStat]):
        """Set the thermostat's temperature.

        The temperature will be reset once next comfort level is reached
        """

        names = self._devices_to_names(devices)
        message = {"SET_TEMP": [temperature, names]}
        reply = {"result": "temperature was set"}

        return await self._send(message, reply)

    async def set_diff(self, switching_differential: int, devices: [NeoStat]):
        """Set the thermostat's switching differential.

        -1: Undocumented option. Seems to set differential to 204.
        0: 0.5 degrees
        1: 1 degree
        2: 2 degrees
        3: 3 degrees
        """

        names = self._devices_to_names(devices)
        message = {"SET_DIFF": [switching_differential, names]}
        reply = {"result": "switching differential was set"}

        result = await self._send(message, reply)
        self._update_timestamps["TIMESTAMP_ENGINEERS"] = 0
        return result

    async def set_output_delay(self, output_delay: int, devices: [NeoStat]):
        """Set the thermostat's output delay."""

        names = self._devices_to_names(devices)
        message = {"SET_DELAY": [output_delay, names]}
        reply = {"result": "delay was set"}

        result = await self._send(message, reply)
        self._update_timestamps["TIMESTAMP_ENGINEERS"] = 0
        return result

    async def set_floor_limit(self, floor_limit: int, devices: [NeoStat]):
        """Set the thermostat's floor limit temperature."""

        names = self._devices_to_names(devices)
        message = {"SET_FLOOR": [floor_limit, names]}
        # reply = {"result": "floor limit was set"}

        result = await self._send(message)
        self._update_timestamps["TIMESTAMP_ENGINEERS"] = 0
        return result

    async def set_preheat(self, preheat_period: int, devices: [NeoStat]):
        """Set the thermostat's preheat period."""

        names = self._devices_to_names(devices)
        message = {"SET_PREHEAT": [preheat_period, names]}
        reply = {"result": "max preheat was set"}

        result = await self._send(message, reply)
        self._update_timestamps["TIMESTAMP_ENGINEERS"] = 0
        return result

    async def set_fan_speed(self, fan_speed: str, devices: [NeoStat]):
        """Set the thermostat's fan speed (NeoStat HC)."""

        names = self._devices_to_names(devices)
        message = {"SET_FAN_SPEED": [fan_speed, names]}
        # reply = {"result": "fan speed was set"}

        return await self._send(message)

    async def rate_of_change(self, devices: [NeoStat]):
        """Return time in minutes required to change temperature by 1 degree."""

        names = self._devices_to_names(devices)
        message = {"VIEW_ROC": names}

        result = await self._send(message)
        return result.__dict__

    async def set_timer(self, state: bool, devices: [NeoStat]):
        """Turn the output of timeclock on or off.

        This function works only with NeoPlugs and does not work on
        NeoStats that are in timeclock mode.
        """

        names = self._devices_to_names(devices)
        message = {"TIMER_ON" if state else "TIMER_OFF": names}
        reply = {"result": "timers on" if state else "timers off"}

        return await self._send(message, reply)

    async def set_manual(self, state: bool, devices: [NeoStat]):
        """Control NeoPlug manual mode.

        Controls the timeclock built into the neoplug, can be enabled and disabled to allow for manual operation.
        This function works only with NeoPlugs and does not work on NeoStats that are in timeclock mode.
        """

        names = self._devices_to_names(devices)
        message = {"MANUAL_ON" if state else "MANUAL_OFF": names}
        reply = {"result": "manual on" if state else "manual off"}

        return await self._send(message, reply)

    async def set_hold(
        self, temperature: int, hours: int, minutes: int, devices: [NeoStat]
    ):
        """Tells a thermostat to maintain the current temperature for a fixed time."""

        names = self._devices_to_names(devices)
        ids = self._devices_to_device_ids(devices)
        message = {
            "HOLD": [
                {
                    "temp": temperature,
                    "hours": hours,
                    "minutes": minutes,
                    "id": f"{ids}",
                },
                names,
            ]
        }
        reply = {"result": "temperature on hold"}

        return await self._send(message, reply)

    async def set_timer_hold(self, state: bool, minutes: int, devices: [NeoStat]):
        """Turn the output of timeclock on or off for certain duration.

        This function works with NeoStats in timeclock mode
        """

        names = self._devices_to_names(devices)
        message = {"TIMER_HOLD_ON" if state else "TIMER_HOLD_OFF": [minutes, names]}
        reply = {"result": "timer hold on" if state else "timer hold off"}

        return await self._send(message, reply)

    async def set_profile_id(self, profile_id: int, devices: [NeoStat]):
        """Set the profile id on a device."""

        names = self._devices_to_names(devices)

        message = {"RUN_PROFILE_ID": [profile_id, names]}
        reply = {"result": "profile was run"}

        return await self._send(message, reply)

    async def clear_profile_id(self, devices: [NeoStat]):
        """Set the profile id on a device."""

        names = self._devices_to_names(devices)

        message = {"CLEAR_CURRENT_PROFILE": names}
        reply = {"result": "Profile ID cleared"}

        return await self._send(message, reply)

    async def get_engineers(self):
        """Get engineers data."""
        message = {"GET_ENGINEERS": 0}

        return await self._send(message)

    async def get_profiles(self):
        """Get profiles."""

        message = {"GET_PROFILES": 0}

        return await self._send(message)

    async def get_profile_names(self):
        """Get profile names."""

        message = {"GET_PROFILE_NAMES": 0}

        return await self._send(message)

    async def get_timer_profiles(self):
        """Get timer profiles."""
        message = {"GET_PROFILE_TIMERS": 0}

        return await self._send(message)

    async def get_profile_0(self, device_name: str):
        """Get profile 0 from a device."""

        message = {"GET_PROFILE_0": device_name}

        return await self._send(message)

    async def get_timer_profile_0(self, device_name: str):
        """Get timer profile 0 from a device."""

        message = {"GET_TIMER_0": device_name}

        return await self._send(message)

    async def get_devices_data(self):
        """Return live data from hub and all devices."""

        # Get live data from Neohub
        live_hub_data = await self.get_live_data()

        # Get the engineers data from the Neohub for things like Device Type, Sensor Mode etc.
        eng_hub_data = await self.get_engineers()

        # Remove the devices node from the hub_data.
        devices = live_hub_data.devices
        delattr(live_hub_data, "devices")

        neo_devices = []  # Initialize the list to hold NeoStat devices

        for device in devices:
            # Find matching device ID in Engineers data
            for engineers_data_value in eng_hub_data.__dict__.values():
                # Check if there is a DEVICE_ID first (some devices may not have one, e.g. repeaters)
                device_id = getattr(device, "DEVICE_ID", None)
                engineer_device_id = getattr(engineers_data_value, "DEVICE_ID", None)

                if device_id is None or engineer_device_id is None:
                    self._logger.debug(
                        "Ignoring device '%s', which has no ID and might be a repeater.",
                        device.device,
                    )
                elif device_id == engineer_device_id:
                    for x in engineers_data_value.__dict__.items():
                        # Don't overwrite FLOOR_LIMIT, instead set ENG_FLOOR_LIMIT
                        if x[0] == "FLOOR_LIMIT":
                            setattr(device, "ENG_FLOOR_LIMIT", x[1])
                        else:
                            setattr(device, x[0], x[1])

            # Only append devices with a valid device_id
            device_id = getattr(device, "DEVICE_ID", None)
            if device_id is not None:
                neo_devices.append(NeoStat(self, device))

        # Prepare the final devices dictionary, excluding those without a valid device ID
        return {"neo_devices": neo_devices}

    async def get_all_live_data(self):
        """Return live data from hub and all devices."""

        # Get live data from Neohub
        live_hub_data = await self.get_live_data()

        # Remove the devices node from the hub_data.
        devices = live_hub_data.devices
        delattr(live_hub_data, "devices")

        keys_to_update = [
            k
            for k, v in self._update_timestamps.items()
            if getattr(live_hub_data, k, 0) != v
        ]

        profiles_updated = False
        timer_profiles_updated = False

        for k in keys_to_update:
            if k == "TIMESTAMP_ENGINEERS":
                eng_result = await self.get_engineers()
                self._update_timestamps[k] = getattr(live_hub_data, k, 0)
                self._eng_hub_data = {
                    getattr(device, "DEVICE_ID", None): device
                    for _, device in eng_result.__dict__.items()
                }

            if k == "TIMESTAMP_SYSTEM":
                system_result = await self.get_system()
                self._update_timestamps[k] = getattr(live_hub_data, k, 0)
                self._system_data = system_result

            if k in ("TIMESTAMP_PROFILE_0", "TIMESTAMP_PROFILE_COMFORT_LEVELS"):
                if not profiles_updated:
                    profiles_result = await self.get_profiles()
                    self._profiles = profiles_result
                    self._profiles = {
                        getattr(profile, "PROFILE_ID", None): profile
                        for _, profile in profiles_result.__dict__.items()
                    }
                    self._profiles_0 = {
                        getattr(device, "DEVICE_ID", None): await self.get_profile_0(
                            getattr(device, "ZONE_NAME", None)
                        )
                        for device in devices
                        if hasattr(device, "THERMOSTAT")
                        and getattr(device, "ACTIVE_PROFILE", None) == 0
                    }
                    profiles_updated = True
                self._update_timestamps[k] = getattr(live_hub_data, k, 0)

            if k in ("TIMESTAMP_PROFILE_TIMERS_0", "TIMESTAMP_PROFILE_TIMERS"):
                if not timer_profiles_updated:
                    timer_profiles_result = await self.get_timer_profiles()
                    self._timer_profiles = {
                        getattr(profile, "PROFILE_ID", None): profile
                        for _, profile in timer_profiles_result.__dict__.items()
                    }
                    self._timer_profiles_0 = {
                        getattr(
                            device, "DEVICE_ID", None
                        ): await self.get_timer_profile_0(
                            getattr(device, "ZONE_NAME", None)
                        )
                        for device in devices
                        if hasattr(device, "TIMECLOCK")
                        and getattr(device, "ACTIVE_PROFILE", None) == 0
                    }
                    timer_profiles_updated = True
                self._update_timestamps[k] = getattr(live_hub_data, k, 0)

            if k == "TIMESTAMP_DEVICE_LISTS":
                device_serial_numbers = await self.devices_sn()
                self._logger.debug("device serial numbers: %s", device_serial_numbers)
                # Convert device_serial_numbers (SimpleNamespace) to a dictionary
                device_serial_numbers_dict = vars(device_serial_numbers)
                self._device_sns = {
                    v[0]: {"name": k, "serial_number": v[1]}
                    for (k, v) in device_serial_numbers_dict.items()
                }
                self._update_timestamps[k] = getattr(live_hub_data, k, 0)

        neo_devices = []  # Initialize the list to hold NeoStat devices

        for device in devices:
            # Check if there is a DEVICE_ID first (some devices may not have one, e.g. repeaters)
            device_id = getattr(device, "DEVICE_ID", None)
            if device_id:
                eng_device = self._eng_hub_data.get(device_id, None)
                # If any matching serials are found, assign the first one, else set to "UNKNOWN"
                serial_number = self._get_device_sn(device_id)

                # Add serial number if it doesn't already exist
                if getattr(device, "SERIAL_NUMBER", None) is None:
                    setattr(device, "SERIAL_NUMBER", serial_number)

            if eng_device:
                for k, v in eng_device.__dict__.items():
                    if k == "FLOOR_LIMIT":
                        setattr(device, "ENG_FLOOR_LIMIT", v)
                    else:
                        setattr(device, k, v)
            if not device_id:
                # repeaters don't have a device id. Use the "device" attribute and set the device type
                repeater_name = getattr(device, "device", None)
                if repeater_name.startswith("repeaternode"):
                    setattr(device, "DEVICE_ID", repeater_name)
                    if getattr(device, "DEVICE_TYPE", None) is None:
                        setattr(device, "DEVICE_TYPE", 10)
                    if getattr(device, "SERIAL_NUMBER", None) is None:
                        setattr(device, "SERIAL_NUMBER", repeater_name)

            device_id = getattr(device, "DEVICE_ID", None)
            if device_id:
                neo_devices.append(NeoStat(self, device))

        return {
            ATTR_LIVE: live_hub_data,
            ATTR_DEVICES: neo_devices,
            ATTR_SYSTEM: self._system_data,
            ATTR_PROFILES: self._profiles,
            ATTR_PROFILES_0: self._profiles_0,
            ATTR_TIMER_PROFILES: self._timer_profiles,
            ATTR_TIMER_PROFILES_0: self._timer_profiles_0,
        }

    def _get_device_sn(self, device_id: int) -> str:
        """Get a device serial number by its device id."""

        return self._device_sns.get(device_id, {}).get("serial_number", "UNKNOWN")
