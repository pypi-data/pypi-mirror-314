#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2020 Andrius Štikonas <andrius@stikonas.eu>
# SPDX-License-Identifier: LGPL-3.0-or-later
"""Enums for neohubapi."""

import enum

ATTR_LIVE = "live"
ATTR_DEVICES = "devices"
ATTR_SYSTEM = "system"
ATTR_PROFILES = "profiles"
ATTR_PROFILES_0 = "profiles_0"
ATTR_TIMER_PROFILES = "timer_profiles"
ATTR_TIMER_PROFILES_0 = "timer_profiles_0"


class ScheduleFormat(enum.Enum):
    """Enum to specify Schedule Format.

    ZERO  - non programmable (time clocks cannot be non programmable)
    ONE   - same format every day of the week
    TWO   - 5 day / 2 day
    SEVEN - 7 day (every day different)
    """

    ZERO = "NONPROGRAMMABLE"
    ONE = "24HOURSFIXED"
    TWO = "5DAY/2DAY"
    SEVEN = "7DAY"


def schedule_format_int_to_enum(int_format):
    """Convert schedule int to enum."""
    if int_format is None:
        return None
    if int_format == 0:
        return ScheduleFormat.ZERO
    if int_format == 1:
        return ScheduleFormat.ONE
    if int_format == 2:
        return ScheduleFormat.TWO
    if int_format == 4:
        return ScheduleFormat.SEVEN
    raise ValueError("Unrecognized ScheduleFormat")


class Weekday(enum.Enum):
    """Weekdays."""

    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"


class HCMode(enum.Enum):
    """Modes for HC devices."""

    AUTO = "AUTO"
    COOLING = "COOLING"
    HEATING = "HEATING"
    VENT = "VENT"
