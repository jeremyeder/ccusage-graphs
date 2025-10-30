#!/bin/bash
set -e  # Exit on error

# Enhanced refresh script for Claude Code usage data
# Supports timezone, project filtering, date ranges, and multiple report types

# Configuration with defaults
DATA_DIR="${CCUSAGE_DATA_DIR:-data}"
TIMEZONE="${CCUSAGE_TIMEZONE:-}"
PROJECT="${CCUSAGE_PROJECT:-}"
SINCE="${CCUSAGE_SINCE:-}"
UNTIL="${CCUSAGE_UNTIL:-}"
VERBOSE="${CCUSAGE_VERBOSE:-false}"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${GREEN}ℹ${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}⚠${NC} $1"
}

log_error() {
    echo -e "${RED}✗${NC} $1"
}

log_success() {
    echo -e "${GREEN}✓${NC} $1"
}

# Validate data directory exists
if [ ! -d "$DATA_DIR" ]; then
    log_warn "Data directory not found, creating: $DATA_DIR"
    mkdir -p "$DATA_DIR" || {
        log_error "Failed to create data directory: $DATA_DIR"
        exit 1
    }
fi

# Check if ccusage is available
if ! command -v ccusage &> /dev/null; then
    log_error "ccusage command not found. Please install ccusage first."
    exit 1
fi

# Build ccusage options
CCUSAGE_OPTS="-j"

if [ -n "$TIMEZONE" ]; then
    CCUSAGE_OPTS="$CCUSAGE_OPTS -z $TIMEZONE"
fi

if [ -n "$PROJECT" ]; then
    CCUSAGE_OPTS="$CCUSAGE_OPTS -p $PROJECT"
fi

if [ -n "$SINCE" ]; then
    CCUSAGE_OPTS="$CCUSAGE_OPTS -s $SINCE"
fi

if [ -n "$UNTIL" ]; then
    CCUSAGE_OPTS="$CCUSAGE_OPTS -u $UNTIL"
fi

# Display configuration
log_info "Refreshing Claude Code usage data..."
[ "$VERBOSE" = "true" ] && log_info "Data directory: $DATA_DIR"
[ -n "$TIMEZONE" ] && log_info "Timezone: $TIMEZONE"
[ -n "$PROJECT" ] && log_info "Project filter: $PROJECT"
[ -n "$SINCE" ] && log_info "Since: $SINCE"
[ -n "$UNTIL" ] && log_info "Until: $UNTIL"

# Generate daily export with error checking
log_info "Generating daily export..."
if ccusage daily $CCUSAGE_OPTS > "$DATA_DIR/export.json"; then
    log_success "Daily export generated: $DATA_DIR/export.json"
else
    log_error "Failed to generate daily export"
    exit 1
fi

# Validate JSON structure
if ! python3 -m json.tool "$DATA_DIR/export.json" > /dev/null 2>&1; then
    log_error "Invalid JSON in export.json"
    exit 1
fi

# Generate instances data with error checking
log_info "Generating per-project breakdown..."
if ccusage daily -i $CCUSAGE_OPTS > "$DATA_DIR/export_instances.json"; then
    log_success "Instances export generated: $DATA_DIR/export_instances.json"
else
    log_warn "Failed to generate instances export (non-critical)"
fi

# Generate weekly report (optional)
if [ "${CCUSAGE_WEEKLY:-false}" = "true" ]; then
    log_info "Generating weekly report..."
    if ccusage weekly $CCUSAGE_OPTS > "$DATA_DIR/export_weekly.json"; then
        log_success "Weekly report generated: $DATA_DIR/export_weekly.json"
    else
        log_warn "Failed to generate weekly report (non-critical)"
    fi
fi

# Generate monthly report (optional)
if [ "${CCUSAGE_MONTHLY:-false}" = "true" ]; then
    log_info "Generating monthly report..."
    if ccusage monthly $CCUSAGE_OPTS > "$DATA_DIR/export_monthly.json"; then
        log_success "Monthly report generated: $DATA_DIR/export_monthly.json"
    else
        log_warn "Failed to generate monthly report (non-critical)"
    fi
fi

# Update latest data file
log_info "Updating latest data snapshot..."
cp "$DATA_DIR/export.json" "$DATA_DIR/export_latest.json"
log_success "Latest data updated: $DATA_DIR/export_latest.json"

# Update HTML dashboard with latest data
log_info "Updating HTML dashboard..."
python3 -c "
import json
import sys

try:
    # Read the current data
    with open('$DATA_DIR/export_latest.json', 'r') as f:
        current_data = json.load(f)

    # Read the HTML file
    with open('index.html', 'r') as f:
        html_content = f.read()

    # Find the embedded data section and replace it
    start_marker = 'const dashboardData = {'
    end_marker = '};'

    start_idx = html_content.find(start_marker)
    if start_idx != -1:
        start_data_idx = start_idx + len('const dashboardData = ')
        end_idx = html_content.find(end_marker, start_idx) + 1

        # Replace the data section
        new_html = (html_content[:start_data_idx] +
                    json.dumps(current_data, indent=2) +
                    html_content[end_idx:])

        # Write back to file
        with open('index.html', 'w') as f:
            f.write(new_html)

        print('✅ HTML dashboard updated!', file=sys.stderr)
    else:
        print('❌ Could not find data section in HTML file', file=sys.stderr)
        sys.exit(1)
except Exception as e:
    print(f'❌ Error updating HTML dashboard: {e}', file=sys.stderr)
    sys.exit(1)
"

if [ $? -eq 0 ]; then
    log_success "HTML dashboard updated"
else
    log_error "Failed to update HTML dashboard"
    exit 1
fi

# Summary
echo ""
log_success "Data refresh complete!"
echo ""
echo "📊 Files updated:"
echo "  - $DATA_DIR/export.json (daily usage)"
echo "  - $DATA_DIR/export_instances.json (per-project breakdown)"
echo "  - $DATA_DIR/export_latest.json (latest snapshot)"
echo "  - index.html (dashboard updated)"

# Show optional report files if generated
[ -f "$DATA_DIR/export_weekly.json" ] && echo "  - $DATA_DIR/export_weekly.json (weekly report)"
[ -f "$DATA_DIR/export_monthly.json" ] && echo "  - $DATA_DIR/export_monthly.json (monthly report)"

# Show quick stats
echo ""
log_info "Quick stats:"
python3 -c "
import json
with open('$DATA_DIR/export_latest.json', 'r') as f:
    data = json.load(f)
    total_records = len(data.get('daily', []))
    if total_records > 0:
        latest = data['daily'][-1]
        print(f'  📅 Total days: {total_records}')
        print(f'  🗓️  Latest: {latest[\"date\"]}')
        print(f'  💰 Latest cost: \${latest[\"totalCost\"]:.2f}')
        print(f'  🎯 Latest tokens: {latest[\"totalTokens\"]:,}')
        models = ', '.join(latest.get('modelsUsed', []))
        print(f'  🤖 Models: {models}')
" || log_warn "Could not parse stats from export data"

echo ""
log_info "Next steps:"
echo "  - View dashboard: open index.html"
echo "  - Update database: python3 create_sqlite_db.py"
echo "  - Start Grafana: docker compose up -d"
