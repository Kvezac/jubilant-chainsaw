import uuid
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_EVEN


@dataclass
class Calculate:
    weight_factor: Decimal = Decimal("0.5")
    content_factor: Decimal = Decimal("0.01")

    def calculate_cost(self, weight: Decimal, cost_content: Decimal, dollar_rate: Decimal) -> Decimal:
        cost = (self.weight * self.weight_factor + self.cost_content * self.content_factor) * self.dollar_rate
        return self.round_cost(cost)

    @staticmethod
    def round_cost(value: Decimal, places: int = 2) -> Decimal:
        rounded_value = value.quantize(Decimal(f"0.{'0' * places}"), rounding=ROUND_HALF_EVEN)
        return rounded_value

    def create_session_token(self):
        token = str(uuid.uuid4())
        return token
