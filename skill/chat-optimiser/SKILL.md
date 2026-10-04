---
name: chat-optimiser
description: Reviews the current conversation and reports how to make it cheaper. It estimates the chat's token cost, flags wasted context, says whether a cheaper Claude model (Haiku or Sonnet) could have done the same work, and writes a condensed fresh start prompt. Use when the user asks to optimise, audit or slim down this chat, asks whether the chat is expensive or uses too much of their limit, or asks whether a cheaper or smaller model could do the job.
---

# Chat Optimiser

Review **this conversation** (everything before the request) and produce one short report.
Running this skill uses the user's own limit, so be economical: no preamble, no essay, at most ~25 lines plus the fresh start prompt.

## Steps
1. **Size it.** Estimate the chat's total tokens as characters ÷ 4, including pasted files. Count the user turns and estimate the total assistant output. Note the current model (ask only if you can't tell; assume Opus otherwise and say so).
2. **Find the waste.** Check `reference/waste-patterns.md`. List up to 3 patterns that clearly occur here, largest first. Don't pad: if none occur, write "None significant — chat is lean."
3. **Judge the model fit.** Use `reference/routing-rubric.md` to list the distinct tasks, with one tier per task (the lower tier if confidence is High, otherwise the upper) and a confidence level. Work out `movable`, the share of tokens a cheaper tier could handle.
4. **Cost it.** If code execution is available, run this from the skill directory (leave out `--suggested`/`--movable` if no cheaper tier applies):
   `python scripts/savings.py --context N --turns T --output O --current MODEL --suggested MODEL --movable M --fresh-start F --future-turns 10`
   Otherwise, do the same arithmetic using `reference/pricing.md`: cumulative input ≈ context × (turns+1) ÷ 2.
5. **Write the fresh start prompt.** Write a self-contained brief (aim for under 10% of the chat's size) covering the goal, decisions made, key facts and data, current state, and the next step. Leave out the discussion that led there. Never invent details; use `<placeholder>` for anything not in the chat. If the chat covers several unrelated tasks, write one short brief per task. If the chat is under ~2k tokens or already finished, write "Not needed" and drop the fresh start savings line.

## Report format
```
## Chat Optimiser report
**Size:** ≈ N tokens · T turns · model: X
**Top waste**
1. <pattern> — ≈ n tokens — <one-line fix>
2. …
3. …
**Model fit**
- <task> → <tier> (<High/Med/Low>)
**Estimated savings** (API-equivalent, list prices, no caching)
- Cheaper model for suitable tasks: ≈ $a–$b (≈ p% of this chat)
- Fresh start for the next 10 turns: ≈ $c–$d
_Assumptions: list prices, no caching, tokens ≈ chars ÷ 4 (±25%)._
**Recommendation:** <one sentence: e.g. "Continue in a new chat on Sonnet using the prompt below.">
### Fresh start prompt (paste into a new chat)
<brief>
```

## Trust rules
- Mark every estimated number (tokens, $, %) with "≈"; exact counts such as turns don't need it. Keep the assumptions line. Never present an estimate as exact.
- When confidence is Low, recommend **keep current model**. Never overstate savings. Low confidence rules out a model switch, but a fresh start can still be offered.
- If the chat is already lean or the model is already the right one, say so plainly. That is a valid result.
- Make no external calls. Nothing leaves this conversation.
- On claude.ai plans, explain that $ is the API-equivalent cost and that the real benefit is using less of the plan's usage limit.
