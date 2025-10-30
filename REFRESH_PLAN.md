# ccusage-graphs Repository Refresh Plan

**Generated:** 2025-10-30
**Target:** Update repository for latest ccusage version compatibility
**Scope:** Full repository overhaul (all components)

## Repository Context

This repository provides comprehensive visualization and tracking for Claude Code usage metrics:
- **HTML Dashboard**: Standalone web-based visualization
- **Grafana Integration**: Professional monitoring dashboards
- **SQLite Backend**: Database storage for historical analysis
- **Docker Stack**: Complete monitoring infrastructure (Prometheus + Grafana + nginx)

**Current State:**
- Not a git repository
- Data files exist in `data/` directory (last updated Sep 11, 2025)
- Working refresh script (`refresh_data.sh`)
- Multiple visualization paths (HTML, Grafana, SQLite)

**Latest ccusage Capabilities:**
- New commands: daily, weekly, monthly, session, blocks, mcp, statusline
- New flags: --instances, --project, --timezone, --locale, --breakdown
- Supports per-project filtering
- Enhanced JSON output format

## Execution Plan

### Phase 1: Git Initialization & Branch Setup

**Objective:** Set up proper version control without making it public

```bash
# Initialize repository
git init

# Create comprehensive .gitignore
cat > .gitignore << 'EOF'
# Data files (regenerable)
data/*.json
*.db

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
ENV/
.venv

# Docker
.env

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Temporary files
embedded_data_temp.json
EOF

# Initial commit
git add .
git commit -m "Initial commit: ccusage-graphs visualization suite

- HTML dashboard for standalone visualization
- Grafana dashboard configurations
- SQLite integration for historical data
- Docker compose stack for monitoring
- Refresh scripts for data updates"

# Create feature branch
git checkout -b feature/refresh-for-latest-ccusage
```

### Phase 2: Test Current Compatibility

**Objective:** Verify all components work with latest ccusage

**Tests to Run:**
1. `./refresh_data.sh` - Should complete without errors
2. `python3 create_sqlite_db.py` - Should create valid database
3. Check JSON structure matches expected format
4. Verify HTML dashboard renders correctly
5. Test Grafana dashboard with current data

**Expected Issues:**
- New model names (claude-sonnet-4-5-20250929, claude-opus-4-1-20250805)
- Potential JSON structure changes
- Date/timezone handling differences

**Document findings in:** `COMPATIBILITY_NOTES.md`

### Phase 3: Update Core Components

#### 3.1 Refresh Script (`refresh_data.sh`)

**Improvements:**
- Add data directory validation
- Add error handling for ccusage command failures
- Add support for timezone configuration
- Add optional project filtering
- Add verbose/quiet modes
- Add date range options

**Enhanced version:**
```bash
#!/bin/bash
set -e  # Exit on error

# Configuration
DATA_DIR="data"
TIMEZONE="${CCUSAGE_TIMEZONE:-America/New_York}"
PROJECT="${CCUSAGE_PROJECT:-}"

# Validate data directory exists
if [ ! -d "$DATA_DIR" ]; then
    echo "Creating data directory..."
    mkdir -p "$DATA_DIR"
fi

# Build ccusage command with options
CCUSAGE_OPTS="-j -z $TIMEZONE"
if [ -n "$PROJECT" ]; then
    CCUSAGE_OPTS="$CCUSAGE_OPTS -p $PROJECT"
fi

# Generate exports with error checking
echo "Refreshing Claude Code usage data..."
echo "Timezone: $TIMEZONE"
[ -n "$PROJECT" ] && echo "Project: $PROJECT"

ccusage daily $CCUSAGE_OPTS > "$DATA_DIR/export.json" || {
    echo "Error: Failed to generate export.json"
    exit 1
}

ccusage daily -i $CCUSAGE_OPTS > "$DATA_DIR/export_instances.json" || {
    echo "Error: Failed to generate export_instances.json"
    exit 1
}

# Update latest data
cp "$DATA_DIR/export.json" "$DATA_DIR/export_latest.json"

# Update HTML dashboard (existing Python script)
python3 -c "..." # (keep existing logic)

echo "✅ Data refresh complete!"
```

#### 3.2 SQLite Database Script (`create_sqlite_db.py`)

**Improvements:**
- Add validation for JSON structure
- Add proper error handling
- Add support for incremental updates (append vs. replace)
- Add data quality checks
- Support for timezone-aware dates
- Add summary statistics generation

**Key Updates:**
```python
#!/usr/bin/env python3
"""
Convert Claude Code usage JSON data to SQLite database for Grafana.

Features:
- Validates JSON structure before processing
- Supports incremental updates
- Generates summary statistics
- Handles timezone-aware dates
"""

import json
import sqlite3
import os
import sys
from datetime import datetime
from pathlib import Path

def validate_json_structure(data):
    """Validate expected JSON structure"""
    required_fields = ['daily']
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")

    # Validate daily entries
    for entry in data['daily']:
        required_entry_fields = ['date', 'totalTokens', 'totalCost']
        for field in required_entry_fields:
            if field not in entry:
                raise ValueError(f"Missing field {field} in daily entry")

    return True

# ... rest of implementation with error handling
```

#### 3.3 HTML Dashboard (`index.html`)

**Improvements:**
- Add support for new model names
- Improve date range filtering
- Add timezone display
- Add summary statistics
- Modernize chart library (if needed)
- Add responsive design improvements
- Add export functionality

**Updates:**
- Verify Chart.js version is current
- Add model color mapping for new models
- Add cost per token calculations
- Add cache efficiency metrics visualization

#### 3.4 Documentation Files

**Create comprehensive README.md:**
```markdown
# Claude Code Usage Visualization Suite

Comprehensive visualization and tracking for Claude Code usage metrics.

## Features
- 📊 HTML Dashboard - Standalone web-based visualization
- 📈 Grafana Integration - Professional monitoring dashboards
- 💾 SQLite Backend - Historical data storage and analysis
- 🐳 Docker Stack - Complete monitoring infrastructure

## Quick Start
1. Refresh data: `./refresh_data.sh`
2. View HTML dashboard: `open index.html`
3. Create database: `python3 create_sqlite_db.py`
4. Start Grafana: `docker compose up -d`

## Usage
[Detailed usage instructions]

## Configuration
[Configuration options]

## Troubleshooting
[Common issues and solutions]
```

**Update CLAUDE.md:**
```markdown
# ccusage-graphs Project Instructions

## Project Overview
Visualization suite for Claude Code usage metrics.

## Development Workflow
- Always use virtual environment for Python work
- Run `./refresh_data.sh` to update data files
- Test HTML dashboard with: `open index.html`
- Test SQLite with: `python3 create_sqlite_db.py`

## Before Committing
1. Run `./refresh_data.sh` to verify it works
2. Test SQLite database creation
3. Verify HTML dashboard loads correctly
4. Update documentation if adding features

## Linting
- Python: `black *.py && flake8 *.py`
- Shell: `shellcheck *.sh`
- Markdown: `markdownlint *.md`
```

### Phase 4: Grafana & Docker Stack Updates

#### 4.1 Docker Compose (`docker-compose.yml`)

**Improvements:**
- Update to latest stable image versions
- Add health checks
- Add volume configurations
- Add environment variable support
- Add network configuration

**Verify versions:**
- Prometheus: latest stable
- Grafana: latest stable
- nginx: latest stable
- json-exporter: latest stable

#### 4.2 Grafana Dashboards

**Update dashboard JSON files:**
- `grafana-dashboard.json`
- `grafana-sqlite-dashboard.json`

**Changes:**
- Add panels for new model types
- Update queries for latest JSON structure
- Add cache efficiency panels
- Add cost trend analysis
- Add project breakdown (if using --instances)

#### 4.3 Setup Documentation

**Update:**
- `grafana-setup.md`
- `grafana-sqlite-setup.md`

**Add:**
- Screenshots of expected dashboards
- Troubleshooting section
- Common queries for ad-hoc analysis

### Phase 5: Optional Enhancements

#### 5.1 New ccusage Features Integration

**Weekly/Monthly Reports:**
```bash
# Add to refresh script
ccusage weekly -j > data/export_weekly.json
ccusage monthly -j > data/export_monthly.json
```

**Session-Based Analytics:**
```bash
# Add session tracking
ccusage session -j > data/export_sessions.json
```

**Create visualizations for:**
- Weekly/monthly trends
- Session-based cost analysis
- Project comparison (multi-project setups)
- Model usage patterns over time

#### 5.2 Automation & CI

**Add dependabot configuration:**
```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "docker"
    directory: "/"
    schedule:
      interval: "weekly"
```

**Add GitHub Actions (optional):**
- Automated data refresh
- Dashboard validation
- Documentation updates

#### 5.3 Data Analysis Scripts

**Add new scripts:**
- `analyze_trends.py` - Identify usage patterns
- `cost_report.py` - Generate cost summaries
- `model_comparison.py` - Compare model efficiency

### Phase 6: Testing & Validation

**Comprehensive Testing:**
1. Run `./refresh_data.sh` - Verify no errors
2. Check `data/*.json` files are valid JSON
3. Run `python3 create_sqlite_db.py` - Verify database creation
4. Query SQLite database for data validation
5. Open `index.html` in browser - Verify charts render
6. Start docker stack - Verify Grafana dashboards load
7. Test with different date ranges
8. Test with project filtering (if applicable)

**Quality Checks:**
- All scripts have error handling
- All documentation is up-to-date
- All files follow linting standards
- No sensitive data in repository

## Execution Checklist

- [ ] Phase 1: Git initialization and branch creation
- [ ] Phase 2: Compatibility testing and documentation
- [ ] Phase 3.1: Update refresh_data.sh
- [ ] Phase 3.2: Update create_sqlite_db.py
- [ ] Phase 3.3: Update index.html
- [ ] Phase 3.4: Create/update documentation
- [ ] Phase 4.1: Update docker-compose.yml
- [ ] Phase 4.2: Update Grafana dashboards
- [ ] Phase 4.3: Update setup documentation
- [ ] Phase 5: Optional enhancements (as needed)
- [ ] Phase 6: Full testing and validation
- [ ] Final: Commit all changes with detailed commit message

## Success Criteria

✅ All scripts run without errors
✅ Data refreshes successfully with latest ccusage
✅ HTML dashboard displays current data correctly
✅ SQLite database creates and populates properly
✅ Grafana dashboards load and display metrics
✅ Docker stack starts successfully
✅ Documentation is comprehensive and accurate
✅ All code follows linting standards
✅ Repository is well-organized and maintainable

## Notes

- This is NOT a git repository yet - start with Phase 1
- User requested full overhaul but NO git repo initialization initially - SKIP git steps or ask first
- Focus on all four components: HTML, Grafana, SQLite, Docker
- Leverage new ccusage features where valuable
- Maintain backward compatibility where possible
- Test thoroughly before committing changes
