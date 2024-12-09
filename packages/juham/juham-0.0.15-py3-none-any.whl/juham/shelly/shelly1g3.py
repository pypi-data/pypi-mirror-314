import json
from typing import Any, Dict
from typing_extensions import override
from influxdb_client_3 import Point
from juham.base import Base, MqttMsg
from juham.base.time import epoc2utc, timestamp
from juham.shelly.jshelly import JShelly


class Shelly1G3(JShelly):
    """Shelly Plus 1 smart relay time series record.

    Listens MQTT messages from dht22 (am2302) temperature sensors attached to
    Shelly 1 PM Add on module and writes them to time series database.
    """

    shelly_topic = "/events/rpc"  # source topic

    def __init__(self, name: str = "shelly1g3-humidity") -> None:
        super().__init__(name)
        self.relay_started: float = 0
        self.temperature_topic = self.make_topic_name("temperature/")  # target topic
        self.humidity_topic = self.make_topic_name("humidity/")  # target topic

    @override
    def on_connect(self, client: object, userdata: Any, flags: int, rc: int) -> None:
        super().on_connect(client, userdata, flags, rc)
        if rc == 0:
            self.subscribe(self.mqtt_prefix + self.shelly_topic)

    @override
    def on_message(self, client: object, userdata: Any, msg: MqttMsg) -> None:
        # optimize out excessive notifications
        tsnow = timestamp()
        self.relay_started = tsnow

        m = json.loads(msg.payload.decode())
        mth = m["method"]
        if mth == "NotifyStatus":
            params = m["params"]
            self.on_sensor(params)
        else:
            self.warning("Unknown method " + mth, str(m))

    def on_sensor(self, params: dict[str, Any]) -> None:
        """Map Shelly Plus 1GM specific event to juham format and post it to
        temperature topic.

        Args:
            params (dict): message from Shelly Plus 1 wifi relay
        """
        self.info(f"on_sensor() event {params}")
        ts = params["ts"]
        for key, value in params.items():
            if key.startswith("humidity:"):
                self.on_value(ts, key, value, "humidity", "rh")
            elif key.startswith("temperature:"):
                self.on_value(ts, key, value, "temperature", "tC")

    def on_value(
        self, ts: float, key: str, value: dict[str, Any], attr: str, unit: str
    ) -> None:
        sensor_id = key.split(":")[1]
        humidity = value[unit]

        msg = {
            "sensor": sensor_id,
            "timestamp": ts,
            attr: float(humidity),
        }
        self.publish(self.humidity_topic + sensor_id, json.dumps(msg), 1, True)
        self.info(
            f"Humidity reading { self.humidity_topic + sensor_id} {humidity} published"
        )
        try:
            point = (
                Point("ylakerta_humidity")
                .tag("sensor", sensor_id)
                .field(attr, humidity)
                .time(epoc2utc(ts))
            )
            self.write(point)
        except Exception as e:
            self.error(f"Writing to influx failed {str(e)}")

    @override
    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = super().to_dict()
        data["_shelly1g3"] = {
            "shelly_topic": self.shelly_topic,
            "temperature_topic": self.temperature_topic,
        }
        return data

    @override
    def from_dict(self, data: Dict[str, Any]) -> None:
        super().from_dict(data)
        if "_shelly1g3" in data:
            for key, value in data["_shelly1g3"].items():
                setattr(self, key, value)
