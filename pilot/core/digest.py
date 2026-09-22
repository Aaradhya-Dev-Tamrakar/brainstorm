import subprocess
from datetime import datetime, timedelta
from typing import List, Dict, Any

class DigestGenerator:
    def __init__(self, cwd: str = "."):
        self.cwd = cwd

    def get_git_commits(self, days: int = 7) -> List[str]:
        since_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        cmd = ["git", "log", f"--since={since_date}", "--pretty=format:%h|%an|%ad|%s", "--date=short"]
        try:
            res = subprocess.run(cmd, cwd=self.cwd, capture_output=True, text=True, check=True)
            return [line.strip() for line in res.stdout.splitlines() if line.strip()]
        except Exception:
            return []

    def categorize_commits(self, commit_lines: List[str]) -> Dict[str, List[str]]:
        categories: Dict[str, List[str]] = {
            "Features": [],
            "Fixes": [],
            "Performance": [],
            "Documentation": [],
            "Chores & Refactoring": []
        }

        for line in commit_lines:
            parts = line.split("|", 3)
            if len(parts) < 4:
                continue
            sha, author, date, subject = parts
            entry = f"- `{sha}` {subject} ({author}, {date})"

            subject_lower = subject.lower()
            if subject_lower.startswith("feat"):
                categories["Features"].append(entry)
            elif subject_lower.startswith("fix"):
                categories["Fixes"].append(entry)
            elif subject_lower.startswith("perf"):
                categories["Performance"].append(entry)
            elif subject_lower.startswith("docs"):
                categories["Documentation"].append(entry)
            else:
                categories["Chores & Refactoring"].append(entry)

        return categories

    def render_markdown_digest(self, days: int = 7) -> str:
        commits = self.get_git_commits(days=days)
        categories = self.categorize_commits(commits)
        
        lines = [
            f"# Ecosystem Engineering Digest (Past {days} Days)",
            f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*",
            ""
        ]

        total_commits = len(commits)
        lines.append(f"**Total Commits Recorded**: {total_commits}\n")

        for cat, entries in categories.items():
            if entries:
                lines.append(f"### {cat}")
                lines.extend(entries)
                lines.append("")

        if total_commits == 0:
            lines.append("No commits recorded during this timeframe.")

        return "\n".join(lines)
