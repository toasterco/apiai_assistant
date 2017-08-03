=======
 Index
=======

* `Assistant <#assistant>`__

* `Agent <#agent>`__

  * `Response <#response>`__

* `Corpus <#corpus>`__

* `Utils <#utils>`__

* `Parser <#parser>`__

  * `User <#user>`__

  * `PayloadParser <#payloadparser>`__

  * `GoogleAssistantPayloadParser <#googleassistantpayloadparser>`__

* `Widgets <#widgets>`__

  * `InvalidGoogleAssistantWidget <#invalidgoogleassistantwidget>`__

  * `GoogleAssistantWidget <#googleassistantwidget>`__

  * `SimpleResponseWidget <#simpleresponsewidget>`__

  * `SuggestionsWidget <#suggestionswidget>`__

  * `LinkOutChipWidget <#linkoutchipwidget>`__

  * `ImageCardWidget <#imagecardwidget>`__

  * `Image <#image>`__

  * `Button <#button>`__

  * `ListSelectWidget <#listselectwidget>`__

  * `CarouselSelectWidget <#carouselselectwidget>`__

  * `SelectItem <#selectitem>`__

  * `OptionInfo <#optioninfo>`__


------------------------------------------

Assistant Module
================

Assistant Object
----------------

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
    ``None`` if no path to a corpus was passed when initializing the instance, otherwise an instance of `corpus.Corpus <#corpus>`__

  **magic_key**
    Key compared to a ``magic-key`` header when verifying the origin of a request



------------------------------------------

Agent Module
============

Module Contents
---------------

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
------------

.. _agent:

*class* ``agent``. **Agent**\([*corpus* [, *request* [, *ssml=True*])
  Provides methods to instruct the agent on how to respond tu user queries.

  *corpus* must be a `corpus.Corpus <#corpus>`_ instance

  *request* is the API.ai POST request as a ``dict``

  *ssml* is a flag to enable or disable the formatting of speech messages to enable `Speech Synthesis Markup Language <https://developers.google.com/actions/reference/ssml>`__

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

    **reason** textual reason for requesting the permissions as a ``string`` (see `Requesting Permissions <../#requesting-permissions>`_ to learn more)

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
    `utils.Enum <#enum>`_ object of keys `NAME`, `COARSE_LOCATION`, and `PRECISE_LOCATION`


Response Object
---------------

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



------------------------------------------

Corpus Module
=============

Corpus Object
-------------

.. _corpus:

*class* ``corpus``. **Corpus** (*filepath*)
  Used to managed and access a JSON filed that holds the outputs of an API.ai agent.

  *filepath* is a path to a JSON file as a ``string``.

  The `Corpus`_ class supports the following methods and attributes:

  **init_corpus**\()
    Opens the file at ``filepath`` for reading and loads its content as JSON into ``corpus``.

  **validate**\(*data*)
    Returns ``True`` if the ``dict`` **data** object is a valid corpus JSON object. False otherwise.

  **get**\(*key*)
    Inits the corpus if it wasn't initialized yet and returns a random value of **key** within ``corpus``.
    If **key** cannot be found, ``None`` is returned.

  **get_confirmation**\()
    Inits the corpus if it wasn't initialized yet and returns a random confirmation.

  **__getitem__**\(*key*)
    Abstraction for **get()**, allows square bracket notation on ``corpus.Corpus`` instances.

  **__contains__**\(*x*)
    Allows use of the ``in`` operator with ``corpus.Corpus`` instances.
    Inits the corpus if it wasn't initialized yet and returns returns ``True`` if **x** is in ``corpus`` else ``False``.

  **corpus**
    JSON data as a ``dict``

  **filepath**
    Path to a JSON file

  **DEFAULT_CONFIRMATIONS**
    Default confirmations used if not found in the JSON object.



------------------------------------------

.. _utils:

Utils Module
============

Provides utility functions for the modules of the apiai_assistant package.

Module Contents
---------------

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

    >>> readable_list(['Zack'])
    'Zack'
    >>> readable_list(['Zack', 'Jonny'])
    'Zack and Jonny'
    >>> readable_list(['Zack', 'Jonny', 'Lisa'])
    'Zack, Jonny, and Lisa'
    >>> readable_list(['Zack', 'Jonny', 'Lisa'], liaison='or')
    'Zack, Jonny, or Lisa'



------------------------------------------

.. _parser:

Parser Module
=============

Provides Actions on Google Parser classes to read from the API.ai POST request payload and offers abstractions to access objects of the payload.

Device Object
-------------

.. _device:

*class* ``parser``. **Device**\([*device_id* [, *coordinates* [, *address* [, *city* [, *zip_code*])
  A simple device class used to encapsulate the device object from the API.ai request

  *device_id* id of the device as a ``str``

  *coordinates* coordinates of the device as a ``dict``

  *address* formatted address of the device as a ``str``

  *city* city of the device a ``str``

  *zip_code* zip code of the device as a ``str``

  *phone_number* phone number of the location as a ``str``

  *notes* notes about the location of the device as a ``str``

  The `Device`_ class supports the following attributes:

  **coordinates**
    Longitude and lattitude of the device.

  **address**
    Formatted address of the device.

  **city**
    City of the device.

  **zip_code**
    Zip code.

  **phone_number**
    Phone number if available.

  **notes**
    Notes if any.

  **id**
    ID of the device.


User Object
-----------

.. _user:

*class* ``parser``. **User**\(*user_id* [, *locale* [, *display_name* [, *given_name* [, *family_name* [, *device*])
  A simple user class used to encapsulate the user object from the API.ai request

  *user_id* id of the user as a ``str``

  *locale* locale of the user as a ``str``

  *display_name* display name of the user as a ``str``

  *given_name* given name of the user as a ``str``

  *family_name* family name of the user as a ``str``

  *device* device of the user as a `Device`_

  The `User`_ class supports the following attributes:

  **display_name**
    Display name of the user.

  **given_name**
    Given name of the user (first name).

  **family_name**
    Family name of the user (last name).

  **device**
    Device the user is using. Contains information abotu the user's location.

  **locale**
    Locale of the user.

  **id**
    ID of the user.


PayloadParser Object
--------------------

.. _PayloadParser:

*class* ``parser``. **PayloadParser**\(*data*)
  Base class for all parsers

  *data* API.ai POST payload as a ``dict``

  The `PayloadParser`_ class supports the following methods and attributes:

  **get**\(*param* [, *default* [, *_type* [, *globbing=False*])
    General getter to access parameters inside the API.ai request.

    **param** key of the parameter to get

    **default** default value to be returned if the parameter could not be found

    **_type** one of ``parser.PayloadParser.PARAM_TYPES`` to format the parameter's value, mostly used for numbers

    **globbing** if ``True``, will also get the values of numbered parameters that have the base name **param** (i.e.: ``given-name``, ``given-name2``, ``given-name3``)

  **is_valid**
    Validation property that must be implemented to validate the parser and data.

  The following is defined as clas-level attribute of ``PaylaodParser``:

  **PARAM_TYPES**
    `utils.Enum <#enum>`__ object of keys `NUMBER`, `STRING`, and `LIST`

GoogleAssistantPayloadParser Object
------------------------------------

.. _GoogleAssistantPayloadParser:

*class* ``parser``. **GoogleAssistantPaylaodParser**\(*data*)
  Parser for the Actions on Google API.ai integration

  *data* API.ai POST payload as a ``dict``

  The `GoogleAssistantPayloadParser`_ class supports the following methods and attributes:

  **get**\(*param* [, *default* [, *_type* [, *globbing=False*])
    General getter to access parameters inside the API.ai request.

    **param** key of the parameter to get

    **default** default value to be returned if the parameter could not be found

    **_type** one of ``parser.PayloadParser.PARAM_TYPES`` to format the parameter's value, mostly used for numbers

    **globbing** if ``True``, will also get the values of numbered parameters that have the base name **param** (i.e.: ``given-name``, ``given-name2``, ``given-name3``)

  **_init_user**\()
    Returns a User_ instance initialized with data from the API.ai request.

  **get_contexts**\([*name*])
    Get the contexts from the request data as a ``list`` of ``dict``.

    If **name** is not ``None``, it will look for a context named **name** and return its parameters if found, otherwise an empty ``dict``.

  **has_screen_capability**\()
    Returns ``True`` if the device the request originated from has a screen capability, ``False`` otherwise.

  **has_audio_capability**\()
    Returns ``True`` if the device the request originated from has an audio capability, ``False`` otherwise.

  **is_valid**
    Validation property that must be implemented to validate the parser and data.

  **PARAM_TYPES**
    `utils.Enum <#enum>`__ object of keys `NUMBER`, `STRING`, and `LIST`.

  **action**
    Property that gets the action from the request data.

  **parameters**
    Property that gets the parameters from the request data as a ``dict``.

  **request**
    Property that returns the ``result`` object from the API.ai request.

  **capabilities**
    Property that returns the names of the ``capabilities`` from the request.

  **user**
    Property that returns the initialized User_ instance.

  **device**
    Property that returns the Device_ from the initialized User_ instance.



------------------------------------------

.. _widgets:

Widgets Module
==============

Module Contents
---------------

.. _InvalidGoogleAssistantWidget:

*exception* **InvalidGoogleAssistantWidget**
  Raised when a widget isn't initialized properly


GoogleAssistantWidget Object
----------------------------

.. _GoogleAssistantWidget:

*class* ``widgets``. **GoogleAssistantWidget**\()
  Base class for `Actions on Google widgets <https://developers.google.com/actions/assistant/responses>`_.

  The `GoogleAssistantWidget`_ class supports the following methods and attributes:

  **platform**
    Platform the widget is supported on, always ``google``.

  **render**\()
    Renders the widget to a ``dict`` that is ready to be added to the API.ai response messages.


SimpleResponseWidget Object
---------------------------

.. _SimpleResponseWidget:

*class* ``widgets``. **SimpleResponseWidget**\(*speech*, *text* [, *ssml=True*])
  Abstraction for `SimpleResponse <https://developers.google.com/actions/reference/rest/Shared.Types/AppResponse#simpleresponse>`__ Actions on Google object.

  | *speech*
  |   Text to be spoken out as a ``string``
  |
  | *text*
  |   Text to be displayed as a ``string``.
  |   If ``None``, **speech** will be used as the text to be displayed.
  |   If an empty ``string``, the display text will stay empty (note that you will have to provide an other type of text display to form a valid Actions on Google response)
  |
  | *ssml*
  |   If ``True``, the **speech** will be formated to enable SSML
  |

  `InvalidGoogleAssistantWidget`_ is raised if **speech** and **text** are ``None``.

  The `SimpleResponseWidget`_ class supports the following methods and attributes:

  **platform**
    Platform the widget is supported on, always ``google``.

  **type**
    Required by Actions on Google to identify the type of the response, always ``simple_response``

  **render**\()
    Renders the widget to a ``dict`` that is ready to be added to the API.ai response messages.

  **ssml_format**\(*s*)
    Formats the ``string`` **s** to SSML (essentially wrapping it in a ``speak`` tag)

SuggestionsWidget Object
------------------------

.. _SuggestionsWidget:

*class* ``widgets``. **SuggestionsWidget**\(*suggestions*)
  Abstraction for `Suggestions <https://developers.google.com/actions/reference/rest/Shared.Types/AppResponse#richresponse>`__ Actions on Google object.

  *suggestions*
    Title of the suggestions as a ``list`` of ``string``.

  The `SuggestionsWidget`_ class supports the following methods and attributes:

  **platform**
    Platform the widget is supported on, always ``google``.

  **type**
    Required by Actions on Google to identify the type of the response, always ``suggestion_chips``

  **render**\()
    Renders the widget to a ``dict`` that is ready to be added to the API.ai response messages.


LinkOutChipWidget Object
------------------------

.. _LinkOutChipWidget:

*class* ``widgets``. **LinkOutChipWidget**\(*title*, *url*)
  Abstraction for `LinkOutChip <https://developers.google.com/actions/reference/rest/Shared.Types/AppResponse#LinkOutSuggestion>`__ Actions on Google object.

  *title*
    Title of the chip as a ``string``.

  *url*
    URL target of the chip as a ``string``.

  The `LinkOutChipWidget`_ class supports the following methods and attributes:

  **platform**
    Platform the widget is supported on, always ``google``.

  **type**
    Required by Actions on Google to identify the type of the response, always ``link_out_chip``

  **render**\()
    Renders the widget to a ``dict`` that is ready to be added to the API.ai response messages.


ImageCardWidget Object
----------------------

.. _ImageCardWidget:

*class* ``widgets``. **ImageCardWidget**\(*title* [, *text* [, *image* [, *button*])
  Abstraction for `ImageCard <https://developers.google.com/actions/reference/rest/Shared.Types/AppResponse#basiccard>`__ Actions on Google object.

  *title*
    Title of the card as a ``string``.

  *text*
    Text dscription of the card as a ``string``.

  *image*
    Image of the card as a `Image`_ instance.

  *button*
    CTA button of the card as a `Button`_ instance.

  `InvalidGoogleAssistantWidget`_ is raised if **text** and **image** are ``None``.

  The `ImageCardWidget`_ class supports the following methods and attributes:

  **platform**
    Platform the widget is supported on, always ``google``.

  **type**
    Required by Actions on Google to identify the type of the response, always ``basic_card``

  **render**\()
    Renders the widget to a ``dict`` that is ready to be added to the API.ai response messages.


Image Object
------------

.. _Image:

*class* ``widgets``. **Image**\(*url* [, *alt*])
  Abstraction for `Image <https://developers.google.com/actions/reference/rest/Shared.Types/Image>`__ Actions on Google object.

  *url*
    URL where the image is hosted as a ``string``.

  *alt*
    accessibility text of the image as a ``string``.

  The `Image`_ class supports the following methods and attributes:

  **platform**
    Platform the widget is supported on, always ``google``.

  **render**\()
    Renders the widget to a ``dict`` that is ready to be added to the API.ai response messages.


Button Object
-------------

.. _Button:

*class* ``widgets``. **Button**\(*title* [, *weblink*])
  Abstraction for `Button <https://developers.google.com/actions/reference/rest/Shared.Types/AppResponse#button>`__ Actions on Google object.

  *title*
    CTA text to appear on the button, as a ``string``.

  *weblink*
    URL target when a user interacts with the button, as a ``string``.

  The `Button`_ class supports the following methods and attributes:

  **platform**
    Platform the widget is supported on, always ``google``.

  **render**\()
    Renders the widget to a ``dict`` that is ready to be added to the API.ai response messages.


ListSelectWidget Object
-----------------------

.. _ListSelectWidget:

*class* ``widgets``. **ListSelectWidget**\(*items* [, *title*])
  Abstraction for `ListSelect <https://developers.google.com/actions/reference/rest/Shared.Types/OptionValueSpec#ListSelect>`__ Actions on Google object.

  *items*
    List of items for the list as a ``list`` of `SelectItem`_ instances.

  *title*
    Optional title for the list, as a ``string``.

  The `ListSelectWidget`_ class supports the following methods and attributes:

  **platform**
    Platform the widget is supported on, always ``google``.

  **type**
    Required by Actions on Google to identify the type of the response, always ``list_card``

  **render**\()
    Renders the widget to a ``dict`` that is ready to be added to the API.ai response messages.


CarouselSelectWidget Object
---------------------------

.. _CarouselSelectWidget:

*class* ``widgets``. **CarouselSelectWidget**\(*items*)
  Abstraction for `CarouselSelect <https://developers.google.com/actions/reference/rest/Shared.Types/OptionValueSpec#CarouselSelect>`__ Actions on Google object.

  *items*
    List of items for the carousel as a ``list`` of `SelectItem`_ instances.

  The `CarouselSelectWidget`_ class supports the following methods and attributes:

  **platform**
    Platform the widget is supported on, always ``google``.

  **type**
    Required by Actions on Google to identify the type of the response, always ``carousel_card``

  **render**\()
    Renders the widget to a ``dict`` that is ready to be added to the API.ai response messages.


SelectItem Object
-----------------

.. _SelectItem:

*class* ``widgets``. **SelectItem**\(*title*, *option_info* [, *text* [, *image*])
  Abstraction for `ListItem/CarouselItem <https://developers.google.com/actions/reference/rest/Shared.Types/OptionValueSpec#ListItem>`__ Actions on Google object.

  *title*
    Title of the item as a ``string``.

  *option_info*
    Information about the item as an `OptionInfo`_ instance.

  *text*
    Text body of the item as a ``string``.

  *image*
    Image of the item as an `Image`_ instance.

  The `SelectItem`_ class supports the following methods and attributes:

  **platform**
    Platform the widget is supported on, always ``google``.

  **render**\()
    Renders the widget to a ``dict`` that is ready to be added to the API.ai response messages.


OptionInfo Object
-----------------

.. _OptionInfo:

*class* ``widgets``. **OptionInfo**\(*key* [, *synonyms*])
  Abstraction for `OptionInfo <https://developers.google.com/actions/reference/rest/Shared.Types/OptionInfo>`__ Actions on Google object.

  *key*
    Unique key for the option as a ``string``. This is also the text sent to your agent when a user select the option.

  *synonyms*
    List of synonyms for the option as a ``list`` of ``string``.

  `InvalidGoogleAssistantWidget`_ is raised if **key** and **synonyms** are ``None``

  The `OptionInfo`_ class supports the following methods and attributes:

  **platform**
    Platform the widget is supported on, always ``google``.

  **render**\()
    Renders the widget to a ``dict`` that is ready to be added to the API.ai response messages.
