import json
import math
import time
from typing import Any, Optional, cast
from typing_extensions import override
from influxdb_client_3 import Point

from juham.base import Base
from juham.base import JMqtt, MqttMsg
from juham.base.time import epoc2utc
from juham.web.rthread import RThread, IWorkerThread


class RTrackerThread(IWorkerThread):
    """A tracker simulation thread generating and publishing geographic
    coordinates.

    """

    def __init__(self, client: Optional[JMqtt] = None) -> None:
        super().__init__(client)
        self._sensor_topic: str = ""
        self._topic: str = ""
        self._interval: float = 60
        self._lon: float = 25.63
        self._lat: float = 60.95
        self._rad: float = 3

    @override
    def update(self) -> bool:
        rc: bool = super().update()
        self.update_track(1, "fixed", 0.5, 1.0, 0, 0)
        self.update_track(2, "rotary", 0.7, 1.8, -0.9, 0)
        return rc

    def init(
        self, lon: float, lat: float, rad: float, interval: float, topic: str
    ) -> None:
        """Initialize the thread

        Args:
            lon (float): longitude coordinate
            lat (float): latitude
            rad (float): radius
            interval (float): update interval in seconds
            topic (str): Mqtt topic
        """
        self._lon = lon
        self._lat = lat
        self._rad = rad
        self._interval = interval
        self._topic = topic

    def update_track(
        self,
        id: int,
        type: str,
        radLon: float,
        radLat: float,
        offLon: float,
        offLat: float,
    ) -> None:
        epoc = time.time()
        rec = {
            "ts": epoc,
            "lon": math.sin(epoc / 360000.0) * math.sin(epoc * 0.001) * radLon
            + self._lon
            + offLon,
            "lat": 0.5 * math.cos(epoc / 360000.0) * math.sin(epoc * 0.001) * radLat
            + self._lat
            + offLat,
            "alt": math.cos(epoc / 360000.0) * (10 * id) + 100,
            "fom": math.cos(epoc / 360000.0) * (0.1 * id) * 10 + 100,
            "type": type,
            "id": str(id),
        }
        self.publish(self._topic, json.dumps(rec), qos=1, retain=False)
        self.debug("Track " + str(id) + " moved")


class RTracker(RThread):
    """A tracker automation object. Spawns async thread to generate geographic
    coordinates at specific rate, and writes them to time series database.

    Args:
        RThread (class): super class
    """

    workerThreadId = RTrackerThread.get_class_id()
    lon = 25.636786
    lat = 60.968117
    rad = 3
    update_interval = 60

    def __init__(self, name: str = "rtracker") -> None:
        super().__init__(name)
        self.topic = self.make_topic_name("tracks")

    @override
    def on_connect(self, client: object, userdata: Any, flags: int, rc: int) -> None:
        super().on_connect(client, userdata, flags, rc)
        if rc == 0:
            self.subscribe(self.topic)

    @override
    def on_message(self, client: object, userdata: Any, msg: MqttMsg) -> None:
        if msg.topic == self.topic:
            em = json.loads(msg.payload.decode())
            self.on_sensor(em)
        else:
            super().on_message(client, userdata, msg)

    def on_sensor(self, msg: dict[str, Any]) -> None:
        point = (
            Point("track")
            .tag("id", msg["id"])
            .field("lon", msg["lon"])
            .field("lat", msg["lat"])
            .field("alt", msg["alt"])
            .field("type", msg["type"])
            .field("fom", msg["fom"])
            .time(epoc2utc(msg["ts"]))
        )
        self.write(point)
        self.debug(
            f"Track {msg['type']} {msg['lat']} {msg['lon']} recorded to timeseries"
        )

    @override
    def run(self) -> None:
        self.worker = cast(RTrackerThread, Base.instantiate(RTracker.workerThreadId))
        self.worker.init(self.lon, self.lat, self.rad, self.update_interval, self.topic)
        super().run()
