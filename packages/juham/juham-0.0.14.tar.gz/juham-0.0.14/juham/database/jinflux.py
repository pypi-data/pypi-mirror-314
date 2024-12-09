from typing import Any
from typing_extensions import override
from influxdb_client_3 import InfluxDBClient3, Point
from juham.base import JDatabase


class JInflux(JDatabase):
    """Influx time series database version 3."""

    def __init__(self, name: str = "influx"):
        """Construct InfluxDB v3 client for writing and reading time series.

        Args:
            name (str, optional): Name of the object to be created. Defaults to "influx".
        """
        super().__init__(name)
        self.influx_client = InfluxDBClient3(
            host=JDatabase.host,
            token=JDatabase.token,
            org=JDatabase.org,
            database=JDatabase.database,
        )

    @override
    def write(self, point: Point) -> None:
        self.influx_client.write(record=point)

    @override
    def write_point(self, name : str, tags : dict[str, Any], fields : dict[str, Any], ts : str ) -> None:
        point : dict[str, Any] = {
            "measurement": name,
            "tags":  tags,
            "fields": fields,
            "time": ts
        }
        self.influx_client.write(record=point)
