"""Functions for interacting with GitHub pull requests."""

from typing import Any

from github import Auth, Github, PullRequest
from pydash import pick

from beamlit.common.secrets import Secret


def list_open_pull_requests(
    repository: str,
):
    """
    This function will fetch a list of the repository's Pull Requests (PRs).
    It will return the title, and PR number of 5 PRs.
    """
    auth = Auth.Token(Secret.get("GITHUB_TOKEN"))
    gh = Github(auth=auth)
    repo = gh.get_repo(repository)
    return [_format_pull_request(pr) for pr in repo.get_pulls(state="open")[:5]]


def _format_pull_request(pr: PullRequest) -> dict[str, Any]:
    raw_data = pr.raw_data
    raw_data["reviewers"] = [reviewer["login"] for reviewer in raw_data["requested_reviewers"]]
    raw_data["assignees"] = [assignee["login"] for assignee in raw_data["assignees"]]

    return pick(
        raw_data,
        [
            "id",
            "title",
            "labels",
            "number",
            "html_url",
            "diff_url",
            "patch_url",
            "commits",
            "additions",
            "deletions",
            "changed_files",
            "comments",
            "state",
            "user.login",
            "assignees",
            "reviewers",
            "created_at",
            "updated_at",
        ],
    )
