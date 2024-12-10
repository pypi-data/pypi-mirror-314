from rich.console import Console
from rich.logging import RichHandler
from rich.traceback import install
import logging
from typing import Any


# console styling helpers
class STYLES:

    @staticmethod
    def STRING_MAIN(message : Any) -> str:
        return f"[bold red]{message}[/bold red]"
    
    @staticmethod
    def STRING_VALUE_1(message : Any) -> str:
        return f"[italic dark_turquoise]{message}[/italic dark_turquoise]"

    @staticmethod
    def STRING_VALUE_2(message : Any) -> str:
        return f"[italic dark_cyan]{message}[/italic dark_cyan]"
    
    @staticmethod
    def STRING_VALUE_3(message : Any) -> str:
        return f"[italic dark_green]{message}[/italic dark_green]"
    
    @staticmethod
    def INT_1(message : Any) -> str:
        return f"[bold light_coral]{message}[/bold light_coral]"
    
    @staticmethod
    def INT_2(message : Any) -> str:
        return f"[bold light_steel_blue1]{message}[/bold light_steel_blue1]"
    
    @staticmethod
    def INT_3(message : Any) -> str:
        return f"[bold pale_violet_red1]{message}[/bold pale_violet_red1]"

    @staticmethod
    def TEXT(message : Any) -> str:
        return f"[dim italic]{message}[/dim italic]"


# init console
console = Console()


def setup_logging(console : Console):

    install(console = console)

    logging.basicConfig(
        level = "INFO",
        format = "%(message)s",
        datefmt = "[%X]",
        handlers = [RichHandler(console = console)]
    )

    return logging.getLogger("nanoprompt")


# init logger
logger = setup_logging(console)