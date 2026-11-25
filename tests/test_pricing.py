"""Tests for token cost math"""

import pytest

from llmcost.pricing import cost_usd

MODEL = "claude-sonnet-5-5"


def test_one_million_input_tokens_cost_input_price() -> None:
    assert cost_usd(MODEL, input_tokens=1_000_000, output_tokens=0) == pytest.approx(2.0)


def test_one_million_output_tokens_costs_output_price() -> None:
    assert cost_usd(MODEL, input_tokens=0, output_tokens=1_000_000) == pytest.approx(10.0)


def test_small_request_adds_input_and_output_cost() -> None:
    assert cost_usd(MODEL, input_tokens=1_000, output_tokens=500) == pytest.approx(0.007)


def test_unknown_model_raises_value_error() -> None:
    with pytest.raises(ValueError):
        cost_usd("not-a-model", input_tokens=10, output_tokens=10)


def test_negative_tokens_raise_value_error() -> None:
    with pytest.raises(ValueError):
        cost_usd(MODEL, input_tokens=-1, output_tokens=0)
