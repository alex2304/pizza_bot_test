from typing import Union

from src.constants import Messages, PizzaType, PaymentMethod
from src.order_processing import process_order
from src.text_processing.morph import MorphParser
from src.text_processing.processor import TextProcessor
from src.user_session import UserSession


class DialogEngine:
    keywords = {
        PizzaType.big: 'большая, огромная, побольше',
        PizzaType.small: 'небольшая, маленькая, поменьше',

        PaymentMethod.card: 'банковская карта, перевод',
        PaymentMethod.cash: 'наличка, кэш',

        'yes': 'да, ок, верно, правильно, ага, угу',
        'no': 'нет, отмена, неверно, неправильно, не, неа'
    }

    lemmas = {}

    for k in keywords.keys():
        lemmas[k] = set(MorphParser.lemmatize(TextProcessor.tokenize_and_process(keywords[k], rm_stopwords=False)))

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
    def _match_keywords(cls, text, keys) -> Union[str, None]:
        """
        Process given text and find matches of text lemma with lemmas of given keys.

        :param text: text for processing
        :param keys: list of keys from cls.keywords dict
        :return: None if found 0 or more than 1 matches, otherwise - key which lemmas were matched
        """
        tokens = TextProcessor.tokenize_and_process(text, rm_stopwords=False, spell_correct=True)

        lemmas = MorphParser.lemmatize(tokens)

        keys_matches = [(key, cls.lemmas[key].intersection(lemmas))
                        for key in keys]

        # remove empty sets
        keys_matches = list(filter(lambda k_m: k_m[1], keys_matches))

        if len(keys_matches) != 1:
            return None

        # return key which has matches
        return keys_matches[0][0]

    @classmethod
    def parse_pizza_type(cls, text):
        return cls._match_keywords(text, keys=[PizzaType.small, PizzaType.big])

    @classmethod
    def parse_payment_method(cls, text):
        return cls._match_keywords(text, keys=[PaymentMethod.card, PaymentMethod.cash])

    @classmethod
    def parse_verifying_order(cls, text) -> bool:
        return cls._match_keywords(text, keys=['yes', 'no']) == 'yes'
