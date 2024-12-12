"""
Custom exceptions for the contrast-vuln-remediations tool.
"""

from typing import Optional
import httpx


class ContrastAPIError(Exception):
    """Custom error class for Contrast API errors."""

    def __init__(self, message: str, response: Optional[httpx.Response] = None) -> None:
        super().__init__(message)
        self.response: Optional[httpx.Response] = response
        self.response_text: str = (
            response.text if response is not None else "No response content"
        )


class ConfigurationError(Exception):
    """Exception raised for errors in the configuration."""

    pass


class SessionError(Exception):
    """Exception raised for errors related to session handling."""

    pass


class VulnerabilityError(Exception):
    """Exception raised for errors related to vulnerability processing."""

    pass
