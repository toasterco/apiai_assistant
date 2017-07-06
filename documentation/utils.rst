==============
 Utils module
==============

Module Contents
===============

``utils``. **NUMBER_WORDS**

  Mapping of words to numbers, used by **text_to_int()**

``utils``. **text_to_int**\(*textnum*)

  Translates the **textnum**, a ``string`` representation of a number, to an ``int``

  Raises ``Exception`` if a part of **textnum** couldn't be found in ``utils.NUMBER_WORDS``

``utils``. **enum**\(*\*sequential*, *\*\*named*)

  Dynamically creates an enumeration object of type ``Enum``.

  The ``Enum`` object will have attributes named after sequence of strings, of which the values are increments of 1 starting at 0.

  The ``Enum`` class supports the following attributes:

  **by_values**

    ``dict`` of keys mapped to their value

  **by_key**

    ``dict`` of values mapped to their key

  **keys**

    Iterable of the instance's keys

  **values**

    Iterable of the instance's values


``utils``. **readable_list**\(*elements* [, *lisaision='and'*])

  Creates a readable sentence by joining the elements of **elements**:

.. code:: python

  >>> names = ['Zack', 'Jonny', 'Lisa']
  >>> readable_list(['Zack'])
  'Zack'
  >>> readable_list(['Zack', 'Jonny'])
  'Zack and Jonny'
  >>> readable_list(['Zack', 'Jonny', 'Lisa'])
  'Zack, Jonny, and Lisa'
  >>> readable_list(['Zack', 'Jonny', 'Lisa'], liaison='or')
  'Zack, Jonny, or Lisa'

