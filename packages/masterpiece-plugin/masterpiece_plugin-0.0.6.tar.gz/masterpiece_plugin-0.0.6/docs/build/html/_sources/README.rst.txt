
masterpiece_plugin
==================

`masterpiece_plugin` is a simple demonstration plugin designed to extend `masterpiece` applications by adding a
basic "Hello, World!" greeting feature. While this plugin is straightforward in its functionality, it serves as an
excellent starting point for developers looking to implement real plugins for `masterpiece`.

Source code
-----------

.. code-block:: python

    from masterpiece.base import Plugin, Composite

    class Foo(Plugin):

        def __init__(self, name: str = "noname", description: str = "foo") -> None:
            super().__init__(name)
            self.description = description

        # @override
        def install(self, app: Composite) -> None:
            obj = Foo("Hello World - A Plugin")
            app.add(obj)

        # @override
        def to_dict(self):
            """Convert instance attributes to a dictionary."""
            return {
                "_class": self.get_class_id(),  # the real class
                "_version:": 0,
                "_foo": {
                    "description": self.description,
                },
            }

        # @override
        def from_dict(self, data):
            """Update instance attributes from a dictionary."""
            for key, value in data["_foo"].items():
                setattr(self, key, value)


Features
--------

The plugin adds one Foo object named 'Hello World - A Plugin' into the masterpiece application. 

The primary purpose of `masterpiece_plugin` is educational. It is intended to demonstrate the fundamental steps
involved in creating and integrating plugins with `masterpiece`. Developers can use this as a reference or template
when building more complex plugins for real-world applications.

Installation
------------

To install:

.. code-block:: python

    pip install masterpiece
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
