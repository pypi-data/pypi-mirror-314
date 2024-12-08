import os
from typing import Any, Callable, Optional
from typing_extensions import override

import paho.mqtt.client as paho
from juham.base import JMqtt, MqttMsg


class JPaho(JMqtt):
    """MQTT broker implementation based on paho.mqtt.

    Creates a paho mosquitto client running on localhost and port 1883.
    """

    paho_version = 1

    def __init__(self, name: str = "paho") -> None:
        """Construct MQTT client for the configured mqtt broker of the
        configured paho_version.

        Args:
            name (str): name for the object.
        """
        super().__init__(name)
        if self.paho_version == 2:
            self.mqtt_client = paho.Client(
                paho.CallbackAPIVersion.VERSION1, name + str(os.getpid())
            )
        else:
            self.mqtt_client = paho.Client(name + str(os.getpid()))

    @override
    def connect_to_server(
        self,
        host: str = "locahost",
        port: int = 1883,
        keepalive: int = 60,
        bind_address: str = "",
    ) -> int:
        """Connects the client to the mqtt broker."""
        return self.mqtt_client.connect(host, port, keepalive, bind_address)

    @override
    def disconnect(
        self, reasoncode: Optional[int] = None, properties: Optional[Any] = None
    ) -> None:
        """Disconnect.

        Args:
            reasoncode (Optional[int]): MQTT 5 reason code for disconnection. Defaults to None.
            properties (Optional[Any]): MQTT 5 properties for disconnection. Defaults to None.
        """
        self.mqtt_client.disconnect()

    @override
    def subscribe(self, topic: str, qos: int = 0) -> None:
        """Subscribe to the given topic."""
        self.info(f"Subscribe to {topic}")
        self.mqtt_client.subscribe(topic, qos)

    @override
    def loop_stop(self) -> None:
        self.mqtt_client.loop_stop()

    @override
    def publish(self, topic: str, msg: str, qos: int = 0, retain: bool = False) -> None:
        """Publishes an MQTT message.

        This method sends a message to the MQTT broker and publish it
        to the given topic.

        Parameters:
        msg (str): The topic the message is published to.
        msg (str): The message to be published.

        Raises:
        ValueError: If the message is not a string or is empty.
        ConnectionError: If there is a problem connecting to the MQTT broker.
        MQTTException: If there is an error during the publish operation.
        """
        self.mqtt_client.publish(topic, msg, qos, retain)
        self.info(f"Publish to {topic}")

    @override
    def loop_start(self) -> None:
        self.mqtt_client.loop_start()

    @override
    def loop_forever(self) -> None:
        self.mqtt_client.loop_forever()

    @property
    @override
    def on_message(self) -> Callable[[object, Any, MqttMsg], None]:
        return self.mqtt_client.on_message

    @on_message.setter
    @override
    def on_message(self, value: Callable[[object, Any, MqttMsg], None]) -> None:
        """Set the message handler, a method to be called when new messages are published.

        Args:
            value (Callable): Python method to be called on arrival of messages.
        """
        self.mqtt_client.on_message = value

    @property
    @override
    def on_connect(self) -> Callable[[object, Any, int, int], None]:
        return self.mqtt_client.on_connect

    @on_connect.setter
    @override
    def on_connect(self, value: Callable[[object, Any, int, int], None]) -> None:
        self.mqtt_client.on_connect = value

    @property
    @override
    def on_disconnect(self) -> Callable[[Any, Any, int], None]:
        return self.mqtt_client.on_disconnect

    @on_disconnect.setter
    @override
    def on_disconnect(self, value: Callable[[Any, Any, int], None]) -> None:
        self.mqtt_client.on_disconnect = value
