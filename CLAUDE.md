# ccusage-graphs Project Instructions

## Project Overview

Comprehensive visualization suite for Claude Code usage metrics with multiple output formats:
- HTML dashboard for standalone visualization
- Grafana integration for professional monitoring
- SQLite backend for historical analysis
- Docker stack for complete monitoring infrastructure

**Key Components:**
- `refresh_data.sh` - Data refresh script with error handling and validation
- `create_sqlite_db.py` - SQLite database generator with comprehensive stats
- `index.html` - Standalone HTML dashboard with embedded data
- `docker-compose.yml` - Grafana + Prometheus + nginx stack

## Development Workflow

### Always Use Feature Branches
This project follows GitHub Flow. Create feature branches for all changes:
```bash
git checkout -b feature/description-of-change
```

### Before Starting Work
**MANDATORY: Always verify current branch before any file modifications:**
```bash
git branch --show-current
```

### Standard Development Cycle

1. **Make changes** to code/scripts
2. **Test locally** using the commands below
3. **Run linters** before committing
4. **Commit frequently** with clear messages
5. **Update documentation** if adding features

## Testing Workflow

### Test Data Refresh
```bash
./refresh_data.sh
```

**Expected output:**
-  Daily export generated
-  Instances export generated
-  Latest data updated
-  HTML dashboard updated
- Quick stats displayed

### Test SQLite Database
```bash
python3 create_sqlite_db.py --verbose
```

**Expected output:**
-  JSON validation passed
-  SQLite database updated
- =Ê Records summary
- =Ë Sample data
- > Model usage summary
- =¾ Cache efficiency

### Test HTML Dashboard
```bash
open index.html
```

**Verify:**
- Charts render correctly
- Data is current (check dates)
- All models are displayed
- No JavaScript errors in console

### Test Grafana Stack (Optional)
```bash
docker compose up -d
open http://localhost:3000
```

**Verify:**
- Grafana loads
- Data source connects
- Dashboards display data

## Before Committing

### 1. Run All Tests
```bash
# Refresh data
./refresh_data.sh

# Create database
python3 create_sqlite_db.py

# Verify HTML loads
open index.html
```

### 2. Lint Shell Scripts
```bash
shellcheck refresh_data.sh
```

### 3. Lint Python Code
```bash
# Format code
black create_sqlite_db.py

# Sort imports
isort create_sqlite_db.py

# Lint (ignore line length)
flake8 create_sqlite_db.py --ignore=E501
```

### 4. Lint Markdown
```bash
markdownlint README.md CLAUDE.md *.md
```

### 5. Verify No Sensitive Data
```bash
# Check that data files are gitignored
git status

# Should NOT see:
# - data/*.json
# - *.db
```

## Code Standards

### Shell Scripts
- Use `set -e` for error handling
- Validate all inputs and outputs
- Use colored output for user feedback
- Check command availability before use
- Provide clear error messages

### Python Scripts
- Use type hints where helpful
- Comprehensive error handling with try/except
- Validate JSON structure before processing
- Log progress with clear messages
- Use argparse for CLI options
- Follow PEP 8 (except line length)

### Documentation
- Update README.md for user-facing changes
- Update CLAUDE.md for development changes
- Document all configuration options
- Provide examples for all features

## Common Tasks

### Add New ccusage Feature
1. Update `refresh_data.sh` to generate new export
2. Update `create_sqlite_db.py` if database changes needed
3. Test with `./refresh_data.sh && python3 create_sqlite_db.py`
4. Update README.md with new feature
5. Commit changes

### Update for New Model
No code changes needed! The system automatically detects new models from ccusage output.

### Add New Visualization
1. Update HTML dashboard or Grafana dashboard JSON
2. Test display with current data
3. Document in README.md
4. Commit changes

### Fix Bug
1. Create feature branch: `git checkout -b fix/bug-description`
2. Fix the bug
3. Test all components
4. Run linters
5. Commit with clear description of fix
6. Create pull request

## File Responsibilities

| File | Purpose | When to Modify |
|------|---------|----------------|
| `refresh_data.sh` | Generate data files | Adding ccusage features, error handling |
| `create_sqlite_db.py` | Create database | Schema changes, new metrics |
| `index.html` | HTML dashboard | UI changes, new charts |
| `docker-compose.yml` | Grafana stack | Version updates, new services |
| `grafana-*.json` | Dashboards | New panels, queries |
| `README.md` | User docs | New features, usage examples |
| `CLAUDE.md` | Dev docs | Workflow changes, standards |

## Environment Setup

### Required Tools
- Python 3.8+
- ccusage CLI
- Docker & Docker Compose (for Grafana)
- shellcheck (for linting)
- markdownlint (for docs)

### Python Dependencies
None! Scripts use only standard library.

### Optional Tools
- sqlite3 (for database queries)
- jq (for JSON debugging)

## Debugging

### Data Issues
```bash
# Validate JSON structure
python3 -m json.tool data/export.json

# Check ccusage output
ccusage daily -j

# View database contents
sqlite3 claude_usage.db "SELECT * FROM daily_usage LIMIT 5"
```

### Script Issues
```bash
# Run with verbose output
CCUSAGE_VERBOSE=true ./refresh_data.sh

# Test individual ccusage commands
ccusage daily -j > /tmp/test.json
python3 -m json.tool /tmp/test.json
```

### Dashboard Issues
```bash
# Check browser console for JavaScript errors
open index.html
# Open browser dev tools (F12)

# Verify embedded data
grep "const dashboardData" index.html | head -5
```

## Configuration Options

### Refresh Script Environment Variables
```bash
CCUSAGE_DATA_DIR=data          # Data directory
CCUSAGE_TIMEZONE=America/New_York  # Timezone
CCUSAGE_PROJECT=my-project     # Project filter
CCUSAGE_SINCE=20251001        # Start date
CCUSAGE_UNTIL=20251031        # End date
CCUSAGE_VERBOSE=true          # Verbose output
CCUSAGE_WEEKLY=true           # Generate weekly report
CCUSAGE_MONTHLY=true          # Generate monthly report
```

### Database Script Options
```bash
python3 create_sqlite_db.py --help

Options:
  --json PATH       JSON file path
  --db PATH         Database path
  --mode MODE       replace or append
  -v, --verbose     Verbose output
```

## Git Workflow

### Standard Commit
```bash
git add <files>
git commit -m "Brief description

Detailed explanation if needed"
```

### Feature Branch Workflow
```bash
# Create branch
git checkout -b feature/add-weekly-reports

# Make changes and commit
git add .
git commit -m "Add weekly report generation"

# Push to remote (when ready)
git push origin feature/add-weekly-reports
```

### Commit Message Style
- Use present tense ("Add feature" not "Added feature")
- Be concise but descriptive
- Reference issues if applicable
- Explain why, not just what

## Data Privacy

**IMPORTANT:** Never commit actual usage data to git.

**Gitignored Items:**
- `data/*.json` - Generated data files
- `*.db` - SQLite databases
- `embedded_data_temp.json` - Temporary files

**Safe to Commit:**
- Scripts (`*.sh`, `*.py`)
- Documentation (`*.md`)
- Configuration (`docker-compose.yml`, etc.)
- Dashboard templates (`*.html`, `*.json` configs)

## Performance Considerations

### Data Refresh
- Runs in seconds for typical usage
- Validates JSON to catch ccusage errors early
- Parallel-safe (can run multiple times)

### Database Creation
- Fast on modern hardware (< 1 second for months of data)
- Uses indexes for query performance
- UPSERT support for incremental updates

### HTML Dashboard
- Loads instantly (embedded data)
- Works offline
- Responsive design

## Troubleshooting Guide

### "Command not found: ccusage"
```bash
# Install ccusage
npm install -g @anthropic/ccusage
```

### "Invalid JSON" errors
```bash
# Check ccusage is working
ccusage daily -j | python3 -m json.tool

# Manually run refresh
./refresh_data.sh
```

### "Database locked" errors
```bash
# Stop Grafana if running
docker compose down

# Remove lock file
rm claude_usage.db-journal

# Retry
python3 create_sqlite_db.py
```

### HTML dashboard not updating
```bash
# Force refresh
./refresh_data.sh

# Check embedded data
grep "const dashboardData" index.html | head -10
```

## Support

For help with this project:
1. Check README.md for usage
2. Check this file (CLAUDE.md) for development
3. Check COMPATIBILITY_NOTES.md for known issues
4. Review closed issues on GitHub

## Related Documentation

- [README.md](README.md) - User-facing documentation
- [COMPATIBILITY_NOTES.md](COMPATIBILITY_NOTES.md) - Compatibility testing results
- [grafana-sqlite-setup.md](grafana-sqlite-setup.md) - Grafana setup guide
- [grafana-setup.md](grafana-setup.md) - Alternative Grafana setup

## Version History

See [README.md](README.md) changelog section for version history and changes.
