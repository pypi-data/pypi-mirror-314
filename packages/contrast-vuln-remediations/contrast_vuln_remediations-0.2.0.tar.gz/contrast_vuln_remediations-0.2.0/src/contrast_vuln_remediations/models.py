"""
Type definitions for the contrast-vuln-remediations tool.
"""

from typing import TypedDict, Dict, Any
from typing_extensions import NotRequired


class Application(TypedDict):
    """Type definition for application data from the Contrast API"""
    id: str
    name: str
    path: str
    language: str
    total_modules: int
    master: bool


class Vulnerability(TypedDict):
    """Type definition for vulnerability data from the Contrast API"""
    id: str
    title: str
    severity: str
    status: str
    application_id: str
    first_time_seen: str
    last_time_seen: str
    category: str
    rule_name: str
    confidence: str
    impact: str
    url: NotRequired[str]
    vuln_id: NotRequired[str]


class Session(TypedDict):
    """Type definition for session data from the Contrast API"""
    id: str
    application_id: str
    start_time: str
    end_time: NotRequired[str]
    active: bool
    metadata: Dict[str, Any]


class EnvConfig(TypedDict, total=True):
    """Type definition for environment configuration"""
    CONTRAST_BASE_URL: str
    CONTRAST_ORG_UUID: str
    CONTRAST_API_KEY: str
    CONTRAST_AUTH: str


class ApplicationStats(TypedDict):
    """Type definition for per-application statistics"""
    name: str
    remediated: int
    open: int


class RemediationStats(TypedDict):
    """Type definition for remediation analysis results"""
    total_apps: int
    total_open: int
    total_remediated: int
    by_application: Dict[str, ApplicationStats]