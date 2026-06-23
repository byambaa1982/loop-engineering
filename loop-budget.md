# loop-budget

Use this budget before scheduling a recurring agent loop.

| Item | Estimate |
| --- | ---: |
| Runs per month | 20 |
| Input tokens per run | 50,000 |
| Output tokens per run | 10,000 |
| Human review minutes per run | 10 |
| Monthly budget limit | TBD |
| Rollback owner | TBD |

## Cost Notes
- Prefer smaller context windows over broad repository scans.
- Cache stable documentation and architecture notes where possible.
- Stop the loop when repeated runs produce no meaningful changes.
