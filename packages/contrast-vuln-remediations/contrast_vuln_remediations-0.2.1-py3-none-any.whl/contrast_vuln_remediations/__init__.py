"""
contrast-vuln-remediations package.
A tool for tracking remediated vulnerabilities in Contrast Security applications.
"""

from contrast_vuln_remediations.analyzer import VulnerabilityAnalyzer
from contrast_vuln_remediations.models import (
    Application,
    Vulnerability,
    Session,
    RemediationStats,
    ApplicationStats,
)
from contrast_vuln_remediations.exceptions import (
    ContrastAPIError,
    ConfigurationError,
    SessionError,
    VulnerabilityError,
)

__version__ = "0.2.1"

__all__ = [
    "VulnerabilityAnalyzer",
    "Application",
    "Vulnerability",
    "Session",
    "RemediationStats",
    "ApplicationStats",
    "ContrastAPIError",
    "ConfigurationError",
    "SessionError",
    "VulnerabilityError",
]
