# Set up and publish your course

## Prerequisites

- A GitHub account with permission to manage the learning repository.
- Git and Python 3.12 locally; Docker for Day 6 onward.
- A terminal and editor. GitHub's browser editor also works for early workflow labs.
- For cloud labs: an AWS sandbox, AWS CLI v2 and permission to configure IAM, ECR, EC2 and SSM.
- Terraform 1.10.5 for Day 9's local exercise.

This kit ships without active workflows so publishing the guide alone does not launch every lab. Copy examples into `.github/workflows/` as instructed each day.

## Publish to a new GitHub repository

Create an empty repository named `github-actions-10-days` under the account you choose. Choose public if you want others to read it; choose private if you want restricted access. Do not initialize it with README if you will push this complete folder.

Extract the downloaded ZIP. Open a terminal inside its `github-actions-10-days` folder. Replace YOUR-USERNAME with the actual owner:

```bash
git init -b main
git add .
git commit -m "Add visual 10-day GitHub Actions guide"
git remote add origin https://github.com/YOUR-USERNAME/github-actions-10-days.git
git push -u origin main
```

Use GitHub's supported Git credential manager, SSH setup or GitHub CLI login. Do not put a token inside the remote URL or commit it to the repository.

For an existing repository, clone it and copy this guide into a new branch first. Inspect overlapping filenames instead of overwriting them blindly; open a PR for review. Repository-root lab paths assume the course files live at the root—adjust them if using a subdirectory.

## Confirm the published result

1. Open README on GitHub. Confirm the cover image appears.
2. Open a day link and confirm the Mermaid diagram renders.
3. Open the workflow source link and use the Back/Next lesson navigation.
4. Activate Day 1 and confirm its first run.

Mermaid diagrams render in GitHub Markdown without publishing a website. Some local Markdown viewers need an extension for Mermaid. A GitHub Pages website is a separate optional project, not required for this guide.

## Optional polishing

Add a repository description and topics such as `github-actions`, `cicd`, `devops` and `learning`. Choose a license before inviting reuse; no license has been selected for you. Add a CI status badge after the repository owner/name and active workflow filename are known.
