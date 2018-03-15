from src.constants import PizzaType, PaymentMethod


class TextProcessor:
    @classmethod
    def parse_pizza_type(cls, text):
        return PizzaType.big

    @classmethod
    def parse_payment_method(cls, text):
        return PaymentMethod.card

    @classmethod
    def parse_verifying_order(cls, text) -> bool:
        return True
