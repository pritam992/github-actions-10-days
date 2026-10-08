# Official references

Reviewed 8 October 2026. Versions and plan availability can change; consult these upstream sources when upgrading.

- [GitHub Actions concepts](https://docs.github.com/en/actions/get-started/understand-github-actions)
- [Workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)
- [Reuse workflows](https://docs.github.com/en/actions/how-tos/reuse-automations/reuse-workflows)
- [Manage environments and plan availability](https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/manage-environments)
- [OIDC with AWS](https://docs.github.com/en/actions/how-tos/secure-your-work/security-harden-deployments/oidc-in-aws)
- [Checkout action](https://github.com/actions/checkout)
- [Python setup action](https://github.com/actions/setup-python)
- [Artifact upload action](https://github.com/actions/upload-artifact)
- [AWS credentials action](https://github.com/aws-actions/configure-aws-credentials)
- [Terraform setup action](https://github.com/hashicorp/setup-terraform)
- [AWS Systems Manager CLI walkthrough](https://docs.aws.amazon.com/systems-manager/latest/userguide/walkthrough-cli.html)
- [AWS CLI installation](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)
- [Terraform plan](https://developer.hashicorp.com/terraform/cli/commands/plan)
- [Terraform apply](https://developer.hashicorp.com/terraform/cli/commands/apply)

## Version choices

The teaching workflows use checkout v6, setup-python v7, configure-aws-credentials v6.3.0, setup-terraform v4, and upload-artifact v4. These are intentional example references, not a promise that every action uses its latest release. Terraform CLI is pinned to 1.10.5 for the small built-in-resource lab. Production workflows should pin actions and container bases to reviewed immutable references and maintain an update process.
