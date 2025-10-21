# Setup Guide - Cryptocurrency Price Tracker

This guide will help you set up the project with a virtual environment.

---

## Quick Setup

### 1. Navigate to Project Directory

```bash
cd /Users/vipin/Downloads/Opensource/crypto-tracker
```

### 2. Activate Virtual Environment

The virtual environment is already created! Just activate it:

**On macOS/Linux:**
```bash
source venv/bin/activate
```

**On Windows:**
```bash
venv\Scripts\activate
```

You'll see `(venv)` appear in your terminal prompt.

### 3. Verify Installation

```bash
# Check taskx is installed
taskx --version

# Should output: taskx version 0.1.0
```

### 4. Run the Project

```bash
# List all available tasks
taskx list

# Run the complete pipeline
taskx run pipeline

# Generate and view report
taskx run view
```

---

## What's Installed

The virtual environment includes:

- **taskx** - Modern Python task runner
- **Python standard library** - All scripts use only built-in modules

No external API keys or additional dependencies needed!

---

## Deactivating Virtual Environment

When you're done working:

```bash
deactivate
```

---

## Full Setup from Scratch

If you need to recreate the virtual environment:

```bash
# Remove old virtual environment (if exists)
rm -rf venv

# Create new virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Verify installation
taskx --version
```

---

## Project Structure

```
crypto-tracker/
├── venv/                   # Virtual environment (git-ignored)
├── scripts/                # Python scripts
│   ├── fetch_prices.py
│   ├── validate_data.py
│   ├── analyze_data.py
│   └── generate_report.py
├── data/                   # Generated data (git-ignored)
├── reports/                # Generated reports (git-ignored)
├── pyproject.toml          # taskx configuration
├── requirements.txt        # Python dependencies
├── .gitignore              # Git ignore rules
└── README.md               # Main documentation
```

---

## Common Commands

```bash
# Activate virtual environment
source venv/bin/activate

# List all tasks
taskx list

# Run complete pipeline
taskx run pipeline

# Run individual tasks
taskx run fetch
taskx run validate
taskx run analyze
taskx run report

# Run parallel quality checks
taskx run check

# Watch mode (auto-run on changes)
taskx watch dev

# View dependency graph
taskx graph

# Clean generated files
taskx run clean
```

---

## Troubleshooting

### Virtual environment not found

```bash
# Recreate it
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### taskx command not found

Make sure you've activated the virtual environment:
```bash
source venv/bin/activate
```

### Permission denied errors

```bash
# Make scripts executable
chmod +x scripts/*.py
```

---

## Development Workflow

1. **Activate virtual environment**
   ```bash
   source venv/bin/activate
   ```

2. **Make changes to scripts**
   - Edit files in `scripts/`

3. **Test your changes**
   ```bash
   taskx run pipeline
   ```

4. **Use watch mode for live development**
   ```bash
   taskx watch dev
   ```

5. **Deactivate when done**
   ```bash
   deactivate
   ```

---

## Next Steps

- Read the main [README.md](README.md) for full documentation
- Explore the [pyproject.toml](pyproject.toml) to see task definitions
- Check out the scripts in `scripts/` to understand the pipeline

Happy coding! 🚀
