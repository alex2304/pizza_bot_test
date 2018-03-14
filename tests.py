from unittest import TestCase

from src.constants import Messages, Options
from src.sessions import UserSession


class TestInitDialog(TestCase):
    def setUp(self):
        self.user_session = UserSession('1488228')

    # === test dialog initializing ===

    def test_init_dialog(self):
        messages = self.user_session.get_messages('любое сообщение для начала диалога')

        self.assertEqual(len(messages), 2, msg='в первом состоянии должно быть два сообщения')

        self.assertListEqual(messages, [Messages.hello, Messages.choose_pizza])

        self.assertTrue(self.user_session.is_waiting_pizza_type())


class TestChoosingPizzaDialog(TestCase):
    def setUp(self):
        self.user_session = UserSession('1488228')

        self.user_session.to_waiting_pizza_type()

    # === test pizza choosing ===

    def test_pizza_choosing_wrong_choice(self):
        previous_state = self.user_session.state

        message = self.user_session.get_messages('любой неверный выбор')

        self.assertEqual(message, Messages.error)

        self.assertEqual(self.user_session.state, previous_state)

    def test_pizza_choosing_small_pizza_choice(self):
        message = self.user_session.get_messages(Options.pizza_small)

        self.assertEqual(message, Messages.choose_payment)

        self.assertTrue(self.user_session.is_waiting_payment_method())

        self.assertEqual(self.user_session.pizza_type, Options.pizza_small)

    def test_pizza_choosing_big_pizza_choice(self):
        message = self.user_session.get_messages(Options.pizza_big)

        self.assertEqual(message, Messages.choose_payment)

        self.assertTrue(self.user_session.is_waiting_payment_method())

        self.assertEqual(self.user_session.pizza_type, Options.pizza_big)


class TestChoosingPaymentDialog(TestCase):
    def setUp(self):
        self.user_session = UserSession('1488228')

        self.user_session.to_waiting_pizza_type()

        self.user_session.get_messages(Options.pizza_big)

    # === test payment method choosing ===

    def test_payment_choosing_wrong_choice(self):
        previous_state = self.user_session.state

        message = self.user_session.get_messages('любой неверный выбор')

        self.assertEqual(message, Messages.error)

        self.assertEqual(previous_state, self.user_session.state)

    def test_payment_choosing_cash_choice(self):
        message = self.user_session.get_messages(Options.payment_cash)

        self.assertEqual(message, Messages.verify_order_msg(Options.pizza_big, Options.payment_cash))

        self.assertTrue(self.user_session.is_verifying_order())

        self.assertEqual(self.user_session.payment_method, Options.payment_cash)

    def test_payment_choosing_card_choice(self):
        message = self.user_session.get_messages(Options.payment_card)

        self.assertEqual(message, Messages.verify_order_msg(Options.pizza_big, Options.payment_card))

        self.assertTrue(self.user_session.is_verifying_order())

        self.assertEqual(self.user_session.payment_method, Options.payment_card)


class TestOrderVerifyingDialog(TestCase):
    def setUp(self):
        self.user_session = UserSession('1488228')

        self.user_session.to_waiting_pizza_type()

        self.user_session.get_messages(Options.pizza_big)

        self.user_session.get_messages(Options.payment_card)

    # === test order verifying ===

    def test_order_verifying_wrong_choice(self):
        previous_state = self.user_session.state

        message = self.user_session.get_messages('любой неверный выбор')

        self.assertEqual(message, Messages.error)

        self.assertEqual(self.user_session.state, previous_state)

    def test_order_verifying_verify_choice(self):
        message = self.user_session.get_messages(Options.order_verify)

        self.assertEqual(message, Messages.order_created)

        self.assertTrue(self.user_session.is_initial())

    def test_order_verifying_decline_choice(self):
        messages = self.user_session.get_messages(Options.order_decline)

        self.assertListEqual(messages, [Messages.restart_order, Messages.choose_pizza])

        self.assertTrue(self.user_session.is_waiting_pizza_type())
