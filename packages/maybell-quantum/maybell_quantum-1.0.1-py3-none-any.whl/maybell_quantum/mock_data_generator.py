# pylint: disable=invalid-name
import builtins
import datetime
import enum
import logging
import random
import string
import time
from typing import Any, Type

import influxdb_client.client.influxdb_client
import influxdb_client.client.write.point
import influxdb_client.client.write_api
import pydantic

from maybell_quantum import models


def get_random_of_type(target_type: Type[Any]) -> Any:
    """Return a random value of type: target_type.

    Supported types are:
        str,
        int,
        float,
        bool
        Enum

    Unions of supported types are also allowed.

    In the case of a union of types, a random valid type in the union is used.

    Args:
        target_type:
            The type of the random value to return.

    """
    match target_type:
        case builtins.str:
            # Generate a random string of length 6.
            return "".join(  # pragma: no cover
                random.SystemRandom().choice(string.ascii_uppercase + string.digits)
                for _ in range(6)
            )
        case builtins.int:
            return random.randint(0, 100)

        case builtins.float:
            return random.random() * 100

        case builtins.bool:
            return random.random() > 0.5

        # Case for enum types
        case _ if isinstance(target_type, enum.EnumMeta):
            # Return a random value from the enum type
            return random.choice(list(target_type))

        case _:  # pragma: no cover
            raise TypeError("Unsupported Type: ", target_type)


def random_model(model: Type[pydantic.BaseModel]):
    """Populate fields with example values.

    Parses the fields of a pydantic model and generates random values for
    each field.

    Excludes the 'name' field, if it exists.

    Args:
        model: The BaseModel metaclass to generate values for.

    Returns:
        dict[str, Any]: A dictionary mapping the field names to their random values.
    """

    result: dict[str, Any] = {}

    for name, field in model.model_fields.items():
        if name != "name":
            if field.annotation is not None:
                result[name] = get_random_of_type(field.annotation)

    return dict(result)


def load_mock_data(
    token: str,
    interval: float = 10,  # units of seconds
    n_cycles: int = 100,
    bucket: str = "mock_datadb",
    url: str = "https://us-east-1-1.aws.cloud2.influxdata.com",
    org: str = "Maybell Quantum",
):
    """Generate and log random system data.

    Generates random data for a realistic set of devices, and logs the data to
    influxdb on an interval.

    The default logging interval is 10 seconds, but this can be adjusted by setting
    the 'INTERVAL' environment variable.

    The default influxdb bucket is 'datadb', but this can be changed by setting
    the "BUCKET" environment variable.

    The default influxdb url is 'http://localhost:8086', but this can be changed by
    setting the "URL" environment variable.

    The default influxdb org is 'maybell', but this can be changed by setting the
    "ORG" environment variable.

    The default influxdb username is 'admin', but this can be changed by setting
    the "USERNAME" environment variable.

    The default influxdb password is 'password', but this can be changed by
    setting the "PASSWORD" environment variable.
    """

    # Create the influxdb client used to write the random data points.
    client = influxdb_client.client.influxdb_client.InfluxDBClient(
        url=url, org=org, token=token
    )

    write_api = client.write_api(
        write_options=influxdb_client.client.write_api.SYNCHRONOUS
    )

    # Construct a set of devices to use as a mock system.
    mocks: dict[Type[models.Model], list[str]] = {}

    # Add sensors first (for no particular reason).  These are read-only components.
    mocks[models.Flow] = ["f1"]
    mocks[models.Pressure] = [f"p{ii}" for ii in range(1, 9)]
    mocks[models.Thermometer] = ["prp", "rgp", "cfp", "icp", "stp", "mxp"]

    # Now add the devices.  These are components that can accept commands.
    mocks[models.Compressor] = ["cp1", "cp2"]
    mocks[models.Heater] = ["sample", "still", "warmup"]
    mocks[models.Inverter] = ["inv1"]
    mocks[models.Ecodry] = ["pm2"]
    mocks[models.Pump] = ["pm4", "pm5"]
    mocks[models.Turbo] = ["pm1", "pm3"]
    mocks[models.Valve] = [f"v{ii}" for ii in range(1, 27)]

    counter = 0
    while counter < n_cycles:
        counter += 1
        logging.debug(f"cycle {counter}")
        points: list[influxdb_client.client.write.point.Point] = []
        current_time = datetime.datetime.now(datetime.timezone.utc)
        # pylint: disable=protected-access
        for type_, list_ in mocks.items():
            for name in list_:
                new_model = type_(name=name, **random_model(type_))
                points.append(new_model.as_point(time=current_time))

        with write_api:
            write_api.write(bucket=bucket, record=points)

        time.sleep(interval)
