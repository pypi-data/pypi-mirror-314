"""Module providing database models for influxdb."""

import datetime
import enum
from typing import Literal, Tuple
import typing

import influxdb_client
import influxdb_client.client
import influxdb_client.client.write.point
import influxdb_client.client.write_api
import influxdb_client.domain
import pydantic


class Alarm(enum.Enum):
    """Enumerate the toshiba alarm flags."""

    NO_ALARM = 0
    ALARM_OVER_CURRENT = 1 << 0
    ALARM_INVERTER_OVERLOAD = 1 << 1
    ALARM_MOTOR_OVERLOAD = 1 << 2
    ALARM_OVERHEAT = 1 << 3
    ALARM_OVER_VOLTAGE = 1 << 4
    ALARM_UNDER_VOLTAGE = 1 << 5
    ALARM_MAIN_OVERLOAD = 1 << 6
    ALARM_LOW_CURRENT = 1 << 7
    ALARM_OVER_TORQUE = 1 << 8
    ALARM_BRAKE_OVERLOAD = 1 << 9
    ALARM_OPERATION_HOURS = 1 << 10
    ALARM_OPTION_COMMUNICATION = 1 << 11
    ALARM_SERIAL_COMMUNICATION = 1 << 12
    ALARM_MAIN_VOLTAGE = 1 << 13


SupportedType = Literal[
    "bga",
    "compressor",
    "ecodry",
    "flow",
    "heater",
    "inverter",
    "loop",
    "pressure",
    "pump",
    "thermometer",
    "trap",
    "turbo",
    "valve",
]

SUPPORTED_TYPES: Tuple[SupportedType, ...] = typing.get_args(SupportedType)


class Model(pydantic.BaseModel):
    """Generic db model for influxdb data entries."""

    _type: str
    _tag: str

    # Name should not be dumped.
    name: str = pydantic.Field(exclude=True)

    def as_point(self, time: datetime.datetime):
        """Return the model represented as an influxdb Point."""
        point = influxdb_client.client.write.point.Point(measurement_name=self._type)
        point.time(time)
        point.tag(self._tag, self.name)

        for key, value in self.model_dump().items():
            if isinstance(value, enum.Enum):
                point.field(key, value.name)
            else:
                point.field(key, value)

        return point


class Thermometer(Model):
    """Model for thermometer sensor devices."""

    _type: str = "thermometer"
    _tag: str = "sensor"
    temperature: float
    resistance: float
    quadrature: float
    power: float


class Pressure(Model):
    """Model for pressure gauge devices."""

    _type: str = "pressure"
    _tag: str = "sensor"
    pressure: float


class Bga(Model):
    """Model for bga devices."""

    _type: str = "bga"
    _tag: str = "sensor"
    percent: float


class Flow(Model):
    """Model for Turbo devices.

    This model is designed to support Flowmeter devices using the lib/alicat interface.
    """

    _type: str = "flow"
    _tag: str = "sensor"
    pressure: float
    temperature: float
    volumetric_flow: float
    mass_flow: float


class Valve(Model):
    """Model for valve device."""

    _type: str = "valve"
    _tag: str = "device"
    open: bool


class Trap(Model):
    """Model for trap devices with pwm output."""

    _type: str = "trap"
    _tag: str = "device"
    output: float


class Pump(Model):
    """Model for on/off pump devices."""

    _type: str = "pump"
    _tag: str = "device"
    active: bool


class Heater(Model):
    """Model for heater devices."""

    _type: str = "heater"
    _tag: str = "device"
    power: float
    current: float
    voltage: float
    native: float


class Loop(Model):
    """Model for loop devices.

    This model is designed to support interfaces for Lakeshore PID loops.
    """

    _type: str = "loop"
    _tag: str = "device"
    setpoint: float
    gain: float
    integral: float
    derivative: float
    ramp_rate: float
    state: bool


class Turbo(Model):
    """Model for Turbo devices.

    This model is designed to support Turbo devices using the lib/turbovac interface.
    """

    _type: str = "turbo"
    _tag: str = "device"
    state: bool
    speed: int
    converter: int
    motor: int
    bearing: int
    setpoint: int
    voltage: int
    error: bool


class Ecodry(Model):
    """Model for Ecodry devices.

    This model is designed to support Turbo devices using the lib/ecodry interface.
    """

    _type: str = "ecodry"
    _tag: str = "device"
    setpoint: float
    frequency: float
    current: float
    voltage: float
    bus_voltage: float
    power: float
    state: bool


class Inverter(Model):
    """Model for Inverter devices.

    This model is designed to support Turbo devices using the lib/inverter interface.
    """

    _type: str = "inverter"
    _tag: str = "device"
    state: bool
    frequency: float
    current: float
    voltage: float
    alarm: Alarm


class Compressor(Model):
    """Model for Compressor devices.

    This model is designed to support Turbo devices using the lib/f70 interface.
    """

    _type: str = "compressor"
    _tag: str = "device"
    state: bool
    discharge_temperature: float
    outlet_temperature: float
    inlet_temperature: float
    return_pressure: float
