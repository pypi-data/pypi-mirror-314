from abc import ABC, abstractmethod
from typing import Protocol, Any, Optional, Callable
from paho.mqtt.client import MQTTMessage as MqttMsg
from masterpiece import MasterPiece


class JMqtt(MasterPiece, ABC):
    """Abstract base class for MQTT brokers."""

    connected_flag: bool = False
    host: str = "localhost"
    _not_implemented: str = "Subclasses must implement this method."

    def __init__(self, name: str) -> None:
        super().__init__(name)

    @abstractmethod
    def connect_to_server(
        self,
        host: str = "localhost",
        port: int = 1883,
        keepalive: int = 60,
        bind_address: str = "",
    ) -> int:
        """Connect to MQTT server

        Args:
            host (str, optional): host. Defaults to "localhost".
            port (int, optional): port. Defaults to 1883.
            keepalive (int, optional): keep alive, in seconds. Defaults to 60.

        Returns:
            0 if ok, non-zero values indicate errors

        """
        raise NotImplementedError(self._not_implemented)

    @abstractmethod
    def disconnect(self) -> None:
        """Disconnect from the MQTT broker.

        It is up to the sub classes to implement the method.
        """
        raise NotImplementedError(self._not_implemented)

    @abstractmethod
    def subscribe(self, topic: str, qos: int = 0) -> None:
        """Subscribe to the given topic

        Args:
            topic (str): to be subscribed
        """
        raise NotImplementedError(self._not_implemented)

    @abstractmethod
    def loop_stop(self) -> None:
        """Stop the network loop.

        No further messages shall be dispatched.

        """
        raise NotImplementedError(self._not_implemented)

    @abstractmethod
    def publish(self, topic: str, msg: str, qos: int = 0, retain: bool = False) -> None:
        raise NotImplementedError(self._not_implemented)

    @abstractmethod
    def loop_start(self) -> None:
        raise NotImplementedError(self._not_implemented)

    @abstractmethod
    def loop_forever(self) -> None:
        raise NotImplementedError(self._not_implemented)

    @property
    @abstractmethod
    def on_message(self) -> Callable[[object, Any, "MqttMsg"], None]:
        raise NotImplementedError(self._not_implemented)

    @on_message.setter
    @abstractmethod
    def on_message(self, value: Callable[[object, Any, "MqttMsg"], None]) -> None:
        """Set the message handler, a method to be called when new messages are published.

        Args:
            value (Callable): Python method to be called on arrival of messages.
        """
        raise NotImplementedError(self._not_implemented)

    @property
    @abstractmethod
    def on_connect(self) -> Callable[[object, Any, int, int], None]:
        raise NotImplementedError(self._not_implemented)

    @on_connect.setter
    @abstractmethod
    def on_connect(self, value: Callable[[object, Any, int, int], None]) -> None:
        raise NotImplementedError(self._not_implemented)

    @property
    @abstractmethod
    def on_disconnect(self) -> Callable[[Any, Any, int], None]:
        raise NotImplementedError(self._not_implemented)

    @on_disconnect.setter
    @abstractmethod
    def on_disconnect(self, value: Callable[[Any, Any, int], None]) -> None:
        raise NotImplementedError(self._not_implemented)
