"""Token prices and cost math"""

from dataclasses import dataclass

TOKENS_PER_MILLION = 1_000_000


@dataclass(frozen=True)
class Price:
    """Price in USD per million tokens"""

    input_per_mtok: float
    output_per_mtok: float


# Source: https://platform.claude.com/docs/en/about-claude/pricing
# Read on 2026-11-25. Prices change. Check the page again before you trust them.
PRICES: dict[str, Price] = {
    "claude-sonnet-5-5": Price(input_per_mtok=2.0, output_per_mtok=10.0),
}


def cost_usd(model: str, input_tokens: int, output_tokens: int) -> float:
    """Return the cost in USD of one API call."""
    if model not in PRICES:
        raise ValueError(f"Unknown model: {model}")

    if input_tokens < 0 or output_tokens < 0:
        raise ValueError(
            f"Token counts must be 0 or more: input={input_tokens}, output={output_tokens}"
        )

    price = PRICES[model]

    input_cost = price.input_per_mtok * input_tokens / TOKENS_PER_MILLION
    output_cost = price.output_per_mtok * output_tokens / TOKENS_PER_MILLION
    return input_cost + output_cost
