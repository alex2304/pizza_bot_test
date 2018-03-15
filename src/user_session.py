from transitions import Machine

from src.constants import PizzaType, PaymentMethod

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

        'conditions': PizzaType.is_valid,

        'before': 'set_pizza_type'
    },
    {
        'trigger': 'approve_payment_method',

        'source': 'waiting_payment_method',
        'dest': 'verifying_order',

        'conditions': PaymentMethod.is_valid,

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
