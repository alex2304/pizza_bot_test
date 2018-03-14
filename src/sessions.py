from typing import Union, Any

from transitions import Machine

from src.constants import Messages, Options
from src.order_processing import process_order

states = [
    {
        'name': 'initial',
        'on_enter': 'reset_data'
    },
    'waiting_pizza_type',
    'waiting_payment_method',
    'verifying_order'
]

transitions = [
    ['start_ordering', 'initial', 'waiting_pizza_type'],
    {
        'trigger': 'approve_pizza_type',

        'source': 'waiting_pizza_type',
        'dest': 'waiting_payment_method',

        'conditions': Options.is_valid_pizza,

        'before': 'set_pizza_type'
    },
    {
        'trigger': 'approve_payment_method',

        'source': 'waiting_payment_method',
        'dest': 'verifying_order',

        'conditions': Options.is_valid_payment,

        'before': 'set_payment_method'
    },
    ['verify_order', 'verifying_order', 'initial'],
    {
        'trigger': 'decline_order',

        'source': 'verifying_order',
        'dest': 'waiting_pizza_type',

        'after': 'reset_data'
    }
]


class UserSession(Machine):
    def __init__(self, user_id):
        super().__init__(model=self,
                         states=states,
                         initial='initial',
                         transitions=transitions)

        self.user_id = user_id

        self.pizza_type = None
        self.payment_method = None

    def reset_data(self):
        self.pizza_type = None
        self.payment_method = None

    def set_pizza_type(self, pizza_type):
        self.pizza_type = pizza_type

    def set_payment_method(self, payment_method):
        self.payment_method = payment_method

    def __str__(self):
        return 'UserSession(user_id=%s, state=%s, pizza_type=%s, payment_method=%s)' % (self.user_id,
                                                                                        self.state,
                                                                                        self.pizza_type,
                                                                                        self.payment_method)

    __repr__ = __str__

    def get_messages(self, message_text: str) -> Union[list, Any]:
        if self.state == 'initial':
            if self.start_ordering():
                return [Messages.hello, Messages.choose_pizza]

            else:
                return Messages.error

        elif self.state == 'waiting_pizza_type':
            if self.approve_pizza_type(message_text):
                return Messages.choose_payment

            else:
                return Messages.error

        elif self.state == 'waiting_payment_method':
            if self.approve_payment_method(message_text):
                return Messages.verify_order_msg(self.pizza_type, self.payment_method)

            else:
                return Messages.error

        elif self.state == 'verifying_order':
            if message_text == Options.order_decline:
                if self.decline_order():
                    return [Messages.restart_order, Messages.choose_pizza]

                else:
                    return Messages.error

            elif message_text == Options.order_verify:
                if self.verify_order():
                    # further order processing
                    process_order(self.user_id, self.pizza_type, self.payment_method)

                    return Messages.order_created

                else:
                    return Messages.error

        return Messages.error

# if __name__ == '__main__':
#     session = UserSession('1488')
#
#     session.start_ordering()
#
#     print(session.approve_pizza_type(pizza_type=PizzaType.big))
#
#     print(session.approve_payment_method(payment_method=PaymentMethod.card))
#
#     print(session.decline_order())
#     print(session)
