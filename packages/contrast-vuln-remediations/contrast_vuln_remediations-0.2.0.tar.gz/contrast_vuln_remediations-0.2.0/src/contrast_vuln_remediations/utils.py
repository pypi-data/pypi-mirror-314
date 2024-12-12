"""
Utility functions for the contrast-vuln-remediations tool.
"""

import csv
import logging
from pathlib import Path

from contrast_vuln_remediations.models import RemediationStats

logger = logging.getLogger(__name__)


def write_to_csv(output_file: Path, stats: RemediationStats) -> None:
    """Write vulnerability remediation stats to a CSV file"""
    logger.info(f"Writing results to {output_file}")

    with output_file.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Application", "AppID", "OpenVulns", "RemediatedVulns"])
        
        for app_id, app_stats in stats["by_application"].items():
            writer.writerow([
                app_stats["name"],
                app_id,
                app_stats["open"],
                app_stats["remediated"]
            ])

    logger.info(f"Successfully wrote results to {output_file}")


def format_percentage(value: float) -> str:
    """Format a decimal value as a percentage string"""
    return f"{value:.1f}%"


def calculate_remediation_percentage(
    remediated: int, total: int, default: str = "0.0%"
) -> str:
    """Calculate and format remediation percentage"""
    if total == 0:
        return default
    return format_percentage((remediated / total) * 100)