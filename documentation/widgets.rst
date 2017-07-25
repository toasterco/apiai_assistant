===============
 Widgets module
===============

Module Contents
===============

.. _InvalidGoogleAssistantWidget:

*exception* **InvalidGoogleAssistantWidget**
  Raised when a widget isn't initialized properly


GoogleAssistantWidget Object
============================

.. _GoogleAssistantWidget:

*class* ``widgets``. **GoogleAssistantWidget**\()
  Base class for `Actions on Google widgets <https://developers.google.com/actions/assistant/responses>`_.

  The `GoogleAssistantWidget`_ class supports the following methods and attributes:

  **platform**
    Platform the widget is supported on, always ``google``.

  **render**\()
    Renders the widget to a ``dict`` that is ready to be added to the API.ai response messages.


SimpleRsponseWidget Object
==========================

.. _SimpleRsponseWidget:

*class* ``widgets``. **SimpleRsponseWidget**\(*speech*, *text* [, *ssml=True*])
  Abstraction for `SimpleRsponse <https://developers.google.com/actions/reference/rest/Shared.Types/AppResponse#simpleresponse>`__ Actions on Google object.

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

  The `SimpleRsponseWidget`_ class supports the following methods and attributes:

  **platform**
    Platform the widget is supported on, always ``google``.

  **type**
    Required by Actions on Google to identify the type of the response, always ``simple_response``

  **render**\()
    Renders the widget to a ``dict`` that is ready to be added to the API.ai response messages.

  **ssml_format**\(*s*)
    Formats the ``string`` **s** to SSML (essentially wrapping it in a ``speak`` tag)

SuggestionsWidget Object
========================

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
========================

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
======================

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
============

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
=============

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
=======================

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
===========================

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
=================

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
=================

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
