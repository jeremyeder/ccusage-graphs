# Open Source Preparation - Complete Execution Guide

**Project:** ccusage-graphs
**Goal:** Prepare codebase for public release on GitHub
**License:** MIT
**Estimated Time:** 1-2 hours

## Executive Summary

The ccusage-graphs codebase is a comprehensive visualization suite for Claude Code usage metrics. Code review shows **EXCELLENT** code quality and documentation, but requires **6 critical/high priority fixes** before open sourcing, primarily:
1. Missing LICENSE file (CRITICAL)
2. Personal paths in documentation (HIGH)
3. Data file verification (HIGH)
4. Attribution additions (MEDIUM)

## Review Findings Summary

### Severity Breakdown
- **Critical:** 1 (No LICENSE file)
- **High:** 2 (Personal paths, data verification)
- **Medium:** 3 (Attribution, privacy note, license check)
- **Low:** 3 (Nice-to-haves)

### Overall Assessment
- ✅ Code Quality: ★★★★★ (Excellent)
- ✅ Documentation: ★★★★★ (Excellent)
- ✅ Security: ★★★★☆ (Good, minor fixes needed)
- ❌ Licensing: ★★★☆☆ (Fair, missing LICENSE file)

---

## PHASE 1: CRITICAL FIXES (Must Complete)

### Task 1.1: Create MIT LICENSE File

**File:** `LICENSE` (new file at repository root)

**Action:** Create file with the following content:

```text
MIT License

Copyright (c) 2025 Jeremy Eder

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

**Rationale:** README.md line 387 references "MIT License - See LICENSE file" but no file exists. Without this, code is "all rights reserved" by default.

**Verification:**
```bash
ls -la LICENSE
cat LICENSE | grep "MIT License"
```

---

### Task 1.2: Remove Personal Paths from grafana-sqlite-setup.md

**File:** `grafana-sqlite-setup.md`

**Problem:** Contains hardcoded paths `/Users/jeder/repos/ccusage-graphs/` at lines 20, 54, 62, 80

**Action:** Replace all instances of `/Users/jeder/repos/ccusage-graphs/` with one of:
- `$PROJECT_ROOT/` (recommended for shell commands)
- `/path/to/ccusage-graphs/` (for general references)
- Relative paths where appropriate

**Specific Changes:**

**Line 20 (approx):**
```markdown
# BEFORE
sqlite3 /Users/jeder/repos/ccusage-graphs/claude_usage.db

# AFTER
sqlite3 $PROJECT_ROOT/claude_usage.db
# or
sqlite3 /path/to/ccusage-graphs/claude_usage.db
```

**Line 54, 62, 80 (approx):**
Apply same pattern - replace `/Users/jeder/repos/ccusage-graphs/` with generic path

**Verification:**
```bash
grep -n "/Users/jeder" grafana-sqlite-setup.md
# Should return no results
```

**Rationale:** Exposes personal username and directory structure.

---

### Task 1.3: Fix Hardcoded Path in index.html

**File:** `index.html`

**Problem:** Line 2523 contains hardcoded absolute path

**Current Code (line 2523):**
```javascript
await fetch('/Users/jeder/repos/ccusage-graphs/refresh-data', { method: 'POST' })
```

**Action:** Change to relative path:
```javascript
await fetch('./refresh-data', { method: 'POST' })
```

**Verification:**
```bash
grep -n "/Users/jeder" index.html
# Should return no results
```

**Rationale:** Hardcoded absolute path will not work for other users and exposes personal information.

---

### Task 1.4: Verify Data Files Are Gitignored

**Files to check:** `data/*.json`, `*.db`

**Action:** Run verification commands:

```bash
# Check .gitignore contains patterns
grep "data/.*\.json" .gitignore
grep ".*\.db" .gitignore

# Verify files are not tracked by git
git status --ignored

# Verify no data files in git history
git log --all --full-history -- "data/*.json"
git log --all --full-history -- "*.db"
```

**Expected Results:**
- ✅ `.gitignore` contains `data/*.json` pattern
- ✅ `.gitignore` contains `*.db` pattern
- ✅ `git status --ignored` shows data files as ignored (not staged)
- ✅ `git log` returns no results (files never committed)

**If files ARE tracked:**
```bash
# Remove from git but keep locally
git rm --cached data/*.json
git rm --cached *.db
git commit -m "Remove data files from git tracking"
```

**Rationale:** Data files contain personal project names and usage patterns:
- `vTeam`, `rh-2brain` (Red Hat internal projects)
- Personal directory structures
- Usage metrics that may be confidential

---

## PHASE 2: IMPORTANT IMPROVEMENTS (Should Complete)

### Task 2.1: Add Dependencies/Attribution Section to README

**File:** `README.md`

**Action:** Add new section before "License" section (before line 387)

**Content to add:**

```markdown
## Dependencies & Attribution

This project builds on excellent open source tools:

### Required Dependencies
- **[ccusage CLI](https://github.com/anthropics/ccusage)** - Claude Code usage data export (check npm package license)
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
```

**Location:** Insert after line 386 (before "## License" section)

**Verification:**
```bash
grep -n "## Dependencies & Attribution" README.md
# Should show the new section
```

**Rationale:** Proper attribution and license documentation for open source compliance.

---

### Task 2.2: Add Privacy Note to README

**File:** `README.md`

**Action:** Add new section in "Getting Started" area (after Installation, around line 100)

**Content to add:**

```markdown
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
```

**Location:** Insert around line 100 (after "Installation" section, before "Quick Start")

**Verification:**
```bash
grep -n "## Privacy & Data Security" README.md
# Should show the new section
```

**Rationale:** Users need to understand data privacy implications when using/sharing this tool.

---

### Task 2.3: Verify ccusage License Compatibility

**Action:** Check the license of @anthropic/ccusage npm package

**Commands:**
```bash
# Check npm package info
npm view @anthropic/ccusage license

# Or check package.json if installed
npm ls @anthropic/ccusage --json | grep license
```

**Expected:** Compatible license (MIT, Apache 2.0, BSD, etc.)

**If incompatible:**
- Document in README that ccusage is required but has different license
- Ensure compliance with that license's requirements

**Update README if needed:** In Dependencies section, add actual license info:
```markdown
- **[ccusage CLI](https://github.com/anthropics/ccusage)** - [LICENSE_HERE] - Claude Code usage data export
```

**Rationale:** Ensure all dependencies are compatible with MIT license for the main project.

---

## PHASE 3: OPTIONAL ENHANCEMENTS (Nice to Have)

### Task 3.1: Add CONTRIBUTING.md

**File:** `CONTRIBUTING.md` (new file)

**Content:**

```markdown
# Contributing to ccusage-graphs

Thank you for your interest in contributing! This project welcomes contributions from the community.

## Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/[USERNAME]/ccusage-graphs.git
   cd ccusage-graphs
   ```

2. Install dependencies:
   ```bash
   # Install ccusage CLI
   npm install -g @anthropic/ccusage

   # Install linting tools
   brew install shellcheck
   npm install -g markdownlint-cli
   ```

3. Run tests:
   ```bash
   ./refresh_data.sh
   python3 create_sqlite_db.py
   open index.html
   ```

## Development Workflow

See [CLAUDE.md](CLAUDE.md) for detailed development instructions including:
- Branch workflow (always use feature branches)
- Testing procedures
- Linting requirements
- Code standards

## Pull Request Process

1. Create a feature branch: `git checkout -b feature/description`
2. Make your changes
3. Run all linters (shellcheck, markdownlint, black, isort, flake8)
4. Test thoroughly
5. Update documentation if needed
6. Submit PR with clear description

## Code Style

- **Shell**: Follow shellcheck recommendations
- **Python**: PEP 8 (use black, isort, flake8)
- **Markdown**: Follow markdownlint rules
- **Documentation**: Clear, concise, with examples

## Questions?

Open an issue for questions or discussions.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
```

**Verification:**
```bash
ls -la CONTRIBUTING.md
```

---

### Task 3.2: Add License Badge to README

**File:** `README.md`

**Action:** Add badges to the top of README (after title, around line 3)

**Content to add:**

```markdown
# Claude Code Usage Graphs

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Shell Script](https://img.shields.io/badge/shell-bash-green.svg)](https://www.gnu.org/software/bash/)

Comprehensive visualization suite for Claude Code usage metrics...
```

**Location:** Insert after line 1 (the main title)

---

### Task 3.3: Consider CHANGELOG.md

**File:** `CHANGELOG.md` (new file, optional)

**Action:** Create from UPGRADE_SUMMARY.md content or start fresh

**Sample structure:**
```markdown
# Changelog

All notable changes to this project will be documented in this file.

## [1.0.0] - 2025-01-XX

### Added
- Initial public release
- HTML dashboard with Chart.js visualizations
- SQLite database backend
- Grafana integration
- Docker compose stack
- Comprehensive documentation

### Features
- Daily, weekly, monthly usage reports
- Model breakdown (Sonnet, Opus, Haiku)
- Cache efficiency metrics
- Cost tracking
- Multiple export formats

## [Unreleased]

### Planned
- Additional visualization options
- Enhanced filtering
- Real-time metrics
```

---

## PRE-RELEASE CHECKLIST

Execute this checklist in order before publishing:

### Critical Items (MUST COMPLETE)
```markdown
- [ ] LICENSE file created with MIT license text
- [ ] grafana-sqlite-setup.md updated (removed /Users/jeder/ paths)
- [ ] index.html line 2523 updated (relative path)
- [ ] Data files verified as gitignored:
  - [ ] data/*.json not tracked
  - [ ] *.db not tracked
  - [ ] No data files in git history
```

### Important Items (SHOULD COMPLETE)
```markdown
- [ ] Dependencies & Attribution section added to README.md
- [ ] Privacy & Data Security section added to README.md
- [ ] ccusage license verified and documented
- [ ] All personal paths removed from docs (grep verification)
```

### Optional Items (NICE TO HAVE)
```markdown
- [ ] CONTRIBUTING.md created
- [ ] License badge added to README.md
- [ ] CHANGELOG.md created or UPGRADE_SUMMARY.md converted
- [ ] GitHub repository URL added to README.md
```

### Final Verification
```bash
# Run all verification commands
grep -r "/Users/jeder" . --exclude-dir=.git --exclude-dir=data
# Should return NO results

git status
# Should show NO data files staged

ls -la LICENSE
# Should exist

grep -n "## Dependencies & Attribution" README.md
# Should show section

grep -n "## Privacy & Data Security" README.md
# Should show section
```

---

## COMPLETE EXECUTION COMMANDS

For quick execution, run these commands in order:

```bash
# Navigate to project
cd /Users/jeder/repos/ccusage-graphs

# Task 1.1: Create LICENSE (manual - copy content above)
cat > LICENSE << 'EOF'
MIT License

Copyright (c) 2025 Jeremy Eder

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF

# Task 1.2 & 1.3: Edit files (use Claude Code or manual editing)
# Replace personal paths in grafana-sqlite-setup.md
# Fix path in index.html line 2523

# Task 1.4: Verify gitignore
git status --ignored | grep -E "(data/.*json|.*db)"
git log --all --full-history -- "data/*.json"
git log --all --full-history -- "*.db"

# Task 2.1 & 2.2: Add sections to README (use Claude Code or manual editing)

# Task 2.3: Check ccusage license
npm view @anthropic/ccusage license

# Final verification
grep -r "/Users/jeder" . --exclude-dir=.git --exclude-dir=data
git status
ls -la LICENSE
```

---

## CONTEXT: CODEBASE STRUCTURE

### Project Files
```
ccusage-graphs/
├── LICENSE                          # ❌ MISSING - CREATE THIS
├── README.md                        # ✏️ EDIT - Add sections
├── CLAUDE.md                        # ✅ OK - Dev docs
├── COMPATIBILITY_NOTES.md           # ✅ OK
├── refresh_data.sh                  # ✅ OK - Main data script
├── create_sqlite_db.py              # ✅ OK - Database generator
├── index.html                       # ✏️ EDIT - Fix line 2523
├── docker-compose.yml               # ✅ OK
├── grafana-sqlite-setup.md          # ✏️ EDIT - Remove personal paths
├── grafana-setup.md                 # ✅ OK
├── grafana-dashboard.json           # ✅ OK
├── grafana-dashboard-sqlite.json    # ✅ OK
├── prometheus.yml                   # ✅ OK
├── json-exporter-config.yml         # ✅ OK
├── .gitignore                       # ✅ OK - Properly configured
├── data/                            # ⚠️ GITIGNORED - Never commit
│   ├── export.json                  # Personal usage data
│   ├── export_instances.json        # Contains project names
│   └── export_instances_small.json  # Contains project names
└── *.db                             # ⚠️ GITIGNORED - Never commit
```

### Key Files Analysis

**No Issues (Safe):**
- `refresh_data.sh` - Clean shell script, no hardcoded paths
- `create_sqlite_db.py` - Clean Python, standard library only
- `docker-compose.yml` - Uses default credentials with env override
- All Grafana/Prometheus configs - No personal info
- `.gitignore` - Properly excludes sensitive data

**Requires Editing:**
- `LICENSE` - Must create
- `README.md` - Add 2 sections
- `grafana-sqlite-setup.md` - Remove personal paths (4 locations)
- `index.html` - Fix 1 hardcoded path

**Monitor (Gitignored but Verify):**
- `data/*.json` - Contains personal project names
- `*.db` - Contains usage history

---

## SENSITIVE DATA DETAILS

### Personal Information Found

**Username:** `jeder`
**Home Directory:** `/Users/jeder/`
**Project Path:** `/Users/jeder/repos/ccusage-graphs/`

### Internal Project Names (in data files)
- `vTeam` (multiple variants) - Appears to be Red Hat internal
- `rh-2brain` - Red Hat prefix suggests internal
- `claude-slash` - May be personal/internal
- `awtrix3-py` - May be personal
- `rover`, `spec-kit`, `patternfly-react-seed` - Uncertain

**Status:** All in gitignored files, but verify never committed to history

---

## DEPENDENCY LICENSES (Verified)

### Compatible Licenses
- **Prometheus** - Apache 2.0 ✅
- **Grafana** - AGPL v3 ✅ (used as service, not modified/distributed)
- **JSON Exporter** - Apache 2.0 ✅
- **nginx** - 2-clause BSD ✅
- **Chart.js** - MIT ✅
- **Python** - PSF License ✅

### To Verify
- **@anthropic/ccusage** - License TBD (check npm package)

### License Compatibility
All verified dependencies are compatible with MIT license for this project.

---

## GITHUB REPOSITORY SETUP (Post-Release)

After all fixes are complete and code is pushed to GitHub:

1. **Repository Settings:**
   - Set description: "Comprehensive visualization suite for Claude Code usage metrics"
   - Add topics: `claude-code`, `usage-metrics`, `visualization`, `grafana`, `prometheus`
   - Enable Issues
   - Enable Discussions (optional)

2. **Setup Dependabot:**
   ```yaml
   # .github/dependabot.yml
   version: 2
   updates:
     - package-ecosystem: "docker"
       directory: "/"
       schedule:
         interval: "weekly"
   ```

3. **Add GitHub Actions (optional):**
   - Linting workflow
   - Documentation build
   - Link checker

4. **Repository Badges:**
   - Add to README: License, Shell, Python version

---

## SUCCESS CRITERIA

### Pre-Release Validation

**Code is ready for open source when:**
- ✅ `grep -r "/Users/jeder" . --exclude-dir=.git --exclude-dir=data` returns NO results
- ✅ `git status` shows NO data files (*.json, *.db) staged
- ✅ `git log --all --full-history -- "data/*.json"` returns NO results
- ✅ `ls LICENSE` shows file exists
- ✅ `cat LICENSE | grep "MIT License"` succeeds
- ✅ README.md contains "Dependencies & Attribution" section
- ✅ README.md contains "Privacy & Data Security" section
- ✅ No credentials, API keys, or tokens in any committed files
- ✅ All linters pass (shellcheck, markdownlint)
- ✅ All functionality still works (test with `./refresh_data.sh` and `python3 create_sqlite_db.py`)

### Post-Release Validation

**After pushing to GitHub:**
- ✅ Repository is PUBLIC (or PRIVATE if desired)
- ✅ README displays correctly on GitHub
- ✅ LICENSE badge shows in README
- ✅ Dependabot is configured
- ✅ No sensitive data visible in any committed files
- ✅ Documentation is complete and accurate
- ✅ Issue templates created (optional)
- ✅ Contributing guidelines clear

---

## ESTIMATED TIMELINE

### Phase 1 (Critical): 30-45 minutes
- Create LICENSE: 5 min
- Edit grafana-sqlite-setup.md: 10 min
- Edit index.html: 5 min
- Verify gitignore: 10 min
- Testing: 10 min

### Phase 2 (Important): 30-45 minutes
- Add Dependencies section: 15 min
- Add Privacy section: 10 min
- Verify ccusage license: 5 min
- Testing: 10 min

### Phase 3 (Optional): 30-60 minutes
- Create CONTRIBUTING.md: 20 min
- Add badges: 5 min
- Create CHANGELOG: 15 min
- Final review: 20 min

**Total Time: 1.5 - 2.5 hours**

---

## ROLLBACK PLAN

If issues are discovered after release:

1. **Immediate Actions:**
   ```bash
   # Make repository private
   gh repo edit --visibility private

   # Or delete if necessary
   gh repo delete [REPO_NAME] --confirm
   ```

2. **Fix Issues Locally:**
   - Address the problem
   - Test thoroughly
   - Verify no sensitive data

3. **Re-release:**
   - Push fixed code
   - Make repository public again
   - Announce the update

---

## CONTACT & SUPPORT

**Project Owner:** Jeremy Eder (Distinguished Engineer, Red Hat)
**Repository:** [To be added after creation]
**Issues:** [GitHub Issues URL]
**Discussions:** [GitHub Discussions URL]

---

## NOTES FOR EXECUTOR

### Using This Document

This document contains complete context to execute the open source preparation from scratch. You can:

1. **Manual Execution:** Follow each task sequentially
2. **Claude Code Execution:** Provide this entire document to Claude Code as context
3. **Automated Execution:** Extract bash commands into a script

### Important Reminders

- ⚠️ **NEVER commit data files** (*.json, *.db)
- ⚠️ **Test after each phase** to ensure functionality preserved
- ⚠️ **Create feature branch** for this work
- ⚠️ **Run linters** before final commit
- ⚠️ **Verify no personal paths** before pushing to GitHub

### When in Doubt

- Review the Pre-Release Checklist
- Run all verification commands
- Check git status multiple times
- Test the HTML dashboard and database creation
- Grep for personal information patterns

---

**END OF EXECUTION GUIDE**
