import json
from typing import Any
from typing_extensions import override

from juham.base import Base, MqttMsg
from juham.base.time import quantize, timestamp, timestamp_hour, timestampstr

# TODO: rewrite and implement heat sensors to publish boiler temperatures
# in device independent format and more


class RPowerPlan(Base):
    """Automation class for optimized control of home energy consumers e.g hot
    water boilers. Reads spot prices, boiler water temperatures and controls
    heating radiators.

    .. todo:: rewrite to meet the architecture and design patterns.
    .. todo:: introduce general algorithm for managing any number of any consumers.

    """

    # hourly energy balance energy for time based settlement
    uoi_limit = 0.75
    maximum_boiler_temperature = 70
    minimum_boiler_temperature = 43
    energy_balancing_interval: float = 3600
    radiator_power = 3000  # 3 kW
    operation_threshold = 5 * 60
    spot_limit = 0.02  # euros, use electricity if below this price
    heating_hours_per_day = 4  # use the four cheapest hours per day

    def __init__(self, name: str = "rpowerplan") -> None:
        super().__init__(name)
        self.main_boiler_temperature = 100
        self.pre_boiler_temperature = 0
        self.current_heating_plan = 0
        self.heating_plan: list[dict[str, int]] = []
        self.power_plan: list[dict[str, Any]] = []
        self.ranked_spot_prices: list[dict[Any, Any]] = []
        self.ranked_solarpower: list[dict[Any, Any]] = []
        self.relay: bool = False
        self.relay_started_ts: float = 0
        self.current_power: float = 0
        self.net_energy_balance: float = 0.0
        self.net_energy_power: float = 0
        self.net_energy_balance_ts: float = 0
        self.net_energy_balancing_rc: bool = False
        self.net_energy_balancing_mode = False

        self.topic_spot = self.make_topic_name("spot")
        self.topic_forecast = self.make_topic_name("forecast")
        self.topic_temperature = self.make_topic_name("temperature/102")
        self.topic_powerplan = self.make_topic_name("powerplan")
        self.topic_power = self.make_topic_name("power")
        self.topic_in_powerconsumption = self.make_topic_name("powerconsumption")
        self.topic_in_net_energy_balance = self.make_topic_name("net_energy_balance")


    @override
    def on_connect(self, client: object, userdata: Any, flags: int, rc: int) -> None:
        super().on_connect(client, userdata, flags, rc)
        if rc == 0:
            self.subscribe(self.topic_spot)
            self.subscribe(self.topic_forecast)
            self.subscribe(self.topic_temperature)
            self.subscribe(self.topic_in_powerconsumption)
            self.subscribe(self.topic_in_net_energy_balance)

    def sort_by_rank(
        self, hours: list[dict[str, Any]], ts_utc_now: float
    ) -> list[dict[str, Any]]:
        """Sort the given electricity prices by their rank value. Given a list
        of electricity prices, return a sorted list from the cheapest to the
        most expensive hours. Entries that represent electricity prices in the
        past are excluded.

        Args:
            hours (list): list of hourly electricity prices
            ts_utc_now (float): current time

        Returns:
            list: sorted list of electricity prices
        """
        sh = sorted(hours, key=lambda x: x["Rank"])
        ranked_hours = []
        for h in sh:
            utc_ts = h["Timestamp"]
            if utc_ts > ts_utc_now:
                ranked_hours.append(h)

        return ranked_hours

    def sort_by_power(
        self, solarpower: list[dict[Any, Any]], ts_utc_now: float
    ) -> list[dict[Any, Any]]:
        """Sort forecast of solarpower to decreasing order.

        Args:
            solarpower (list): list of entries describing hourly solar energy forecast
            ts_utc_now (float): curren time, for exluding entries that are in the past

        Returns:
            list: list from the highest solarenergy to lowest.
        """
        ts_utc_quantized = quantize(3600, ts_utc_now)
        self.debug(
            f"Sorting {len(solarpower)} days of forecast starting at {timestampstr(ts_utc_quantized)}"
        )
        # if all items have solarenergy key then
        # sh = sorted(solarpower, key=lambda x: x["solarenergy"], reverse=True)
        # else skip items that don't have solarenergy key
        sh = sorted(
            [item for item in solarpower if "solarenergy" in item],
            key=lambda x: x["solarenergy"],
            reverse=True,
        )
        self.debug(f"Sorted {len(sh)} days of forecast")
        ranked_hours = []

        for h in sh:
            utc_ts: float = float(h["ts"])
            if utc_ts >= ts_utc_quantized:
                ranked_hours.append(h)
        self.debug(f"Forecast sorted for the next {str(len(ranked_hours))} days")
        return ranked_hours

    @override
    def on_message(self, client: object, userdata: Any, msg: MqttMsg) -> None:
        m = None
        ts_utc_now = timestamp()
        if msg.topic == self.topic_spot:
            self.ranked_spot_prices = self.sort_by_rank(
                json.loads(msg.payload.decode()), ts_utc_now
            )
            self.info(
                f"Spot prices received and ranked for {len(self.ranked_spot_prices)} hours"
            )
            self.power_plan = []  # reset power plan, it depends on spot prices
            return
        elif msg.topic == self.topic_forecast:
            forecast = json.loads(msg.payload.decode())
            # reject messages that don't have  solarenergy forecast
            found_solarenergy: bool = False
            for f in forecast:
                if not "solarenergy" in f:
                    self.debug(f"Reject forecast {f}, no solarenergy")
                    return
                elif f["solarenergy"] > 0:
                    found_solarenergy = True
                    break
            if not found_solarenergy:
                return
            self.ranked_solarpower = self.sort_by_power(forecast, ts_utc_now)
            self.info(
                f"Solar energy forecast received and ranked for {len(self.ranked_solarpower)} hours"
            )
            self.power_plan = []  # reset power plan, it depends on forecast
            return
        elif msg.topic == self.topic_temperature:
            m = json.loads(msg.payload.decode())
            self.main_boiler_temperature = m["temperature"]
            self.info(
                f"Boiler temperature reading { self.main_boiler_temperature}C received"
            )
        elif msg.topic == self.topic_in_net_energy_balance:
            m = json.loads(msg.payload.decode())
            self.net_energy_balance = m["energy"]
            self.net_energy_power = m["power"]
            self.info(
                f"Net energy { self.net_energy_balance}J, power {self.net_energy_power}W"
            )
        elif msg.topic == self.topic_in_powerconsumption:
            m = json.loads(msg.payload.decode())
            self.current_power = m["real_total"]
            self.debug(f"Current power {self.current_power/1000.0} kW")
        else:
            super().on_message(client, userdata, msg)
            return
        self.on_powerplan(ts_utc_now)

    def on_powerplan(self, ts_utc_now: float) -> None:
        """Apply power plan.

        Args:
            ts_utc_now (float): utc time
        """
        if not self.ranked_spot_prices:
            self.debug("Waiting  spot prices...", "")
            return

        if not self.power_plan:
            self.power_plan = self.create_power_plan()
            self.heating_plan = []
            self.info(
                f"Power plan of length {len(self.power_plan)} created",
                str(self.power_plan),
            )

        if not self.power_plan:
            self.error("Failed to create a power plan", "")
            return

        if len(self.power_plan) < 4:
            self.warning(
                f"Suspiciously short {len(self.power_plan)}  power plan, wait more data ..",
                "",
            )
            self.heating_plan = []
            self.power_plan = []
            return

        if not self.ranked_solarpower or len(self.ranked_solarpower) < 4:
            self.warning("No forecast, optimization compromised..", "")

        if not self.heating_plan:
            self.heating_plan = self.create_heating_plan()
            self.info(f"Heating plan of length {len(self.heating_plan)} created", "")
        if not self.heating_plan:
            self.error("Failed to create heating plan")
            return
        if len(self.heating_plan) < 4:
            self.info("Ditch remaining short heating plan ..", "")
            self.heating_plan = []
            self.power_plan = []
            return

        if ts_utc_now - self.relay_started_ts < 60:
            return
        self.relay_started_ts = ts_utc_now
        tsstr: str = timestampstr(ts_utc_now)
        self.debug(f"Considering heating {tsstr}")
        relay = self.consider_heating(ts_utc_now)
        heat = {"Unit": "main_boiler", "Timestamp": ts_utc_now, "State": relay}
        self.publish(self.topic_power, json.dumps(heat), 1, True)
        self.info(f"Heating state published with relay state {relay}", "")

    def consider_net_energy_balance(self, ts: float) -> bool:
        """Check when there is enough energy available for the radiators heat
        the water the remaining time within the  balancing interval,
        and switch the balancing mode on. If the remaining time in the
        current balancing slot is less than the threshold then
        optimize out.


        Args:
            ts (float): current time

        Returns:
            bool: true if production exceeds the consumption
        """

        # elapsed and remaining time within the current balancing slot
        elapsed_ts = ts - quantize(self.energy_balancing_interval, ts)
        remaining_ts = self.energy_balancing_interval - elapsed_ts

        # don't bother to switch the relay on for small intervals, to avoid
        # wearing contactors out
        if remaining_ts < self.operation_threshold:
            return False

        # check if the balance is sufficient for heating the next half of the energy balancing interval
        # if yes then switch heating on for the next half an hour
        needed_energy = 0.5 * self.radiator_power * remaining_ts
        elapsed_interval = ts - self.net_energy_balance_ts
        if (
            self.net_energy_balance > needed_energy
        ) and not self.net_energy_balancing_rc:
            self.net_energy_balance_ts = ts
            self.net_energy_balancing_rc = True  # heat
            self.info("Enough to supply the radiator, enable")
            self.net_energy_balancing_mode = True  # balancing mode indicator on
        else:
            # check if we have reach the end of the interval, or consumed all the energy
            # of the current slot. If so switch the energy balancer mode off
            if (
                elapsed_interval > self.energy_balancing_interval / 2.0
                or self.net_energy_balance < 0
            ):
                self.net_energy_balancing_rc = False  # heating off
                self.info(
                    "All the balance used , or the end of the interval reached, disable"
                )
        return self.net_energy_balancing_rc

    def consider_heating(self, ts: float) -> int:
        """Consider whether the target boiler needs heating.

        Args:
            ts (float): current UTC time

        Returns:
            int: 1 if heating is needed, 0 if not
        """

        # check if we have energy to consume, if so return 1
        if self.consider_net_energy_balance(ts):
            self.warning("Net energy balance says YES, but disabled for now")
            # return 1
        elif self.net_energy_balancing_mode:
            balancing_slot_start_ts = quantize(self.energy_balancing_interval, ts)
            elapsed_b = ts - balancing_slot_start_ts
            if elapsed_b > self.energy_balancing_interval:
                self.net_energy_balancing_mode = False
                self.info(
                    "Exit net energy balancing mode because elapsed {elapsed_b}s is less than balancing interval {self.energy_balancing_interval}s"
                )
            else:
                self.info(
                    f"Waiting remaining energy balancing interval {elapsed_b}s end"
                )
                self.warning(
                    "but net energy balance disabled, continue instead of return 0"
                )
                # return 0

        if self.main_boiler_temperature < self.minimum_boiler_temperature:
            self.info(
                f"Low temp, force heating because {self.main_boiler_temperature}C is less than {self.minimum_boiler_temperature}C"
            )
            return 1

        if self.main_boiler_temperature > self.maximum_boiler_temperature:
            self.debug(
                f"Temperature beyond maximum already {self.main_boiler_temperature}C"
            )
            return 0
        hour = timestamp_hour(ts)
        for pp in self.heating_plan:
            ppts: float = pp["Timestamp"]
            h: float = timestamp_hour(ppts)

            if h == hour:
                self.debug(
                    f"Heatingplan entry found for hour {hour} with spot {pp['Spot']} e/kWh"
                )
                return pp["State"]

        self.error(f"Cannot find heating plan for hour {hour}")
        return 0

    # compute figure of merit (FOM) for each hour
    # the higher the solarenergy and the lower the spot the higher the FOM

    # compute fom
    def compute_fom(self, solpower: float, spot: float) -> float:
        """Compute UOI - utilization optimization index.

        Args:
            solpower (float): current solar power forecast
            spot (float): spot price

        Returns:
            float: utilization optimization index
        """
        # total solar power is 6kW and max pow consumption about twice as much
        # so when sun is shining with full power nearly half of the energy comes for free

        if spot < 0.001:
            return 2  # use
        elif spot > 0.1:
            return 0  # try not to use
        else:
            fom = 2 * (0.101 - spot) / 0.1
            return fom

    def create_power_plan(self) -> list[dict[Any, Any]]:
        """Create power plan.

        Returns:
            list: list of utilization entries
        """
        ts_now = timestamp()
        self.info(
            f"Creating new powerplan from {len(self.ranked_spot_prices)}  hourly spot prices",
            "",
        )

        # syncronize spot and solarenergy by timestamp
        spots = []
        for s in self.ranked_spot_prices:
            if s["Timestamp"] > ts_now:
                spots.append(
                    {"Timestamp": s["Timestamp"], "PriceWithTax": s["PriceWithTax"]}
                )
        self.info(
            f"Have spot prices for the next {len(spots)} hours",
            "",
        )
        powers = []
        for s in self.ranked_solarpower:
            if s["ts"] > ts_now:
                powers.append({"Timestamp": s["ts"], "Solarenergy": s["solarenergy"]})
            else:
                self.debug(f"Skipped past solar forecast hour {timestampstr(s['ts'])}")

        self.info(
            f"Have solar forecast  for the next {len(powers)} hours",
            "",
        )
        hplan = []
        if len(powers) >= 12:
            for spot, solar in zip(spots, powers):
                # maximum FOM is if spot is negative
                solarenergy = solar["Solarenergy"]
                spotprice = spot["PriceWithTax"]
                fom = self.compute_fom(solarenergy, spotprice)
                plan = {"Timestamp": spot["Timestamp"], "FOM": fom, "Spot": spotprice}
                hplan.append(plan)
        else:
            for spot in spots:
                # maximum FOM is if spot is negative
                solarenergy = 0.0
                spotprice = spot["PriceWithTax"]
                fom = self.compute_fom(solarenergy, spotprice)
                plan = {"Timestamp": spot["Timestamp"], "FOM": fom, "Spot": spotprice}
                hplan.append(plan)

        shplan = sorted(hplan, key=lambda x: x["FOM"], reverse=True)

        self.info(f"Powerplan of {len(shplan)} hours created", str(shplan))
        return shplan

    def create_heating_plan(self) -> list[dict[str, Any]]:
        """Create heating plan.

        Returns:
            int: list of heating entries
        """
        self.info("Creating heating plan", "")
        state = 0
        heating_plan = []
        count: int = 0
        for hp in self.power_plan:
            fom = hp["FOM"]
            spot = hp["Spot"]
            if (
                float(fom) >= self.uoi_limit or float(spot) < self.spot_limit
            ) and count < self.heating_hours_per_day:
                state = 1
            else:
                state = 0
            ts: float = hp["Timestamp"]
            heat = {
                "Unit": "main_boiler",
                "Timestamp": ts,
                "State": state,
                "FOM": fom,
                "UOI": fom,
                "Spot": spot,
            }
            self.debug(
                f"Heating entry {timestampstr(ts)} with spot {spot} and state {state}"
            )
            self.publish(self.topic_powerplan, json.dumps(heat), 1, False)
            heating_plan.append(heat)
            count = count + 1

        return heating_plan
