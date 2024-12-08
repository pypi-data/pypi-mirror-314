import json
from typing import Any, Dict, Optional, cast, override
from influxdb_client_3 import Point
from juham.base import Base
from juham.base import JMqtt, MqttMsg
from juham.base.time import epoc2utc, timestamp
from juham.web.rcloud import RCloud, RCloudThread


class HomeWizardThread(RCloudThread):
    """Thread that reads HomeWizard's water meter sensor."""

    def __init__(self, client: Optional[JMqtt] = None) -> None:
        """Construct HomeWizard water meter acquisition thread.

        Args:
            topic (str, optional): MQTT topic to post the sensor readings. Defaults to None.
            interval (float, optional): Interval specifying how often the sensor is read. Defaults to 60 seconds.
            url (str, optional): url for reading watermeter. Defaults to None.
        """
        super().__init__(client)

    def init(self, topic: str = "", url: str = "", interval: float = 60) -> None:
        """Initialize thread for reading HomeWizard sensor and publishing
        the readings to Mqtt network.

        Args:
            topic (str, optional): Mqtt topic to publish the readings
            url (str, optional): HomeWizard url for reading sensor data.
            interval (float, optional): Update interval. Defaults to 60.
        """
        self._sensor_topic = topic
        self._interval = interval
        self._device_url = url

    @override
    def make_weburl(self) -> str:
        return self._device_url

    @override
    def update_interval(self) -> float:
        return self._interval

    @override
    def process_data(self, data: Any) -> None:
        super().process_data(data)
        data = data.json()
        msg = json.dumps(data)
        self.publish(self._sensor_topic, msg, qos=1, retain=False)


class HomeWizardWaterMeter(RCloud):
    """Homewizard watermeter sensor."""

    workerThreadId = HomeWizardThread.get_class_id()
    url = "http://192.168.86.70/api/v1/data"
    update_interval = 60

    def __init__(
        self,
        name: str = "homewizardwatermeter",
        topic: str = "",
        url: str = "",
        interval: float = 60.0,
    ) -> None:
        """Create Homewizard water meter sensor.

        Args:
            name (str, optional): name identifying the sensor. Defaults to 'homewizardwatermeter'.
            topic (str, optional): Juham topic to publish water consumption readings. Defaults to None.
            url (str, optional): Homewizard url from which to acquire water consumption readings. Defaults to None.
            interval (float, optional): Frequency at which the watermeter is read. Defaults to None.
        """
        super().__init__(name)
        self.active_liter_lpm: float = -1
        self.update_ts: float = 0.0
        if topic != "":
            self.topic = topic
        if url != "":
            self.url = url
        if interval > 0.0:
            self.interval = interval
        self.sensor_topic = self.make_topic_name("watermeter")

    @override
    def on_connect(self, client: object, userdata: Any, flags: int, rc: int) -> None:
        super().on_connect(client, userdata, flags, rc)
        if rc == 0:
            self.subscribe(self.sensor_topic)

    @override
    def on_message(self, client: object, userdata: Any, msg: MqttMsg) -> None:
        if msg.topic == self.sensor_topic:
            em = json.loads(msg.payload.decode())
            self.on_sensor(em)
        else:
            super().on_message(client, userdata, msg)

    def on_sensor(self, em: dict[str, Any]) -> None:
        """Handle data coming from the watermeter sensor. Writes the sensor
        telemetry to time series.

        Args:
            em (dict): data from the sensor
        """
        active_liter_lpm = float(em["active_liter_lpm"])
        total_liter_m3 = float(em["total_liter_m3"])
        ts = timestamp()
        if (active_liter_lpm != self.active_liter_lpm) or (ts > self.update_ts + 60.0):
            point = (
                Point("watermeter")
                .tag("sensor", "0")
                .field("total_liter", total_liter_m3)
                .field("active_lpm", active_liter_lpm)
                .time(epoc2utc(timestamp()))
            )
            self.write(point)
            self.info("Water consumption " + str(total_liter_m3))
            self.update_ts = ts
            self.active_liter_lpm = active_liter_lpm

    @override
    def run(self) -> None:
        self.worker = cast(
            HomeWizardThread, Base.instantiate(HomeWizardWaterMeter.workerThreadId)
        )
        self.worker.init(self.sensor_topic, self.url, self.update_interval)
        super().run()

    @override
    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = super().to_dict()
        data["_homewizardwatermeter"] = {
            "topic": self.sensor_topic,
            "url": self.url,
            "interval": self.update_interval,
        }
        return data

    @override
    def from_dict(self, data: Dict[str, Any]) -> None:
        super().from_dict(data)
        if "_homewizardwatermeter" in data:
            for key, value in data["_homewizardwatermeter"].items():
                setattr(self, key, value)
