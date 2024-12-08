
masterpiece_plugin
==================

`masterpiece_plugin` is a simple demonstration plugin designed to extend `masterpiece` applications by adding a
basic "Hello, World!" greeting feature. While this plugin is straightforward in its functionality, it serves as a
starting point for developers looking to implement real plugins for `masterpiece`.

Consult the `Masterpiece project <https://gitlab.com/juham/masterpiece>`_ for more information.


Features
--------

The plugin adds one HelloWorld object named 'Hello World - A Plugin' into any masterpiece application that
allows its structure to be expanded. 

The primary purpose of `masterpiece_plugin` is educational. It is intended to demonstrate the fundamental steps
involved in creating and integrating plugins with `masterpiece`. Developers can use this as a reference or template
when building more complex plugins for real-world applications.


Installation
------------

To install:

.. code-block:: python

    pip install masterpiece_plugin


Usage
-----

Once installed, the plugin integrates into the 'masterpiece/examples/myapp.py' application:

.. code-block:: python

    cd masterpiece/examples
    python myapp.py


This will output the following diagram:

.. code-block:: text

    home
    ├─ grid
    ├─ downstairs
    │   └─ kitchen
    │       ├─ oven
    │       └─ fridge
    ├─ garage
    │   └─ EV charger
    └─ Hello World - A Plugin



   

License
-------

This project is licensed under the MIT License - see the `LICENSE` file for details.
