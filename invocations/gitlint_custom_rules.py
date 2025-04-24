import re

import gitlint


class BranchName(gitlint.rules.CommitRule):
    """Rule to validate branch name."""

    name = "branch-name"
    jira_keys = (
        "BIKA",
        "SD",
        "SA3P",
    )
    id = "UC1"

    def validate(
        self,
        commit: gitlint.git.StagedLocalGitCommit,
    ) -> list[gitlint.rules.RuleViolation] | None:
        """Validate branch name."""
        jira_keys = "|".join(self.jira_keys)
        jira_issue = rf"({jira_keys})-\d+(?:-[a-z0-9]+)+"
        branch_name_format = rf"^(feature|hotfix)\/{jira_issue}$"
        current_branch = commit.context.current_branch
        # Ignore rule during rebase
        if current_branch == "HEAD":
            return None
        if re.fullmatch(branch_name_format, current_branch):
            return None
        msg = (
            "Branch name is not valid. "
            "Template: feature/[task-id]-[short-and-meaningful-description]. "
            f"Got: {current_branch}."
        )
        return [gitlint.rules.RuleViolation(self.id, msg, line_nr=1)]
