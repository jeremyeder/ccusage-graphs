# Claude Code Usage Visualization Suite

Comprehensive visualization and tracking for Claude Code usage metrics with multiple visualization options.

## Features

- **HTML Dashboard** - Standalone web-based visualization with interactive charts
- **Grafana Integration** - Professional monitoring dashboards with time-series analysis
- **SQLite Backend** - Historical data storage for advanced queries and analysis
- **Docker Stack** - Complete monitoring infrastructure (Prometheus + Grafana + nginx)
- **Flexible Export** - Daily, weekly, and monthly reports with JSON export
- **Multi-Project Support** - Track usage across multiple projects
- **Cache Analytics** - Monitor prompt caching efficiency

## Quick Start

### Prerequisites

- [Claude Code](https://claude.com/claude-code) installed and configured
- [ccusage](https://github.com/anthropics/claude-code) CLI tool installed
- Python 3.8+ for database scripts
- Docker and Docker Compose (for Grafana stack, optional)

### 1. Clone and Setup

```bash
git clone <your-repo-url>
cd ccusage-graphs
```

### 2. Refresh Data

Generate the latest usage data from Claude Code:

```bash
./refresh_data.sh
```

This will create:
- `data/export.json` - Daily usage data
- `data/export_instances.json` - Per-project breakdown
- `data/export_latest.json` - Latest snapshot
- `index.html` - Updated HTML dashboard

### 3. View HTML Dashboard

Simply open the HTML file in your browser:

```bash
open index.html
```

### 4. Create SQLite Database (Optional)

For Grafana integration and advanced queries:

```bash
python3 create_sqlite_db.py
```

This creates `claude_usage.db` with optimized tables and indexes.

### 5. Start Grafana Stack (Optional)

```bash
docker compose up -d
```

Access Grafana at http://localhost:3000 (default credentials: admin/admin)

## Privacy & Data Security

**IMPORTANT:** This tool processes local usage data and does not transmit any information externally.

### Gitignored Data Files
The following files contain your personal usage metrics and are automatically excluded from git:
- `data/*.json` - Generated usage exports (project names, timestamps, token counts)
- `*.db` - SQLite databases with historical data
- `embedded_data_temp.json` - Temporary HTML dashboard data

### Before Sharing or Open Sourcing
If you fork this project or share your repository:
1. ✅ Verify data files are in `.gitignore`
2. ✅ Run `git status` to ensure no data files are staged
3. ✅ Check for personal paths in documentation
4. ✅ Review for internal project names in examples

### Data Contents
Usage data files may include:
- Project directory names and paths
- Usage timestamps and token counts
- Model selections (e.g., sonnet, opus, haiku)
- Repository names and locations

**Never commit these files to version control or public repositories.**

## Usage

### Basic Data Refresh

```bash
# Standard refresh
./refresh_data.sh

# With timezone (recommended for consistency)
CCUSAGE_TIMEZONE=America/New_York ./refresh_data.sh

# Verbose output
CCUSAGE_VERBOSE=true ./refresh_data.sh

# Filter by project
CCUSAGE_PROJECT="my-project" ./refresh_data.sh

# Date range
CCUSAGE_SINCE=20251001 CCUSAGE_UNTIL=20251031 ./refresh_data.sh

# Generate weekly and monthly reports
CCUSAGE_WEEKLY=true CCUSAGE_MONTHLY=true ./refresh_data.sh
```

### Database Operations

```bash
# Create/update database
python3 create_sqlite_db.py

# Append new data (keep existing)
python3 create_sqlite_db.py --mode append

# Use different files
python3 create_sqlite_db.py --json data/export_weekly.json --db weekly.db

# Verbose output
python3 create_sqlite_db.py --verbose

# View help
python3 create_sqlite_db.py --help
```

### Query Database

```bash
# Interactive SQL queries
sqlite3 claude_usage.db

# Example queries
sqlite3 claude_usage.db "SELECT date, total_cost FROM daily_usage ORDER BY date DESC LIMIT 10"
sqlite3 claude_usage.db "SELECT model_name, SUM(cost) as total FROM model_usage GROUP BY model_name"
```

## Configuration

### Environment Variables

The refresh script supports these environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `CCUSAGE_DATA_DIR` | Data directory path | `data` |
| `CCUSAGE_TIMEZONE` | Timezone for date grouping | System timezone |
| `CCUSAGE_PROJECT` | Filter to specific project | All projects |
| `CCUSAGE_SINCE` | Start date (YYYYMMDD) | All history |
| `CCUSAGE_UNTIL` | End date (YYYYMMDD) | Today |
| `CCUSAGE_VERBOSE` | Verbose output | `false` |
| `CCUSAGE_WEEKLY` | Generate weekly report | `false` |
| `CCUSAGE_MONTHLY` | Generate monthly report | `false` |

### Example .env File

Create a `.env` file for persistent configuration:

```bash
CCUSAGE_TIMEZONE=America/New_York
CCUSAGE_VERBOSE=true
CCUSAGE_WEEKLY=true
CCUSAGE_MONTHLY=true
```

Then run:
```bash
source .env && ./refresh_data.sh
```

## Visualization Options

### 1. HTML Dashboard

**Best for:** Quick standalone visualization, sharing reports

**Features:**
- Interactive charts (Chart.js)
- Token usage trends
- Cost analysis by model
- Cache efficiency metrics
- Embedded data (works offline)

**Access:** `open index.html`

### 2. Grafana Dashboards

**Best for:** Continuous monitoring, team dashboards, alerting

**Features:**
- Real-time updates
- Time-series analysis
- Custom queries
- Multi-dashboard support
- Alerting capabilities

**Access:** http://localhost:3000 (after `docker compose up -d`)

**Available Dashboards:**
- `grafana-dashboard.json` - JSON-based metrics
- `grafana-sqlite-dashboard.json` - SQLite-based metrics (recommended)

See [grafana-sqlite-setup.md](grafana-sqlite-setup.md) for detailed setup.

### 3. SQLite Database

**Best for:** Custom analysis, data export, integration

**Features:**
- Fast queries
- Historical analysis
- Data export (CSV, JSON)
- Integration with other tools

**Schema:**
- `daily_usage` - Daily aggregated metrics
- `model_usage` - Per-model breakdown

## Data Files

| File | Description | Updated By |
|------|-------------|------------|
| `data/export.json` | Daily usage data | `refresh_data.sh` |
| `data/export_instances.json` | Per-project breakdown | `refresh_data.sh` |
| `data/export_latest.json` | Latest snapshot | `refresh_data.sh` |
| `data/export_weekly.json` | Weekly aggregates (optional) | `refresh_data.sh` |
| `data/export_monthly.json` | Monthly aggregates (optional) | `refresh_data.sh` |
| `claude_usage.db` | SQLite database | `create_sqlite_db.py` |
| `index.html` | HTML dashboard | `refresh_data.sh` |

## Automation

### Cron Job Example

Update data hourly:

```cron
0 * * * * cd /path/to/ccusage-graphs && ./refresh_data.sh && python3 create_sqlite_db.py
```

### Daily Summary Email

```bash
#!/bin/bash
# daily-summary.sh
./refresh_data.sh
python3 create_sqlite_db.py --verbose > /tmp/ccusage-summary.txt
mail -s "Claude Code Daily Usage" you@example.com < /tmp/ccusage-summary.txt
```

## Troubleshooting

### "ccusage command not found"

Install the ccusage CLI:
```bash
npm install -g @anthropic/ccusage
```

### "Invalid JSON in export.json"

The ccusage command may have failed. Run manually:
```bash
ccusage daily -j
```

### "No data in Grafana dashboard"

1. Verify SQLite database has data: `sqlite3 claude_usage.db "SELECT COUNT(*) FROM daily_usage"`
2. Restart Grafana: `docker compose restart grafana`
3. Check Grafana data source configuration

### "HTML dashboard shows old data"

The refresh script updates the embedded data. Run:
```bash
./refresh_data.sh
```

### Database errors about UNIQUE constraint

Remove the old database and recreate:
```bash
rm claude_usage.db
python3 create_sqlite_db.py
```

## Model Support

The system automatically supports new Claude models. Currently tracked models include:

- **Claude Opus 4.1** (`claude-opus-4-1-20250805`)
- **Claude Sonnet 4.5** (`claude-sonnet-4-5-20250929`)
- **Claude Haiku 3.5** (`claude-3-5-haiku-20241022`)

New models are automatically detected from ccusage output.

## Cache Efficiency

The dashboard tracks prompt caching metrics:
- **Cache Creation Tokens** - Tokens cached for reuse
- **Cache Read Tokens** - Tokens read from cache
- **Cache Hit Rate** - Percentage of tokens served from cache

High cache hit rates (>80%) indicate efficient prompt caching.

## Cost Analysis

Costs are calculated based on:
- Input/output token counts
- Cache creation/read tokens
- Per-model pricing
- Real-time API pricing (when available)

The `--mode calculate` flag in ccusage forces recalculation of costs.

## Development

### File Structure

```
ccusage-graphs/
├── data/                      # Generated data files (gitignored)
├── refresh_data.sh            # Main refresh script
├── create_sqlite_db.py        # SQLite database creator
├── index.html                 # HTML dashboard
├── docker-compose.yml         # Grafana stack
├── grafana-dashboard.json     # Grafana dashboard config
├── grafana-sqlite-dashboard.json  # SQLite-based dashboard
├── grafana-setup.md           # Setup guide
└── README.md                  # This file
```

### Contributing

1. Test changes with `./refresh_data.sh` and `python3 create_sqlite_db.py`
2. Verify HTML dashboard loads correctly
3. Test SQLite database creation
4. Update documentation if adding features

## Advanced Usage

### Custom Queries

```sql
-- Top 5 most expensive days
SELECT date, total_cost, total_tokens
FROM daily_usage
ORDER BY total_cost DESC
LIMIT 5;

-- Cost by model
SELECT model_name,
       SUM(cost) as total_cost,
       SUM(input_tokens + output_tokens) as total_tokens
FROM model_usage
GROUP BY model_name
ORDER BY total_cost DESC;

-- Weekly cost trends
SELECT strftime('%Y-%W', date) as week,
       SUM(total_cost) as weekly_cost
FROM daily_usage
GROUP BY week
ORDER BY week DESC;

-- Cache efficiency over time
SELECT date,
       cache_read_tokens,
       total_tokens,
       ROUND(100.0 * cache_read_tokens / total_tokens, 1) as cache_hit_pct
FROM daily_usage
WHERE cache_read_tokens > 0
ORDER BY date DESC;
```

### Export Data

```bash
# Export to CSV
sqlite3 -header -csv claude_usage.db "SELECT * FROM daily_usage" > usage.csv

# Export to JSON
sqlite3 claude_usage.db "SELECT json_group_array(json_object(
    'date', date,
    'cost', total_cost,
    'tokens', total_tokens
)) FROM daily_usage" > usage.json
```

## Resources

- [Claude Code Documentation](https://docs.claude.com/claude-code)
- [ccusage GitHub](https://github.com/anthropics/claude-code)
- [Grafana Documentation](https://grafana.com/docs/)
- [Chart.js Documentation](https://www.chartjs.org/docs/)

## Dependencies & Attribution

This project builds on excellent open source tools:

### Required Dependencies
- **[ccusage CLI](https://github.com/anthropics/ccusage)** - MIT License - Claude Code usage data export
- **Python 3.8+** - Standard library only (PSF License)
- **Bash** - Standard Unix shell

### Visualization Components
- **[Chart.js](https://www.chartjs.org/)** (v4.4.1) - MIT License - JavaScript charting library
- **[Docker](https://www.docker.com/)** - Apache 2.0 - Containerization platform

### Docker Stack Components
- **[Prometheus](https://prometheus.io/)** (v2.48.0) - Apache 2.0 - Metrics collection
- **[Grafana](https://grafana.com/)** (v10.2.2) - AGPL v3 - Dashboards and visualization
- **[JSON Exporter](https://github.com/prometheus-community/json_exporter)** (v0.6.0) - Apache 2.0 - JSON to Prometheus metrics
- **[nginx](https://nginx.org/)** (v1.25-alpine) - 2-clause BSD - Web server

### Credits
- Anthropic for the Claude Code platform and ccusage tool
- The Prometheus and Grafana communities for excellent monitoring tools
- Chart.js community for visualization capabilities

All dependencies use permissive licenses compatible with MIT.

## License

MIT License - See LICENSE file for details

## Support

For issues or questions:
1. Check [Troubleshooting](#troubleshooting) section
2. Review [ccusage documentation](https://github.com/anthropics/claude-code)
3. Open an issue on GitHub

## Changelog

### 2025-10-30 - Major Refresh
- Enhanced refresh script with comprehensive error handling
- Added timezone and project filtering support
- Improved SQLite script with validation and statistics
- Added support for weekly/monthly reports
- Enhanced documentation
- Added cache efficiency tracking
- Support for new Claude models (Opus 4.1, Sonnet 4.5)

### 2025-08-10 - Initial Release
- HTML dashboard with Chart.js
- Grafana integration
- SQLite database support
- Docker compose stack
