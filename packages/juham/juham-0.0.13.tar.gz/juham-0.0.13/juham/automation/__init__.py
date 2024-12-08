"""
Description
===========

Classes implementing automated tasks. Objects in this package typically control some physical device, 
such as heating radiator, or water cirulator bump. In order to do they job they subscribe to appropropate 
Juham MQTT topics to acquire telemetry from sensors and web resources. 
"""

from .rboiler import RBoiler
from .rpowerplan import RPowerPlan
from .watercirculator import WaterCirculator
from .energycostcalculator import EnergyCostCalculator

__all__ = ["EnergyCostCalculator", "RBoiler", "RPowerPlan", "WaterCirculator"]
