import json
from typing import Any, Dict
from typing_extensions import override
from influxdb_client_3 import Point
from juham.base import Base, MqttMsg
from juham.base.jmqtt import JMqtt
from juham.base.time import epoc2utc, timestampstr
from juham.shelly.jshelly import JShelly


class ShellyMotion(JShelly):
    """Shelly Motion 2 - a wifi motion sensor with light and temperature metering."""

    shelly_topic = "shellies/shellymotion2/info"  # source topic

    def __init__(self, name: str = "shellymotion") -> None:
        super().__init__(name)
        self.motion_topic = self.make_topic_name("motion")
 
    @override
    def on_connect(self, client: object, userdata: Any, flags: int, rc: int) -> None:
        super().on_connect(client, userdata, flags, rc)
        if rc == 0:
            self.subscribe(self.shelly_topic)
            self.debug("Topic " + self.shelly_topic + " subscribed")

    @override
    def on_message(self, client: object, userdata: Any, msg: MqttMsg) -> None:
        if msg.topic == self.shelly_topic:
            m = json.loads(msg.payload.decode())
            self.on_sensor(m)
        else:
            super().on_message(client, userdata, msg)

    def on_sensor(self, m: dict[str, Any]) -> None:
        """Handle motion sensor event. This method reads the incoming event,
        translates it, and publishes it to the Juham topic. It also writes the
        attributes to the time series database.

        Args:
            m (dict): MQTT event from Shelly motion sensor
        """

        tmp = m["tmp"]
        sensor_id = "motion"
        roomtemperature = tmp["value"]
        sensor = m["sensor"]
        vibration = sensor["vibration"]
        motion = sensor["motion"]
        timestamp = m["unixtime"]
        self.debug(f"Motion sensor event {timestampstr(timestamp)}")

        msg = {
            "sensor": sensor_id,
            "timestamp": timestamp,
            "temperature": int(roomtemperature),
            "motion": motion,
            "vibration": vibration,
        }

        self.publish(self.motion_topic, json.dumps(msg), 1, True)

        point = (
            Point("motion")
            .tag("sensor", sensor_id)
            .field("motion", motion)
            .field("vibration", vibration)
            .field("roomtemp", roomtemperature)
            .field("timestamp", int(timestamp))
            .time(epoc2utc(timestamp))
        )
        self.write(point)

    @override
    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = super().to_dict()
        data["_shellymotion"] = {
            "shelly_topic": self.shelly_topic,
            "motion_topic": self.motion_topic,
        }
        return data

    @override
    def from_dict(self, data: Dict[str, Any]) -> None:
        super().from_dict(data)
        if "_shellymotion" in data:
            for key, value in data["_shellymotion"].items():
                setattr(self, key, value)
