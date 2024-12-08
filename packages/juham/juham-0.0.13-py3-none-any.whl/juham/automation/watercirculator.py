from typing import Any
from typing_extensions import override
import json

from juham.base import Base, MqttMsg
from juham.base.time import timestamp


class WaterCirculator(Base):
    """Hot Water Circulation Controller.

    Uses motion sensor data to determine if someone is at home. If so,
    it runs the water circulator pump to ensure that hot water is
    instantly available when the tap is turned on.
    """

    uptime = 60 * 60
    min_temperature = 37
    relay_topic = "shellyplus1-a0a3b3c309c4/command/switch:0"
    motion_sensor_topic = "shellies/shellymotion2/info"
    motion_topics = "shellies/shellymotion2/#"

    def __init__(self, name: str = "rwatercirculator") -> None:
        super().__init__(name)
        self.current_motion: bool = False
        self.relay_started_ts: float = 0
        self.water_temperature: float = 0
        self.water_temperature_updated: float = 0
        self.initialized = False
        self.temperature_topic = self.make_topic_name("temperature/103")

    @override
    def on_connect(self, client: object, userdata: Any, flags: int, rc: int) -> None:
        super().on_connect(client, userdata, flags, rc)
        if rc == 0:
            self.subscribe(self.motion_topics)
            self.subscribe(self.temperature_topic)
            # reset the relay to make sure the initial state matches the state of us
            self.publish(self.relay_topic, "off", 1)

    @override
    def on_message(self, client: object, userdata: Any, msg: MqttMsg) -> None:
        if msg.topic == self.temperature_topic:
            m = json.loads(msg.payload.decode())
            self.on_temperature_sensor(m, timestamp())
        elif msg.topic == self.motion_sensor_topic:
            m = json.loads(msg.payload.decode())
            self.on_motion_sensor(m, timestamp())
        else:
            super().on_message(client, userdata, msg)

    def on_temperature_sensor(self, m: dict[str, Any], ts_utc_now: float) -> None:
        """Handle message from the hot water pipe temperature sensor.

        Records the temperature and updates the water_temperature_updated attribute.

        Args:
            m (dict): temperature reading from the hot water blump sensor
            ts_utc_now (float): _current utc time
        """

        self.water_temperature = m["temperature"]
        self.water_temperature_updated = ts_utc_now
        self.info(
            f"Temperature of circulating water updated to {self.water_temperature} C"
        )

    def on_motion_sensor(self, m: dict[str, dict[str, Any]], ts_utc_now: float) -> None:
        """Control the water cirulator bump.

        Given message from the motion sensor consider switching the
        circulator bump on.

        Args:
            msg (dict): directionary holding motion sensor data
            ts_utc_now (float): current time stamp
        """
        sensor = m["sensor"]
        vibration: bool = sensor["vibration"]
        motion: bool = sensor["motion"]

        if motion or vibration:
            # honey I'm home
            if not self.current_motion:
                if self.water_temperature > self.min_temperature:
                    self.info(
                        f"Circulator: motion detected but water warm already {self.water_temperature} > {self.min_temperature} C"
                    )
                else:
                    self.current_motion = True
                    self.relay_started_ts = ts_utc_now
                    self.publish(self.relay_topic, "on", 1)
                    self.initialized = True
                    self.info(
                        f"Circulator pump started, will run for {int(self.uptime / 60)} minutes "
                    )
            else:
                self.info(
                    f"Circulator pump has been running for {int(ts_utc_now - self.relay_started_ts)/60} minutes",
                    " ",
                )
        else:
            if self.current_motion or not self.initialized:
                elapsed: float = ts_utc_now - self.relay_started_ts
                if elapsed > self.uptime:
                    self.publish(self.relay_topic, "off", 1)
                    self.info(
                        f"Circulator  pump stopped after running  {elapsed}/60 minutes",
                        "",
                    )
                    self.current_motion = False
                    self.initialized = True
                else:
                    self.info(
                        f"Circulator bump stop countdown {int(self.uptime - (ts_utc_now - self.relay_started_ts ))/60} min"
                    )
            else:
                self.info(
                    f"Circulator bump off already, temperature {self.water_temperature} C",
                    "",
                )
