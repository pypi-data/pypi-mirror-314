import json
from io import StringIO
import collections
from dataclasses import dataclass

from datetime import datetime
from datetime import timedelta
from datetime import timezone

import influxdb_client
import influxdb_client.client.flux_table


def _transform_json(
    table_flux: influxdb_client.client.flux_table.TableList,
) -> dict[str, dict[str, list[bool | str | float | int]]]:
    """Transform a JSON dictionary into a sane dictionary.

    InfluxDB transforms TableList to something that is technically JSON,
    but really isn't in a representation that's easy to deal with.

    Let's say want to pull temperature data.  The ideal and most intuitive
    structure would look something like this:
    {
        "mxp": {
            "temperature": [<value>],
            "resistence": [<values>],
            "quadrature": [<values>],
        }
    }

    This makes it trivial (and intuitive) to plot temperature data, e.g.:

        temperature = result["mxp"]["temperature"]

    :param table_flux:
    :return:
    """

    # to_json doesn't actually convert to JSON.
    # it returns a string representation of something
    # that evaluates as JSON.
    io = StringIO(table_flux.to_json())
    json_rep = json.load(io)

    result: dict[str, dict[str, list[bool | str | float | int]]] = {}

    for table in json_rep:
        component_name = table["device"] if "device" in table else table["sensor"]
        if component_name not in result:
            result[component_name] = collections.defaultdict(list)
        result[component_name][table["_field"]].append(table["_value"])
    return result


@dataclass
class TimeRange:
    """Simple class that holds start and stop times, of type datetime, for queries.

    Currently only UTC time is supported and highly recommended.  This is the best
    representation under the hood since there are no ambiguities that can arise,
    unlike time zones with daylight savings.
    """

    start_time: datetime
    stop_time: datetime


class FridgeDB:
    """Convenience wrapper around InfluxDB client.

    https://influxdb-client.readthedocs.io/en/latest/

    This class has one primary method `fetch` and a couple convenience methods:
    `fetch_all` (retrieves all devices and sensor data for the given time range)
    and `last` (retrieves data from now until the last provided timedelta).
    """

    sensor_names = [f"p{idx}" for idx in range(1, 9)]
    sensor_names.extend(["cfp", "f1", "icp", "mxp", "prp", "rgp", "stp"])

    device_names = [f"v{idx}" for idx in range(1, 27)]
    device_names.extend([f"pm{idx}" for idx in range(1, 6)])
    device_names.extend(["warmup", "still", "sample", "cp1", "cp2", "inv1"])

    def __init__(
        self,
        org: str,
        url: str,
        token: str,
        timeout: int = 1000,  # units of ms
        bucket: str = "datadb",
    ) -> None:
        """Create an instance of FridgeDB

        Args:
            org: Name of the InfluxDB org (typically "Maybell Quantum")
            url: Either 'localhost:<port>' or 'https://us-east-1-1.aws.cloud2.influxdata.com'
            token: API token provided by Maybell Quantum.
            bucket: Name of the bucket assigned to the fridge (provided by Maybell Quantum).
            timeout: Amount of time to wait making a connection to the database before failing.
        Returns:
            Instance of FridgeDB.

        Note: The bucket parameter is intentionally left publicly exposed to make it easier
              for customers with multiple fridges to switch between them in the same session.
              `self.client` is also exposed for any users who want to easily reassign the underlying
              object using Influx's API directly.
        """
        self.client = influxdb_client.InfluxDBClient(
            url=url,
            token=token,
            org=org,
            verify_ssl=True,
            timeout=timeout,
        )

        # leaving these publicly exposed since it does more good than harm
        # to allow users to change this on the fly.
        self.bucket = bucket

    def fetch(
        self, time_range: TimeRange, components: list[str]
    ) -> dict[str, dict[str, list[bool | str | float | int]]]:
        """Fetch data from InfluxDB

        :param time_range: start and stop times TimeRange(datetime, datetime)
        :param components: name of the sensor or device (e.g. "p1" for pressure gauge #1)
        :return: InfluxDB TableList converted to JSON
        """
        start_time = time_range.start_time
        stop_time = time_range.stop_time
        params = {
            "bucket_name": self.bucket,
            "start_time": start_time,
            "stop_time": stop_time,
        }

        devices = [name for name in components if name in self.device_names]
        sensors = [name for name in components if name in self.sensor_names]

        result: dict[str, dict[str, list[bool | str | float | int]]] = {}
        for component_type, component_names in [
            ("sensor", sensors),
            ("device", devices),
        ]:
            if component_names:
                query = "from(bucket: bucket_name) |> range(start: start_time, stop: stop_time)"
                query += "|> filter(fn: (r) => "
                query += " or ".join(
                    [f'r["{component_type}"] == "{name}"' for name in component_names]
                )
                query += ")"
                query_result = _transform_json(
                    self.client.query_api().query(query=query, params=params)
                )
                result.update(query_result)

        return result

    def fetch_all(
        self, time_range: TimeRange
    ) -> dict[str, dict[str, list[bool | str | float | int]]]:
        """Convenience method that could be a standalone function.

        :param time_range:
        :return: InfluxDB TableList converted to JSON
        """
        return self.fetch(time_range, self.sensor_names + self.device_names)

    def last(
        self, since: timedelta
    ) -> dict[str, dict[str, list[bool | str | float | int]]]:
        """Convenience method that could be a standalone function.

        Retrieves all the records for a specific time range, e.g.
        result = fdb.last(timedelta(years=1, months=2, weeks=3, days=4, hours=5, minutes=6)
        will fetch data between now and 1 year, 2 months, 3 weeks, 4 days, 5 hours, and 6 minutes ago.

        :param since: datetime.timedelta (e.g. datetime.timedelta(hours=1)
        :return: InfluxDB TableList converted to JSON
        """
        stop_time = datetime.now(timezone.utc)
        start_time = stop_time - since
        return self.fetch_all(TimeRange(start_time, stop_time))
