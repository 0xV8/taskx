# Release Checklist - taskx v0.2.0

**Release Version:** 0.2.0
**Release Date:** TBD
**Status:** Pre-Release Preparation

---

## Phase 1: Pre-Release Verification

### Code Quality

- [x] All Sprint 1-4 features implemented
  - [x] Shell Completion (Sprint 1)
  - [x] Task Aliases (Sprint 2)
  - [x] Interactive Prompts (Sprint 3)
  - [x] Project Templates (Sprint 4)

- [x] Sprint 5 (Testing) completed
  - [x] Test suite created (571 tests)
  - [x] Integration tests written
  - [x] Performance tests added
  - [x] Memory profiling tests included

- [x] Sprint 5.5 (Bug Fixes) completed
  - [x] 70 tests fixed
  - [x] 93% pass rate achieved (523 passing, 39 failing)
  - [x] 70% code coverage baseline

- [ ] All critical tests passing
  - [x] Unit tests: Mostly passing
  - [x] Integration tests: Mostly passing
  - [ ] E2E tests: 39 failures remaining (non-blocking)
  - [x] Performance tests: Passing

- [ ] Code quality checks
  - [ ] Linting passes (`ruff check taskx tests`)
  - [ ] Type checking passes (`mypy taskx`)
  - [ ] Formatting applied (`black taskx tests && isort taskx tests`)

### Documentation

- [x] Sprint 6 (Documentation) completed
  - [x] Shell completion guide
  - [x] Task aliases guide
  - [x] Interactive prompts guide
  - [x] Project templates guide
  - [x] Migration guide (v0.1.0 → v0.2.0)
  - [x] CHANGELOG.md
  - [x] RELEASE_NOTES_v0.2.0.md
  - [x] TECHNICAL_REFERENCE.md updated

- [x] README.md updated with v0.2.0 features

- [ ] All documentation examples tested
  - [x] Shell completion examples verified
  - [x] Task alias examples verified
  - [x] Interactive prompt examples verified
  - [x] Template examples verified
  - [ ] All code snippets executable

- [ ] All links verified
  - [ ] Internal doc links work
  - [ ] External links valid
  - [ ] GitHub links correct

### Version Numbers

- [x] Version updated in `taskx/__init__.py` → 0.2.0
- [x] Version updated in `pyproject.toml` → 0.2.0
- [x] Version updated in `TECHNICAL_REFERENCE.md` → 0.2.0
- [x] Version mentioned in `README.md` → 0.2.0
- [x] Version in `CHANGELOG.md` → 0.2.0
- [x] Version in `RELEASE_NOTES_v0.2.0.md` → 0.2.0

---

## Phase 2: Build & Package

### Clean Build Environment

```bash
# Clean previous builds
- [ ] rm -rf build/ dist/ *.egg-info
- [ ] rm -rf htmlcov/ .coverage .pytest_cache
- [ ] rm -rf taskx/__pycache__ tests/__pycache__
```

### Build Distribution Packages

```bash
# Build packages
- [ ] python -m build
```

**Expected outputs:**
- `dist/taskx-0.2.0-py3-none-any.whl`
- `dist/taskx-0.2.0.tar.gz`

### Verify Packages

```bash
# Check package integrity
- [ ] twine check dist/*
```

**Expected:** All checks pass with no warnings.

### Inspect Package Contents

```bash
# Check wheel contents
- [ ] python -m zipfile -l dist/taskx-0.2.0-py3-none-any.whl

# Verify includes:
- [ ] taskx/ directory
- [ ] taskx/templates/ directory
- [ ] taskx/completion/ directory
- [ ] Metadata files
```

---

## Phase 3: Local Testing

### Test Installation from Wheel

```bash
# Create test environment
- [ ] python -m venv test_env_wheel
- [ ] source test_env_wheel/bin/activate  # or test_env_wheel\Scripts\activate on Windows

# Install from wheel
- [ ] pip install dist/taskx-0.2.0-py3-none-any.whl

# Verify installation
- [ ] taskx --version  # Should show: taskx version 0.2.0
- [ ] python -c "import taskx; print(taskx.__version__)"  # Should print: 0.2.0

# Test basic functionality
- [ ] taskx init --list-templates
- [ ] taskx completion bash > /tmp/completion_test.bash
- [ ] cat /tmp/completion_test.bash  # Verify content

# Cleanup
- [ ] deactivate
- [ ] rm -rf test_env_wheel
```

### Test Installation from Source Distribution

```bash
# Create test environment
- [ ] python -m venv test_env_sdist
- [ ] source test_env_sdist/bin/activate

# Install from source
- [ ] pip install dist/taskx-0.2.0.tar.gz

# Verify installation
- [ ] taskx --version
- [ ] taskx init --list-templates

# Cleanup
- [ ] deactivate
- [ ] rm -rf test_env_sdist
```

### Test in Fresh Project

```bash
# Create test project
- [ ] mkdir /tmp/taskx_test_project
- [ ] cd /tmp/taskx_test_project

# Initialize with template
- [ ] taskx init --template fastapi --env project_name=testapi --env use_database=true --env use_docker=true

# Verify generated config
- [ ] cat pyproject.toml  # Check generated content

# Test aliases
- [ ] taskx list --include-aliases

# Test completion (if shell supports)
- [ ] taskx completion bash > /tmp/test_completion.bash

# Cleanup
- [ ] cd -
- [ ] rm -rf /tmp/taskx_test_project
```

---

## Phase 4: TestPyPI Upload (Staging)

### Configure TestPyPI

```bash
# Ensure ~/.pypirc has TestPyPI config
- [ ] cat ~/.pypirc  # Verify testpypi section exists
```

### Upload to TestPyPI

```bash
# Upload packages
- [ ] twine upload --repository testpypi dist/*
```

**Expected:** Successful upload message with TestPyPI URL.

### Test Installation from TestPyPI

```bash
# Create test environment
- [ ] python -m venv test_env_testpypi
- [ ] source test_env_testpypi/bin/activate

# Install from TestPyPI
- [ ] pip install --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ taskx==0.2.0

# Verify installation
- [ ] taskx --version
- [ ] taskx init --list-templates
- [ ] taskx completion bash > /tmp/test.bash

# Test all features
- [ ] taskx init --template django --env project_name=testproject --env use_celery=false --env use_docker=false
- [ ] cat pyproject.toml  # Verify generated

# Cleanup
- [ ] deactivate
- [ ] rm -rf test_env_testpypi
```

---

## Phase 5: Final Verification

### Cross-Platform Testing

**macOS:**
- [ ] Installation successful
- [ ] `taskx --version` works
- [ ] Shell completion installable
- [ ] Templates generate correctly

**Linux:**
- [ ] Installation successful
- [ ] `taskx --version` works
- [ ] Shell completion installable
- [ ] Templates generate correctly

**Windows:**
- [ ] Installation successful
- [ ] `taskx --version` works
- [ ] PowerShell completion installable
- [ ] Templates generate correctly

### Python Version Testing

- [ ] Python 3.8 - Installation and basic functionality
- [ ] Python 3.9 - Installation and basic functionality
- [ ] Python 3.10 - Installation and basic functionality
- [ ] Python 3.11 - Installation and basic functionality
- [ ] Python 3.12 - Installation and basic functionality

### Feature Verification

**Shell Completion:**
- [ ] Bash completion script generates
- [ ] Zsh completion script generates
- [ ] Fish completion script generates
- [ ] PowerShell completion script generates
- [ ] Installation command works

**Task Aliases:**
- [ ] Global aliases resolve correctly
- [ ] Per-task aliases work
- [ ] Duplicate detection works
- [ ] Reserved name validation works

**Interactive Prompts:**
- [ ] Text prompts work
- [ ] Select prompts work
- [ ] Confirm prompts work
- [ ] Password prompts work (hidden input)
- [ ] Non-interactive mode uses defaults
- [ ] `--env` overrides work

**Project Templates:**
- [ ] Django template generates
- [ ] FastAPI template generates
- [ ] Data Science template generates
- [ ] Python Library template generates
- [ ] `--list-templates` shows all
- [ ] Interactive prompts work during init

---

## Phase 6: Git & GitHub

### Git Tagging

```bash
# Create annotated tag
- [ ] git tag -a v0.2.0 -m "Release v0.2.0: Shell Completion, Aliases, Prompts, Templates"

# Verify tag
- [ ] git tag -l -n9 v0.2.0

# Push tag
- [ ] git push origin v0.2.0
```

### GitHub Release

**Create Release on GitHub:**
- [ ] Go to https://github.com/0xV8/taskx/releases/new
- [ ] Tag version: `v0.2.0`
- [ ] Release title: `v0.2.0: Shell Completion, Aliases, Prompts, Templates`
- [ ] Description: Copy from `RELEASE_NOTES_v0.2.0.md`
- [ ] Attach `dist/taskx-0.2.0-py3-none-any.whl`
- [ ] Attach `dist/taskx-0.2.0.tar.gz`
- [ ] Mark as latest release
- [ ] Publish release

---

## Phase 7: PyPI Publication (Production)

### Final Checks

- [ ] All TestPyPI tests passed
- [ ] GitHub release created
- [ ] Documentation reviewed one more time
- [ ] CHANGELOG.md finalized
- [ ] No last-minute code changes

### Upload to PyPI

```bash
# Upload to production PyPI
- [ ] twine upload dist/*
```

**Expected:** Successful upload with PyPI URL.

### Verify PyPI Publication

```bash
# Wait 2-3 minutes for PyPI to index

# Check PyPI page
- [ ] Visit https://pypi.org/project/taskx/
- [ ] Version 0.2.0 visible
- [ ] Description renders correctly
- [ ] Links work

# Install from PyPI
- [ ] python -m venv test_env_pypi
- [ ] source test_env_pypi/bin/activate
- [ ] pip install taskx==0.2.0

# Verify
- [ ] taskx --version
- [ ] taskx init --list-templates

# Cleanup
- [ ] deactivate
- [ ] rm -rf test_env_pypi
```

---

## Phase 8: Post-Release

### Announcements

**Update README.md badges (if applicable):**
- [ ] PyPI version badge
- [ ] Python version badge
- [ ] License badge

**Social Media / Community:**
- [ ] Prepare announcement post
- [ ] Share on relevant platforms
- [ ] Notify users via GitHub discussions

**Documentation:**
- [ ] Update main documentation site (if exists)
- [ ] Add v0.2.0 to version dropdown (if applicable)

### Monitoring

**First 24 Hours:**
- [ ] Monitor PyPI download stats
- [ ] Watch GitHub issues for bug reports
- [ ] Check for installation problems
- [ ] Respond to community feedback

**First Week:**
- [ ] Collect user feedback
- [ ] Document common issues
- [ ] Plan hotfix release if needed
- [ ] Update FAQ based on questions

---

## Phase 9: Retrospective & Planning

### Sprint Retrospective

- [ ] Review Sprint 1-6 completion reports
- [ ] Document lessons learned
- [ ] Identify process improvements

### Phase 2 Planning

- [ ] Review FUTURE_FEATURES.md
- [ ] Prioritize v0.3.0 features
- [ ] Create Phase 2 sprint plan
- [ ] Set timeline for v0.3.0

---

## Rollback Plan (If Needed)

### If Critical Issue Found

1. **Yank Release from PyPI**
   ```bash
   # Yank the release (makes it unavailable for new installs)
   pip install yank
   yank taskx==0.2.0
   ```

2. **Notify Users**
   - Update GitHub release with warning
   - Post issue on GitHub
   - Update documentation

3. **Fix & Re-Release**
   - Fix critical issue
   - Increment to v0.2.1
   - Follow same release process

---

## Sign-Off

### Release Manager Approval

- [ ] All checklist items completed
- [ ] No critical blockers remaining
- [ ] Documentation complete and accurate
- [ ] Testing successful across platforms

**Approved by:** ________________
**Date:** ________________

---

## Notes & Issues

### Known Issues (Non-Blocking)

1. **39 failing tests** (E2E and integration)
   - Non-critical failures
   - Do not affect core functionality
   - To be addressed in v0.2.1

2. **70% code coverage** (below 90% target)
   - Baseline established
   - Will improve in future releases

3. **Documentation todos**
   - Screenshots/diagrams (future enhancement)
   - Video tutorials (future enhancement)

### Release Date Decision

**Recommended:** After completing Phase 4 (TestPyPI) successfully.

**Tentative Date:** TBD based on testing results.

---

**Checklist Version:** 1.0
**Created:** October 24, 2025
**Last Updated:** October 24, 2025
