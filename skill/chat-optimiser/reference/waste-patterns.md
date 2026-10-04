# Context-waste patterns

Look for these, and report the 3 that cost the most tokens. Estimate each as chars ÷ 4.

| Pattern | What it looks like | One-line fix |
|---|---|---|
| Repeated paste | The same file, doc or error log pasted more than once | Paste once; refer back to it ("the file above") |
| Oversized paste | A whole file or document pasted when only one section mattered | Paste only the relevant section |
| Topic drift | The chat moved on to an unrelated task partway through | Start a new chat for each new task |
| Long-lived thread | Many turns of old back-and-forth still being re-sent | Use the fresh start prompt to restart with a summary |
| Verbose outputs | Long answers when a short one was enough; full rewrites for small changes | Ask for "only the changed lines" or "answer in 3 bullets" |
| Preamble and pleasantries | Long set-up or role-play instructions repeated each message | Put stable instructions in a Project or custom instructions once |
| Unused attachments | Files uploaded but never referenced | Remove them, or don't attach them next time |
| Correction loops | Several rounds of "no, I meant…" | State constraints and an example up front |
| Over-powered model | Simple tasks run on Opus or Fable | Switch model for these tasks (see routing-rubric.md) |

Only flag a pattern you can point to in this chat. If the chat is already lean, say so.
