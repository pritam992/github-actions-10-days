# Debugging field guide

Start with the first failing step, not the last error on screen. Write expected result, actual result and evidence before changing code.

| Symptom | Check first | Fix direction |
|---|---|---|
| No workflow run | File location, YAML, Actions enabled, event filters | Use `.github/workflows/*.yml`; match the event |
| No manual-run button | Default branch contains `workflow_dispatch` | Commit workflow to default branch |
| Required check stays pending | Workflow path or branch filter skipped it | Reconsider filters on required workflows |
| Files missing | Checkout and current directory | Checkout before reading repo files |
| Downstream job skipped | `needs` dependency failed | Fix dependency; use `always()` only when appropriate |
| Empty variable or secret | Name, scope, environment, fork restrictions | Configure correct scope; do not expose secrets to forks |
| Empty job output | Step ID, output key, job mapping | Trace step → job → needs expression |
| Matrix artifact conflict | Repeated artifact name | Include matrix value in name |
| Tests fail but step succeeds | Pipeline exit status | Use pipefail; avoid swallowing errors |
| GHCR permission denied | Token permissions and package access | `packages: write` plus allowed package/repo relationship |
| OIDC denied | Role ARN, aud, sub, branch/environment | Match trust policy to actual token identity |
| ECR tag already exists | Immutable tag reused | Deploy existing tag or publish a new commit |
| SSM target offline | Agent, instance profile, network, region | Restore managed-node connectivity |
| Container cannot pull | Instance ECR role and network | Fix pull permissions and ECR/S3 access |
| Health check fails | Container logs, port mapping, endpoint | Inspect remote service before retrying |
| Terraform plan differs | Commit, state, variables, provider versions | Replan and review the exact intended change |

## Useful evidence

- Run URL and workflow commit SHA.
- First failing step and error text, with credentials removed.
- Trigger type, branch and selected environment.
- Expected role/account/region, using redacted IDs when sharing publicly.
- SSM command status and remote output for deployment failures.

Do not print the entire environment or dump tokens to debug authentication. Use identity APIs and nonsecret configuration checks.
