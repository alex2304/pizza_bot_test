from typing import List

from pymorphy2 import MorphAnalyzer


class Parsing:
    def __init__(self, token, lemma, tag):
        self.token = token
        self.lemma = lemma or self.token
        self.tag = tag

    def __eq__(self, other):
        if isinstance(other, Parsing):
            return self.lemma == other.lemma

        elif isinstance(other, str):
            return self.lemma == other

        else:
            raise NotImplementedError(type(other))

    def __hash__(self):
        return hash(self.lemma)

    def __str__(self):
        return self.lemma

    __repr__ = __str__


class ParsedToken:
    def __init__(self, token, parsings: List[Parsing]):
        self.token = token

        self.parsings = []

        # leave ordered unique parsings
        for p in parsings:
            if p not in self.parsings:
                self.parsings.append(p)

    def tag(self):
        return self.parsings[0].tag if self.parsings else self.token

    def lemma(self):
        return self.parsings[0].lemma if self.parsings else self.token

    def __str__(self):
        if self.parsings:
            return str(self.parsings[0])

        return self.token

    def __hash__(self):
        return hash(self.__str__())

    def __eq__(self, other):
        if isinstance(other, str):
            return self.__str__() == other

        elif isinstance(other, ParsedToken):
            return self.__str__() == str(other)

        else:
            raise NotImplementedError(type(other))

    __repr__ = __str__


class MorphParser:
    _morph = MorphAnalyzer()

    @classmethod
    def parse(cls, tokens: List[str]) -> List[ParsedToken]:
        tokens_parsings = []

        for token in tokens:
            pymorphy_parsings = cls._morph.parse(token)

            token_parsings = [Parsing(pp.word,
                                      pp.normal_form,
                                      pp.tag)
                              for pp in pymorphy_parsings]

            tokens_parsings.append(ParsedToken(token, token_parsings))

        return tokens_parsings

    @classmethod
    def lemmatize(cls, tokens: List[str]) -> List[str]:
        if isinstance(tokens, str):
            tokens = [tokens]

        lemmas = [str(parsed_token)
                  for parsed_token in cls.parse(tokens)]

        return lemmas
