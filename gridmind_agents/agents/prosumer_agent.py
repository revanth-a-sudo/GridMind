import random


class ProsumerAgent:

    def __init__(self):

        self.base_ev_price = 4.0
        self.base_solar_buyback = 3.5


    def respond(self, status, risk):

        if status != "CRITICAL":
            return "No pricing signal required"

        # simulate number of controllable loads
        ev_chargers = random.randint(3000, 6000)
        home_batteries = random.randint(400, 1200)

        # price adjustment based on risk
        ev_price = self.base_ev_price + (risk * 8)

        solar_buyback = self.base_solar_buyback + (risk * 5)

        return (
            f"EV price signal → ₹{round(ev_price,2)} | "
            f"Solar buyback → ₹{round(solar_buyback,2)} | "
            f"Targets: {ev_chargers} EV chargers, {home_batteries} home batteries"
        )