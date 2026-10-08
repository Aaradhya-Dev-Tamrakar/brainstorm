# Fleet-Orchestrator Worker Architecture & Concurrency

## 1. Multi-Account Credit Pooling ($N \times 200$)
- Accounts configured in `.env.fleet`:
  - `COPILOT_ACCOUNT_1_NAME="user1"`, `COPILOT_ACCOUNT_1_TOKEN="ghu_..."`
  - Up to 27 accounts pooled dynamically.
- `copilot_fleet.py` round-robins requests across available accounts.
- If an account hits rate limits or monthly exhaustion, it automatically enters a cooldown state while the next active account takes over.

## 2. Worktree Sandboxing
- Workers isolate changes inside `.worktrees/<task_id>`.
- Multiple workers can execute concurrently without merge collisions or dirty working trees on `main`.
- On completion, the worker commits the worktree branch, updates `orchestrator-state/checkpoints/`, and tears down the worktree directory.
