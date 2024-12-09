import json
from typing import Any, cast
from typing_extensions import override
from juham.base.jmqtt import JMqtt
from juham.shelly import JShelly
from juham.base import MqttMsg


class RBoiler(JShelly):
    """Automation class for controlling Shelly Wifi relay. Subscribes to
    'power' topic and controls the Shelly relay accordingly.

    """

    power_topic = "power"  # topic to listen
    relay_url = "shellyplus1-alakerta/command/switch:0"  # relay to control

    def __init__(self, name: str = "rboiler") -> None:
        super().__init__(name)
        self.current_relay_state: int = 0
        self.power_topic_in = self.make_topic_name(self.power_topic)

    @override
    def on_connect(self, client: object, userdata: Any, flags: int, rc: int) -> None:
        super().on_connect(client, userdata, flags, rc)
        if rc == 0:
            self.subscribe(self.power_topic_in)

    @override
    def on_message(self, client: object, userdata: Any, msg: MqttMsg) -> None:
        if msg.topic == self.power_topic_in:
            self.on_power(json.loads(msg.payload.decode()))
        else:
            super().on_message(client, userdata, msg)

    def on_power(self, m: dict[str, str]) -> None:
        """Process power_topic message.

        Args:
            m (dict): holding data from the power sensor
        """
        if "Unit" in m and m["Unit"] == "main_boiler":
            new_state = cast(int, m["State"])

            if new_state != self.current_relay_state:
                self.current_relay_state = new_state
                if new_state == 0:
                    relay = "off"
                else:
                    relay = "on"
                self.publish(self.relay_url, relay, 1)
                self.info(m["Unit"] + " state: " + relay, self.relay_url)
            else:
                self.info(
                    m["Unit"] + " Relay state " + str(new_state) + " not changed", ""
                )
