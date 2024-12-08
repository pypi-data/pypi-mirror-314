"""Example application for testing 'masterpiece_yaml'
"""

from typing_extensions import override
from masterpiece import Application


class MyApp(Application):
    """Plugin aware application to test the plugin. If the plugin module is properly
    installed, then the 'YamlFormat' should get automatically imported and be available
    for serialization."""

    def __init__(self, name: str = "myhome") -> None:
        """Initialize the home application with the given name.
        Args:
            name (str): The name of the application.
        """
        super().__init__(name)
        self.install_plugins()

    @override
    def run(self) -> None:
        """Start the application."""
        super().run()

        # Print out the instance hierarchy
        self.print()


def main() -> None:
    """Main function, yes, main function!."""

    MyApp.load_plugins()
    home = MyApp("myapp")
    home.run()


if __name__ == "__main__":
    main()
