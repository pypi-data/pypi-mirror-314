from dataclasses import dataclass
from typing import Optional


@dataclass
class GitHubPatAuth:
    token: str


@dataclass
class GitHubAppAuth:
    app_id: str
    installation_id: str
    jwk_private_key: bytes


@dataclass
class InvestigatorConfig:
    def __post_init__(self):
        if self.organization_name is None:
            raise ValueError("A GitHub organization name must be provided")

    organization_name: str
    github_auth: GitHubAppAuth | GitHubPatAuth
    base_url: str = "https://api.github.com"
    user_agent: str = "Investigator"
