# Which model is enough?

Classify each distinct task in the chat, then take the cheapest tier that fits.

| Task type | Examples | Cheapest viable |
|---|---|---|
| Lookup / factual Q&A | definitions, "what's the syntax for…" | Haiku |
| Rewrite / format / translate | tone changes, bullet-ifying, fixing grammar, JSON reshaping | Haiku |
| Summarise / extract | summarise a doc, pull fields from text | Haiku (Sonnet if > ~50 pages or subtle) |
| Brainstorm / draft | emails, outlines, name ideas | Haiku–Sonnet |
| Everyday code | small functions, bug fixes with clear errors, scripts, SQL | Sonnet |
| Analysis with judgement | comparing options, reviewing a contract, data interpretation | Sonnet |
| Multi-step / ambiguous reasoning | architecture, tricky debugging across many files, maths proofs, strategy with many constraints | Opus |
| Long autonomous / frontier work | very long agentic tasks, novel research-grade problems | Opus or Fable |

## Confidence
- **High**: the task matches one row clearly, the answers were short or mechanical, and the user
  accepted them without pushback.
- **Med**: mixed task types, or a cheaper model would likely need one extra turn to get there.
- **Low**: the chat needed deep reasoning, many correction rounds, or the stakes are high
  (legal, medical, financial, production code). → Recommend **keep current model**.

## Rules
- Judge the work that was done, not the length of the chat.
- If the current model is already the cheapest viable tier, say so and stop.
- `movable` (for the script) = the share of the chat's tokens spent on tasks a cheaper tier
  can handle with High or Med confidence. Count Low-confidence tasks as not movable.
- A cheaper model that needs extra turns is not cheaper. When in doubt, round `movable` down.
