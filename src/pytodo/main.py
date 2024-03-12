"""
pytodo tool main module
"""

from rich.traceback import install

from pytodo import cli

install()  # setup rich


def main() -> None:
    """
    Runs the cli application code.
    """

    # Run the typer app.
    cli.app()


if __name__ == "__main__":  # pragma: no cover
    main()
