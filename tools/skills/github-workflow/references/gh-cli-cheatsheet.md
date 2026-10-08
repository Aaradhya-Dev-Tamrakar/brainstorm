# GitHub CLI (`gh`) Workflow Cheatsheet

A concise operational reference for managing issues, branches, reviews, and pull requests via the GitHub CLI.

---

## 1. Issue Management

### Create an Issue
```bash
# Interactive mode
gh issue create

# Direct flag-based creation with explicit assignee and labels
gh issue create \
  --title "feat(scope): descriptive title" \
  --assignee "AaradhyaDT" \
  --label "enhancement" \
  --body "## Overview\nContext here...\n\n## Tasks\n- [ ] Task 1\n- [ ] Task 2"
```

### View & Inspect Issues
```bash
# View formatted issue in terminal
gh issue view <ISSUE_NUMBER>

# View raw JSON data
gh issue view <ISSUE_NUMBER> --json number,title,body,state,assignees

# View web URL in browser
gh issue view <ISSUE_NUMBER> --web
```

### Update Issue Body & Comments
```bash
# Overwrite full body markdown
gh issue edit <ISSUE_NUMBER> --body "Updated body content"

# Append progress update comment
gh issue comment <ISSUE_NUMBER> --body "Completed refactor. Verified 116 tests passing."

# Close Issue with Verification Comment & Commit Evidence
gh issue close <ISSUE_NUMBER> --comment "Completed in commit <SHORT_SHA>. Verified 100% test pass (0 discrepancies)."

# Reopen Issue
gh issue reopen <ISSUE_NUMBER>
```

### Set Native Issue Type (Bug, Feature, Task)
```bash
# Set type via GitHub REST API
gh api -X PATCH repos/{owner}/{repo}/issues/<ISSUE_NUMBER> -f type="Feature"
gh api -X PATCH repos/{owner}/{repo}/issues/<ISSUE_NUMBER> -f type="Bug"
gh api -X PATCH repos/{owner}/{repo}/issues/<ISSUE_NUMBER> -f type="Task"
```

### Milestone & Label Management
> [!NOTE]
> `gh milestone` is not a native top-level command in GitHub CLI. Milestones must be queried/created via the REST API (`gh api`) or attached via `gh issue edit --milestone`.

```bash
# List active milestones
gh api repos/{owner}/{repo}/milestones --jq '.[] | "\(.number): \(.title) (\(.state))"'

# Create a milestone
gh api -X POST repos/{owner}/{repo}/milestones -f title="M1: Architecture Freeze" -f description="Milestone scope"

# Attach issue to milestone
gh issue edit <ISSUE_NUMBER> --milestone "M1: Architecture Freeze"

# Add or remove labels
gh issue edit <ISSUE_NUMBER> --add-label "WP4,enhancement"
gh issue edit <ISSUE_NUMBER> --remove-label "wontfix"

# Enrich label metadata with description and hex color
gh label edit WP4 --description "Work Package 4: Fairness Metrics" --color "d4c5f9"
gh label create "phase-2" --description "Post-capstone backlog" --color "006b75"
```

### Native Sub-Issue Relationships (GraphQL)
```bash
# Capture Node IDs
gh api graphql -f query='query { repository(owner: "{owner}", name: "{repo}") { issue(number: 28) { id } } }'

# Link Parent -> Child Sub-Issue
gh api graphql -f query='mutation {
  addSubIssue(input: {
    issueId: "<PARENT_NODE_ID>",
    subIssueId: "<CHILD_NODE_ID>"
  }) {
    issue { id }
    subIssue { id }
  }
}'
```

### GitHub Projects (ProjectsV2) & Cross-Repo Tracking
```bash
# Create project under personal namespace (if org creation is restricted)
gh project create --owner @me --title "Project Board Title"

# Link project to personal mirror repository
gh api graphql -f query='mutation {
  linkProjectV2ToRepository(input: {
    projectId: "<PROJECT_NODE_ID>",
    repositoryId: "<REPO_NODE_ID>"
  }) {
    repository { id }
  }
}'

# Add issue to Project Board
gh api graphql -f query='mutation {
  addProjectV2ItemById(input: {
    projectId: "<PROJECT_NODE_ID>",
    contentId: "<ISSUE_NODE_ID>"
  }) {
    item { id }
  }
}'

# List project items
gh project item-list <PROJECT_NUMBER> --owner @me --format json
```

---

## 2. Pull Request Management

### Create a Pull Request (Manual CLI Standard)
```bash
gh pr create \
  --base main \
  --head <FEATURE_BRANCH> \
  --title "feat(scope): descriptive title (#<ISSUE_NUMBER>)" \
  --assignee "AaradhyaDT" \
  --reviewer "tiixsha" \
  --label "enhancement" \
  --body "## Summary\n- Detailed changes...\n\nCloses #<ISSUE_NUMBER>\n\n## Verification\n- Tests passing."
```

### Automated BRL Pull Request Dispatch (Ecosystem Standard)
When `sync.bat` is available in the repository root, avoid manual multi-step `git branch`, `git push`, and `gh pr create`:
```powershell
.\sync.bat -PR -m "feat(scope): summary" -Issue <ISSUE_NUMBER> -Reviewer <REVIEWER_HANDLE>
```

### Issue Linking Keywords
Use any of these in the PR body to automatically close the issue upon merge:
- `Closes #123`
- `Fixes #123`
- `Resolves #123`

### View & Inspect Pull Requests
```bash
# View PR summary
gh pr view <PR_NUMBER>

# View attached commits
gh pr view <PR_NUMBER> --json commits,assignees,reviewRequests,milestone

# Check status of CI workflow runs
gh pr checks <PR_NUMBER>

# Overall PR status across current branch
gh pr status
```

### Request or Modify Reviewers
```bash
# Add peer reviewer
gh pr edit <PR_NUMBER> --add-reviewer <COLLABORATOR_USERNAME>

# Request team review
gh pr edit <PR_NUMBER> --add-reviewer <ORGANIZATION/TEAM>
```

### Edit PR Body & Link Issues (Retroactive / Active)
```bash
# Update PR body to link issue or add test proof (works on open and merged PRs)
gh pr edit <PR_NUMBER> --body "## Summary
- Feature changes...

Closes #<ISSUE_NUMBER>

## Verification
- Tests passed."
```

### Merge Pull Request
```bash
# Squash merge and delete head branch
gh pr merge <PR_NUMBER> --squash --delete-branch

# Rebase merge
gh pr merge <PR_NUMBER> --rebase --delete-branch
```

---

## 3. GitHub Actions & Workflow Telemetry

### Inspect Workflow Runs
```bash
# List recent workflow runs across the repository
gh run list

# List runs for a specific workflow
gh run list --workflow verification.yml

# Watch an active run in real-time until completion
gh run watch <RUN_ID>

# View failure logs for a failed run
gh run view <RUN_ID> --log-failed
```

### Manual Workflow Dispatch
```bash
# Trigger a workflow with workflow_dispatch enabled
gh workflow run verification.yml --ref main
```
