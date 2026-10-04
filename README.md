# Chat Optimiser

> A Claude Skill that makes your Claude chats leaner and cheaper. It spots wasted context, tells you when a smaller Claude model would do the job, and estimates what you'd save.

## What it does

Ask Claude to optimise a chat and the skill reviews it and tells you, in one short report:

- **What it's costing.** Estimated tokens and the API-equivalent $.
- **Where context is wasted.** For example, repeated pastes, topic drift, or verbose answers, each with a one-line fix.
- **Whether a cheaper model would do.** Haiku, Sonnet or Opus for each task, with a confidence level.
- **What you'd save.** Shown as a range, never as an exact figure.
- **A fresh start prompt.** A condensed brief you can paste into a new chat, often on a cheaper model.

Just ask in any chat: *"optimise this chat"*, *"is this chat expensive?"* or *"could a cheaper model do this?"*

## Install (Claude desktop app or claude.ai)

1. Build the zip with `scripts/package.sh`, which creates `dist/chat-optimiser.zip`.
2. In Claude, open **Settings → Capabilities**, make sure **code execution** is on, then under **Skills** choose **Upload skill** and pick the zip.
3. Try it in a chat that's been going for a while.

Custom skills are private to your account. On Team and Enterprise plans they can be shared with your organisation. To update the skill, re-upload the zip. See Anthropic's guide: [Use skills in Claude](https://support.claude.com/en/articles/12512180-use-skills-in-claude).

## Trust and privacy

- **It runs inside your own chat.** The skill makes no external calls, and your conversation doesn't go anywhere new.
- **Every number is an estimate, and labelled as one.** Tokens are counted as characters ÷ 4 (±25%). Prices are API list prices with no caching, so they are an upper bound.
- **It says "keep your current model" when it isn't sure.** If the chat is already lean, it says that too.
- **It uses a little of your usage limit.** Running it is one extra turn. It's kept short on purpose, and the fresh start prompt usually saves far more than the run costs.

On a claude.ai subscription you don't pay per token. Read the $ figures as "how heavy this chat is"; what you actually save is usage limit.

## Repo layout

```
skill/chat-optimiser/     # the skill (this folder is what gets zipped)
  SKILL.md                # instructions, report format, trust rules
  reference/              # pricing, model-routing rubric, waste patterns
  scripts/savings.py      # cost and savings maths (stdlib Python)
scripts/package.sh        # builds dist/chat-optimiser.zip
tests/                    # unit tests for savings.py
evals/evals.json          # sample chats with the verdicts they should get
```

## Development

```bash
python3 -m unittest discover -s tests   # run the tests
scripts/package.sh                      # build the uploadable zip
```

When prices change, update both `reference/pricing.md` and `PRICES` in `scripts/savings.py`.

## Roadmap

- **Verify mode:** with your own API key, re-run sample turns on the cheaper model and show the answers side by side.
- **Claude Code version:** read the session files Claude Code saves on your machine for exact token and cost numbers.
