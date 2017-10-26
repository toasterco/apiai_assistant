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

    pip install apiai-assistant

Latest development release on github
------------------------------------

|GitHub-Status| |GitHub-Stars| |GitHub-Forks|

Pull and install in the current directory:

.. code:: sh

    pip install -e git+https://github.com/toasterco/apiai_assistant.git@master#egg=apiai_assistant

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


Usage
=====

Sample project
--------------

See the `apiai_assistant-sample <https://github.com/toasterco/apiai_assistant-sample>`__ project.

Further reading
---------------

* `Declaring an Assistant <https://github.com/toasterco/apiai_assistant/tree/master/documentation/usage_guide.rst#declaringanAssistant>`__

* `Registering an intent <https://github.com/toasterco/apiai_assistant/tree/master/documentation/usage_guide.rst#registeringanintent>`__

* `Writing intents <https://github.com/toasterco/apiai_assistant/tree/master/documentation/usage_guide.rst#writingintents>`__

  * `Accessing parameters <https://github.com/toasterco/apiai_assistant/tree/master/documentation/usage_guide.rst#accessingparameters>`__

  * `Accessing context parameters <https://github.com/toasterco/apiai_assistant/tree/master/documentation/usage_guide.rst#accessingcontextparameters>`__

  * `Telling the user <https://github.com/toasterco/apiai_assistant/tree/master/documentation/usage_guide.rst#tellingtheuser>`__

  * `Asking the user <https://github.com/toasterco/apiai_assistant/tree/master/documentation/usage_guide.rst#askingtheuser>`__

  * `Showing the user <https://github.com/toasterco/apiai_assistant/tree/master/documentation/usage_guide.rst#showingtheuser>`__

  * `Suggesting options to the user <https://github.com/toasterco/apiai_assistant/tree/master/documentation/usage_guide.rst#suggestingoptionstotheuser>`__

  * `Adding contexts <https://github.com/toasterco/apiai_assistant/tree/master/documentation/usage_guide.rst#addingcontexts>`__

  * `Requesting permissions <https://github.com/toasterco/apiai_assistant/tree/master/documentation/usage_guide.rst#requestingpermissions>`__

  * `Aborting <https://github.com/toasterco/apiai_assistant/tree/master/documentation/usage_guide.rst#aborting>`__


FAQ and Known Issues
====================

- Can I use my agent for all API.ai supported integrations ?

  ``Only Actions on Google is supported as of yet in Alpha.``

If you come across any other difficulties, browse/open issues
`here <https://github.com/toasterco/apiai_assistant/issues?q=is%3Aissue>`__.

To do
=====

- Better error support (all error code, not only 400, and include error message)

- Add follow up intents support

- Support other smart assistant platforms (Alexa, Messenger, Slack as priorities)

- Assist account linking


Documentation
=============

All the doc can be found over `here <https://github.com/toasterco/apiai_assistant/tree/master/documentation/private_api.rst>`__.

Contributions
=============

All source code is hosted on `GitHub <https://github.com/ToasterCo/apiai_assistant>`__.
Contributions are welcome.


LICENCE
=======

Open Source : |LICENCE|

Authors
=======

Ranked by contributions.

-  Zack Dibe (Zack--) *
-  Dominic Santos (dominicglenn)


`*` Original author

.. |Logo| image:: https://raw.githubusercontent.com/toasterco/apiai_assistant/master/images/apiai_assistant-logo.png
   :height: 180px
   :width: 180 px
   :alt: apiai_assistant logo

.. |Branch-Coverage-Status| image:: https://codecov.io/github/toasterco/apiai_assistant/coverage.svg?branch=master
   :target: https://codecov.io/github/toasterco/apiai_assistant?branch=master

.. |GitHub-Status| image:: https://img.shields.io/github/tag/toasterco/apiaiassistant.svg?maxAge=2592000
   :target: https://github.com/toasterco/apiai_assistant/releases

.. |GitHub-Forks| image:: https://img.shields.io/github/forks/toasterco/apiaiassistant.svg
   :target: https://github.com/toasterco/apiai_assistant/network

.. |GitHub-Stars| image:: https://img.shields.io/github/stars/toasterco/apiaiassistant.svg
   :target: https://github.com/toasterco/apiai_assistant/stargazers

.. |PyPI-Status| image:: https://img.shields.io/pypi/v/apiai_assistant.svg
   :target: https://pypi.python.org/pypi/apiai_assistant

.. |PyPI-Downloads| image:: https://img.shields.io/pypi/dm/apiai_assistant.svg
   :target: https://pypi.python.org/pypi/apiai_assistant

.. |PyPI-Versions| image:: https://img.shields.io/pypi/pyversions/apiai_assistant.svg
   :target: https://pypi.python.org/pypi/apiai_assistant

.. |LICENCE| image:: https://img.shields.io/pypi/l/apiai_assistant.svg
   :target: https://raw.githubusercontent.com/toasterco/apiai_assistant/master/LICENCE
