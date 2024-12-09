from typing import Optional
from typing_extensions import override

from masterpiece import Application


# Note: don't remove these, even if they are not referenced.
# Importing the files will auto-configure the Juham to use these implementations
# for its timeseries and mqtt API
from juham.base import Base
from juham.database import JInflux as _JInflux
from juham.mqtt import JPaho as _JPaho

from juham.simulation import EnergyMeterSimulator
from juham.base import JApp


from juham.web import HomeWizardWaterMeter
from juham.shelly import ShellyPlus1
from juham.shelly import Shelly1G3
from juham.shelly import ShellyPro3EM
from juham.shelly import ShellyMotion
from juham.automation import RPowerPlan
from juham.automation import RBoiler
from juham.automation import WaterCirculator


class MyHomeApp(JApp):
    """Juham home automation application."""

    shelly_temperature = "shellyplus1-a0a3b3c309c4"  # temperature sensors
    shelly_boilerradiator = "shellyplus1-alakerta"  # hot water heating relay

    encoding = "utf-8"

    def __init__(self, name: str = "myhome"):
        """Creates home automation application with the given name."""
        super().__init__(name)
        self.instantiate_classes()

    @override
    def instantiate_classes(self) -> None:
        super().instantiate_classes()
        self.add(EnergyMeterSimulator("powerconsumption"))
        self.add(HomeWizardWaterMeter())
        self.add(ShellyPlus1(self.shelly_temperature))  # for temperature sensors
        self.add(ShellyPlus1(self.shelly_boilerradiator))  # boiler heating radiator
        self.add(Shelly1G3())  # humidity
        self.add(ShellyPro3EM())
        self.add(ShellyMotion())
        self.add(RPowerPlan())
        self.add(RBoiler())
        self.add(WaterCirculator())

        self.print()


def main() -> None:
    id = "myhome"
    Base.mqtt_root_topic = id
    Application.init_app_id(id)
    Application.register_plugin_group(id)
    MyHomeApp.load_plugins()
    Application.load_configuration()
    app = MyHomeApp(id)
    app.run_forever()


if __name__ == "__main__":
    main()
