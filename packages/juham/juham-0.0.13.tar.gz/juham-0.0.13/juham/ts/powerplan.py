import json
from typing import Any
from typing_extensions import override
from influxdb_client_3 import Point

from juham.base import Base, JMqtt, MqttMsg
from juham.base.time import epoc2utc


class PowerPlanRecord(Base):
    """Power plan time series record.

    Listens powerplan topic and updates time series database
    accordingly.
    """

    def __init__(self, name: str = "powerplanrecord") -> None:
        super().__init__(name)
        self.powerplan_topic = self.make_topic_name("powerplan")

    @override
    def on_connect(self, client: object, userdata: Any, flags: int, rc: int) -> None:
        super().on_connect(client, userdata, flags, rc)
        self.subscribe(self.powerplan_topic )

    @override
    def on_message(self, client: object, userdata: Any, msg: MqttMsg) -> None:
        super().on_message(client, userdata, msg)
        m = json.loads(msg.payload.decode())
        fom = m["FOM"]
        uoi = m["UOI"]
        ts = m["Timestamp"]

        point = (
            Point("powerplan")
            .tag("unit", m["Unit"])
            .field("state", m["State"])  # 1 on, 0 off
            .field("name", m["Unit"])  # e.g main_boiler
            .field("type", "C")  # C=consumption, S = supply
            .field("power", 16.0)  # kW
            .field("FOM", int(fom))  # figures of merit
            .field("UOI", float(uoi))  # Utilitzation Optimizing Index
            .time(epoc2utc(ts))
        )
        self.write(point)
