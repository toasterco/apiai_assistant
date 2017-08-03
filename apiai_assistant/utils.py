""" Utils

Provides utility functions for the modules of the apiai_assistant package """

import re


NUMBER_WORDS = {
    'and': (1, 0), 'twelve': (1, 12), 'seven': (1, 7),
    'trillion': (1000000000000, 0), 'ten': (1, 10), 'seventeen': (1, 17),
    'two': (1, 2), 'four': (1, 4), 'zero': (1, 0), 'eighteen': (1, 18),
    'thirteen': (1, 13), '': (1, 10), 'one': (1, 1), 'fifty': (1, 50),
    'nineteen': (1, 19), 'six': (1, 6), 'three': (1, 3), 'eleven': (1, 11),
    'hundred': (100, 0), 'thousand': (1000, 0), 'million': (1000000, 0),
    'eighty': (1, 80), 'fourteen': (1, 14), 'five': (1, 5), 'sixty': (1, 60),
    'sixteen': (1, 16), 'fifteen': (1, 15), 'seventy': (1, 70),
    'billion': (1000000000, 0), 'forty': (1, 40), 'thirty': (1, 30),
    'ninety': (1, 90), 'nine': (1, 9), 'twenty': (1, 20), 'eight': (1, 8)
}


def text_to_int(textnum):
    """ Translates the string representation of a number to an int

    Args:
        textnum (str): string to translate

    Returns:
        :obj:`int` translated string literal

    http://stackoverflow.com/questions/493174/is-there-a-way-to-convert-number-words-to-integers
    """

    try:
        return float(textnum)
    except ValueError:
        pass

    ordinal_words = {
        'first': 1, 'second': 2, 'third': 3, 'fifth': 5,
        'eighth': 8, 'ninth': 9, 'twelfth': 12}

    ordinal_endings = [('ieth', 'y'), ('th', '')]
    current = result = 0
    for word in re.split('[ \-]', textnum):
        if word in ordinal_words:
            scale, increment = (1, ordinal_words[word])
        else:
            for ending, replacement in ordinal_endings:
                if word.endswith(ending):
                    word = "%s%s" % (word[:-len(ending)], replacement)

            if word not in NUMBER_WORDS:
                if word[0].isdigit() and word[-2:] in {'st', 'nd', 'rd', 'th'}:
                    return text_to_int(word[:-2])
                try:
                    return float(word)
                except:
                    raise Exception("Illegal word: " + word)

            scale, increment = NUMBER_WORDS[word]

        current = current * scale + increment
        if scale > 100:
            result += current
            current = 0

    return result + current


def enum(*sequential, **named):
    """ Dynamically creates an enum object

    Args:
        sequential (:obj:`list`): sequence of enum values
        named (:obj:`dict`): map of enum values with their name and respective value

    Returns:
        :obj:`Enum` an Enum object
    """

    enums = dict(zip(sequential, range(len(sequential))), **named)
    by_value = dict((value, key) for key, value in enums.iteritems())
    by_key = dict((key, value) for key, value in enums.iteritems())
    enums['keys'] = by_value.keys()
    enums['values'] = by_key.values()
    enums['by_value'] = by_value
    enums['by_key'] = by_key
    return type('Enum', (), enums)


def readable_list(elements, liaison='and'):
    """ Creates a readable sentence by joining elements of a list

    Args:
        elements (:obj:`list` of :obj:`str`): elements to join together
        liaison (`str`, optional, 'and'): liaison to use to join elements

    Returns:
        `str` A human readable sentence joining all elements
    """

    if not elements:
        return ""

    if len(elements) == 1:
        return str(elements[0])

    if len(elements) == 2:
        return '{} {} {}'.format(elements[0], liaison, elements[1])

    # "Oxford comma innit" -Zack, France
    return "{}, {} {}".format(
        ', '.join((str(e) for e in elements[:-1])),
        liaison,
        elements[-1])
