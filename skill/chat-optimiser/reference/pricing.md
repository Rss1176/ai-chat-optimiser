# Claude API list prices (USD per million tokens)

As of 2026-09-25. Keep in sync with `PRICES` in `scripts/savings.py`.

| Tier   | Current model     | Input | Output |
|--------|-------------------|-------|--------|
| Haiku  | Claude Haiku 4.5  | $1    | $5     |
| Sonnet | Claude Sonnet 5.5 | $2    | $10    |
| Opus   | Claude Opus 5.5   | $4    | $20    |
| Fable  | Claude Fable 5.1  | $10   | $50    |

Notes for the report:
- claude.ai and the desktop app use a subscription, not per-token billing. Present $ as
  "API-equivalent cost" and translate savings into "% of your usage" as well.
- Every turn re-sends the whole chat, so input grows with each turn. Long chats cost much
  more per message than short ones.
- Opus and Fable use a newer tokenizer, which counts ~1.0–1.35× as many tokens as Haiku for
  the same text. This is covered by the ±25% band, so don't add a separate correction.
- Prompt caching lowers real cost; the script ignores it, so its figures are upper bounds.
