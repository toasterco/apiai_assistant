==========
Disclaimer
==========

This README is a work in progress and some links (such as the PyPi links) and shields won't be available until the official release of the ``apiaiassistant`` package.

------------------------------------------

|Logo|

================
 apiaiassistant
================

|PyPI-Status| |PyPI-Versions| |Branch-Coverage-Status|

|LICENCE|

``apiaiassistant`` aims to offer developers the easiest and most intuitive way to create smart assistants through API.ai

------------------------------------------

.. contents:: Table of contents
   :backlinks: top
   :local:


Installation
============

Latest PyPI stable release
--------------------------

|PyPI-Status|

.. code:: sh

    pip install apiaiassistant

Latest development release on github
------------------------------------

|GitHub-Status| |GitHub-Stars| |GitHub-Forks|

Pull and install in the current directory:

.. code:: sh

    pip install -e git+https://github.com/toasterco/apiaiassistant.git@master#egg=apiaiassistant

Running tests
-------------

.. code:: sh

    python -m unittest discover tests/

Or

.. code:: sh

   nosetests --with-coverage --cover-package=apiaiassistant


Changelog
=========

The list of all changes is available either on GitHub's Releases:
|GitHub-Status| or on crawlers such as
`allmychanges.com <https://allmychanges.com/p/python/apiaiassistant/>`_.


Sample Usage
============

See the `apiaiassistant-sample <https://github.com/toasterco/apiaiassistant-sample>`__ project.

Usage
=====

``apiaiassistant`` can be used with any web framework

Simply declare an ``Assistant``, register your intents with it by decorating them with ``Assistant.intent`` and then process the API.ai POST request with ``Assistant.process``

Declaring an ``Assistant``
--------------------------

The ``Assistant`` class is your entrypoint to the package, it is used to register intents and process received API.ai POST requests.

.. code:: python

    myassistant = Assistant()


No parameters are required to declare an ``Assistant`` but it is highly recommended to use a corpus to manage your agents outputs (see `Writing a corpus <#writing-a-corpus>`__) and a magic key to identify requests.

.. code:: python

    myassistant = Assistant(
        corpus=CORPUS_FILEPATH,
        magic_key=MY_MAGIC_KEY)


`Example <https://github.com/toasterco/apiaiassistant-sample/blob/master/agent/__init__.py#L5>`__


Registering an intent
---------------------

Registration of intents is straightforward, write your intent and wrap it with the ``Assistant.intent`` decorator, passing the intent id specified on API.ai (called 'Action') to the decorator.

Each intent takes an ``apiaiassistant.agent.Agent`` instance as parameter

.. code:: python

    @myassistant.intent(APIAI_ACTION)
    def intent_name(agent_instance):
        ...


`Example <https://github.com/toasterco/apiaiassistant-sample/blob/master/agent/actions/start.py#L5>`__

Writing intents
---------------

`Example <https://github.com/toasterco/apiaiassistant-sample/blob/master/agent/actions/animal_info.py#L24>`__

Accessing parameters
~~~~~~~~~~~~~~~~~~~~

Each agent instance has a ``parser`` attribute that is an instance of the superclassed ``apiaiassistant.parser.PayloadParser``

Using ``parser.get`` you can retrieve parameters for your intent and even parse numbers by specifying the type of the parameter to get

Parsing numbers turns the received string in the request payload to a python ``int`` object (i.e.: '3rd', 'three', and 'third' will be converted to ``3``)

.. code:: python

   @myassistant.intent('place-order')
   def place_order_intent(agent):
       food_choice = agent.parser.get('food')
       amount = agent.parser.get('number', _type=agent.parser.PARAM_TYPES.NUMBER)
       ...

Accessing context parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use the agent instances to retrieve the parameters of a context by passing the name of the context to the ``get_contexts`` method of the agent instance.

If the context was found in the request, its parameters will be returned in a ``dict`` as they are received from API.ai

.. code:: python

    from apiaiassistant import utils

    context = agent.get_contexts('context-name')
    amount = utils.text_to_int(context.get('number'))

To retrieve the list of all contexts as they are in the request payload

.. code:: python

    contexts = agent.get_contexts()
    for context in contexts:
        context_parameters = context['parameters']
        ...

Telling the user
~~~~~~~~~~~~~~~~

To have your agent answer the user's query and close the device's mic, you can use the ``tell`` and ``tell_raw`` methods of the agent instance.

.. code:: python

    def tell(self, corpus_id, context=None):
      """
      Looks for the output with key corpus_id,
      gets a random value and and formats it with the context

      Args:
          corpus_id (str): ID of the output to tell
          context (:obj:`dict`, optional): context to format the output with
      """


.. code:: python

    def tell_raw(self, speech, text=None):
      """
      Tells the user

      Args:
          speech (str): speech to tell
          text (str, optional): text to tell, if None, speech will be used
      """

Asking the user
~~~~~~~~~~~~~~~

To have your agent asks the user something and wait for an answer, you can use the ``ask`` and ``ask_raw`` methods of the agent instance.

.. code:: python

    def ask(self, corpus_id, context=None):
      """
      Looks for the output with key corpus_id,
      gets a random value, and and formats it with the context

      Args:
          corpus_id (str): ID of the output to ask
          context (:obj:`dict`, optional): context to format the output with
      """


.. code:: python

    def ask_raw(self, speech, text=None):
      """
      Asks the user

      Args:
          speech (str): speech to ask
          text (str, optional): text to ask, if None, speech will be used
      """

Showing the user
~~~~~~~~~~~~~~~~

In its current state, ``apiaiassistant`` only supports integration with *Actions on Google* so only visual responses for AoG will be covered in this section for now.

Using ``tell`` and ``ask`` only creates simple text speech bubbles in conjunction with spoken speech;

*Actions on Google* supports Rich Responses which are essentially visual widgets that allow you to offer a better user experience when a user invokes your app/service from a device with screen capabilities (such as a user using Google Assistant on amobile device).

To make use of rich responses, simply create a ``GoogleAssistantWidget`` and use the agent method ``show`` to add it to your response

.. code:: python

    from apiaiassistant.widgets import ImageCardWidget, Image

    @myassistant.intent('show-animal-card')
    def show_animal_card(agent):
        ...
        animal_card = ImageCardWidget(
            title=animal_name,
            text=animal_info,
            image=Image(url=animal_pic))

        agent.show(animal_card)


Rich responses supported: ``ListSelect``, ``CarouselSelectWidget``, ``ImageCardWidget``, ``LinkOutChipWidget``

For a detailed description of each rich responses available with *Actions on Google* `see here <https://developers.google.com/actions/assistant/responses>`__.

Suggesting options to the user
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Suggestions are a form of rich responses but ``apiaiassitant.agent.Agent`` offers a ``suggest`` and ``suggest_raw`` (that behave similaryl to ``tell`` and ``tell_raw`` or ``ask`` and ``ask_raw``) to easily add suggestions.

.. code:: python

   agent.suggest('suggest-options') # Suggests the values of 'suggest-options'
   agent.suggest_raw(['Yes', 'No']) # Suggests 'Yes' or 'No'
   agent.suggest_raw('Yes I am sure') # Suggests 'Yes I am sure'

Just like ``tell` and ``ask``, ``suggest`` retrieves a random value of the output id from the corpus but the format of suggestions is the same as the one for the other simple outputs, the only difference being that when having a list of lists, the nested lists are not limited to a size of 2 elements, see `Writing a corpus <#writing-a-corpus>`__.

.. code:: javascript

    {
        simple-output-key: [
            [voiceChoiceA, textChoiceA],	// must be 2 elements MAX
            voiceChoiceB,			// can also be just a string
            [voiceChoicec, textChoicec]
        ],
        suggestion-output-key: [
            singleSuggestion,						// can be just a string
            [suggestionA, suggestionB, suggestionC, suggestionD],	// can also be a list of strings
            [suggestionA, suggestionB, suggestionC]
        ],
        ...
    }


Adding contexts
~~~~~~~~~~~~~~~

(For *retrieving* contexts from the API.ai request, see `Accessing context parameters <#accessing-context-parameters>`__.)

Contexts are a good way to control the conversation flow, you must create input contexts from API.ai but then you can dinamycally set output contexts from within your intents using the agent instance ``add_context`` method

.. code:: python

    def add_context(self, context_name, parameters=None, lifespan=5):
        """
        Adds a context to the response's contexts

        Args:
            context_name (str): name of the context to add
            parameters (:obj:`dict`, optional): parameters of the context
            lifespan (:obj:`int`, optional, 5): lifespan of the context
        """

Read more about contexts `here <https://api.ai/docs/contexts>`__.

Requesting permissions
~~~~~~~~~~~~~~~~~~~~~~

You are able to request permissions to access user data, the permissions are:

* NAME - to access the user's full name (given name and family name)

* COARSE_LOCATION - to access the user's coarse location (zipcode or postcode and city if available)

* PRECEISE_LOCATION - to access the user's precise location (latitude and longitude, also formatted address and city if available)

To do so, simply use the agent instance ``ask_for_permissions`` method by passing the reason of your permission request and a ``list`` of permissions you require.

.. code:: python

    agent.ask_for_permissions('To deliver the pizza', [
        agent.SupportedPermissions.PRECISE_LOCATION,
        agent.SupportedPermissions.COARSE_LOCATION
    ])

The reason of the permission request is used by Google when asking the user for the requested permission using the following format:

* NAME: `<reason>, I'll just need to get your name from Google. Is that ok?`

* COARSE_LOCATION: `<reason>, I'll just need to get your zip code from Google. Is that ok?`

* PRECISE_LOCATION: `<reason>, I'll just need to get your street address from Google. Is that ok?`

It is also important to note that for the permissions request to work properly you need to setup a fallback intent for the intent that triggers the request permission.

*Example:*

::

 Intent: Create pizza ->
 Intent: Confirm pizza creation is done ->
 Intent: Ask for location permission ->
   Fallback intent: Place order (use requested data here)

The requested data can be found in the ``user`` attribute of the ``agent.parser`` - see `User <documentation/parser.rst#user>`__

Aborting
~~~~~~~~

If something goes wrong and you wish to return an error to API.ai, simply pass your error message to ``Agent.error``

The response object of your agent will be properly formated with the correct format for errors.

.. code:: python

    agent.error('my error message')
    return

Writing a corpus
----------------

A corpus is a large and structured set of texts, in the contexts of ``apiaiassistant``, corpora are JSON files containing all outputs of your agent.

When rendering an output via ``.tell()``, ``.ask()``, or ``.suggest()``, the agent looks up the output id within the corpus and **randomly selects a choice from the list value for that output id**, thus making your agent responses less predictable and more organic.

Your corpus must contain only one object and the value for each key must be a list of strings or list of jsonified tuples (unless it's a suggestion output, see `Suggesting options to the user <#suggesting-options-to-the-user>`__.

When having a list of string as the value, the text output will be the same as the speech output.

When having a list of jsonified tuples as the value, the speech output will be the first element and the text will be the second.


Shown below are the required structures

.. code:: javascript

    {
        key: [
            choiceA,
            choiceB,
            choiceC
        ],
        ...
    }

Or

.. code:: javascript

    {
        key: [
            [voiceChoiceA, textChoiceA],
            [voiceChoiceB, textChoiceB],
            [voiceChoicec, textChoicec]
        ],
        ...
    }


`Example <https://github.com/toasterco/apiaiassistant-sample/blob/master/corpora/animal_wiki_corpus.json>`__

Processing a request
---------------------

In your webhook, when receiving the POST request from API.ai, simply pass the POST payload as a ``dict`` to the assistant.

.. code:: python

    # example using webapp2
    payload = json.loads(self.request.body)
    agent = myassistant.process(payload)


If you specified a magic key when declaring your assistant, you can also pass the HTTP headers of the received request, as a ``dict``, to verify the request's source.

.. code:: python

    # example using webapp2
    payload = json.loads(self.request.body)
    agent = myassistant.process(
        payload,
        headers=self.request.headers)

`Example <https://github.com/toasterco/apiaiassistant-sample/blob/master/handlers/assistant_webhook.py#L16>`__

Responding to the POST request
------------------------------

Processing a request through an ``assistant`` returns an ``apiaiassistant.agent.Agent`` instance of which you can simply render the ``response`` attribute.

If something went wrong during the intent execution, the ``code`` attribute of the agent instance will be set to one of the error statuses (see ``apiaiassistant.agent.Status``) and the ``error_message`` attribute will describe what went wrong.

The ``response`` attribute will also be appropriately set with the API.ai error format so you can render the response regardless of the agent status code.

.. code:: python

    agent = myassistant.process(payload)
    agent.response.to_dict()


FAQ and Known Issues
====================

- How can I get the user's location or name?

  ``Unfortunately, permissions aren't supported as of yet in Alpha``

- Can I use my agent for all API.ai supported integrations ?

  ``Only Actions on Google is supported as of yet in Alpha.``

If you come across any other difficulties, browse/open issues
`here <https://github.com/toasterco/apiaiassistant/issues?q=is%3Aissue>`__.

To do
=====

- Better error support (all error code, not only 400, and include error message)

- Support follow up intents

- Support other smart assistant platforms (Alexa, Messenger, Slack as priorities)

- Support permission requests

- Assist account linking

- Support API.ai sandbox mode


Documentation
=============

* `Assistant <documentation/assistant.rst#assistant>`__

* `Agent <documentation/agent.rst#agent>`__

  * `Response <documentation/agent.rst#response>`__

* `Corpus <documentation/corpus.rst#corpus>`__

* `Utils <documentation/utils.rst>`__

* `Parser <documentation/parser.rst>`__

  * `User <documentation/parser.rst#user>`__

  * `PayloadParser <documentation/parser.rst#payloadparser>`__

  * `GoogleAssistantPayloadParser <documentation/parser.rst#googleassistantpayloadparser>`__

* `widgets <documentation/widgets.rst>`__

  * `InvalidGoogleAssistantWidget <documentation/widgets.rst#InvalidGoogleAssistantWidget>`__

  * `GoogleAssistantWidget <documentation/widgets.rst#googleassistantwidget>`__

  * `SimpleResponseWidget <documentation/widgets.rst#simpleresponsewidget>`__

  * `SuggestionsWidget <documentation/widgets.rst#suggestionswidget>`__

  * `LinkOutChipWidget <documentation/widgets.rst#linkoutchipwidget>`__

  * `ImageCardWidget <documentation/widgets.rst#imagecardwidget>`__

  * `Image <documentation/widgets.rst#image>`__

  * `Button <documentation/widgets.rst#button>`__

  * `ListSelectWidget <documentation/widgets.rst#listselectwidget>`__

  * `CarouselSelectWidget <documentation/widgets.rst#carouselselectwidget>`__

  * `SelectItem <documentation/widgets.rst#selectitem>`__

  * `OptionInfo <documentation/widgets.rst#optioninfo>`__

Contributions
=============

All source code is hosted on `GitHub <https://github.com/ToasterCo/apiaiassistant>`__.
Contributions are welcome.

See the
`CONTRIBUTING <https://raw.githubusercontent.com/toasterco/apiaiassistant/master/CONTRIBUTING.md>`__
file for more information.


LICENCE
=======

Open Source : |LICENCE|

Authors
=======

Ranked by contributions.

-  Zack Dibe (Zack--) *
-  Dominic Santos (dominicglenn)


README structure and style based on `tqdm <https://pypi.python.org/pypi/tqdm>`__.

`*` Original author

.. |Logo| image:: https://raw.githubusercontent.com/toasterco/apiaiassistant/master/images/apiaiassistant-logo.png
   :height: 180px
   :width: 180 px
   :alt: apiaiassistant logo

.. |Branch-Coverage-Status| image:: https://codecov.io/github/toasterco/apiaiassistant/coverage.svg?branch=master
   :target: https://codecov.io/github/toasterco/apiaiassistant?branch=master

.. |GitHub-Status| image:: https://img.shields.io/github/tag/toasterco/apiaiassistant.svg?maxAge=2592000
   :target: https://github.com/toasterco/apiaiassistant/releases

.. |GitHub-Forks| image:: https://img.shields.io/github/forks/toasterco/apiaiassistant.svg
   :target: https://github.com/toasterco/apiaiassistant/network

.. |GitHub-Stars| image:: https://img.shields.io/github/stars/toasterco/apiaiassistant.svg
   :target: https://github.com/toasterco/apiaiassistant/stargazers

.. |PyPI-Status| image:: https://img.shields.io/pypi/v/apiaiassistant.svg
   :target: https://pypi.python.org/pypi/apiaiassistant

.. |PyPI-Downloads| image:: https://img.shields.io/pypi/dm/apiaiassistant.svg
   :target: https://pypi.python.org/pypi/apiaiassistant

.. |PyPI-Versions| image:: https://img.shields.io/pypi/pyversions/apiaiassistant.svg
   :target: https://pypi.python.org/pypi/apiaiassistant

.. |LICENCE| image:: https://img.shields.io/pypi/l/apiaiassistant.svg
   :target: https://raw.githubusercontent.com/toasterco/apiaiassistant/master/LICENCE
