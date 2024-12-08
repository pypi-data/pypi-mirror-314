from datetime import datetime
import time
import json
from typing import Any, Dict, Optional, cast
from typing_extensions import override
from influxdb_client_3 import Point

from juham.base import Base
from juham.base import JMqtt, MqttMsg
from juham.base.time import epoc2utc
from juham.web import RCloud, RCloudThread


class SpotHintaFiThread(RCloudThread):
    """Thread running SpotHinta.fi.

    Periodically fetches the spot electricity prices and publishes them
    to  'spot' topic.
    """

    _spot_topic: str = ""
    _url: str = ""
    _interval: float = 6 * 3600

    def __init__(self, client: Optional[JMqtt] = None) -> None:
        super().__init__(client)
        self._interval = 60

    def init(self, topic: str, url: str, interval: float) -> None:
        self._spot_topic = topic
        self._url = url
        self._interval = interval

    @override
    def make_weburl(self) -> str:
        return self._url

    @override
    def update_interval(self) -> float:
        return self._interval

    @override
    def process_data(self, rawdata: Any) -> None:
        """Publish electricity price message to Juham topic.

        Args:
            rawdata (dict): electricity prices
        """

        super().process_data(rawdata)
        data = rawdata.json()

        spot = []
        for e in data:
            ts = time.mktime(time.strptime(e["DateTime"], "%Y-%m-%dT%H:%M:%S%z"))
            hour = datetime.utcfromtimestamp(ts).strftime("%H")
            h = {
                "Timestamp": ts,
                "hour": hour,
                "Rank": e["Rank"],
                "PriceWithTax": e["PriceWithTax"],
            }
            spot.append(h)
        self.publish(self._spot_topic, json.dumps(spot), 1, True)
        self.info(f"Spot electricity prices published for the next {len(spot)} days")


class RSpotHintaFi(RCloud):

    worker_thread_id = SpotHintaFiThread.get_class_id()
    url = "https://api.spot-hinta.fi/TodayAndDayForward"
    update_interval = 6 * 3600

    def __init__(self, name: str = "rspothintafi") -> None:
        super().__init__(name)
        self.active_liter_lpm = -1
        self.update_ts = None
        self.spot_topic = self.make_topic_name("spot")

    @override
    def on_connect(self, client: object, userdata: Any, flags: int, rc: int) -> None:
        super().on_connect(client, userdata, flags, rc)
        if rc == 0:
            self.subscribe(self.spot_topic)

    @override
    def on_message(self, client: object, userdata: Any, msg: MqttMsg) -> None:
        if msg.topic == self.spot_topic:
            em = json.loads(msg.payload.decode())
            self.on_spot(em)
        else:
            super().on_message(client, userdata, msg)

    def on_spot(self, m: dict[Any, Any]) -> None:
        """Write hourly spot electricity prices to time series database.

        Args:
            m (dict): holding hourlys spot electricity prices
        """
        for h in m:
            point = (
                Point("spot")
                .tag("hour", h["Timestamp"])
                .field("value", h["PriceWithTax"])
                .time(epoc2utc(h["Timestamp"]))
            )
            self.write(point)

    @override
    def run(self) -> None:
        self.worker = cast(
            SpotHintaFiThread, Base.instantiate(RSpotHintaFi.worker_thread_id)
        )
        self.worker.init(self.spot_topic, self.url, self.update_interval)
        super().run()

    @override
    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = super().to_dict()
        data["_spothintafi"] = {
            "topic": self.spot_topic,
            "url": self.url,
            "interval": self.update_interval,
        }
        return data

    @override
    def from_dict(self, data: Dict[str, Any]) -> None:
        super().from_dict(data)
        if "_spothintafi" in data:
            for key, value in data["_spothintafi"].items():
                setattr(self, key, value)
