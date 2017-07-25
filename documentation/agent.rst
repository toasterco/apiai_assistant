==============
 Agent module
==============

Module Contents
===============

``agent``. **Status**
  Different statuses of an ``agent``. Agent_ or ``agent``. Response_ object

  Possible values for statuses are

  - 'OK': nothing to report
  - 'GenericError': something went wrong
  - 'InvalidData': malformed or missing data in the request
  - 'AccessDenied': could not verify the origin of the request
  - 'Aborted': the user aborted the process
  - 'NotImplemented': incomplete implementation

Agent Object
============

.. _agent:

*class* ``agent``. **Agent**\([*corpus* [, *request* [, *ssml=True*])
  Provides methods to instruct the agent on how to respond tu user queries.

  *corpus* must be a `corpus.Corpus <corpus.rst#corpus>`_ instance

  *request* is the API.ai POST request as a ``dict``

  *ssml* is a flag to enable or disable the formatting of speech messages to enable `Speech Synthesis Markup Language <https://developers.google.com/actions/reference/ssml>`_

  The `Agent`_ class supports the following methods and attributes:

  **abort**\(*reason*)
    Sets ``code`` to ``Status.Aborted`` and ``error_message`` to **reason** for the agent instance and aborts response with the same code and error message

  **error**\(*error_message* [, *code=Status.GenericError*])
    Sets ``code`` to **code** and ``error_message`` to **error_message** for the agent instance and aborts response with the same code and error message

  **tell**\(*corpus_id* [, *context*])
    Looks for the **corpus_id** in the corpus and formats with the ``dict`` **context** to create a ``widgets.SimpleResponseWidget`` and passes it down to **show()**, the mic will also be closed.

  **ask**\(*corpus_id* [, *context*])
    Looks for the **corpus_id** in the corpus and formats with the ``dict`` **context** to create a ``widgets.SimpleResponseWidget`` and passes it down to **show()**.

  **suggest**\(*corpus_id*)
    Looks for the **corpus_id** in the corpus to create a ``widgets.SuggestionWidget``  and passes it down to **show()**

  **ask_for_confirmation**\(*corpus_id*)
    Looks for the **corpus_id** in the corpus and passes it down to ``agent.ask()``, then suggests a confirmation from the corpus using ``agent.suggest_raw()``

  **tell_raw**\(*speech* [, *text*])
    Creates a ``widgets.SimpleResponseWidget`` with the **speech** and **text** and passes it down to **show()**, the mic will also be closed.

  **ask_raw**\(*speech* [, *text*])
    Creates a ``widgets.SimpleResponseWidget`` with the **speech** and **text** and passes it down to **show()**.

  **suggest_raw**\(*suggestions*)
    **suggestions** can be a list of strings or a simple string

    Creates a ``widgets.SuggestionWidget`` with **suggestions** and passes it down to **show()**

  **ask_for_confirmation_raw**\(*question*)
    Passes *question* to ``agent.ask_raw()``, then suggests a confirmation from the corpus using ``agent.suggest_raw()``.

  **show**\(*obj*)
    Renders a response widget and adds it to ``response.messages``

  **add_context**\(*context_name* [, *parameters* [, *lifespan=5*])
    Adds a context to ``response._contexts``

    **context_name** name of the context to add

    **parameters** parameters of the context

    **lifespan** lifespan of the context

  **ask_for_permissions**\(*reason*, *permissions*)
    Adds a permission to ``response._permissions``

    Permissions are formatted when ``Response.to_dict`` is called so you can use ``ask_for_permissions`` more than once and all permissions will be requested at once.

    **reason** textual reason for requesting the permissions as a ``string`` (see `Requesting Permissions <../README.rst#requesting-permissions>`_ to learn more)

    **permissions** a ``list`` of ``agent.SupportedPermissions``

  **code**
    Status of the instance

  **error_message**
    ``None`` if instance is healthy (``code == Status.OK``) else the reason why it is not

  **parser**
    ``parser.GoogleAssistantParser`` instance initialized with the ``request`` when initializing the agent instance

  **response**
    ``agent.Response`` instance

  **SupportedPermissions**
    `utils.Enum <utils.rst#enum>`_ object of keys `NAME`, `COARSE_LOCATION`, and `PRECISE_LOCATION`


Response Object
===============

.. _response:

*class* ``agent``. **Response**
  Abstraction to build API.ai compatible responses.

  The `Response`_ class supports the following methods:

  **abort**\(*error_message* [, *code=Status.GenericError*])
    Sets ``code`` to **code** and ``error_message`` to **error_message**

  **close_mic**\()
    Sets ``expect_user_response`` to ``False``

  **open_mic**\()
    Sets ``expect_user_response`` to ``True``

  **add_message**\(*message*, [, *position*])
    Appends **message** in ``_messages`` or inserts it at position **position**

  **add_context**\(*context*, [, *position*])
    Appends **context** in ``_contexts`` or inserts it at position **position**

  **add_permission**\(*reason*, *permissions*)
    Resolve ``string`` values of the *permissions* and appends a tuple of ``reason`` and the resolved ``permissions`` in ``_permissions``.

    Permissions are formatted when ``Response.to_dict`` is called so you can use ``add_permission`` more than once and all permissions will be requested at once.

  **to_dict**\()
    Formats the ``Response`` instance to a ``dict``

    If ``code`` is anything different than ``Status.OK``, **to_dict()** will return an error payload

  **PERMISSIONS**
    ``dict`` mapping of ``Agent.SupportedPermissions`` to their ``string`` equivalent for the Actions on Google integration
