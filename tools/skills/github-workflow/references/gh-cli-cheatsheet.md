# GitHub CLI (`gh`) Workflow Cheatsheet

A concise operational reference for managing issues, branches, reviews, and pull requests via the GitHub CLI.

---

## 1. Issue Management

### Create an Issue
```bash
# Interactive mode
gh issue create

# Direct flag-based creation
gh issue create \
  --title "feat(scope): descriptive title" \
  --body "## Overview\nContext here...\n\n## Tasks\n- [ ] Task 1\n- [ ] Task 2"

# Create with specific assignees or labels
gh issue create --title "fix(data): bug title" --label "bug" --assignee "@me"
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
gh issue comment <ISSUE_NUMBER> --body "Completed refactor of data ingestion pipeline. Verified 85 tests passing."

# Close or Reopen Issue
gh issue close <ISSUE_NUMBER> --reason "completed"
gh issue reopen <ISSUE_NUMBER>
```

---

### Create a Pull Request
```bash
# Standard PR with full sidebar metadata (reviewer, assignee, labels, issue link)
gh pr create \
  --base main \
  --head <FEATURE_BRANCH> \
  --title "feat(scope): descriptive title (#<ISSUE_NUMBER>)" \
  --assignee "@me" \
  --label "enhancement,WP4" \
  --reviewer <COLLABORATOR_USERNAME> \
  --body "## Summary\n- Detailed changes...\n\nCloses #<ISSUE_NUMBER>\n\n## Verification\n- Tests passing."
```

### Key GitHub Issue Linking Keywords
Use any of these in the PR body to automatically close the issue upon merge:
- `Closes #123`
- `Fixes #123`
- `Resolves #123`

### View & Inspect Pull Requests
```bash
# View PR summary
gh pr view <PR_NUMBER>

# View attached commits
gh pr view <PR_NUMBER> --json commits

# Check review and check runs status
gh pr checks <PR_NUMBER>
gh pr status
```

### Request or Modify Reviewers
```bash
# Add reviewer
gh pr edit <PR_NUMBER> --add-reviewer <COLLABORATOR_USERNAME>

# Request team review
gh pr edit <PR_NUMBER> --add-reviewer <ORGANIZATION/TEAM>
```

### Merge Pull Request
```bash
# Squash merge and delete head branch
gh pr merge <PR_NUMBER> --squash --delete-branch

# Rebase merge
gh pr merge <PR_NUMBER> --rebase --delete-branch
```
