from ast import Str
from typing import Any, Dict, override
from masterpiece import Plugin, Composite


class HelloWorld(Plugin):
    """Minimal plugin example for demonstration purposes.

    This plugin instantiates and installs a "Hello World" object into the host
    application by calling `app.add()`. While this approach works, it is not typical
    for plugins to behave this way unless the object being added is inherently
    non-singleton in nature.

    Typically, classes provided by a plugin are explicitly instantiated based on
    user-defined configurations. For example, a configuration file or user input
    might determine the exact behavior or parameters of the plugin's objects.
    """

    _HELLO_WORLD_KEY = "_hello_world"

    def __init__(self, name: str = "noname", description: str = "hello") -> None:
        """Create hello world object."""
        super().__init__(name)
        self.description = description

    @override
    def install(self, app: Composite) -> None:
        # Create and insert a HelloWorld object into the host application.
        # This allows easy verification that the plugin is functioning as intended.
        obj = HelloWorld("Hello World - A Plugin")
        app.add(obj)

    @override
    def to_dict(self) -> Dict[str, Any]:
        return {
            "_class": self.get_class_id(),  # the real class
            "_version:": 0,
            self._HELLO_WORLD_KEY: {
                "description": self.description,
            },
        }

    @override
    def from_dict(self, data: Dict[str, Any]):
        for key, value in data[self._HELLO_WORLD_KEY].items():
            setattr(self, key, value)
