from src.constants import Messages, PizzaType, PaymentMethod
from src.order_processing import process_order
from src.user_session import UserSession
from src.text_processing import TextProcessor


class DialogEngine:
    @classmethod
    def process_message(cls, session: UserSession, message_text: str):
        if session.state == 'initial':
            if session.start_ordering():
                return [Messages.hello, Messages.choose_pizza]

            else:
                return Messages.error

        elif session.state == 'waiting_pizza_type':
            pizza_type = cls.parse_pizza_type(message_text)

            if pizza_type is None:
                return Messages.error

            if session.approve_pizza_type(pizza_type):
                return Messages.choose_payment

            else:
                return Messages.error

        elif session.state == 'waiting_payment_method':
            payment_method = cls.parse_payment_method(message_text)

            if payment_method is None:
                return Messages.error

            if session.approve_payment_method(payment_method):
                return Messages.verify_order_msg(session.pizza_type, session.payment_method)

            else:
                return Messages.error

        elif session.state == 'verifying_order':
            order_was_verified = cls.parse_verifying_order(message_text)

            if not order_was_verified:
                if session.decline_order():
                    return [Messages.restart_order, Messages.choose_pizza]

                else:
                    return Messages.error

            else:
                if session.verify_order():
                    # TODO: further order processing here
                    process_order(session.user_id, session.pizza_type, session.payment_method)

                    return Messages.order_created

                else:
                    return Messages.error

        return Messages.error

    @classmethod
    def parse_pizza_type(cls, text):
        return PizzaType.big

    @classmethod
    def parse_payment_method(cls, text):
        return PaymentMethod.card

    @classmethod
    def parse_verifying_order(cls, text) -> bool:
        return True