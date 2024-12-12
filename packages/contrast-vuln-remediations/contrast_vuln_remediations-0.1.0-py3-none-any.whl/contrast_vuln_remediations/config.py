"""
Configuration management for the contrast-vuln-remediations tool.
Handles loading and validating environment variables.
"""

import os
import logging
from pathlib import Path
from typing import Dict, Final, Optional
from urllib.parse import urlparse

from dotenv import load_dotenv

from contrast_vuln_remediations.models import EnvConfig
from contrast_vuln_remediations.exceptions import ConfigurationError

logger = logging.getLogger(__name__)


def load_config() -> EnvConfig:
    """Load configuration from environment variables and/or .env file"""
    # Try to load from .env if it exists
    if Path(".env").exists():
        logger.debug("Found .env file, loading...")
        load_dotenv(Path(".env"))

    required_vars: Final[Dict[str, str]] = {
        "CONTRAST_BASE_URL": "Base URL",
        "CONTRAST_ORG_UUID": "Organization UUID",
        "CONTRAST_API_KEY": "API Key",
        "CONTRAST_AUTH": "Authorization header",
    }

    config: Dict[str, Optional[str]] = {}
    missing_vars: list[str] = []

    for var, description in required_vars.items():
        value = os.getenv(var)
        if value:
            logger.debug(
                f"Found {var} from {'environment' if var in os.environ else '.env file'}"
            )
        else:
            missing_vars.append(f"{var} ({description})")
        config[var] = value

    if missing_vars:
        raise ConfigurationError(
            "Missing required variables (check both environment and .env file):\n"
            f"{chr(10).join(missing_vars)}"
        )

    # Validate URL format
    base_url = config.get("CONTRAST_BASE_URL", "")
    if base_url:
        try:
            parsed = urlparse(base_url)
            if not all([parsed.scheme, parsed.netloc]):
                raise ValueError("Invalid URL format")
            if parsed.scheme not in ["http", "https"]:
                raise ValueError("URL must use http or https scheme")
        except Exception as e:
            raise ConfigurationError(f"Invalid CONTRAST_BASE_URL: {str(e)}")

    # Validate UUID format
    org_uuid = config.get("CONTRAST_ORG_UUID", "")
    if org_uuid and not is_valid_uuid(org_uuid):
        raise ConfigurationError("CONTRAST_ORG_UUID must be a valid UUID format")

    # Create validated config
    validated_config: Dict[str, str] = {
        k: v for k, v in config.items() if v is not None and k in required_vars
    }

    return EnvConfig(
        CONTRAST_BASE_URL=validated_config["CONTRAST_BASE_URL"],
        CONTRAST_ORG_UUID=validated_config["CONTRAST_ORG_UUID"],
        CONTRAST_API_KEY=validated_config["CONTRAST_API_KEY"],
        CONTRAST_AUTH=validated_config["CONTRAST_AUTH"],
    )


def is_valid_uuid(uuid_str: str) -> bool:
    """Simple UUID format validation"""
    try:
        uuid_parts = uuid_str.split("-")
        if len(uuid_parts) != 5:
            return False
        if not all(len(part) == exp for part, exp in zip(uuid_parts, [8, 4, 4, 4, 12])):
            return False
        # Check if string contains only hexadecimal characters and hyphens
        hex_chars = set("0123456789abcdefABCDEF-")
        return all(c in hex_chars for c in uuid_str)
    except Exception:
        return False
