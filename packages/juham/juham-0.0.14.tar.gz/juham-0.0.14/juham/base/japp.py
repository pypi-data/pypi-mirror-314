# Note: don't remove these, even if they are not referenced.
# Importing the files will auto-configure the Juham to use these implementations
# for its timeseries and mqtt API
from juham.base import Base
from juham.base import JMqtt as _JMqtt
from juham.database import JInflux as _JInflux
from juham.mqtt import JPaho as _JPaho

from masterpiece import Application

from juham.ts import (
    ForecastRecord,
    PowerRecord,
    PowerPlanRecord,
    PowerMeterRecord,
    LogRecord,
    EnergyCostCalculatorRecord,
)
from juham.web import RSpotHintaFi
from juham.automation import EnergyCostCalculator


class JApp(Application):
    """Juham home automation application base class. Registers new plugin group 'juham'."""

    def __init__(self, name: str) -> None:
        """Creates home automation application with the given name.
        If --enable_plugins is False create hard coded configuration
        by calling instantiate_classes() method.

        Args:
            name (str): name for the application
        """
        super().__init__(name, Base(name))

    def instantiate_classes(self) -> None:
        """Instantiate automation classes .

        Returns:
            None
        """
        self.add(ForecastRecord())
        self.add(PowerRecord())
        self.add(PowerPlanRecord())
        self.add(PowerMeterRecord())
        self.add(LogRecord())
        self.add(RSpotHintaFi())
        self.add(EnergyCostCalculator())
        self.add(EnergyCostCalculatorRecord())

        # install plugins
        self.add(self.instantiate_plugin_by_name("VisualCrossing"))
        self.add(self.instantiate_plugin_by_name("OpenWeatherMap"))

    @classmethod
    def register(cls) -> None:
        """Register plugin group `juham`."""
        Application.register_plugin_group("juham")
