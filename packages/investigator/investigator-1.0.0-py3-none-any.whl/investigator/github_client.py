from dataclasses import dataclass, field
from datetime import datetime, timedelta
import functools
import logging
import os
import time
from typing import Any, Generator, List, Optional, Self

import pydash
import requests

from investigator import utils
from investigator.config import GitHubAppAuth, GitHubPatAuth, InvestigatorConfig

log = logging.getLogger("investigator.github_client")


class GitHubClientError(Exception):
    pass


@dataclass
class BranchProtectionRule:
    """
    A simplified representation of the graphQL BranchProtectionRule object

    Reference: https://docs.github.com/en/graphql/reference/objects#branchprotectionrule

    """

    # TODO: add all needed rules

    @classmethod
    def from_json(cls, json_object: dict[str, Any]) -> Self:
        def parse_branches(branch_dict: dict[str]) -> List[str]:
            branches = []
            for branch in branch_dict:
                branches.append(branch["name"])
            return branches

        return BranchProtectionRule(
            allow_deletions=pydash.get(json_object, "allowsDeletions", default=False),
            allow_force_pushes=pydash.get(json_object, "allowsForcePushes", default=False),
            branches=parse_branches(pydash.get(json_object, "matchingRefs.nodes")),
            is_admin_enforced=pydash.get(json_object, "isAdminEnforced", default=False),
            required_approving_review_count=pydash.get(json_object, "requiredApprovingReviewCount", default=0),
            requires_code_owner_review=pydash.get(json_object, "requiresCodeOwnerReviews", default=False),
            requires_commit_signatures=pydash.get(json_object, "requiresCommitSignatures", default=False),
            requires_converstaion_resolution=pydash.get(json_object, "requiresConversationResolution", default=False),
        )

    allows_deletions: bool
    allows_force_pushes: bool
    branches: List[str]
    is_admin_enforced: bool
    required_approving_review_count: int
    requires_code_owner_reviews: bool
    requires_commit_signatures: bool
    requires_conversational_resolution: bool
	

def _parse_branch_protection_rules(repo_json: dict[str, Any]):
    branch_protection_rules = []
    for rule in pydash.get(repo_json, "branchProtectionRules.nodes", default=[]):
        branch_protection_rules.append(BranchProtectionRule.from_json(rule))
    return branch_protection_rules


@dataclass
class RepositoryVulnerabilityAlert:
    """
    A simplified representation of the graphQL RepositoryVulnerabilityAlert object

    Reference: https://docs.github.com/en/graphql/reference/objects#repositoryvulnerabilityalert

    """

    @classmethod
    def from_json(cls, json_object: dict[str, Any]) -> Self:
        return RepositoryVulnerabilityAlert(
            created_at=pydash.get(json_object, "createdAt"),
            dismiss_reason=pydash.get(json_object, "dismissReason"),
            dismissed_at=pydash.get(json_object, "dismissedAt"),
            dismisser_login=pydash.get(json_object, "dismisser.login"),
            fixed_at=pydash.get(json_object, "fixedAt"),
            permalink=pydash.get(json_object, "securityAdvisory.severity"),
            severity=pydash.get(json_object, "state"),
            state=pydash.get(json_object, "securityAdvisory.permalink"),
            summary=pydash.get(json_object, "securityAdvisory.summary"),
        )

    created_at: datetime
    dismiss_reason: Optional[str]
    dismissed_at: Optional[datetime]
    dismisser_login: Optional[str]
    fixed_at: Optional[datetime]
    permalink: str
    severity: str
    state: str
    summary: str


@dataclass
class RepositorySecretScanAlert:
    """
    A representation of the data returned by:
    https://docs.github.com/en/rest/secret-scanning/secret-scanning

    """

    @classmethod
    def from_json(cls, alert_json: dict[str, Any]) -> Self:
        return RepositorySecretScanAlert(
            created_at=pydash.get(alert_json, "created_at"),
            html_url=pydash.get(alert_json, "html_url"),
            locations_url=pydash.get(alert_json, "locations_url"),
            multi_repo=pydash.get(alert_json, "multi_repo"),
            number=pydash.get(alert_json, "number"),
            publicly_leaked=pydash.get(alert_json, "publicly_leaked"),
            push_protection_bypassed_by=pydash.get(alert_json, "push_protection_bypassed_by"),
            push_protection_bypassed=pydash.get(alert_json, "push_protection_bypassed"),
            resolution_comment=pydash.get(alert_json, "resolution_comment"),
            resolution=pydash.get(alert_json, "resolution"),
            resolved_at=pydash.get(alert_json, "resolved_at"),
            resolved_by=pydash.get(alert_json, "resolved_by"),
            secret_type_display_name=pydash.get(alert_json, "secret_type_display_name"),
            secret_type=pydash.get(alert_json, "secret_type"),
            state=pydash.get(alert_json, "state"),
            updated_at=pydash.get(alert_json, "updated_at"),
            url=pydash.get(alert_json, "url"),
            validity=pydash.get(alert_json, "validity"),
        )

    created_at: datetime
    html_url: str
    locations_url: str
    multi_repo: Optional[bool]
    number: int
    publicly_leaked: Optional[bool]
    push_protection_bypassed_by: Optional[str]
    push_protection_bypassed: bool
    resolution_comment: Optional[str]
    resolution: Optional[str]
    resolved_at: Optional[datetime]
    resolved_by: Optional[str]
    secret_type_display_name: str
    secret_type: str
    state: str
    updated_at: Optional[datetime]
    url: str
    validity: str


@dataclass
class RepositoryCodeScanAlert:
    """
    A representation of the data returned by:
    https://docs.github.com/en/rest/code-scanning/code-scanning

    """

    @classmethod
    def from_json(cls, json_object: dict[str, Any]) -> Self:
        return RepositoryCodeScanAlert(
            created_at=pydash.get(json_object, "created_at"),
            dismissed_at=pydash.get(json_object, "dismissed_at"),
            dismissed_by=pydash.get(json_object, "dismissed_by.name"),
            dismissed_reason=pydash.get(json_object, "dismissed_reason"),
            fixed_at=pydash.get(json_object, "fixed_at"),
            rule_description=pydash.get(json_object, "rule.description"),
            rule_id=pydash.get(json_object, "rule.id"),
            rule_name=pydash.get(json_object, "rule.name"),
            rule_severity=pydash.get(json_object, "rule.severity"),
            state=pydash.get(json_object, "state"),
            tool_name=pydash.get(json_object, "tool.name"),
            tool_version=pydash.get(json_object, "tool.version"),
            url=pydash.get(json_object, "url"),
        )

    created_at: datetime
    dismissed_at: Optional[datetime]
    dismissed_by: Optional[str]
    dismissed_reason: Optional[str]
    fixed_at: Optional[datetime]
    rule_description: str
    rule_id: str
    rule_name: str
    rule_severity: str
    state: str
    tool_name: str
    tool_version: str
    url: str


@dataclass
class RepositoryCodeScanningAnalysis:
    """
    A simplified representation of the object returned by:
    https://docs.github.com/en/rest/code-scanning/code-scanning?apiVersion=2022-11-28#list-code-scanning-analyses-for-a-repository

    """

    @classmethod
    def from_json(cls, json_object: dict[str, Any]) -> Self:
        return RepositoryCodeScanningAnalysis(
            category=pydash.get(json_object, "category"),
            created_at=pydash.get(json_object, "created_at"),
            tool_name=pydash.get(json_object, "tool.name"),
            tool_version=pydash.get(json_object, "tool.version"),
            url=pydash.get(json_object, "url"),
        )

    category: str
    created_at: datetime
    tool_name: str
    tool_version: str
    url: str


@dataclass
class RepositorySecuritySettings:
    """
    A simplified representation of the security settings returned by:
    https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28#get-a-repository

    """

    @classmethod
    def from_json(cls, json_object: dict[str, Any]) -> Self:
        return RepositorySecuritySettings(
            advanced_security=pydash.get(json_object, "security_and_analysis.advanced_security.status") == "enabled",
            dependabot_security_updates=pydash.get(
                json_object, "security_and_analysis.dependabot_security_updates.status"
            )
            == "enabled",
            secret_scanning_ai_detection=pydash.get(
                json_object, "security_and_analysis.secret_scanning_ai_detection.status"
            )
            == "enabled",
            secret_scanning_non_provider_patterns=pydash.get(
                json_object,
                "security_and_analysis.secret_scanning_non_provider_patterns.status",
            )
            == "enabled",
            secret_scanning_push_protection=pydash.get(
                json_object,
                "security_and_analysis.secret_scanning_push_protection.status",
            )
            == "enabled",
            secret_scanning_validity_checks=pydash.get(
                json_object,
                "security_and_analysis.secret_scanning_validity_checks.status",
            )
            == "enabled",
            secret_scanning=pydash.get(json_object, "security_and_analysis.secret_scanning.status") == "enabled",
        )

    advanced_security: bool
    dependabot_security_updates: bool
    secret_scanning_ai_detection: bool
    secret_scanning_non_provider_patterns: bool
    secret_scanning_push_protection: bool
    secret_scanning_validity_checks: bool
    secret_scanning: bool


@dataclass
class RepositoryDefaultWorkflowPermissions:
    """
    A representation of the data returned by:
    https://docs.github.com/en/rest/actions/permissions?apiVersion=2022-11-28#get-default-workflow-permissions-for-a-repository

    """

    @classmethod
    def from_json(cls, json_object: dict[str, Any]) -> Self:
        return RepositoryDefaultWorkflowPermissions(
            default_workflow_permissions=pydash.get(json_object, "default_workflow_permissions"),
            can_approve_pull_request_review=pydash.get(json_object, "can_approve_pull_request_review"),
        )

    default_workflow_permissions: str  # read or write
    can_approve_pull_request_review: bool


def _parse_vulnerabilities(vuln_alerts_json, include_fixed_dismissed: bool = True) -> list[RepositoryVulnerabilityAlert]:
    vulnerabilities = []
    for vuln_alert_json in vuln_alerts_json:
        alert = RepositoryVulnerabilityAlert.from_json(vuln_alert_json)
        if include_fixed_dismissed | (alert.state == "OPEN"):
            vulnerabilities.append(alert)
    return vulnerabilities


@dataclass
class Repository:
    @classmethod
    def from_json(cls, json_object: dict[str, Any]) -> Self:
        return Repository(
            created_at=pydash.get(json_object, "createdAt"),
            database_id=pydash.get(json_object, "databaseId"),
            default_branch_last_commit=pydash.get(json_object, "defaultBranchRef.target.oid"),
            default_branch_name=pydash.get(json_object, "defaultBranchRef.name"),
            description=pydash.get(json_object, "description"),
            has_no_codeowners_errors=pydash.get(json_object, "codewoners.error", default=[]) == [],
            id=pydash.get(json_object, "id"),
            is_archived=type(pydash.get(json_object, "arhivedAt")) == datetime,
            is_private=pydash.get(json_object, "isPrivate"),
            is_template=pydash.get(json_object, "isTemplate"),
            name=pydash.get(json_object, "name"),
            pushed_at=pydash.get(json_object, "pushedAt"),
            url=pydash.get(json_object, "url"),
            branch_protection_rules=_parse_branch_protection_rules(pydash.get(json_object, "default_workflow_permissions")),
            language=pydash.get(json_object, "primaryLanguage.name"),
            license_name=pydash.get(json_object, "licenseInfo.name"),
            visibility=pydash.get(json_object, "visibility"),
            vulnerability_alerts=_parse_vulnerabilities(
                pydash.get(json_object, "vulnerabilityAlerts.nodes", default=[])
            ),
        )

    created_at: datetime
    database_id: str
    default_branch_last_commit: str
    default_branch_name: str
    description: str
    has_no_codeowners_errors: bool
    id: str
    is_archived: bool
    is_private: bool
    is_template: bool
    name: str
    pushed_at: datetime
    url: str
    branch_protection_rules: List[BranchProtectionRule] = field(default_factory=list)
    language: Optional[str] = None
    license_name: str = None
    visibility: str = None
    vulnerability_alerts: List[RepositoryVulnerabilityAlert] = field(default_factory=list)


class GitHubClient:
    _config: InvestigatorConfig
    _installation_tokens: dict[str, dict[str, str]]

    def __init__(self, config: InvestigatorConfig):
        self._config = config

    def _retrieve_github_app_installation_token(self, auth: GitHubAppAuth):
        jwk_token = utils.generate_jwt(private_key=auth.jwk_private_key, app_id=auth.app_id)

        query = """
            query($installationId: ID!) {
                installation(accessTokensFirst: 1, targetIds: [$installationId]) {
                    nodes {
                        accessToken
                    }
                }
            }
        """
        variables = {"installationId": auth.installation_id}

        return self.graphql_client(query, variables, auth_token=jwk_token)

    def _app_installation_token(self, auth: GitHubAppAuth) -> str:
        if auth.installation_id in self._installation_tokens:
            validity_time = datetime.now() + timedelta(minutes=3)
            expire_time = datetime.strptime(
                self._installation_tokens[auth.installation_id]["expires_at"],
                "%Y-%m-%dT%H:%M:%SZ",
            )
            if expire_time > validity_time:
                return self._installation_tokens[auth.installation_id]["token"]

        self.installation_tokens[auth.installation_id] = self._retrieve_github_app_installation_token(auth)
        return self._installation_tokens[auth.installation_id]["token"]

    def _get_bearer_token(self) -> str:
        if isinstance(self._config.github_auth, GitHubPatAuth):
            return self._config.github_auth.token
        elif isinstance(self._config.github_auth, GitHubAppAuth):
            return self._app_installation_token(self.self._config.github_app_auth)
        else:
            raise ValueError("Either GitHub PAT or GitHub App authentication must be provided")

    def _get_headers(self) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {self._get_bearer_token()}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": self._config.user_agent,
        }

    @functools.cache
    def _get_graphql_query(self, query_name: str) -> str:
        return utils.read_file(f"{os.path.dirname(__file__)}/queries/{query_name}.graphql")

    def graphql_client(self, query: str, variables: dict = None, max_retries: int = 5):
        """Send a GraphQL query to GitHub's API
        :param query: the query to send
        :param variables: the variables to send
        :return: the response from the API
        """
        if variables is None:
            variables = {}

        response = requests.post(
            url=self._config.base_url + "/graphql",
            headers=self._get_headers(),
            json={
                "query": query,
                "variables": variables,
            },
        )

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 403 and "Retry-After" in response.headers:
            retry_after = int(response.headers["Retry-After"])
            log.warning(f"Rate limit exceeded. Retrying after {retry_after} seconds.")
            time.sleep(retry_after)
            max_retries -= 1
            if max_retries > 0:
                return self.graphql_client(query, variables, max_retries)
            else:
                raise GitHubClientError(f"Max retries limit reached")
        else:
            raise GitHubClientError(f"Error while executing query: {response.status_code} {response.text}")

    def rest_v3_client(self, path: str) -> str:
        request = requests.get(
            f"{self._config.base_url}/{path}",
            headers=self._get_headers(),
        )
        if request.status_code == 200 and request.json():
            return request.json()
        else:
            raise GitHubClientError(f"GitHubClientError: {request.status_code} {request.text}")

    def rest_v3_client_paging(self, path: str) -> Generator[Any, Any, Any]:
        def get_next_page(page):
            return page if page.headers.get("link") is not None else None

        session = requests.Session()
        headers = self._get_headers()

        first_page = session.get(
            f"{self._config.base_url}/{path}",
            headers=headers,
        )
        yield first_page

        next_page = first_page
        while get_next_page(next_page) is not None:
            try:
                next_page_url = next_page.links["next"]["url"]
                next_page = session.get(next_page_url, headers=headers)
                yield next_page

            except KeyError:
                logging.info("No more Github pages")
                break

    def get_repository(self, repository_id: str) -> Repository:
        """
        Note: Only OPEN vulnerabilities are retrieved
        TODO: last limited to 5 repos
        TODO: paging
        """

        query = self._get_graphql_query("gh_query_repo")
        variables = {"query": f"repo:{self._config.organization_name}/{repository_id}", "resultsPerPage": 100}

        response = self.graphql_client(query, variables=variables)

        repositories = pydash.get(response, "data.search.repos", default=[])
        log.info(len(repositories))
        if len(repositories) == 0:
            log.info(f"No repositories found for {repository_id}")
            return None
        return Repository.from_json(json_object=repositories[0]["repo"])

    def get_org_repositories(self) -> list[Repository]:
        """
        Note: Only OPEN vulnerabilities are retrieved
        TODO: last limited to 10 repos
        TODO: paging
        """

        query = self._get_graphql_query("gh_query_org_repos")
        variables = {"owner": self._config.organization_name, "cursor": ""}

        response = self.graphql_client(query, variables=variables)

        repositories = pydash.get(response, "data.repositoryOwner.repositories.nodes", default=[])

        if len(repositories) == 0:
            log.info(f"No repositories found for organization {self._config.organization_name}")
            return []
        return [Repository.from_json(json_object=repo) for repo in repositories]

    def get_team_repositories(self, team_slug: str) -> list[Repository]:
        query = self._get_graphql_query("gh_query_team_repos")
        variables = {"org": self._config.organization_name, "team_slug": team_slug}

        response = self.graphql_client(query, variables=variables)

        repositories = pydash.get(response, "data.organization.team.repositories.nodes", default=[])

        if len(repositories) == 0:
            log.info(f"No repositories found for {team_slug}")
            return []
        return [Repository.from_json(json_object=repo) for repo in repositories]

    def get_repo_security_settings(self, repo_name: str) -> RepositorySecuritySettings:
        return RepositorySecuritySettings.from_json(
            self.rest_v3_client(f"repos/{self._config.organization_name}/{repo_name}")
        )

    def get_repo_workflow_permissions(self, repo_name: str) -> RepositoryDefaultWorkflowPermissions:
        return RepositoryDefaultWorkflowPermissions.from_json(
            self.rest_v3_client(f"repos/{self._config.organization_name}/{repo_name}/actions/permissions/workflow")
        )

    def get_repo_last_code_ql_analysis(
        self, repo_name: str, per_page: int = 10, state: str = "open"
    ) -> Optional[RepositoryCodeScanningAnalysis]:
        # There's a risk of this reporting wrong if a codeql analysis is not in the most recent 'per page' results
        json_object = self.rest_v3_client(
            f"repos/{self._config.organization_name}/{repo_name}/code-scanning/analyses?per_page={per_page}"
        )
        for analysis in json_object:
            if pydash.get(analysis, "tool.name") == "CodeQL":
                return RepositoryCodeScanningAnalysis.from_json(analysis)
        return None

    def get_repo_code_scanning_alerts(
        self, repo_name: str, per_page: int = 100, state: str = "open"
    ) -> list[RepositoryCodeScanAlert]:
        alert_list = []
        for response in self.rest_v3_client_paging(
            f"repos/{self._config.organization_name}/{repo_name}/code-scanning/alerts?per_page={per_page}&state={state}&tool_name=CodeQL"
        ):
            if response.status_code == 200:
                if response.json():
                    for alert in response.json():
                        alert_list.append(RepositoryCodeScanAlert.from_json(alert))
                else:
                    continue
            else:
                raise GitHubClientError(f"GitHubClientError for {repo_name}: {response.status_code} {response.text}")

        return alert_list

    def get_repo_secret_scanning_alerts(
        self, repo_name: str, per_page: int = 100, state: str = "open"
    ) -> list[RepositorySecretScanAlert]:
        alert_list = []
        for response in self.rest_v3_client_paging(
            f"repos/{self._config.organization_name}/{repo_name}/secret-scanning/alerts?per_page={per_page}&state={state}"
        ):
            if response.status_code == 200:
                if response.json():
                    for alert in response.json():
                        alert_list.append(RepositorySecretScanAlert.from_json(alert))
                else:
                    continue
            else:
                raise GitHubClientError(f"GitHubClientError for {repo_name}: {response.status_code} {response.text}")

        return alert_list
