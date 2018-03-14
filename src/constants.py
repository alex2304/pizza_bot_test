class PizzaType:
    big = 'big'
    small = 'small'

    @classmethod
    def is_valid(cls, pizza_type: str):
        return pizza_type in vars(cls)


class PaymentMethod:
    cash = 'cash'
    card = 'card'

    @classmethod
    def is_valid(cls, payment_method: str):
        return payment_method in vars(cls)


class Options:
    pizza_big = 'Большую'
    pizza_small = 'Маленькую'

    payment_card = 'Картой'
    payment_cash = 'Наличкой'

    order_verify = 'Да'
    order_decline = 'Нет'

    @classmethod
    def is_valid_pizza(cls, pizza_option):
        return pizza_option in (cls.pizza_big, cls.pizza_small)

    @classmethod
    def is_valid_payment(cls, payment_option):
        return payment_option in (cls.payment_card, cls.payment_cash)


class Messages:
    error = {
        'message': 'Попробуй ещё раз'
    }

    hello = {
        'message': 'Я могу принять Ваш заказ на вкусную пиццу.'
    }

    restart_order = {
        'message': 'Окей. Давайте начнём сначала:'
    }

    order_created = {
        'message': 'Ваш заказ принят!',
        'options': '👍'
    }

    choose_pizza = {
        'message': 'Какую пиццу Вы хотите?',
        'options': [Options.pizza_big,
                    Options.pizza_small]
    }

    choose_payment = {
        'message': 'Какой способ оплаты предпочитаете?',
        'options': [Options.payment_card,
                    Options.payment_cash]
    }

    @classmethod
    def verify_order_msg(cls, pizza_type, payment_method):
        return {
            'message': 'Вы хотите %s пиццу, оплата - %s?' % (pizza_type, payment_method),
            'options': [Options.order_verify,
                        Options.order_decline]
        }
