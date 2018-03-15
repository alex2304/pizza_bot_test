import os
import re
import unicodedata
from collections import defaultdict
from typing import List

import nltk
from pyaspeller import YandexSpeller

from src.text_processing.resources import printable_chars, stopwords_set


class TextProcessor:
    _speller = YandexSpeller()

    _word_re = re.compile('[А-яA-zёЁ]+(?:-[а-яА-Яa-zA-ZёЁ]+)?')

    @classmethod
    def tokenize_and_process(cls, text, strip_accents=True, rm_not_ascii=True, rm_stopwords=True, rm_not_words=True,
                             spell_correct=False):
        if isinstance(text, list):
            text = ' '.join(text)

        if strip_accents:
            text = cls.strip_accents(text, rm_not_ascii=rm_not_ascii)

        tokens = cls.tokenize(text)

        if rm_not_words:
            tokens = cls.rm_not_words(tokens)

        if rm_stopwords:
            tokens = cls.rm_stop_words(tokens)

        if spell_correct:
            tokens = cls.spell_correct(tokens)

        return tokens

    # === TOKENIZING HARD-CODED FROM NLTK ===
    # (in order to don't download megabytes of additional resources won't be used)

    _punkt_tokenizer = nltk.load(os.path.join(os.path.dirname(__file__), 'tokenizers/punkt/english.pickle'))

    _tokenizer = nltk.TreebankWordTokenizer()

    # See discussion on https://github.com/nltk/nltk/pull/1437
    # Adding to TreebankWordTokenizer, the splits on
    # - chervon quotes u'\xab' and u'\xbb' .
    # - unicode quotes u'\u2018', u'\u2019', u'\u201c' and u'\u201d'

    improved_open_quote_regex = re.compile(u'([«“‘])', re.U)
    improved_close_quote_regex = re.compile(u'([»”’])', re.U)
    improved_punct_regex = re.compile(r'([^\.])(\.)([\]\)}>"\'' u'»”’ ' r']*)\s*$', re.U)
    _tokenizer.STARTING_QUOTES.insert(0, (improved_open_quote_regex, r' \1 '))
    _tokenizer.ENDING_QUOTES.insert(0, (improved_close_quote_regex, r' \1 '))
    _tokenizer.PUNCTUATION.insert(0, (improved_punct_regex, r'\1 \2 \3 '))

    @classmethod
    def tokenize(cls, text):
        sentences = cls._punkt_tokenizer.tokenize(text)

        return [token for sent in sentences
                for token in cls._tokenizer.tokenize(sent)]

    # === END HARD-CODED FROM NLTK ===

    # === pre-processing ===

    @classmethod
    def strip_accents(cls, text, rm_not_ascii=True):
        not_accents = []
        exceptions = ['ё', 'й']

        for char in text:
            if rm_not_ascii and char not in printable_chars:
                continue

            char_nfd_form = list(unicodedata.normalize('NFD', char))

            if len(char_nfd_form) == 1:
                if unicodedata.category(char) != 'Mn':
                    not_accents.append(char)

            elif len(char_nfd_form) == 2:
                mark, _ = tuple(char_nfd_form)

                if char.lower() in exceptions:
                    not_accents.append(char)

                else:
                    not_accents.append(mark)

        return ''.join(not_accents)

    @classmethod
    def rm_not_words(cls, tokens: List[str]):
        words_tokens = []

        for t in tokens:
            words_tokens.extend(cls._word_re.findall(t))

        return words_tokens

    @classmethod
    def rm_stop_words(cls, words: List[str]):
        return [w
                for w in words
                if w.lower() not in stopwords_set]

    # === spell correction ===

    @classmethod
    def _get_spell_corrections_dict(cls, *words):
        corrections = defaultdict()

        try:
            words_generator = cls._speller.spell(words)

            for w_info in words_generator:
                corrections[w_info.get('word')] = w_info.get('s')

        except:
            pass

        return corrections

    @classmethod
    def get_spell_correction(cls, word):
        corrections = cls._get_spell_corrections_dict(word)

        return corrections.get(word, [])

    @classmethod
    def spell_correct(cls, tokens: List[str]):
        corrections = cls._get_spell_corrections_dict(*tokens)

        corrected_tokens = []

        for token in tokens:
            token_corrections = corrections.get(token)

            if token_corrections:
                if len(token_corrections) > 1:
                    # several corrections for not-local token
                    print('Warning: ambiguous corrections for non-local token %s: %s' %
                          (token, str(token_corrections)))

                    # accept first 2 corrections
                    corrected_tokens.extend(token_corrections[:2])

                else:
                    # accept first correction
                    corrected_tokens.append(token_corrections[0])

            else:
                # accept token without correction
                corrected_tokens.append(token)

        return corrected_tokens
