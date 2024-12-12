# contrast-vuln-remediations

A command-line tool for tracking remediated vulnerabilities across Contrast Security applications. This tool helps identify vulnerabilities that have been fixed by comparing open vulnerabilities against those found in the latest application session.

## Features

- Fast, asynchronous API querying with concurrent requests
- Progress tracking for large datasets
- CSV export for detailed analysis
- Summary statistics including remediation counts and percentages
- Configurable batch size and concurrency
- Flexible session filtering using metadata key/value pairs
- Environment-based configuration
- Rich terminal output with color-coded results
- Resilient API handling with automatic retries and rate limiting

## Installation

1. Install:
```bash
pip install contrast-vuln-remediations
```

2. Create a `.env` file with your Contrast Security credentials:
```ini
CONTRAST_BASE_URL=https://app.contrastsecurity.com/Contrast
CONTRAST_ORG_UUID=your-org-uuid
CONTRAST_API_KEY=your-api-key
CONTRAST_AUTH=your-auth-header
```

## Usage

Basic usage:
```bash
contrast-vuln-remediations
```

With all options:
```bash
contrast-vuln-remediations \
    --csv output.csv \
    --concurrent-requests 20 \
    --metadata "Branch Name=main" \
    --metadata "Environment=production" \
    --verbose
```

### Options

- `--csv`: Output file path for detailed CSV results
- `--concurrent-requests`: Maximum number of concurrent API requests (default: 10)
- `--metadata`: Metadata key=value pairs to filter sessions (can be specified multiple times)
- `--verbose`: Enable verbose logging

### Metadata Filtering Examples

Filter by branch:
```bash
contrast-vuln-remediations --metadata "Branch Name=main"
```

Filter by multiple criteria:
```bash
contrast-vuln-remediations --metadata "Branch Name=main" --metadata "Environment=prod"
```

Multiple values for the same key:
```bash
contrast-vuln-remediations --metadata "Branch Name=main" --metadata "Branch Name=develop"
```

Note: If no metadata filters are specified, the tool defaults to analyzing sessions from 'main' and 'master' branches.

## Output

## Output

The tool provides a summary of remediated vulnerabilities including:

- Total number of applications analyzed
- Number of vulnerabilities currently open
- Number of remediated vulnerabilities
- Percentage of vulnerabilities remediated
- Detailed breakdown by application

Example output:
```
Starting analysis... Using metadata filters: {'Branch Name': ['main'], 'Environment': ['production']}
Analyzing applications: 100% ██████████ 15/15

Vulnerability Analysis Summary
┌──────────────────────────┬────────────┐
│ Total applications      │         15 │
│ Open vulnerabilities    │        428 │
│ Remediated vulns       │        132 │
│ Remediation percentage │      30.8% │
└──────────────────────────┴────────────┘

Detailed results have been written to: output.csv
```

## CSV Output Format

The CSV output includes three columns:
- `Application`: The application name
- `AppID`: The application ID
- `OpenVulns`: Number of open vulnerabilities
- `RemediatedVulns`: Number of remediated vulnerabilities

Example:
```csv
Application,AppID,RemediatedVulns
My App 1,12345,25,10
My App 2,67890,18,5
```

## Environment Variables

| Variable          | Description               | Example                                   |
| ----------------- | ------------------------- | ----------------------------------------- |
| CONTRAST_BASE_URL | Contrast Security API URL | https://app.contrastsecurity.com/Contrast |
| CONTRAST_ORG_UUID | Organization UUID         | 12345678-90ab-cdef-1234-567890abcdef      |
| CONTRAST_API_KEY  | API Key                   | your-api-key                              |
| CONTRAST_AUTH     | Authorization header      | base64-encoded-credentials                |

## Development

Requirements:
- Python 3.8+
- httpx
- typer
- rich
- python-dotenv
- tqdm

## License

Apache License

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run the tests
5. Submit a pull request

## Support

For issues, questions, or contributions, please open an issue in the GitHub repository.
