import json
from typing import Any, Dict
from typing_extensions import override
from influxdb_client_3 import Point

from juham.base import Base
from juham.base import JMqtt, MqttMsg
from juham.base.time import epoc2utc, timestamp
from juham.shelly.jshelly import JShelly


class ShellyPlus1(JShelly):
    """Shelly Plus 1 smart relay time series record.

    Listens MQTT messages from DS18B20 temperature sensors attached to
    Shelly 1 PM Add on module and writes them to time series database.
    """

    shelly_topic = "/events/rpc"  # source topic

    def __init__(self, name: str = "shellyplus1-a0a3b3c309c4") -> None:
        super().__init__(name)
        self.relay_started: float = 0
        self.temperature_topic = self.make_topic_name("temperature/")  # target topic

    @override
    def on_connect(self, client: object, userdata: Any, flags: int, rc: int) -> None:
        super().on_connect(client, userdata, flags, rc)
        if rc == 0:
            self.subscribe(self.mqtt_prefix + self.shelly_topic)

    @override
    def on_message(self, client: object, userdata: Any, msg: MqttMsg) -> None:
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
        """Map Shelly Plus 1 specific event to juham format and post it to
        temperature topic.

        Args:
            params (dict): message from Shelly Plus 1 wifi relay
        """
        ts = params["ts"]
        for key, value in params.items():
            if key.startswith("temperature:"):
                sensor_id = key.split(":")[1]
                temperature_reading = value
                # temperature_id = temperature_reading["id"]
                temperature_celsius = temperature_reading["tC"]

                msg = {
                    "sensor": sensor_id,
                    "timestamp": ts,
                    "temperature": int(temperature_celsius),
                }
                self.publish(
                    self.temperature_topic + sensor_id, json.dumps(msg), 1, True
                )
                self.debug(
                    f"Temperature reading { self.temperature_topic + sensor_id} published"
                )

                try:
                    point = (
                        Point("boiler")
                        .tag("sensor", sensor_id)
                        .field("s" + sensor_id, temperature_celsius)
                        .time(epoc2utc(ts))
                    )
                    self.write(point)
                    self.debug(
                        f"Temperature { str(sensor_id)}  { str(temperature_celsius)} recorded",
                        "",
                    )
                except Exception as e:
                    self.error(f"Writing to influx failed {str(e)}")

    @override
    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = super().to_dict()
        data["_shellyplus1"] = {
            "shelly_topic": self.shelly_topic,
            "temperature_topic": self.temperature_topic,
        }
        return data

    @override
    def from_dict(self, data: Dict[str, Any]) -> None:
        super().from_dict(data)
        if "_shellyplus1" in data:
            for key, value in data["_shellyplus1"].items():
                setattr(self, key, value)
