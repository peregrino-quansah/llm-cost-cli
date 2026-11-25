"""Tests for the llmcost command-line entry point"""

import pytest

from llmcost.cli import main


def test_main_prints_version(capsys: pytest.CaptureFixture[str]) -> None:
    """main() prints the tool name and version"""
    main()
    captured = capsys.readouterr()
    assert captured.out == "llmcost 0.1.0\n"
