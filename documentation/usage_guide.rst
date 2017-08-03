
``apiai_assistant`` can be used with any web framework

Simply declare an ``Assistant``, register your intents with it by decorating them with ``Assistant.intent`` and then process the API.ai POST request with ``Assistant.process``

.. _DeclaringanAssistant:

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


.. _Registeringanintent:

Registering an intent
---------------------

Registration of intents is straightforward, write your intent and wrap it with the ``Assistant.intent`` decorator, passing the intent id specified on API.ai (called 'Action') to the decorator.

Each intent takes an ``apiai_assistant.agent.Agent`` instance as parameter

.. code:: python

    @myassistant.intent(APIAI_ACTION)
    def intent_name(agent_instance):
        ...


`Example <https://github.com/toasterco/apiaiassistant-sample/blob/master/agent/actions/start.py#L5>`__

.. _Writingintents:

Writing intents
---------------

`Example <https://github.com/toasterco/apiaiassistant-sample/blob/master/agent/actions/animal_info.py#L24>`__

.. _Accessingparameters:

Accessing parameters
~~~~~~~~~~~~~~~~~~~~

Each agent instance has a ``parser`` attribute that is an instance of the superclassed ``apiai_assistant.parser.PayloadParser``

Using ``parser.get`` you can retrieve parameters for your intent and even parse numbers by specifying the type of the parameter to get

Parsing numbers turns the received string in the request payload to a python ``int`` object (i.e.: '3rd', 'three', and 'third' will be converted to ``3``)

.. code:: python

   @myassistant.intent('place-order')
   def place_order_intent(agent):
       food_choice = agent.parser.get('food')
       amount = agent.parser.get('number', _type=agent.parser.PARAM_TYPES.NUMBER)
       ...

.. _Accessingcontextparameters:

Accessing context parameters
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Use the agent instances to retrieve the parameters of a context by passing the name of the context to the ``get_contexts`` method of the agent instance.

If the context was found in the request, its parameters will be returned in a ``dict`` as they are received from API.ai

.. code:: python

    from apiai_assistant import utils

    context = agent.get_contexts('context-name')
    amount = utils.text_to_int(context.get('number'))

To retrieve the list of all contexts as they are in the request payload

.. code:: python

    contexts = agent.get_contexts()
    for context in contexts:
        context_parameters = context['parameters']
        ...

.. _Tellingtheuser:

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

.. _Askingtheuser:

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

You can also use ``ask_for_confirmation`` to ask the user something and prompt them with two suggestion chips representing confirmation.

| By default those two chips are "Yes" and "No" but they can be selected from a random list of values if the ``confirmations`` object of your corpus is set, see `Writing a corpus <#writing-a-corpus>`__

.. _Showingtheuser:

Showing the user
~~~~~~~~~~~~~~~~

In its current state, ``apiai_assistant`` only supports integration with *Actions on Google* so only visual responses for AoG will be covered in this section for now.

Using ``tell`` and ``ask`` only creates simple text speech bubbles in conjunction with spoken speech;

*Actions on Google* supports Rich Responses which are essentially visual widgets that allow you to offer a better user experience when a user invokes your app/service from a device with screen capabilities (such as a user using Google Assistant on amobile device).

To make use of rich responses, simply create a ``GoogleAssistantWidget`` and use the agent method ``show`` to add it to your response

.. code:: python

    from apiai_assistant.widgets import ImageCardWidget, Image

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

.. _Suggestingoptionstotheuser:

Suggesting options to the user
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Suggestions are a form of rich responses but ``apiai_assitant.agent.Agent`` offers a ``suggest`` and ``suggest_raw`` (that behave similaryl to ``tell`` and ``tell_raw`` or ``ask`` and ``ask_raw``) to easily add suggestions.

.. code:: python

   agent.suggest('options') # Suggests the values of 'suggestions.options'
   agent.suggest_raw(['Yes', 'No']) # Suggests 'Yes' or 'No'
   agent.suggest_raw('Yes I am sure') # Suggests 'Yes I am sure'

Just like ``tell` and ``ask``, ``suggest`` retrieves a random value of the output id from the ``suggestions`` object of the corpus but the format of suggestions is the same as the one for the other simple outputs, the only difference being that when having a list of lists, the nested lists are not limited to a size of 2 elements and you must placed the suggestions within the ``suggesstions`` attribute of your corpus JSON object, see `Writing a corpus <#writing-a-corpus>`__.

.. code:: javascript

    {
        "corpus": {
            simple-output-key: [
                [voiceChoiceA, textChoiceA],	// must be 2 elements MAX
                voiceChoiceB,			// can also be just a string
                [voiceChoicec, textChoicec]
            ],
        },

        "suggestions": {
            suggestion-output-key: [
                singleSuggestion,					// can be just a string
                [suggestionA, suggestionB, suggestionC, suggestionD],	// can also be a list of strings
                [suggestionA, suggestionB, suggestionC]
            ],
        }
    }

.. _Addingcontexts:

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

.. _Requestingpermissions:

Requesting permissions
~~~~~~~~~~~~~~~~~~~~~~

You are able to request permissions to access user data, the permissions are:

* NAME - to access the user's full name (given name and family name)

* COARSE_LOCATION - to access the user's coarse location (zipcode or postcode and city if available)

* PRECISE_LOCATION - to access the user's precise location (latitude and longitude, also formatted address and city if available)

Please see the `Actions on Google documentation <https://developers.google.com/actions/reference/rest/Shared.Types/Permission>`_ for more information on each permission.

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

.. _Writingacorpus:

Writing a corpus
----------------

A corpus is a large and structured set of texts, in the contexts of ``apiai_assistant``, corpora are JSON files containing all outputs of your agent.

When rendering an output via ``.tell()``, ``.ask()``, ``.suggest()``, or ``.ask_for_confirmation()``, the agent looks up the output id within the corpus and **randomly selects a choice from the list value for that output id**, thus making your agent responses less predictable and more organic.

Your corpus must contain at least the ``corpus`` object and the value for each key must be a list of strings or list of jsonified tuples (unless it's a suggestion output, see `Suggesting options to the user <#suggesting-options-to-the-user>`__.

When having a list of string as the value, the text output will be the same as the speech output.

When having a list of jsonified tuples as the value, the speech output will be the first element and the text will be the second.


Shown below is the required structures

.. code:: javascript

    {
        "corpus": {
            key: [
                choiceA,
                [voiceChoiceB, textChoiceB],	//You can mix strings and lists as values
                choiceC
            ],
            ...
        }
    }

Corpora also support a ``suggestions`` object to lookup corpus ids when using ``suggest()`` and a ``confirmations`` object to randomly get a set of confirmation values instead of the default "Yes" and "No" when using ``ask_for_confirmation()``

.. code:: javascript

    {
        "corpus": {
            key: [
                choiceA,
                [voiceChoiceB, textChoiceB],
                choiceC
            ],
            ...
        },

        "suggestions": {
            key: [
                choiceA,
                [voiceChoiceB, textChoiceB],
                choiceC
            ],
            ...
        },

        "confirmations": [
            ["Yes", "No"],
            ["Yeah", "Nah"],
            ["Yup", "Nop"]
        ]
    }


`Example <https://github.com/toasterco/apiaiassistant-sample/blob/master/corpora/animal_wiki_corpus.json>`__

.. _Processingarequest:

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

.. _RespondingtothePOSTrequest:

Responding to the POST request
------------------------------

Processing a request through an ``assistant`` returns an ``apiai_assistant.agent.Agent`` instance of which you can simply render the ``response`` attribute.

If something went wrong during the intent execution, the ``code`` attribute of the agent instance will be set to one of the error statuses (see ``apiai_assistant.agent.Status``) and the ``error_message`` attribute will describe what went wrong.

The ``response`` attribute will also be appropriately set with the API.ai error format so you can render the response regardless of the agent status code.

.. code:: python

    agent = myassistant.process(payload)
    agent.response.to_dict()
