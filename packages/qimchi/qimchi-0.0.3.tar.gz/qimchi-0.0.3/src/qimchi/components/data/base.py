from pathlib import Path
from abc import ABC, abstractmethod
from dash import html


class Database(ABC):
    def __init__(self, path: Path) -> None:
        """
        Base class for database folders in Qimchi

        """
        super().__init__()
        self.path = path

    @abstractmethod
    def options(self):
        """
        Returns the options for the data selector for current database type

        """

    def selector(self) -> html.Div:
        """
        Returns the data selector component

        Returns:
            html.Div: The data selector component

        """
        return html.Div(
            [
                self.options(),
            ],
            **{"data-theme": "light"},
        )


class Data(ABC):
    def __init__(self, path: Path) -> None:
        """
        Base class for data files in Qimchi

        """
        super().__init__()
        self.path = path
