"""
CLI interface for the contrast-vuln-remediations tool.
Handles command line argument parsing and orchestration.
"""

import asyncio
import logging
from pathlib import Path
from typing import Optional, List, Dict
from typing_extensions import Annotated

import typer
from rich.console import Console
from rich.table import Table
from rich import box
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
)

from contrast_vuln_remediations.analyzer import VulnerabilityAnalyzer
from contrast_vuln_remediations.config import load_config
from contrast_vuln_remediations.exceptions import ContrastAPIError
from contrast_vuln_remediations.utils import write_to_csv

logger = logging.getLogger(__name__)

app = typer.Typer(
    help="Track remediated vulnerabilities in Contrast Security applications"
)
console = Console()


def parse_metadata(metadata_pairs: List[str]) -> Dict[str, List[str]]:
    """Parse metadata key=value pairs into a dictionary of lists."""
    result: Dict[str, List[str]] = {}
    for pair in metadata_pairs:
        try:
            key, value = pair.split("=", 1)
            key = key.strip()
            value = value.strip()
            if key in result:
                result[key].append(value)
            else:
                result[key] = [value]
        except ValueError:
            raise typer.BadParameter(
                f"Invalid metadata format: {pair}. Use key=value format"
            )
    return result


async def analyze_vulnerabilities(
    csv_file: Annotated[
        Optional[Path],
        typer.Option(
            "--csv",
            help="Output results to the specified CSV file",
            dir_okay=False,
            file_okay=True,
            writable=True,
        ),
    ] = None,
    concurrent_requests: Annotated[
        int,
        typer.Option(
            "--concurrent-requests",
            "-c",
            help="Maximum number of concurrent API requests",
            min=1,
            max=50,
            show_default=True,
        ),
    ] = 10,
    metadata: Annotated[
        Optional[List[str]],
        typer.Option(
            "--metadata",
            "-m",
            help="Metadata key=value pairs to filter sessions (can be specified multiple times). Example: --metadata 'Branch Name=main'",
        ),
    ] = None,
    verbose: Annotated[
        bool,
        typer.Option("--verbose", "-v", help="Enable verbose logging"),
    ] = False,
) -> None:
    """Analyze remediated vulnerabilities across applications."""
    try:
        log_level = logging.DEBUG if verbose else logging.INFO
        logging.basicConfig(level=log_level)
        root_logger = logging.getLogger()
        root_logger.setLevel(log_level)

        config = load_config()

        # Parse metadata or use default branch filter
        metadata_filters = {}
        if metadata:
            metadata_filters = parse_metadata(metadata)
        else:
            metadata_filters = {"Branch Name": ["main", "master"]}

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TaskProgressColumn(),
            console=console,
            transient=True,
        ) as progress:
            progress_task = progress.add_task(
                "Initializing analysis...", total=None, start=False
            )

            console.print("\n[bold]Starting analysis...[/bold]")
            console.print(f"Using metadata filters: {metadata_filters}")

            async with VulnerabilityAnalyzer(
                base_url=config["CONTRAST_BASE_URL"],
                org_uuid=config["CONTRAST_ORG_UUID"],
                api_key=config["CONTRAST_API_KEY"],
                auth=config["CONTRAST_AUTH"],
                max_concurrent=concurrent_requests,
                metadata_filters=metadata_filters,  # type: ignore
                verbose=verbose,
            ) as analyzer:
                try:
                    progress.update(
                        progress_task, description="Analyzing applications..."
                    )
                    progress.start_task(progress_task)
                    stats = await analyzer.analyze_all_applications()
                    progress.update(
                        progress_task, completed=True, description="Analysis complete!"
                    )
                except Exception as e:
                    error_msg = f"[red bold]Error during analysis:[/red bold] {str(e)}"
                    console.print(error_msg)
                    raise typer.Exit(1)

            if csv_file:
                write_to_csv(csv_file, stats)

            console.print("\n")

            # Create summary table
            summary_table = Table(
                title="Vulnerability Analysis Summary",
                show_header=False,
                box=box.ROUNDED,
                min_width=50,
            )

            summary_table.add_column("Metric", style="bold", width=30)
            summary_table.add_column("Value", style="cyan", justify="right", width=20)

            # Add summary rows
            summary_table.add_row("Total applications", f"{stats['total_apps']:,}")
            summary_table.add_row("Open vulnerabilities", f"{stats['total_open']:,}")
            summary_table.add_row(
                "Remediated vulnerabilities", f"{stats['total_remediated']:,}"
            )

            if stats["total_open"] > 0:
                remediation_pct = (
                    stats["total_remediated"]
                    / (stats["total_open"] + stats["total_remediated"])
                    * 100
                )
                summary_table.add_row(
                    "Remediation percentage", f"{remediation_pct:.1f}%"
                )

            console.print(summary_table)

            # Create application breakdown table if there are multiple apps
            if len(stats["by_application"]) > 1:
                console.print("\n[bold]Application Breakdown[/bold]")

                app_table = Table(
                    show_header=True,
                    box=box.SIMPLE,
                    min_width=50,
                )

                app_table.add_column("Application", style="bold")
                app_table.add_column("Open", justify="right")
                app_table.add_column("Remediated", justify="right", style="cyan")
                app_table.add_column("Remediation %", justify="right")

                for app_stats in stats["by_application"].values():
                    total_vulns = app_stats["open"] + app_stats["remediated"]
                    rem_pct = (
                        f"{(app_stats['remediated'] / total_vulns * 100):.1f}%"
                        if total_vulns > 0
                        else "0.0%"
                    )

                    app_table.add_row(
                        app_stats["name"],
                        str(app_stats["open"]),
                        str(app_stats["remediated"]),
                        rem_pct,
                    )

                console.print(app_table)

            if csv_file:
                console.print(
                    f"\nDetailed results have been written to: [cyan]{csv_file}[/cyan]"
                )

    except ValueError as e:
        error_msg = f"[red]Configuration error: {str(e)}[/red]"
        console.print(error_msg)
        raise typer.Exit(1)
    except ContrastAPIError as e:
        error_details = f": {e.response_text}" if e.response is not None else ""
        error_msg = f"[red]Error accessing the API: {str(e)}{error_details}[/red]"
        console.print(error_msg)
        raise typer.Exit(1)
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}", exc_info=True)
        error_msg = f"[red]An error occurred: {str(e)}[/red]"
        console.print(error_msg)
        raise typer.Exit(1)


@app.command()
def analyze(
    csv_file: Annotated[
        Optional[Path],
        typer.Option("--csv", help="Output results to the specified CSV file"),
    ] = None,
    concurrent_requests: Annotated[
        int,
        typer.Option(
            "--concurrent-requests",
            "-c",
            help="Maximum number of concurrent API requests",
        ),
    ] = 10,
    metadata: Annotated[
        Optional[List[str]],
        typer.Option(
            "--metadata",
            "-m",
            help="Metadata key=value pairs to filter sessions (can be specified multiple times)",
        ),
    ] = None,
    verbose: Annotated[
        bool,
        typer.Option("--verbose", "-v", help="Enable verbose logging"),
    ] = False,
) -> None:
    """Analyze remediated vulnerabilities across all applications."""
    asyncio.run(
        analyze_vulnerabilities(csv_file, concurrent_requests, metadata, verbose)
    )
