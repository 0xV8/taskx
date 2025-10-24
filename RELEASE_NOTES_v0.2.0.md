# taskx v0.2.0 Release Notes

**Release Date:** 2025-TBD

> **Modern Python Task Runner - Now with shell completion, aliases, prompts, and templates!**

---

## 🎉 What's New

taskx v0.2.0 brings four major productivity features that make task automation faster, smarter, and more flexible.

### ⚡ Shell Completion

TAB completion for your favorite shell! No more typing full command names or remembering exact task names.

```bash
$ taskx completion bash --install
✓ Completion installed

$ taskx <TAB>
list  run  watch  graph  init  completion  --version  --help

$ taskx run te<TAB>
test  test-unit  test-integration  test-e2e
```

**Supported shells:** bash, zsh, fish, PowerShell

**What gets completed:**
- Commands (`list`, `run`, `watch`, etc.)
- Task names (dynamically loaded from your config)
- Options and flags (`--config`, `--format`, etc.)
- Graph formats (`tree`, `dot`, `mermaid`)

[📖 Shell Completion Guide](./docs/shell-completion.md)

---

### 🏷️ Task Aliases

Create short names for your most-used tasks. Type less, do more.

```toml
[tool.taskx.aliases]
t = "test"
b = "build"
d = "deploy"
```

```bash
$ taskx run t
→ Alias 't' resolves to task 'test'
===== 51 tests passed =====
```

**Features:**
- Global aliases in `[tool.taskx.aliases]`
- Per-task aliases in task definitions
- Automatic conflict detection
- Works with shell completion

[📖 Task Aliases Guide](./docs/task-aliases.md)

---

### 💬 Interactive Prompts

Ask users for input during task execution. Perfect for deployments, credentials, and flexible workflows.

```toml
[tool.taskx.tasks.deploy]
cmd = "sh deploy.sh ${ENV}"
prompt.ENV = {
    type = "select",
    message = "Deploy to which environment?",
    choices = ["staging", "production"]
}
confirm = "Deploy to ${ENV}?"
```

```bash
$ taskx run deploy
? Deploy to which environment?
  staging
> production

? Deploy to production? (y/N) y
→ Running: sh deploy.sh production
Deploying to production...
```

**Prompt types:**
- `text` - Free-form text input
- `select` - Choose from dropdown
- `confirm` - Yes/no confirmation
- `password` - Hidden input

**CI/CD safe:** Falls back to defaults in non-interactive mode.

[📖 Interactive Prompts Guide](./docs/interactive-prompts.md)

---

### 📦 Project Templates

Start new projects instantly with production-ready templates. Skip the boilerplate.

```bash
$ taskx init --list-templates
Available templates:

  WEB:
    django               Django web application
    fastapi              FastAPI microservice

  DATA:
    data-science         ML project with Jupyter & MLflow

  LIBRARY:
    python-library       Python package with PyPI publishing

$ taskx init --template fastapi
? Project name: myapi
? Include SQLAlchemy database support? (y/N) y
? Include Docker configuration? (Y/n) y

✓ Created fastapi project with taskx configuration

$ taskx dev
→ Running: uvicorn app:app --reload
INFO: Uvicorn running on http://127.0.0.1:8000
```

**Available templates:**
- **Django** - Full web app with migrations, testing, Celery, Docker
- **FastAPI** - Async microservice with database, Docker, API docs
- **Data Science** - ML pipeline with Jupyter, MLflow, training workflows
- **Python Library** - Package with PyPI publishing, testing, documentation

[📖 Project Templates Guide](./docs/project-templates.md)

---

## 📊 By the Numbers

- **4 major features** - Completion, aliases, prompts, templates
- **93% test pass rate** - 523 passing tests, 39 failures being addressed
- **70% code coverage** - Comprehensive test suite
- **4 project templates** - Production-ready configurations
- **4 shells supported** - bash, zsh, fish, PowerShell
- **100% backward compatible** - Zero breaking changes

---

## 🚀 Getting Started

### Installation

```bash
pip install taskx==0.2.0
```

Or upgrade from v0.1.0:

```bash
pip install --upgrade taskx
```

### Quick Setup

```bash
# 1. Verify installation
$ taskx --version
taskx version 0.2.0

# 2. Enable shell completion (optional)
$ taskx completion bash --install
✓ Completion installed

# 3. Try it out
$ taskx li<TAB>
# Completes to: taskx list
```

---

## 🔄 Upgrade Guide

### For Existing Users

**Good news:** v0.2.0 is **100% backward compatible** with v0.1.0!

Your existing `pyproject.toml` will work without any changes. All new features are opt-in.

### Upgrade Steps

```bash
# 1. Upgrade taskx
$ pip install --upgrade taskx

# 2. Verify upgrade
$ taskx --version
taskx version 0.2.0

# 3. Test your existing tasks
$ taskx list
$ taskx run test

# 4. (Optional) Adopt new features
$ taskx completion bash --install
```

[📖 Full Migration Guide](./docs/migration-v0.1.0-to-v0.2.0.md)

---

## 💡 Usage Examples

### Development Workflow

```toml
# pyproject.toml
[tool.taskx.aliases]
t = "test"
d = "dev"
f = "format"

[tool.taskx.tasks]
dev = { cmd = "uvicorn app:app --reload", watch = ["**/*.py"] }
test = "pytest tests/ -v"
format = "black . && isort ."
check = { parallel = ["format", "test", "lint"] }
```

```bash
$ taskx d        # Start dev server
$ taskx t        # Run tests
$ taskx f        # Format code
```

### Deployment Workflow

```toml
[tool.taskx.tasks.deploy]
depends = ["check", "build"]
cmd = "sh deploy.sh ${ENV}"
prompt.ENV = {
    type = "select",
    message = "🚀 Deploy to which environment?",
    choices = ["staging", "production"],
    default = "staging"
}
confirm = "Ready to deploy to ${ENV}?"
```

```bash
$ taskx run deploy
? 🚀 Deploy to which environment?
> staging
  production

? Ready to deploy to staging? (Y/n) y
→ Running: check
✓ All checks passed
→ Running: build
✓ Build complete
→ Running: deploy
✓ Deployed to staging
```

---

## 🐛 Bug Fixes

- Fixed Click Path validation issue preventing `taskx init` from creating configs
- Improved error messages for configuration errors
- Better handling of non-interactive environments
- Enhanced cross-platform compatibility

---

## 🔒 Security

- **Sandboxed Jinja2 template rendering** - Prevents code injection in templates
- **Input validation** - Aliases and task names validated for safety
- **Secure password prompts** - Hidden input, no echo to terminal
- **Reserved name protection** - Prevents using command names as aliases

---

## 📚 Documentation

### New Guides

- [Shell Completion Guide](./docs/shell-completion.md) - Complete installation and usage
- [Task Aliases Guide](./docs/task-aliases.md) - Global and per-task aliases
- [Interactive Prompts Guide](./docs/interactive-prompts.md) - All prompt types and CI/CD
- [Project Templates Guide](./docs/project-templates.md) - Available templates and customization
- [Migration Guide](./docs/migration-v0.1.0-to-v0.2.0.md) - Upgrade instructions

### Updated

- [README.md](./README.md) - Updated with v0.2.0 features
- [TECHNICAL_REFERENCE.md](./TECHNICAL_REFERENCE.md) - Complete API documentation

---

## 🤝 Acknowledgments

Thank you to all users who provided feedback and helped shape v0.2.0!

Special thanks to:
- Early testers who tried pre-release versions
- Contributors who reported issues
- Community members who suggested features

---

## 🔗 Links

- **Documentation:** [docs/](./docs/)
- **PyPI:** https://pypi.org/project/taskx/
- **GitHub:** https://github.com/0xV8/taskx
- **Issues:** https://github.com/0xV8/taskx/issues
- **Changelog:** [CHANGELOG.md](./CHANGELOG.md)

---

## 📅 What's Next?

v0.2.0 is the foundation for even more powerful features. Here's a sneak peek at what's coming:

**Phase 2 (v0.3.0) - Planned:**
- Remote task execution (SSH, Docker, Kubernetes)
- Advanced caching and incremental builds
- Plugin system for extensibility
- Multi-project workspaces
- Task scheduling and cron-like execution

**Want to contribute?** Check out our [contribution guidelines](./docs/contributing.md)!

---

## 🎊 Try It Now!

```bash
# Install v0.2.0
$ pip install taskx==0.2.0

# Create a new FastAPI project
$ taskx init --template fastapi

# Start coding immediately
$ taskx dev
```

**Welcome to taskx v0.2.0! 🚀**

---

*taskx - Modern Python Task Runner. npm scripts for Python.*
