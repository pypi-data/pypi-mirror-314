import json
import traceback
from typing import Any, Dict, Optional, cast
from typing_extensions import override
from influxdb_client_3 import Point
from paho.mqtt.client import MQTTMessage as MqttMsg
from masterpiece import MasterPiece, URL
from juham.base.time import timestamp
from juham.base.jdatabase import JDatabase
from juham.base.jmqtt import JMqtt


class Base(MasterPiece):
    """An automation object with MQTT networking and time series data storage.

    Example:
    ::

        obj = Base("foo")
        obj.mqtt_host = "myhost.com"
        obj.mqtt_port = 12345
        obj.subscribe('foo/bar')
        obj.run()


    To configure Base class to use a specific MQTT and database set
    the class attributes to refer to desired MQTT and database implementations.
    When instantiated the object will instantiate the given MQTT and database objects with it.

    """

    database_class_id: str = "JInflux"
    mqtt_class_id: str = ""
    write_attempts: int = 3
    mqtt_root_topic: Optional[str] = None
    mqtt_host: str = "localhost"
    mqtt_port: int = 1883

    def __init__(self, name: str = "") -> None:
        """Constructs new automation object with the given name, configured
        time series recorder and MQTT network features.

        Args:
            name (str): name of the object
        """
        super().__init__(name)
        self.database_client: Optional[JDatabase | None] = None
        self.mqtt_client: Optional[JMqtt | None] = None
        self.mqtt_topic_base: str = ""
        self.mqtt_topic_control: str = ""
        self.mqtt_topic_log: str = ""
        if self.mqtt_root_topic == None:
            raise ValueError(f"Unconfigured MQTT topic {self.name}")

    @override
    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = super().to_dict()
        data["_base"] = {}
        attributes = ["mqtt_host", "mqtt_port", "mqtt_root_topic", "write_attempts"]
        for attr in attributes:
            if getattr(self, attr) != getattr(type(self), attr):
                data["_base"][attr] = getattr(self, attr)
        if self.database_client is not None:
            data["_database"] = {"db_client": self.database_client.to_dict()}
        return data

    @override
    def from_dict(self, data: Dict[str, Any]) -> None:
        super().from_dict(data)
        for key, value in data["_base"].items():
            if key == "db_client":
                self.database_client = cast(
                    Optional[JDatabase], MasterPiece.instantiate(value["_class"])
                )
                if self.database_client is not None:
                    self.database_client.from_dict(value)
            else:
                setattr(self, key, value)

    def initialize(self) -> None:
        """Initialize time series database and mqtt networking  for use. This method must be called
        after the object name has been  set .
        """
        self.init_database(self.name)
        self.init_mqtt(self.name)

    def init_database(self, name: str) -> None:
        """Instantiates the configured time series database object.

        Issues a warning if the :attr:`~database_class_id` has not
        been configured, in which case the object will not have the time series
        recording feature.

        This method is called internally and typically there is no need to call it
        from the application code.
        """

        if (
            Base.database_class_id != None
            and MasterPiece.find_class(Base.database_class_id) != None
        ):
            self.database_client = cast(
                Optional[JDatabase], MasterPiece.instantiate(Base.database_class_id)
            )
        else:
            self.warning("Suspicious configuration: no database_class_id set")

    def init_topic_base(self) -> None:
        url: URL = self.make_url()
        self.mqtt_root_topic = self.root().make_url().get()[1:]
        self.mqtt_topic_base = url.get()[1:]
        self.mqtt_topic_control = self.mqtt_root_topic + "/control"
        self.mqtt_topic_log = self.mqtt_root_topic + "/log"
        self.info(f"mqtt_topic_base is {self.mqtt_topic_base}")
        self.info(f"mqtt_topic_control is {self.mqtt_topic_control}")
        self.info(f"mqtt_topic_log is {self.mqtt_topic_log}")

    def make_topic_name(self, topic: str) -> str:
        """Make topic name for the object. The topic name
        consists of the base name plus the given 'topic'.

        Args:
            topic (str): topic name

        Returns:
            str: mqtt topic name
        """
        return f"{self.mqtt_root_topic}/{topic}"

    def init_mqtt(self, name: str) -> None:
        """Instantiates the configured MQTT object for networking. Calls `init_topic()`
        to construct topic base name for the object, and instantiates the mqtt
        client.

        This method is called internally and typically there is no need to call it
        from the application code.

        Issues a warning if the :attr:`mqtt_class_id` has not
        been configured, even though objects without a capability to communicate
        are rather crippled.
        """
        self.init_topic_base()
        if Base.mqtt_class_id == "":
            self.warning(
                f"Suscpicious configuration: no mqtt_class_id set for {self.name}:{self.get_class_id()}"
            )
        elif not Base.find_class(Base.mqtt_class_id):
            self.error(
                f"Couldn't create mqtt broker {Base.mqtt_class_id},  class not imported"
            )
        else:
            self.mqtt_client = cast(
                Optional[JMqtt], MasterPiece.instantiate(Base.mqtt_class_id, name)
            )
            if self.mqtt_client is not None:
                self.mqtt_client.on_message = self.on_message
                self.mqtt_client.on_connect = self.on_connect
                self.mqtt_client.on_disconnect = self.on_disconnect
                if (
                    self.mqtt_client.connect_to_server(self.mqtt_host, self.mqtt_port)
                    != 0
                ):
                    self.error(
                        f"Couldn't connect to the mqtt broker at {self.mqtt_client.host}"
                    )
                else:
                    self.debug(
                        f"{self.name} with mqtt broker {self.mqtt_client.name} connected to {self.mqtt_client.host}"
                    )
            else:
                self.error(f"Couldn't create mqtt broker {Base.mqtt_class_id}")

    def subscribe(self, topic: str) -> None:
        """Subscribe to the given MQTT topic.

        This method sets up the subscription to the specified MQTT topic and registers
        the :meth:`on_message` method as the callback for incoming messages.

        Args:
            topic (str): The MQTT topic to subscribe to.

        Example:
        ::

            # configure
            obj.subscribe('foo/bar')
        """

        if self.mqtt_client:
            self.mqtt_client.connected_flag = True
            self.mqtt_client.subscribe(topic)
            self.info(f"{self.name}  subscribed to { topic}")

    def on_message(self, client: object, userdata: Any, msg: MqttMsg) -> None:
        """MQTT message notification on arrived message.

        Called whenever a new message is posted on one of the
        topics the object has subscribed to via subscribe() method.
        This method is the heart of automation: here, derived subclasses should
        automate whatever they were designed to automate. For example, they could switch a
        relay when a boiler temperature sensor signals that the temperature is too low for
        a comforting shower for say one's lovely wife.

        For more information on this method consult MQTT documentation available
        in many public sources.

        Args:
            client (obj):  MQTT client
            userdata (Any): application specific data
            msg (object): The MQTT message
        """

        if msg.topic == self.mqtt_topic_control:
            m = json.loads(msg.payload)
            if m["command"] == "shutdown" and self.mqtt_client:
                self.mqtt_client.disconnect()
                self.mqtt_client.loop_stop()

    def on_connect(self, client: object, userdata: Any, flags: int, rc: int) -> None:
        """Notification on connect.

        This method is called whenever the MQTT broker is connected.
        For more information on this method consult MQTT documentation available
        in many public sources.

        Args:
            client (obj):  MQTT client
            userdata (Any): application specific data
            flags (int): Consult MQTT
            rc (int): See MQTT docs
        """
        if self.mqtt_client:
            self.mqtt_client.subscribe(self.mqtt_topic_control)
            self.debug(self.name + " connected to the mqtt broker ")

    def on_disconnect(self, client: object, userdata: Any, rc: int = 0) -> None:
        """Notification on disconnect.

        This method is called whenever the MQTT broker is disconnected.
        For more information on this method consult MQTT documentation available
        in many public sources.

        Args:
            client (obj):  MQTT client
            userdata (Any): application specific data
            rc (int): See MQTT docs
        """
        self.info(f"{self.name}  disconnected from the mqtt broker, {rc} ")

    def write(self, point: Point) -> None:
        """Writes the given measurement to the database. In case of an error,
        it tries again until the maximum number of attempts is reached. If it
        is still unsuccessful, it gives up and passes the first encountered
        exception to the caller.

        Args:
            point: a measurement describing a time stamp and related attributes for one measurement.
        """
        if not self.database_client:
            raise ValueError("Database client is not initialized.")

        first_exception: Optional[BaseException] = None
        for i in range(self.write_attempts):
            try:
                self.database_client.write(point)
                return
            except Exception as e:
                if first_exception is None:
                    first_exception = e
                self.warning(f"Writing ts failed, attempt {i+1}: {repr(e)}")

        self.log_message(
            "Error",
            f"Writing failed after {self.write_attempts} attempts, giving up",
            "".join(
                traceback.format_exception_only(type(first_exception), first_exception)
            ),
        )

    def write_point(self, name : str, tags : dict[str, Any], fields: dict[str, Any], ts : str) -> None:
        """Writes the given measurement to the database. In case of an error,
        it tries again until the maximum number of attempts is reached. If it
        is still unsuccessful, it gives up and passes the first encountered
        exception to the caller.

        Args:
            point: a measurement describing a time stamp and related attributes for one measurement.
        """
        if not self.database_client:
            raise ValueError("Database client is not initialized.")

        first_exception: Optional[BaseException] = None
        for i in range(self.write_attempts):
            try:
                self.database_client.write_point(name, tags, fields, ts)
                return
            except Exception as e:
                if first_exception is None:
                    first_exception = e
                self.warning(f"Writing ts failed, attempt {i+1}: {repr(e)}")

        self.log_message(
            "Error",
            f"Writing failed after {self.write_attempts} attempts, giving up",
            "".join(
                traceback.format_exception_only(type(first_exception), first_exception)
            ),
        )

    def read(self, point: Point) -> None:
        """Reads the given measurement from the database.

        Args:
            point: point with initialized time stamp.

        ... note: NOT IMPLEMENTED YET
        """
        if self.database_client:
            self.database_client.read(point)

    @override
    def debug(self, msg: str, details: str = "") -> None:
        """Logs the given debug message to the database after logging it using
        the BaseClass's info() method.

        Args:
            msg (str): The information message to be logged.
            details (str): Additional detailed information for the message to be logged
        """
        super().debug(msg, details)
        self.log_message("Debug", msg, details="")

    @override
    def info(self, msg: str, details: str = "") -> None:
        """Logs the given information message to the database after logging it
        using the BaseClass's info() method.

        Args:
            msg : The information message to be logged.
            details : Additional detailed information for the message to be logged

        Example:
        ::

            obj = new Base('test')
            obj.info('Message arrived', str(msg))
        """
        super().info(msg, details)
        self.log_message("Info", msg, details="")

    @override
    def warning(self, msg: str, details: str = "") -> None:
        """Logs the given warning message to the database after logging it
        using the BaseClass's info() method.

        Args:
            msg (str): The information message to be logged.
            details (str): Additional detailed information for the message to be logged
        """
        super().warning(msg, details)
        self.log_message("Warn", msg, details)

    @override
    def error(self, msg: str, details: str = "") -> None:
        """Logs the given error message to the database after logging it using
        the BaseClass's info() method.

        Args:
            msg (str): The information message to be logged.
            details (str): Additional detailed information for the message to be logged
        """
        super().error(msg, details)
        self.log_message("Error", msg, details)

    def log_message(self, type: str, msg: str, details: str = "") -> None:
        """Publish the given log message to the MQTT 'log' topic.

        This method constructs a log message with a timestamp, class type, source name,
        message, and optional details. It then publishes this message to the 'log' topic
        using the MQTT protocol.

        Parameters:
            type : str
                The classification or type of the log message (e.g., 'Error', 'Info').
            msg : str
                The main log message to be published.
            details : str, optional
                Additional details about the log message (default is an empty string).

        Returns:
            None

        Raises:
            Exception
                If there is an issue with the MQTT client while publishing the message.

        Example:
        ::

            # publish info message to the Juham's 'log' topic
            self.log_message("Info", f"Some cool message {some_stuff}", str(dict))
        """

        try:
            lmsg: dict[str, Any] = {
                "Timestamp": timestamp(),
                "Class": type,
                "Source": self.name,
                "Msg": msg,
                "Details": str(details),
            }
            self.publish(self.mqtt_topic_log, json.dumps(lmsg), 1)
        except Exception as e:
            if self._log is not None:
                self._log.error(f"Publishing log event failed {str(e)}")

    def publish(self, topic: str, msg: str, qos: int = 1, retain: bool = True) -> None:
        """Publish the given message to the given MQTT topic.
        For more information consult MQTT.

        Args:
            topic (str): topic
            msg (str): message to be published
            qos (int, optional): quality of service. Defaults to 1.
            retain (bool, optional): retain. Defaults to True.
        """
        if self.mqtt_client:
            self.mqtt_client.publish(topic, msg, qos, retain)

    def shutdown(self) -> None:
        """Shut down all services, free resources, stop threads, disconnect
        from mqtt, in general, prepare for shutdown."""
        if self.mqtt_client:
            self.mqtt_client.disconnect()
            self.mqtt_client.loop_stop()

    @override
    def run(self) -> None:
        """Start a new thread to runs the network loop in the background.

        Allows the main program to continue executing while the MQTT
        client handles incoming and outgoing messages in the background.
        """
        self.initialize()
        if self.mqtt_client:
            self.mqtt_client.loop_start()
        super().run()

    @override
    def run_forever(self) -> None:
        """Starts the network loop and blocks the main thread, continuously
        running the loop to process MQTT messages.

        The loop will run indefinitely unless the connection is lost or
        the program is terminated.
        """
        self.initialize()
        if self.mqtt_client:
            self.info(f"{self.name} has mqtt client, calling forever...")
            self.mqtt_client.loop_forever()
            self.info(f"{self.name} mqtt client run_forever returned")
        else:
            self.error(
                f"{self.name} does NOT have mqtt client, cannot run_forever, giving up"
            )
