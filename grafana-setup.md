# Grafana Dashboard Setup for Claude Code Usage

This directory contains a Grafana dashboard configuration that replicates your Claude Code usage visualization.

## Files

- `grafana-dashboard.json` - Complete Grafana dashboard configuration
- `grafana-setup.md` - This setup guide

## Data Source Options

Since your data comes from JSON files, you have several options for getting it into Grafana:

### Option 1: Prometheus + JSON Exporter (Recommended)

1. **Install Prometheus JSON Exporter**
   ```bash
   docker run -d -p 7979:7979 prometheuscommunity/json-exporter
   ```

2. **Configure JSON Exporter** (`json-exporter-config.yml`):
   ```yaml
   modules:
     claude_usage:
       http_config:
         method: GET
       metrics:
       - name: claude_total_tokens
         path: "$.daily[*].totalTokens"
         labels:
           date: "$.daily[*].date"
       - name: claude_total_cost
         path: "$.daily[*].totalCost"
         labels:
           date: "$.daily[*].date"
       - name: claude_input_tokens
         path: "$.daily[*].inputTokens"
         labels:
           date: "$.daily[*].date"
       - name: claude_output_tokens
         path: "$.daily[*].outputTokens"
         labels:
           date: "$.daily[*].date"
       - name: claude_cache_read_tokens
         path: "$.daily[*].cacheReadTokens"
         labels:
           date: "$.daily[*].date"
       - name: claude_cache_creation_tokens
         path: "$.daily[*].cacheCreationTokens"
         labels:
           date: "$.daily[*].date"
       - name: claude_model_cost
         path: "$.daily[*].modelBreakdowns[*].cost"
         labels:
           model_name: "$.daily[*].modelBreakdowns[*].modelName"
           date: "$.daily[*].date"
   ```

3. **Configure Prometheus** (`prometheus.yml`):
   ```yaml
   global:
     scrape_interval: 15s
   scrape_configs:
   - job_name: 'claude-usage'
     static_configs:
     - targets: ['json-exporter:7979']
     params:
       module: [claude_usage]
       target: ['http://host.docker.internal:8000/data/export_latest.json']
     scrape_interval: 5m
   ```

### Option 2: InfluxDB + Telegraf

1. **Install InfluxDB and Telegraf**
2. **Configure Telegraf** to parse your JSON files
3. **Use InfluxDB as Grafana data source**

### Option 3: Simple JSON Data Source Plugin

1. **Install JSON Data Source Plugin** in Grafana
2. **Create HTTP endpoint** serving your JSON data
3. **Configure queries** directly in Grafana panels

## Dashboard Import Instructions

1. **Open Grafana** (typically http://localhost:3000)
2. **Go to Dashboards** → **Import**
3. **Upload** the `grafana-dashboard.json` file
4. **Configure Data Source** - select your chosen data source
5. **Save Dashboard**

## Dashboard Features

The Grafana dashboard includes:

### 📈 Daily Usage Trends
- Total tokens and daily costs over time
- Dual-axis chart with smooth line interpolation
- Color-coded: tokens in blue, costs in pink

### 🎯 Model Usage Distribution  
- Pie chart showing cost breakdown by Claude model
- Displays percentages and actual costs
- Matches your HTML dashboard's model distribution

### ⚡ Efficiency Metrics Over Time
- Cost per million tokens trending
- Helps identify efficiency patterns
- Lower values indicate better efficiency

### 🔄 Cache Efficiency Over Time
- Cache hit rate percentage
- Shows how well context caching is working
- Higher percentages = lower costs

### 💬 Input vs Output Tokens
- Dual-line chart comparing input and output
- Shows conversation patterns
- Input in red, output in orange

### 📊 Current Month Summary
- Four key statistics in stat panels
- Total cost, total tokens, active days, average cost per day
- Color-coded for quick assessment

## Customization

### Adding New Panels
To add panels for additional metrics from your data:

1. **Edit Dashboard** in Grafana
2. **Add Panel** 
3. **Configure Query** using your data source
4. **Set Visualization Type** (timeseries, stat, pie, etc.)

### Template Variables
The dashboard includes a model filter variable:
- Filter by specific Claude models
- Multi-select support
- Updates all panels automatically

### Alerts
You can add alerts for:
- Daily spending thresholds
- Unusual token usage patterns  
- Cache efficiency drops
- Model cost anomalies

## Data Refresh

- **Auto-refresh**: Set to 5 minutes by default
- **Manual refresh**: Use the refresh button
- **Time range**: Defaults to last 30 days

## Notes

- The dashboard assumes your JSON data follows the same structure as `export_latest.json`
- Metric names may need adjustment based on your data source configuration
- Time-based queries assume date fields are properly formatted
- Colors match your existing HTML dashboard for consistency

## Troubleshooting

### No Data Showing
- Verify data source connection
- Check metric names in queries
- Ensure JSON structure matches expectations
- Verify time ranges

### Performance Issues
- Reduce query frequency
- Limit time ranges for large datasets
- Consider data aggregation

### Styling Issues  
- Adjust colors in panel field overrides
- Modify display options for better readability
- Use Grafana's theming options