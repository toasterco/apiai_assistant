==========
Disclaimer
==========

This README is a work in progress and some links (such as the PyPi links) and shields won't be available until the official release of the ``apiai_assistant`` package.

------------------------------------------

|Logo|

==================
 API.ai Assistant
==================

|PyPI-Status| |PyPI-Versions| |Branch-Coverage-Status|

|LICENCE|

``apiai_assistant`` aims to offer developers the easiest and most intuitive way to create smart assistants through API.ai

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

    pip install apiai_assistant

Latest development release on github
------------------------------------

|GitHub-Status| |GitHub-Stars| |GitHub-Forks|

Pull and install in the current directory:

.. code:: sh

    pip install -e git+https://github.com/toasterco/apiaiassistant.git@master#egg=apiai_assistant

Running tests
-------------

.. code:: sh

    python -m unittest discover tests/

Or

.. code:: sh

   nosetests --with-coverage --cover-package=apiai_assistant


Changelog
=========

The list of all changes is available either on GitHub's Releases:
|GitHub-Status| or on crawlers such as
`allmychanges.com <https://allmychanges.com/p/python/apiai_assistant/>`_.


Sample Usage
============

See the `apiai_assistant-sample <https://github.com/toasterco/apiaiassistant-sample>`__ project.

Usage
=====

* `Declaring an Assistant <documentation/usage_guide.rst#declaringanAssistant>`__

* `Registering an intent <documentation/usage_guide.rst#registeringanintent>`__

* `Writing intents <documentation/usage_guide.rst#writingintents>`__

  * `Accessing parameters <documentation/usage_guide.rst#accessingparameters>`__

  * `Accessing context parameters <documentation/usage_guide.rst#accessingcontextparameters>`__

  * `Telling the user <documentation/usage_guide.rst#tellingtheuser>`__

  * `Asking the user <documentation/usage_guide.rst#askingtheuser>`__

  * `Showing the user <documentation/usage_guide.rst#showingtheuser>`__

  * `Suggesting options to the user <documentation/usage_guide.rst#suggestingoptionstotheuser>`__

  * `Adding contexts <documentation/usage_guide.rst#addingcontexts>`__

  * `Requesting permissions <documentation/usage_guide.rst#requestingpermissions>`__

  * `Aborting <documentation/usage_guide.rst#aborting>`__


FAQ and Known Issues
====================

- Can I use my agent for all API.ai supported integrations ?

  ``Only Actions on Google is supported as of yet in Alpha.``

If you come across any other difficulties, browse/open issues
`here <https://github.com/toasterco/apiaiassistant/issues?q=is%3Aissue>`__.

To do
=====

- Better error support (all error code, not only 400, and include error message)

- Add follow up intents support

- Support other smart assistant platforms (Alexa, Messenger, Slack as priorities)

- Assist account linking


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

All source code is hosted on `GitHub <https://github.com/ToasterCo/apiai_assistant>`__.
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


`*` Original author

.. |Logo| image:: images/apiai_assistant-logo.png
   :height: 180px
   :width: 180 px
   :alt: apiai_assistant logo

.. |Branch-Coverage-Status| image:: https://codecov.io/github/toasterco/apiaiassistant/coverage.svg?branch=master
   :target: https://codecov.io/github/toasterco/apiaiassistant?branch=master

.. |GitHub-Status| image:: https://img.shields.io/github/tag/toasterco/apiaiassistant.svg?maxAge=2592000
   :target: https://github.com/toasterco/apiaiassistant/releases

.. |GitHub-Forks| image:: https://img.shields.io/github/forks/toasterco/apiaiassistant.svg
   :target: https://github.com/toasterco/apiaiassistant/network

.. |GitHub-Stars| image:: https://img.shields.io/github/stars/toasterco/apiaiassistant.svg
   :target: https://github.com/toasterco/apiaiassistant/stargazers

.. |PyPI-Status| image:: https://img.shields.io/pypi/v/apiai_assistant.svg
   :target: https://pypi.python.org/pypi/apiai_assistant

.. |PyPI-Downloads| image:: https://img.shields.io/pypi/dm/apiai_assistant.svg
   :target: https://pypi.python.org/pypi/apiai_assistant

.. |PyPI-Versions| image:: https://img.shields.io/pypi/pyversions/apiai_assistant.svg
   :target: https://pypi.python.org/pypi/apiai_assistant

.. |LICENCE| image:: https://img.shields.io/pypi/l/apiai_assistant.svg
   :target: https://raw.githubusercontent.com/toasterco/apiaiassistant/master/LICENCE
