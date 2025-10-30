#!/usr/bin/env python3
"""
Convert Claude Code usage JSON data to SQLite database for Grafana.

Features:
- Validates JSON structure before processing
- Supports incremental updates (append vs replace)
- Generates summary statistics
- Handles timezone-aware dates
- Comprehensive error handling
"""

import json
import sqlite3
import os
import sys
from datetime import datetime
from pathlib import Path


def log_info(msg):
    """Print info message with icon"""
    print(f"ℹ️  {msg}")


def log_success(msg):
    """Print success message with icon"""
    print(f"✅ {msg}")


def log_error(msg):
    """Print error message with icon"""
    print(f"❌ {msg}", file=sys.stderr)


def log_warn(msg):
    """Print warning message with icon"""
    print(f"⚠️  {msg}", file=sys.stderr)


def validate_json_structure(data):
    """
    Validate expected JSON structure from ccusage.

    Args:
        data: Parsed JSON data

    Returns:
        tuple: (is_valid, error_message)
    """
    if not isinstance(data, dict):
        return False, "Data must be a JSON object"

    if "daily" not in data:
        return False, "Missing required field: 'daily'"

    if not isinstance(data["daily"], list):
        return False, "'daily' must be an array"

    # Validate daily entries
    required_entry_fields = [
        "date",
        "totalTokens",
        "totalCost",
        "inputTokens",
        "outputTokens",
    ]

    for idx, entry in enumerate(data["daily"]):
        for field in required_entry_fields:
            if field not in entry:
                return False, f"Missing field '{field}' in daily entry {idx}"

        # Validate date format (YYYY-MM-DD)
        try:
            datetime.strptime(entry["date"], "%Y-%m-%d")
        except ValueError:
            return False, f"Invalid date format in entry {idx}: {entry['date']}"

    return True, None


def create_database(
    json_file="data/export_latest.json",
    db_path="claude_usage.db",
    mode="replace",
    verbose=False,
):
    """
    Create/update SQLite database from ccusage JSON data.

    Args:
        json_file: Path to JSON file
        db_path: Path to SQLite database
        mode: 'replace' to clear existing data, 'append' to add to existing
        verbose: Print detailed information
    """
    # Validate JSON file exists
    if not os.path.exists(json_file):
        log_error(f"JSON file not found: {json_file}")
        log_info("Please run ./refresh_data.sh first to generate data files")
        sys.exit(1)

    # Load and validate JSON data
    log_info(f"Loading data from {json_file}...")
    try:
        with open(json_file, "r") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        log_error(f"Invalid JSON in {json_file}: {e}")
        sys.exit(1)

    # Validate JSON structure
    is_valid, error_msg = validate_json_structure(data)
    if not is_valid:
        log_error(f"Invalid JSON structure: {error_msg}")
        sys.exit(1)

    log_success(f"JSON validation passed ({len(data['daily'])} records)")

    # Create/connect to SQLite database
    log_info(f"Connecting to database: {db_path}...")
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create daily usage table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS daily_usage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL UNIQUE,
            input_tokens INTEGER,
            output_tokens INTEGER,
            cache_creation_tokens INTEGER,
            cache_read_tokens INTEGER,
            total_tokens INTEGER,
            total_cost REAL,
            models_used TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """
    )

    # Create model breakdowns table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS model_usage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            model_name TEXT NOT NULL,
            input_tokens INTEGER,
            output_tokens INTEGER,
            cache_creation_tokens INTEGER,
            cache_read_tokens INTEGER,
            cost REAL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(date, model_name)
        )
    """
    )

    # Clear existing data if in replace mode
    if mode == "replace":
        log_info("Clearing existing data (replace mode)...")
        cursor.execute("DELETE FROM daily_usage")
        cursor.execute("DELETE FROM model_usage")
        records_mode = "Replacing"
    else:
        records_mode = "Appending"

    log_info(f"{records_mode} {len(data['daily'])} daily records...")

    # Track statistics
    daily_inserted = 0
    daily_updated = 0
    model_inserted = 0
    model_updated = 0

    # Insert/update daily usage data
    for day in data["daily"]:
        models_used = ",".join(day.get("modelsUsed", []))

        try:
            cursor.execute(
                """
                INSERT INTO daily_usage
                (date, input_tokens, output_tokens, cache_creation_tokens,
                 cache_read_tokens, total_tokens, total_cost, models_used)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(date) DO UPDATE SET
                    input_tokens=excluded.input_tokens,
                    output_tokens=excluded.output_tokens,
                    cache_creation_tokens=excluded.cache_creation_tokens,
                    cache_read_tokens=excluded.cache_read_tokens,
                    total_tokens=excluded.total_tokens,
                    total_cost=excluded.total_cost,
                    models_used=excluded.models_used,
                    updated_at=CURRENT_TIMESTAMP
            """,
                (
                    day["date"],
                    day.get("inputTokens", 0),
                    day.get("outputTokens", 0),
                    day.get("cacheCreationTokens", 0),
                    day.get("cacheReadTokens", 0),
                    day["totalTokens"],
                    day["totalCost"],
                    models_used,
                ),
            )
            if cursor.rowcount == 1:
                daily_inserted += 1
            else:
                daily_updated += 1
        except sqlite3.Error as e:
            log_error(f"Error inserting daily record for {day['date']}: {e}")
            continue

        # Insert/update model breakdown data
        for model in day.get("modelBreakdowns", []):
            try:
                cursor.execute(
                    """
                    INSERT INTO model_usage
                    (date, model_name, input_tokens, output_tokens,
                     cache_creation_tokens, cache_read_tokens, cost)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    ON CONFLICT(date, model_name) DO UPDATE SET
                        input_tokens=excluded.input_tokens,
                        output_tokens=excluded.output_tokens,
                        cache_creation_tokens=excluded.cache_creation_tokens,
                        cache_read_tokens=excluded.cache_read_tokens,
                        cost=excluded.cost
                """,
                    (
                        day["date"],
                        model["modelName"],
                        model.get("inputTokens", 0),
                        model.get("outputTokens", 0),
                        model.get("cacheCreationTokens", 0),
                        model.get("cacheReadTokens", 0),
                        model["cost"],
                    ),
                )
                if cursor.rowcount == 1:
                    model_inserted += 1
                else:
                    model_updated += 1
            except sqlite3.Error as e:
                log_error(
                    f"Error inserting model record for {day['date']}, "
                    f"{model['modelName']}: {e}"
                )
                continue

    # Create useful indexes
    log_info("Creating indexes...")
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_daily_date ON daily_usage(date DESC)"
    )
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_model_date ON model_usage(date DESC)"
    )
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_model_name ON model_usage(model_name)"
    )
    cursor.execute(
        "CREATE INDEX IF NOT EXISTS idx_model_date_name ON model_usage(date, model_name)"
    )

    # Commit changes
    conn.commit()

    # Get final counts
    cursor.execute("SELECT COUNT(*) FROM daily_usage")
    total_daily_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM model_usage")
    total_model_count = cursor.fetchone()[0]

    # Show results
    print()
    log_success(f"SQLite database updated: {db_path}")
    print()
    print("📊 Records summary:")
    print(f"  Daily usage: {total_daily_count} total")
    if mode == "replace":
        print(f"    ✓ {daily_inserted} inserted")
    else:
        print(f"    ✓ {daily_inserted} inserted, {daily_updated} updated")

    print(f"  Model usage: {total_model_count} total")
    if mode == "replace":
        print(f"    ✓ {model_inserted} inserted")
    else:
        print(f"    ✓ {model_inserted} inserted, {model_updated} updated")

    # Show sample data
    print()
    print("📋 Recent daily usage (last 5 days):")
    cursor.execute(
        """
        SELECT date, total_tokens, total_cost, models_used
        FROM daily_usage
        ORDER BY date DESC
        LIMIT 5
    """
    )
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1]:,} tokens, ${row[2]:.2f}")
        if row[3] and verbose:
            print(f"    Models: {row[3]}")

    # Show model summary
    print()
    print("🤖 Model usage summary:")
    cursor.execute(
        """
        SELECT model_name,
               COUNT(*) as days,
               SUM(input_tokens + output_tokens) as total_tokens,
               SUM(cost) as total_cost
        FROM model_usage
        GROUP BY model_name
        ORDER BY total_cost DESC
    """
    )
    for row in cursor.fetchall():
        model_short = row[0].split("-")[-1] if "-" in row[0] else row[0]
        print(f"  {row[0]}")
        print(f"    Days used: {row[1]}, Tokens: {row[2]:,}, Cost: ${row[3]:.2f}")

    # Show cache efficiency
    print()
    print("💾 Cache efficiency:")
    cursor.execute(
        """
        SELECT
            SUM(cache_creation_tokens) as cache_created,
            SUM(cache_read_tokens) as cache_read,
            SUM(total_tokens) as total_tokens
        FROM daily_usage
    """
    )
    row = cursor.fetchone()
    if row[0] and row[1]:
        cache_ratio = (row[1] / row[2] * 100) if row[2] > 0 else 0
        print(f"  Cache created: {row[0]:,} tokens")
        print(f"  Cache read: {row[1]:,} tokens")
        print(f"  Cache hit rate: {cache_ratio:.1f}%")

    conn.close()

    # Next steps
    print()
    log_info("Next steps:")
    print("  - View Grafana dashboard: docker compose up -d")
    print("  - Query database: sqlite3 claude_usage.db")
    print("  - Refresh data: ./refresh_data.sh")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Convert ccusage JSON data to SQLite database"
    )
    parser.add_argument(
        "--json",
        default="data/export_latest.json",
        help="Path to JSON file (default: data/export_latest.json)",
    )
    parser.add_argument(
        "--db",
        default="claude_usage.db",
        help="Path to SQLite database (default: claude_usage.db)",
    )
    parser.add_argument(
        "--mode",
        choices=["replace", "append"],
        default="replace",
        help="Update mode: replace (clear existing) or append (add new)",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Verbose output"
    )

    args = parser.parse_args()

    create_database(
        json_file=args.json, db_path=args.db, mode=args.mode, verbose=args.verbose
    )
