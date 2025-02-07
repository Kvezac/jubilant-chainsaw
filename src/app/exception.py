class DeliveryNotFound(Exception):
    detail = "Delivery not found"


class DollarNotFound(Exception):
    detail = "The dollar exchange rate is not set"
