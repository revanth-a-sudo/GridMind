class DecisionAgent:

    def evaluate(self, risk):

        if risk < 0.35:
            return "STABLE"

        elif risk < 0.65:
            return "WARNING"

        else:
            return "CRITICAL"