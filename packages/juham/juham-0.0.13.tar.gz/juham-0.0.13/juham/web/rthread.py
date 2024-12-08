"""
The `rthread` module provides foundational classes for creating multi-threaded automation objects.

Classes:
    AutomationObject: A generic base class for automation objects.
    IWorkerThread: A base class for threads that can be spawned by automation objects.

These classes are highly flexible and designed to handle various tasks asynchronously, 
making them suitable for a wide range of applications.

Justification for subclassing from `Thread`: sharing the common memory space.

.. todo:: Decouple the functionality from the thread so that it 
can be run by any means, e.g., by process or asyncio.
"""

import json
from threading import Thread, Event
from typing import Any, Optional, cast
from typing_extensions import override
from masterpiece import MasterPiece
from juham.base import Base, JMqtt, MqttMsg


class IWorkerThread(Thread, MasterPiece):
    """Base class for threads used for tasks such as data acquisition
    that need to be run asynchronously. This class defines the `update()`
    method, in which subclasses can execute their specific code. The
    `update_interval()` method (default is 60 seconds) determines how
    frequently the `update()` method is called.

    Args:
        Thread (client): MQTT client for the thread
    """

    event_topic: str = ""

    # TODO: Decouple functionality from thread classes.

    def __init__(self, client: Optional[JMqtt]) -> None:
        """Construct worker thread for acquiring and publishing weather forecast
        from the Visualcrossing web service.

        Args:
            client (Optional[JMqtt]): Mqtt client for publishing the forecast data
        """
        super().__init__()
        self.mqtt_client: Optional[JMqtt] = client
        self.stay = True
        self.name = "unnamed thread"
        self.event_topic = ""
        self._stop_event = Event()

    def stop(self) -> None:
        """Request the thread to stop processing further tasks.

        Note that the method does not wait the thread to terminate.  If
        the thread is sleeping, it will be awakened and stopped. If the
        thread is in the middle of its code execution, it will finish
        its current job before stopping.  In oder to wait until the
        thread has completed its call join() method.
        """
        self._stop_event.set()

    def run(self) -> None:
        """Thread  loop.

        Calls update() method in a loop and if the return value is True
        sleeps the update_interval() number of seconds before the next
        update call. If the update method returns False then the error
        is logged, and the sleep time is shortened to 5 seconds to
        retry. After three subsequent failures the update_interval is
        reset to original
        """
        self.debug(
            f"Thread {self.name} started with update interval {self.update_interval()}"
        )
        failures: int = 0
        updates: int = 0
        while not self._stop_event.is_set():
            if not self.update():
                seconds: float = 5
                failures = failures + 1
                self.error(
                    f"Thread {self.name} update {str(updates)} failure {str(failures)}, retry after {str(seconds)} ..."
                )
                if failures > 3:
                    failures = 0
                    seconds = self.update_interval()
            else:
                seconds = self.update_interval()
            updates = updates + 1
            self._stop_event.wait(seconds)
        self.debug(f"Thread {self.name} stopped")
        # self.mqtt_client = None

    def update_interval(self) -> float:
        """Fetch the update interval in seconds. The default is 60.

        Returns:
            float: number of seconds
        """
        return 60.0

    def update(self) -> bool:
        """Method called from the threads run loop.

        Up to the sub classes to implement.

        Returns:
            bool: True upon succesfull update. False implies an error .
        """
        return True

    def log(self, type: str, msg: str, details: str) -> None:
        """Log event to event log.

        Args:
            type (str): one of the following: "info", "debug", "warning", "error"
            msg (str): message to be logged
            details (str): detailed description
        """
        if self.mqtt_client is not None:
            data = {"type": type, "msg": msg, "details": details}
            msg = json.dumps(data)
            self.publish(self.event_topic, msg, qos=1, retain=True)

    def publish(
        self, topic: str, message: str, qos: int = 1, retain: bool = True
    ) -> None:
        """Publish the given message to given MQTT topic with specified
        quality of service and retain.

        Args:
            topic (str): topic
            message (str): message to be published
            qos (int): quality of service
            retain (bool): retain the message
        """
        if self.mqtt_client != None:
            mqtt_client: JMqtt = cast(JMqtt, self.mqtt_client)
            mqtt_client.publish(topic, message, qos, retain)

    @override
    def error(self, msg: str, details: str = "") -> None:
        self.log("Error", msg, details)

    @override
    def warning(self, msg: str, details: str = "") -> None:
        self.log("Warning", msg, details)

    @override
    def info(self, msg: str, details: str = "") -> None:
        self.log("Info", msg, details)

    @override
    def debug(self, msg: str, details: str = "") -> None:
        self.log("Debug", msg, details)


class RThread(Base):
    """Base class of automation classes that need to run automation tasks using asynchronously running thread.
    Spawns the thread upon creation.
    Subscribes to 'event' topic to listen log events from the thread, and dispatches
    them to corresponding logging methods e.g. `self.info()`.

    """

    def __init__(self, name: str) -> None:
        """Construct automation object. By default no thread is created nor started.

        Args:
            name (str): name of the automation object.
        """
        super().__init__(name)
        self.worker: Optional[IWorkerThread]
        self.event_topic = self.make_topic_name("event")

    def disconnect(self) -> None:
        """Request the asynchronous acquisition thread to stop after it has finished its current job.
        This method does not wait for the thread to stop. See `shutdown()`.
        """
        if self.worker != None:
            worker: IWorkerThread = cast(IWorkerThread, self.worker)
            worker.stay = False

    @override
    def shutdown(self) -> None:
        if self.worker is not None:
            self.worker.stop()  # request to thread to exit its processing loop
            self.worker.join()  # wait for the thread to complete
        super().shutdown()

    @override
    def on_message(self, client: object, userdata: Any, msg: MqttMsg) -> None:
        if msg.topic == self.event_topic:
            em = json.loads(msg.payload.decode())
            self.on_event(em)
        else:
            self.error(f"Unknown message to {self.name}: {msg.topic}")

    def on_event(self, em: dict[str, Any]) -> None:
        """Notification event callback e.g info or warning.

        Args:
            em (dictionary): dictionary describing the event
        """
        if em["type"] == "Info":
            self.info(em["msg"], em["details"])
        elif em["type"] == "Debug":
            self.debug(em["msg"], em["details"])
        elif em["type"] == "Warning":
            self.warning(em["msg"], em["details"])
        elif em["type"] == "Error":
            self.error(em["msg"], em["details"])
        else:
            self.error("PANIC: unknown event type " + em["type"], str(em))

    @override
    def run(self) -> None:
        """Initialize and start the asynchronous acquisition thread."""
        super().run()
        if self.worker is not None:
            self.worker.mqtt_client = self.mqtt_client
            self.worker.name = self.name
            self.worker.event_topic = self.event_topic
            self.worker.start()
            self.info(f"Starting up {self.name} - {self.worker.__class__} ")
        else:
            self.warning(f"No thread, cannot run {self.name}")
