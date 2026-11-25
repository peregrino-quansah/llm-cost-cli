"""Command-line entry point for llmcost."""

from llmcost import __version__


def main() -> None:
    """Print the version."""
    print(f"llmcost {__version__}")


if __name__ == "__main__":
    main()
