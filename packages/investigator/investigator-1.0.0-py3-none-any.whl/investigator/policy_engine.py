from dataclasses import dataclass
from typing import Any


@dataclass
class GithubPoliciesObject:
    default_branch_protection: bool
    default_branch_requires_approving_reviews: bool


def github_policies(repository: GithubPoliciesObject):
    """Validates a parsed GitHub repository against these policies

    :return: Policy with results
    """

    def policy01(repo):
        return repo.default_branch_protection is not None

    def policy02(repo):
        if repo.default_branch_protection is not None:
            return repo.default_branch_requires_approving_reviews
        return False

    return [
        Policy(
            "policy01",
            "main_branch_protection",
            "Branch protection rule for default branch must be enabled",
            policy01(repository),
        ),
        Policy(
            "policy02",
            "pull_request_review_before_merge",
            "Pull request reviews before merge are required",
            policy02(repository),
        ),
    ]


@dataclass
class Policy:
    policy_id: str
    name: str
    description: str
    compliant: bool

    def in_violation(self):
        return not self.compliant


class ResultSet:
    def __init__(self, reference: dict[Any]):
        self.reference = reference
        self.__results = []
        self.__exclusions = []

    def add_results(self, results: list[Policy]):
        self.__results += results

    def add_exclusions(self, exclusions):
        self.__exclusions += [exclusion.casefold() for exclusion in exclusions]

    def results(self) -> list[Policy]:
        return list(
            filter(
                lambda p: p.policy_id.casefold() not in self.__exclusions,
                self.__results,
            )
        )

    def policy_violations(self) -> list[Policy]:
        return list(filter(lambda p: p.in_violation() is True, self.results()))
