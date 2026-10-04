#!/usr/bin/env python3
"""Estimate what a chat cost and what a cheaper model or a fresh start would save.

All inputs are estimates supplied by Claude (chars / 4). Outputs are ranges,
API-equivalent USD at list price, ignoring prompt caching (so an upper bound).

Example:
  python savings.py --context 40000 --turns 12 --output 9000 \
      --current opus --suggested sonnet --movable 0.7 \
      --fresh-start 2500 --future-turns 10
"""
import argparse
import sys

# USD per million tokens (input, output). Keep in sync with reference/pricing.md.
PRICES = {
    "haiku": (1.00, 5.00),
    "sonnet": (2.00, 10.00),
    "opus": (4.00, 20.00),
    "fable": (10.00, 50.00),
}

# Token estimates from character counts are rough; report a +/- band.
UNCERTAINTY = 0.25


def model_key(name):
    key = name.strip().lower()
    for known in PRICES:
        if known in key:
            return known
    raise ValueError(f"unknown model {name!r}; expected one of {', '.join(PRICES)}")


def cumulative_input(context, turns):
    """Every turn re-sends the history, so input grows roughly linearly per turn."""
    if turns <= 0 or context <= 0:
        return 0
    return context * (turns + 1) / 2


def cost(model, input_tokens, output_tokens):
    inp, out = PRICES[model_key(model)]
    return (input_tokens * inp + output_tokens * out) / 1_000_000


def estimate(context, turns, output, current, suggested=None, movable=0.0,
             fresh_start=None, future_turns=0):
    """Return a dict of point estimates. `movable` is the share of the work (0-1)
    a cheaper model could handle; `fresh_start` is the size of a condensed brief."""
    if not 0 <= movable <= 1:
        raise ValueError("movable must be between 0 and 1")
    total_in = cumulative_input(context, turns)
    spent = cost(current, total_in, output)
    result = {"input_tokens": total_in, "output_tokens": output, "spent": spent,
              "model_saving": 0.0, "fresh_saving": 0.0}

    if suggested and movable:
        mixed = (cost(current, total_in, output) * (1 - movable)
                 + cost(suggested, total_in, output) * movable)
        result["model_saving"] = max(spent - mixed, 0.0)

    if fresh_start is not None and future_turns > 0 and context > fresh_start:
        # Each future turn would otherwise re-send the old context.
        result["fresh_saving"] = cost(current, (context - fresh_start) * future_turns, 0)

    return result


def band(value):
    return value * (1 - UNCERTAINTY), value * (1 + UNCERTAINTY)


def fmt_money(value):
    lo, hi = band(value)
    if hi < 0.01:
        return "< $0.01"
    return f"≈ ${lo:,.2f}–${hi:,.2f}"


def fmt_pct(part, whole):
    if whole <= 0:
        return "≈ 0%"
    return f"≈ {part / whole:.0%}"


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--context", type=int, required=True, help="current chat size in tokens")
    p.add_argument("--turns", type=int, required=True, help="number of user turns so far")
    p.add_argument("--output", type=int, required=True, help="total assistant output tokens")
    p.add_argument("--current", required=True, help="model used: haiku|sonnet|opus|fable")
    p.add_argument("--suggested", help="cheaper model that could handle part of the work")
    p.add_argument("--movable", type=float, default=0.0, help="share of work it could handle, 0-1")
    p.add_argument("--fresh-start", type=int, help="tokens in the condensed fresh-start brief")
    p.add_argument("--future-turns", type=int, default=0, help="expected further turns")
    args = p.parse_args(argv)

    try:
        r = estimate(args.context, args.turns, args.output, args.current, args.suggested,
                     args.movable, args.fresh_start, args.future_turns)
    except ValueError as err:
        p.error(str(err))

    print(f"Tokens processed so far   ≈ {r['input_tokens']:,.0f} in / {r['output_tokens']:,} out")
    print(f"API-equivalent cost       {fmt_money(r['spent'])}")
    if r["model_saving"]:
        print(f"Saved with {args.suggested:<14} {fmt_money(r['model_saving'])} "
              f"({fmt_pct(r['model_saving'], r['spent'])} of this chat)")
    if r["fresh_saving"]:
        print(f"Saved by fresh start      {fmt_money(r['fresh_saving'])} "
              f"over the next {args.future_turns} turns")
    print("Assumptions: list prices, no caching, tokens ≈ chars/4 (±25%).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
