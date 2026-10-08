# AWS sandbox setup for Days 7–8

Use one sandbox account and region for the initial lab. Replace every uppercase placeholder below with your actual values. The AWS CLI commands assume you are already authenticated locally to that sandbox with provisioning permissions. These are setup instructions, not actions this guide has already performed.

## 1. Create the image repository

```bash
aws ecr create-repository --repository-name github-actions-bootcamp --image-tag-mutability IMMUTABLE --region ap-south-1
```

You can choose another supported region. With immutable tags, rerunning publication of the exact same SHA will fail if that tag already exists; reuse the published image or publish a new commit.

Set these GitHub repository variables:

| Variable | Example / meaning |
|---|---|
| `AWS_REGION` | `ap-south-1` |
| `ECR_REGISTRY` | `ACCOUNT_ID.dkr.ecr.ap-south-1.amazonaws.com` |
| `ECR_REPOSITORY` | `github-actions-bootcamp` |
| `AWS_ROLE_ARN` | ARN of publisher role created below |
| `AWS_DEPLOY_ROLE_ARN` | ARN of separate deployment role |
| `EC2_INSTANCE_ID` | Your sandbox managed instance ID |

## 2. Register GitHub's OIDC provider

In AWS IAM → Identity providers, reuse or add the OpenID Connect provider:

- Provider URL: `https://token.actions.githubusercontent.com`
- Audience: `sts.amazonaws.com`

Create a publisher role with this trust policy after replacing ACCOUNT_ID, OWNER and REPO:

```json
{
  "Version": "2012-10-17",
  "Statement": [{
    "Effect": "Allow",
    "Principal": {"Federated": "arn:aws:iam::ACCOUNT_ID:oidc-provider/token.actions.githubusercontent.com"},
    "Action": "sts:AssumeRoleWithWebIdentity",
    "Condition": {
      "StringEquals": {
        "token.actions.githubusercontent.com:aud": "sts.amazonaws.com",
        "token.actions.githubusercontent.com:sub": "repo:OWNER/REPO:ref:refs/heads/main"
      }
    }
  }]
}
```

Attach the following permission policy. Replace REGION and ACCOUNT_ID. `GetAuthorizationToken` requires wildcard resource scope; repository operations are restricted to the teaching repository.

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "ecr:GetAuthorizationToken",
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": ["ecr:BatchCheckLayerAvailability", "ecr:InitiateLayerUpload", "ecr:UploadLayerPart", "ecr:CompleteLayerUpload", "ecr:PutImage", "ecr:BatchGetImage"],
      "Resource": "arn:aws:ecr:REGION:ACCOUNT_ID:repository/github-actions-bootcamp"
    }
  ]
}
```

## 3. Prepare a managed EC2 instance

Use an existing disposable Linux instance or launch a small x86_64 Amazon Linux 2023 instance. The hosted runner builds an x86_64 image; do not select an ARM instance unless you also implement a matching image build.

1. Attach an instance profile with `AmazonSSMManagedInstanceCore` and the ECR pull policy below.
2. Ensure SSM Agent is installed and running. Confirm the instance appears online under Systems Manager managed nodes.
3. Provide outbound HTTPS access to required SSM, ECR and S3 endpoints through an appropriate network path. Private subnets need NAT or the relevant VPC endpoints. This lab does not require inbound SSH or an internet-facing app port.
4. Through Session Manager, install the tools:

   ```bash
   sudo dnf install -y docker curl
   sudo systemctl enable --now docker
   aws --version
   docker --version
   ```

   Ensure AWS CLI v2 is installed if `aws --version` fails; follow the official AWS CLI installation guide in SOURCES.md.
5. Verify `sudo docker info` works. SSM shell commands run with elevated privileges in this example.

Instance ECR pull policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {"Effect": "Allow", "Action": "ecr:GetAuthorizationToken", "Resource": "*"},
    {
      "Effect": "Allow",
      "Action": ["ecr:BatchCheckLayerAvailability", "ecr:GetDownloadUrlForLayer", "ecr:BatchGetImage"],
      "Resource": "arn:aws:ecr:REGION:ACCOUNT_ID:repository/github-actions-bootcamp"
    }
  ]
}
```

## 4. Create the separate deployment role

Use the OIDC trust policy from step 2, but change the exact `sub` value to:

```text
repo:OWNER/REPO:environment:sandbox
```

An environment changes the token's subject shape. Restrict the GitHub `sandbox` environment to main; the workflow also checks main. The IAM environment subject alone does not encode a branch restriction.

Attach this policy, replacing all placeholders:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "ssm:SendCommand",
      "Resource": [
        "arn:aws:ssm:REGION::document/AWS-RunShellScript",
        "arn:aws:ec2:REGION:ACCOUNT_ID:instance/INSTANCE_ID"
      ]
    },
    {
      "Effect": "Allow",
      "Action": "ssm:GetCommandInvocation",
      "Resource": "*"
    }
  ]
}
```

`SendCommand` is powerful: this role can execute shell commands on the named instance. Keep it limited to the sandbox and protected workflow changes. The instance role pulls from ECR; the deployment workflow's role does not need ECR push access.

## 5. Configure the environment and verify

Create GitHub environment `sandbox`, restrict deployment branches to main, and configure reviewers where available. On GitHub Free, Pro and Team, required reviewers and wait timers are available for public repositories; private-repository support differs by plan. If unavailable, use a clearly documented manual lab gate, not a claim of enforced independent approval.

Day 8 deploys the container on `127.0.0.1:8080` on EC2 and checks `/health` there. It intentionally does not expose a public website. To inspect the message, open Session Manager and run `curl http://127.0.0.1:8080/`.

The script pulls before removing the old container. A failed pull keeps the old container running. Failure after replacement can leave a broken service; rerun the workflow with a known-good SHA. A timed-out workflow does not guarantee that the remote command stopped—inspect its status before retrying.

## Cleanup

After the cloud labs, remove the training container and image copies you no longer need. Terminate only the disposable instance you created for the course and verify associated EBS volumes. Delete the dedicated ECR repository after confirming it contains no needed images. Remove dedicated IAM roles/policies and networking resources created solely for the lab. Keep shared OIDC providers and existing network resources. Check for chargeable NAT gateways, retained volumes, images and public IPv4 addresses.

## Next level

Promote by image digest, implement blue/green or rolling deployments, verify application behavior beyond a single health endpoint, and test recovery. Add a separate account per environment only after the single-account trust model is understood.
