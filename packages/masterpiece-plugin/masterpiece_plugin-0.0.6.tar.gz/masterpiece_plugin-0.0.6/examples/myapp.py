"""Example application for loading 'masterpiece_plugin'
"""

from typing_extensions import override
from masterpiece import Application


class MyHome(Application):
    """Plugin aware application"""

    def __init__(self, name: str = "myhome") -> None:
        """Initialize the home application with the given name.
        Args:
            name (str): The name of the application.
        """
        super().__init__(name)
        self.install_plugins()

    @override
    def run(self) -> None:
        """Run the application - print the instance diagram"""
        super().run()
        self.print()


def main() -> None:
    """Main function, yes, main function!."""

    # create classes
    MyHome.init_app_id("myapp")
    MyHome.load_plugins()

    # confligure classes from their configuration files in ~/.appname/configuration/*
    Application.load_configuration()

    # create application - that is - instantiate classes
    home = MyHome("home")

    # run like hell
    home.run()


if __name__ == "__main__":
    main()
