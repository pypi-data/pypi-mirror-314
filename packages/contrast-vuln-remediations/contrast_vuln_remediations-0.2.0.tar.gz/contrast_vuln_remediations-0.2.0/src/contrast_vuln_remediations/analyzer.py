"""
Core analyzer class for processing vulnerability data from the Contrast Security API.
"""

import asyncio
import logging
from typing import Dict, List, Optional, Tuple, Any, cast, TypeVar

import httpx
from tqdm.asyncio import tqdm

from contrast_vuln_remediations.models import (
    Application,
    Vulnerability,
    Session,
    RemediationStats,
    ApplicationStats,
)
from contrast_vuln_remediations.exceptions import ContrastAPIError
from contrast_vuln_remediations.resilient import (
    EnhancedAsyncClient,
    TimeoutConfig,
    APIRateLimiter,
)

T = TypeVar("T")

logger = logging.getLogger(__name__)
logger.setLevel(logging.WARNING)
http_logger = logging.getLogger("httpx")
http_logger.setLevel(logging.ERROR)


class VulnerabilityAnalyzer:
    """Analyzes vulnerability data from the Contrast Security API"""

    def __init__(
        self,
        base_url: str,
        org_uuid: str,
        api_key: str,
        auth: str,
        max_concurrent: int = 10,
        metadata_filters: Optional[Dict[str, List[str]]] = None,
        verbose: bool = False,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.org_uuid = org_uuid
        self.verbose = verbose
        self.metadata_filters = metadata_filters or {"Branch Name": ["main", "master"]}
        self.headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "API-Key": api_key,
            "Authorization": auth,
        }

        # Enhanced client configuration
        timeout_config = TimeoutConfig(
            connect_timeout=10.0,
            read_timeout=30.0,
            write_timeout=10.0,
            pool_timeout=10.0,
        )

        rate_limiter = APIRateLimiter(requests_per_second=10.0)

        self.client = EnhancedAsyncClient(
            timeout_config=timeout_config,
            rate_limiter=rate_limiter,
            headers=self.headers,
            follow_redirects=True,
            limits=httpx.Limits(
                max_keepalive_connections=max_concurrent, max_connections=max_concurrent
            ),
        )

        self.semaphore = asyncio.Semaphore(max_concurrent)
        logger.debug("Initialized VulnerabilityAnalyzer")

    async def __aenter__(self) -> "VulnerabilityAnalyzer":
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        await self.client.aclose()

    async def get_applications(self) -> List[Application]:
        """Fetch all applications from the API"""
        url = f"{self.base_url}/ng/{self.org_uuid}/applications"
        params: Dict[str, Any] = {"expand": "skip_links", "limit": 100, "offset": 0}

        try:
            response = await self.client.get(url, params=params)
            response.raise_for_status()
            data = cast(Dict[str, Any], response.json())
            logger.debug(f"Raw API response: {data}")

            applications = cast(List[Dict[str, Any]], data.get("applications", []))
            if not applications:
                logger.warning("No applications found in response")
                return []

            # Debug first application structure
            if applications:
                logger.debug(f"First application structure: {applications[0]}")

            # Process applications with proper typing
            processed_apps: List[Application] = []
            for app in applications:

                app_id: Optional[str] = cast(
                    Optional[str],
                    app.get("app_id")
                    or app.get("application_id")
                    or app.get("applicationId"),
                )
                name: Optional[str] = cast(
                    Optional[str],
                    app.get("name")
                    or app.get("application_name")
                    or app.get("applicationName"),
                )

                if not app_id or not name:
                    logger.warning(
                        f"Skipping application missing required fields: {app}"
                    )
                    continue

                processed_apps.append(
                    Application(
                        id=app_id,
                        name=name,
                        path=str(app.get("path", "")),
                        language=str(app.get("language", "")),
                        total_modules=int(app.get("total_modules", 0)),
                        master=bool(app.get("master", False)),
                    )
                )

            return processed_apps

        except httpx.HTTPError as e:
            logger.error(f"Error fetching applications: {e}")
            raise ContrastAPIError(
                f"Failed to fetch applications: {e}", getattr(e, "response", None)
            )

    async def get_open_vulnerabilities(self, app_id: str) -> List[Vulnerability]:
        """Fetch open vulnerabilities for an application"""
        url = f"{self.base_url}/ng/organizations/{self.org_uuid}/orgtraces/ui"
        params = {"offset": 0, "limit": 100}

        payload: Dict[str, Any] = {
            "quickFilter": "OPEN",
            "modules": [app_id],
            "servers": [],
            "filterTags": [],
            "severities": [],
            "status": [],
            "substatus": [],
            "vulnTypes": [],
            "environments": [],
            "urls": [],
            "sinks": [],
            "securityStandards": [],
            "appVersionTags": [],
            "routes": [],
            "tracked": False,
            "untracked": False,
            "technologies": [],
            "applicationTags": [],
            "applicationImportances": [],
            "languages": [],
            "metadataFilters": [],
        }

        try:
            response = await self.client.post(url, params=params, json=payload)
            response.raise_for_status()
            data = response.json()

            if not data.get("success"):
                logger.warning(f"API indicated failure: {data.get('messages')}")
                return []

            vulnerabilities = []
            for item in data.get("items", []):
                vuln_data = item.get("vulnerability", {})
                # Create a normalized vulnerability object using uuid as id
                normalized_vuln = {
                    "id": vuln_data.get("uuid", ""),  # Use uuid as the id
                    "title": vuln_data.get("title", ""),
                    "severity": vuln_data.get("severity", ""),
                    "status": vuln_data.get("status", ""),
                    "rule_name": vuln_data.get("ruleName", ""),
                }
                vulnerabilities.append(normalized_vuln)  # type: ignore

            if not vulnerabilities and self.verbose:
                logger.info(f"No vulnerabilities found for app {app_id}")

            return vulnerabilities  # type: ignore

        except httpx.HTTPError as e:
            logger.error(f"Error fetching vulnerabilities for app {app_id}: {e}")
            raise ContrastAPIError(
                f"Failed to fetch vulnerabilities: {e}", getattr(e, "response", None)
            )

    async def get_latest_session(self, app_id: str) -> Optional[Session]:
        """Get the most recent session for an application based on metadata filters"""
        url = f"{self.base_url}/ng/organizations/{self.org_uuid}/applications/{app_id}/agent-sessions/filter"

        # Convert metadata filters to API format
        metadata_payload: List[Dict[str, Any]] = [
            {"label": key, "values": values}
            for key, values in self.metadata_filters.items()
        ]

        payload: Dict[str, Any] = {"metadata": metadata_payload}

        try:
            response = await self.client.post(url, json=payload)
            if response.status_code == 404:
                logger.warning(f"No sessions found for app {app_id}")
                return None

            response.raise_for_status()
            data = response.json()

            if not data.get("success"):
                logger.warning(
                    f"API indicated failure for app {app_id}: {data.get('messages')}"
                )
                return None

            agent_sessions = data.get("agentSessions", [])
            if not agent_sessions:
                logger.debug(f"No matching sessions found for app {app_id}")
                return None

            # Sort sessions by createdDate in descending order and get the most recent
            latest_session = max(agent_sessions, key=lambda x: x.get("createdDate", 0))

            # Transform the response into the expected Session format
            return cast(
                Session,
                {
                    "id": latest_session.get("agentSessionId"),
                    "metadata": [
                        {
                            "value": meta.get("value"),
                            "field": meta.get("metadataField", {}).get("displayLabel"),
                        }
                        for meta in latest_session.get("metadataSessions", [])
                    ],
                },
            )

        except httpx.HTTPError as e:
            logger.error(f"Error fetching latest session for app {app_id}: {e}")
            raise ContrastAPIError(
                f"Failed to fetch latest session: {e}", getattr(e, "response", None)
            )
        except (KeyError, ValueError) as e:
            logger.error(f"Error processing session data for app {app_id}: {e}")
            return None

    async def get_session_vulnerabilities(
        self, app_id: str, session_id: str
    ) -> List[Vulnerability]:
        """Get vulnerabilities from a specific session"""
        url = f"{self.base_url}/ng/organizations/{self.org_uuid}/orgtraces/ui"
        params = {"offset": 0, "limit": 100}

        payload: Dict[str, Any] = {
            "agentSessionId": session_id,
            "quickFilter": "OPEN",
            "modules": [app_id],
            "servers": [],
            "filterTags": [],
            "severities": [],
            "status": [],
            "substatus": [],
            "vulnTypes": [],
            "environments": [],
            "urls": [],
            "sinks": [],
            "securityStandards": [],
            "appVersionTags": [],
            "routes": [],
            "tracked": False,
            "untracked": False,
            "technologies": [],
            "applicationTags": [],
            "applicationImportances": [],
            "languages": [],
            "metadataFilters": [],
        }

        try:
            response = await self.client.post(url, params=params, json=payload)
            response.raise_for_status()
            data = response.json()

            if not data.get("success"):
                logger.warning(f"API indicated failure: {data.get('messages')}")
                return []

            # Log the first vulnerability structure for debugging
            if data.get("items"):
                logger.debug(f"Session vulnerability structure: {data['items'][0]}")

            vulnerabilities = []
            for item in data.get("items", []):
                vuln_data = item.get("vulnerability", {})
                # Create a normalized vulnerability object using uuid as id
                normalized_vuln = {
                    "id": vuln_data.get("uuid", ""),  # Use uuid as the id
                    "title": vuln_data.get("title", ""),
                    "severity": vuln_data.get("severity", ""),
                    "status": vuln_data.get("status", ""),
                    "rule_name": vuln_data.get("ruleName", ""),
                }
                vulnerabilities.append(normalized_vuln)  # type: ignore

            if not vulnerabilities and self.verbose:
                logger.info(f"No session vulnerabilities found for app {app_id}")

            return vulnerabilities  # type: ignore

        except httpx.HTTPError as e:
            logger.error(
                f"Error fetching session vulnerabilities for app {app_id}: {e}"
            )
            raise ContrastAPIError(
                f"Failed to fetch session vulnerabilities: {e}",
                getattr(e, "response", None),
            )

    async def analyze_application(self, app: Application) -> Tuple[str, str, int, int]:
        """Analyze remediated vulnerabilities for a single application"""
        async with self.semaphore:
            try:
                # Log the full application object for debugging
                logger.debug(f"Starting analysis for application: {app}")

                app_id = app["id"]
                app_name = app["name"]

                # Get current open vulnerabilities
                open_vulns = await self.get_open_vulnerabilities(app_id)

                # Debug log for vulnerability structure
                if open_vulns:
                    logger.debug(f"First vulnerability structure: {open_vulns[0]}")

                open_vuln_ids = {str(v["id"]) for v in open_vulns}
                logger.debug(f"Open vulnerabilities for app {app_id}: {open_vuln_ids}")
                logger.info(f"App {app_id} has {len(open_vulns)} open vulnerabilities")

                # Get latest session
                latest_session = await self.get_latest_session(app_id)
                if not latest_session:
                    return app_name, app_id, 0, len(open_vulns)

                session_id = latest_session["id"]
                if not session_id:
                    logger.error(f"Session missing ID: {latest_session}")
                    return app_name, app_id, 0, len(open_vulns)

                # Get vulnerabilities from latest session
                session_vulns = await self.get_session_vulnerabilities(
                    app_id, session_id
                )
                # Debug log the first session vulnerability
                if session_vulns:
                    logger.debug(f"First session vulnerability: {session_vulns[0]}")

                session_vuln_ids = {str(v["id"]) for v in session_vulns}
                logger.info(
                    f"Session {session_id} has {len(session_vulns)} vulnerabilities"
                )
                logger.debug(
                    f"Session vulnerabilities for app {app_id}: {session_vuln_ids}"
                )

                # Calculate remediated vulnerabilities
                remediated_count = len(open_vulns) - len(session_vulns)
                logger.info(
                    f"App {app_id} has {remediated_count} remediated vulnerabilities"
                )

                return app_name, app_id, remediated_count, len(open_vulns)

            except Exception as e:
                # Enhanced error logging
                logger.error(
                    f"Error analyzing app {app.get('id', 'unknown')}: {str(e)}\n"
                    f"Application data: {app}\n"
                    f"Error type: {type(e).__name__}\n"
                    f"Full exception details: {repr(e)}",
                    exc_info=True,  # This will include the full stack trace
                )
                return app["name"], app.get("id", "unknown"), 0, 0

    async def analyze_all_applications(self) -> RemediationStats:
        """Analyze remediated vulnerabilities across all applications"""
        try:
            # Get all applications
            applications = await self.get_applications()

            if not applications:
                logger.warning("No applications found")
                return RemediationStats(
                    total_apps=0, total_open=0, total_remediated=0, by_application={}
                )

            # Process applications concurrently with explicit typing and always show progress
            results: List[Tuple[str, str, int, int]] = await tqdm.gather(  # type: ignore
                *[self.analyze_application(app) for app in applications],
                desc="Analyzing applications",
                disable=False,  # Changed from not self.verbose to False
                unit="app",  # Added unit
                colour="green",  # Added color
            )

            # Aggregate results with proper typing
            by_application: Dict[str, ApplicationStats] = {}
            total_remediated: int = 0
            total_open: int = 0

            for app_name, app_id, remediated, open_count in results:  # type: ignore
                by_application[app_id] = ApplicationStats(
                    name=app_name,  # type: ignore
                    remediated=remediated,  # type: ignore
                    open=open_count,  # type: ignore
                )
                total_remediated += remediated  # type: ignore
                total_open += open_count  # type: ignore

            return RemediationStats(
                total_apps=len(applications),
                total_open=total_open,  # type: ignore
                total_remediated=total_remediated,  # type: ignore
                by_application=by_application,
            )

        except Exception as e:
            logger.error(f"Error in vulnerability analysis: {e}")
            raise
