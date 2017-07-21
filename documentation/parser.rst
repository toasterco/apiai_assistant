===============
 Parser module
===============

Provides Actions on Google Parser classes to read from the API.ai POST request payload and offers abstractions to access objects of the payload.

Device Object
=============

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
===========

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
====================

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
    `utils.Enum <utils.rst#enum>`_ object of keys `NUMBER`, `STRING`, and `LIST`

GoogleAssistantPayloadParser Object
====================================

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
    `utils.Enum <utils.rst#enum>`__ object of keys `NUMBER`, `STRING`, and `LIST`.

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

