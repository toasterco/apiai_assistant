==================
 Assistant module
==================

Assistant Object
================

.. _assistant:

*class* ``assistant``. **Assistant**\([*ssml=True* [, *corpus* [, *magic_key*])
  Entrypoint for the apiai_assistant package. The Assistant class manages the different intents of the agent and processes the requests.

  *ssml* is a flag to enable or disable the formatting of speech messages to enable `Speech Synthesis Markup Language <https://developers.google.com/actions/reference/ssml>`_

  *corpus* is a path to a JSON file as a ``string``.

  *magic_key* is the ``string`` value of the magic key to match from the request header to verifiy the incoming requests.

  The `Assistant`_ class supports the following methods and attributes:

  **intent**\(*action_id*)
    Decorates a function to register it as an intent in the ``assistant.Assistant`` instance's ``action_map``.

    The decorated function takes an ``agent.Agent`` as its sole parameter.

  **validate**\(*agent_instance*)
    Performs a series of validation checks on the ``agent.Agent`` instance **agent_instance**.

    Returns ``True`` if **agent_instance** is valid, ``False`` otherwise and sets the apporpriate ``code`` and ``error_message`` on **agent_instance**.

  **process**\(*request* [, *headers*])
    Process the API.ai request **request** and returns an ``agent.Agent`` instance with the performed action in it.

    If **headers** is a non-empty ``dict`` and contains a non-empty ``magic-key`` key, the ``magic_key`` of the ``assistant.Assistant`` instance is compared to the ``magic-key`` of the ``dict`` **headers** to verify the origin of the API.ai request.

  **action_map**
    ``dict`` of the registered intents through **assistant.Assistant.intent**, the keys being the ids of the intents and the values a reference to the function decorated

  **corpus**
    ``None`` if no path to a corpus was passed when initializing the instance, otherwise an instance of `corpus.Corpus <corpus.rst#corpus>`_

  **magic_key**
    Key compared to a ``magic-key`` header when verifying the origin of a request
