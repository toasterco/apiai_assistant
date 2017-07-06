===============
 Corpus module
===============

Corpus Object
=============

.. _corpus:

*class* ``corpus``. **Corpus** (*filepath*)

  Used to managed and access a JSON filed that holds the outputs of an API.ai agent.

  *filepath* is a path to a JSON file as a ``string``.

  The `Corpus`_ class supports the following methods and attributes:

  **init_corpus**\()

    Opens the file at ``filepath`` for reading and loads its content as JSON into ``corpus``.

  **get**\(*key*)

    Inits the corpus if it wasn't initialized yet and returns a random value of **key** within ``corpus``.
    If **key** cannot be found, ``None`` is returned.

  **__getitem__**\(*key*)

    Abstraction for **get()**, allows square bracket notation on ``corpus.Corpus`` instances.

  **__contains__**\(*x*)

    Allows use of the ``in`` operator with ``corpus.Corpus`` instances.
    Inits the corpus if it wasn't initialized yet and returns returns ``True`` if **x** is in ``corpus`` else ``False``.

  **corpus**

    JSON data as a ``dict``

  **filepath**

    Path to a JSON file
