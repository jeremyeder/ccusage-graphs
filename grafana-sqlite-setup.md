# Grafana SQLite Setup Guide

## ✅ Current Status
- [x] SQLite plugin already installed
- [x] SQLite database created (`claude_usage.db`)
- [x] Dashboard configuration ready (`grafana-sqlite-dashboard.json`)

## 🔧 Configure SQLite Data Source

### Step 1: Access Grafana
1. Go to **http://localhost:3001**
2. Login with **admin/admin** (change password if prompted)

### Step 2: Add SQLite Data Source
1. **Click the menu (☰)** → **Connections** → **Data sources**
2. **Click "Add data source"**
3. **Search for "SQLite"** and select it
4. **Configure the data source:**
   - **Name**: `Claude Usage SQLite`
   - **Path**: `/path/to/ccusage-graphs/claude_usage.db`
   - **Query timeout**: `30s`
5. **Click "Save & test"** - should show "Database Connection OK"

### Step 3: Import Dashboard
1. **Click the menu (☰)** → **Dashboards**
2. **Click "New"** → **Import**
3. **Click "Upload JSON file"**
4. **Select** `grafana-sqlite-dashboard.json`
5. **Configure import:**
   - **Name**: Keep as "Claude Code Usage - SQLite"
   - **Folder**: General (or create new folder)
   - **Data source**: Select "Claude Usage SQLite" (the one you just created)
6. **Click "Import"**

## 📊 Dashboard Features

### Available Panels:
1. **Daily Usage Trends** - Tokens and costs over time
2. **Model Cost Distribution** - Pie chart of spending by model
3. **Cache Efficiency** - Cache hit rates over time  
4. **Input vs Output Tokens** - Conversation patterns
5. **Cost Efficiency** - Cost per million tokens trending
6. **Summary Statistics** - Key metrics overview
7. **Model Usage Timeline** - Individual model costs over time

### Data Tables:
- `daily_usage`: Daily aggregated metrics
- `model_usage`: Per-model daily breakdowns

## 🔄 Updating Data

### Manual Update:
```bash
cd /path/to/ccusage-graphs
python3 create_sqlite_db.py
```

### Auto-Update Script:
```bash
#!/bin/bash
# update_grafana_data.sh
cd /path/to/ccusage-graphs

# Run your refresh_data.sh if it exists
if [ -f "refresh_data.sh" ]; then
    ./refresh_data.sh
fi

# Update SQLite database
python3 create_sqlite_db.py

echo "✅ Grafana SQLite data updated"
```

### Automated Updates (Optional):
Add to crontab for hourly updates:
```bash
crontab -e
# Add this line:
0 * * * * cd /path/to/ccusage-graphs && python3 create_sqlite_db.py
```

## 🔍 Custom SQL Queries

You can create custom panels with these sample queries:

### High-Value Days (>20k tokens):
```sql
SELECT 
  date as time,
  total_tokens,
  total_cost,
  models_used
FROM daily_usage 
WHERE total_tokens > 20000
ORDER BY date
```

### Model Efficiency Comparison:
```sql
SELECT 
  REPLACE(REPLACE(model_name, 'claude-', ''), '-20250514', '') as metric,
  AVG((cost / (input_tokens + output_tokens)) * 1000000) as value
FROM model_usage 
WHERE (input_tokens + output_tokens) > 0
GROUP BY model_name
```

### Weekly Spending Trends:
```sql
SELECT 
  strftime('%Y-W%W', date) as time,
  SUM(total_cost) as \"Weekly Cost\"
FROM daily_usage 
GROUP BY strftime('%Y-W%W', date)
ORDER BY time
```

### Cache Performance by Model:
```sql
SELECT 
  date as time,
  REPLACE(REPLACE(model_name, 'claude-', ''), '-20250514', '') as metric,
  CASE 
    WHEN (cache_read_tokens + cache_creation_tokens) > 0 
    THEN (cache_read_tokens * 100.0) / (cache_read_tokens + cache_creation_tokens)
    ELSE 0 
  END as value
FROM model_usage 
ORDER BY date, model_name
```

## 🎨 Customization Tips

### Panel Types:
- **Time series**: Line charts, area charts
- **Stat**: Single value displays  
- **Pie chart**: Distribution visualization
- **Table**: Raw data display
- **Bar gauge**: Progress indicators

### Color Schemes:
- Match your HTML dashboard colors
- Use consistent model colors across panels
- Set thresholds for cost alerts

### Time Ranges:
- Default: Last 30 days
- Custom ranges: 7d, 14d, 90d, 6M
- Real-time updates with refresh intervals

## 🚨 Troubleshooting

### Data Source Issues:
- **Permission denied**: Check file path and permissions
- **Database locked**: Ensure no other processes are using the SQLite file
- **No data**: Run `python3 create_sqlite_db.py` to populate database

### Dashboard Issues:
- **No data in panels**: Verify data source is selected correctly
- **Query errors**: Check SQL syntax in panel queries
- **Time range issues**: Ensure date format matches SQLite expectations

### Plugin Issues:
- **SQLite plugin missing**: Check if process is running (`ps aux | grep sqlite`)
- **Version conflicts**: Restart Grafana (`brew services restart grafana`)

## 📈 Database Schema

### daily_usage table:
```sql
CREATE TABLE daily_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    input_tokens INTEGER,
    output_tokens INTEGER,
    cache_creation_tokens INTEGER,
    cache_read_tokens INTEGER,
    total_tokens INTEGER,
    total_cost REAL,
    models_used TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### model_usage table:
```sql
CREATE TABLE model_usage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT NOT NULL,
    model_name TEXT NOT NULL,
    input_tokens INTEGER,
    output_tokens INTEGER,
    cache_creation_tokens INTEGER,
    cache_read_tokens INTEGER,
    cost REAL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## 🎯 Next Steps

1. **Set up data source** (follow steps above)
2. **Import dashboard** 
3. **Customize panels** to your preferences
4. **Set up automated data updates**
5. **Create alerts** for spending thresholds
6. **Add more visualizations** as needed

Your SQLite database contains **19 daily records** and **22 model records** ready for visualization!