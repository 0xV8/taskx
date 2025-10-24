# PyPI Release Strategy - taskx v0.2.0

**Date:** October 24, 2025
**Current Version:** 0.2.0
**Current Status:** ⚠️ **HOLD** - Critical bugs found during local testing
**Target Release:** v0.2.1-rc1 (after bug fixes)

---

## Executive Summary

Local testing has revealed **3 critical bugs** that must be fixed before releasing to PyPI. This document outlines the bug fixes required, testing plan, and phased release strategy to ensure a successful production release.

**Current Situation:**
- ✅ 6 out of 10 features work perfectly
- ❌ 3 critical bugs block release
- 📦 Package builds successfully
- 📚 Documentation is complete
- 🧪 Need bug fixes + retesting

**Recommendation:** Fix bugs → Retest → TestPyPI → Production PyPI

---

## Critical Bugs Requiring Fixes

### Bug #1: Interactive Prompts - Missing expand_variables Method

**Severity:** 🔴 CRITICAL (Blocking)
**Feature Affected:** Interactive Prompts with Confirmation Dialogs
**Impact:** Tasks with `confirm` parameter fail completely

**Error Message:**
```
✗ Error: Unexpected error: 'EnvironmentManager' object has no attribute 'expand_variables'
```

**Location:** `taskx/core/runner.py:154`

**Current Code:**
```python
message = self.env_manager.expand_variables(confirm, env)
```

**Fix Required:**
```python
# Add import at top of file
from taskx.utils.shell import expand_variables

# Replace line 154 with:
message = expand_variables(confirm, env)
```

**Verification Test:**
```toml
[tool.taskx.tasks.deploy]
cmd = "echo 'Deploying to ${ENV}'"
prompt.ENV = { type = "select", choices = ["dev", "prod"], default = "dev" }
confirm = "Deploy to ${ENV}?"
```

**Timeline:** 15-30 minutes

---

### Bug #2: Parallel Execution - Executes Task Names Instead of Commands

**Severity:** 🔴 CRITICAL (Blocking)
**Feature Affected:** Parallel Task Execution
**Impact:** All tasks with `parallel = [...]` fail

**Error Message:**
```
/bin/sh: lint: command not found
/bin/sh: typecheck: command not found
```

**Root Cause:** Parallel executor tries to run task names as shell commands instead of looking up task definitions and executing their `cmd` values.

**Location:** `taskx/execution/parallel.py` or `taskx/core/runner.py`

**Expected Behavior:**
```python
# For: parallel = ["lint", "typecheck", "test"]
# Should execute:
#   - echo 'Linting... No issues found ✓'
#   - echo 'Type checking... All types valid ✓'
#   - echo 'Running 100 tests... ✓ All passed!'
```

**Actual Behavior:**
```python
# Tries to execute:
#   - lint (as command)
#   - typecheck (as command)
#   - test (as command)
```

**Fix Required:**
Review parallel execution code to ensure:
1. Task names are resolved to task objects
2. Task commands (`task.cmd`) are executed, not task names
3. Environment and dependencies are handled correctly

**Verification Test:**
```toml
[tool.taskx.tasks]
lint = { cmd = "echo 'Linting ✓'", description = "Lint code" }
test = { cmd = "echo 'Testing ✓'", description = "Run tests" }
check = { parallel = ["lint", "test"], description = "Run checks" }
```

**Timeline:** 1-2 hours (requires code review and testing)

---

### Bug #3: Template Listing - --list-templates Flag Not Recognized

**Severity:** 🟡 HIGH (Important but not blocking core functionality)
**Feature Affected:** Project Template Discovery
**Impact:** Users can't discover available templates via CLI

**Error Message:**
```
Error: No such option: --list-templates

Available templates:
```

**Location:** `taskx/cli/main.py:157`

**Current Code:**
```python
@click.option("--list-templates", is_flag=True, help="List available templates and exit")
def init(ctx: click.Context, name: Optional[str], examples: bool, template: Optional[str], list_templates: bool) -> None:
```

**Issue:** Click not recognizing the flag. Possible causes:
1. Command context parsing order
2. Option decorator placement
3. Click version compatibility issue

**Workaround:** Templates still work if you know the name:
```bash
taskx init --template django
```

**Fix Required:**
1. Debug Click command parsing
2. Check option ordering and decorator placement
3. Test with different Click versions if needed
4. Consider alternative flag syntax if Click issue persists

**Verification Test:**
```bash
taskx init --list-templates
# Should display:
# Available templates:
#   WEB:
#     django               Django web application
#     fastapi              FastAPI microservice
#   ...
```

**Timeline:** 30 minutes - 1 hour

---

## Release Timeline

### Phase 1: Bug Fixes (Estimated: 2-4 hours)

**Goal:** Fix all 3 critical bugs

**Tasks:**
1. ✅ Fix Bug #1: `expand_variables` import (30 min)
   - Update import statement
   - Fix function call
   - Test locally

2. ✅ Fix Bug #2: Parallel execution (1-2 hours)
   - Review parallel execution code
   - Fix task lookup logic
   - Test with various parallel scenarios
   - Verify environment variables work
   - Test with dependencies

3. ✅ Fix Bug #3: `--list-templates` flag (30-60 min)
   - Debug Click option parsing
   - Fix flag recognition
   - Test template listing
   - Verify output formatting

4. ✅ Code quality cleanup (30 min)
   - Run linting on changes
   - Fix obvious issues
   - Update any affected tests

**Deliverable:** Fixed code ready for testing

---

### Phase 2: Local Re-Testing (Estimated: 2-3 hours)

**Goal:** Comprehensive feature verification

**Test Suite:**

#### 2.1 Core Features
- ✅ Installation from wheel
- ✅ Version display
- ✅ Help output
- ✅ Task listing

#### 2.2 Shell Completion
- ✅ Bash completion generation
- ✅ Zsh completion generation
- ✅ Fish completion generation
- ✅ PowerShell completion generation

#### 2.3 Task Aliases
- ✅ Global aliases
- ✅ Per-task aliases
- ✅ Alias resolution messages
- ✅ Mixed aliases (global + per-task)

#### 2.4 Interactive Prompts (RE-TEST AFTER FIX)
- ✅ Text prompts
- ✅ Select prompts
- ✅ Confirm prompts
- ✅ Password prompts
- ✅ Confirmation dialogs with variable expansion
- ✅ Non-interactive mode (--env overrides)

#### 2.5 Project Templates (RE-TEST AFTER FIX)
- ✅ List templates (--list-templates)
- ✅ Django template generation
- ✅ FastAPI template generation
- ✅ Data Science template generation
- ✅ Python Library template generation
- ✅ Interactive prompts during init
- ✅ Generated files verification

#### 2.6 Parallel Execution (RE-TEST AFTER FIX)
- ✅ Basic parallel execution
- ✅ Parallel with dependencies
- ✅ Environment variables in parallel tasks
- ✅ Error handling in parallel tasks
- ✅ Progress display

#### 2.7 Task Dependencies
- ✅ Single dependency
- ✅ Multiple dependencies
- ✅ Nested dependencies
- ✅ Dependency execution order

#### 2.8 Real-World Workflows
- ✅ Development workflow (dev, test, format)
- ✅ Build workflow (clean, build)
- ✅ Deployment workflow (check, build, deploy)
- ✅ Quality gate workflow (parallel checks)

**Pass Criteria:** 100% of tests pass (10/10 features)

**Deliverable:** Testing report with all tests passing

---

### Phase 3: Package Rebuild (Estimated: 30 minutes)

**Goal:** Build clean distribution packages with fixes

**Tasks:**
1. Clean previous builds
   ```bash
   rm -rf build/ dist/ *.egg-info
   rm -rf htmlcov/ .coverage .pytest_cache
   ```

2. Bump version to v0.2.1-rc1 (release candidate)
   - Update `taskx/__init__.py`
   - Update `pyproject.toml`

3. Build packages
   ```bash
   python -m build
   ```

4. Verify packages
   ```bash
   twine check dist/*
   python -m zipfile -l dist/taskx-0.2.1rc1-py3-none-any.whl
   ```

5. Test local installation
   ```bash
   python -m venv test_env
   source test_env/bin/activate
   pip install dist/taskx-0.2.1rc1-py3-none-any.whl
   taskx --version  # Should show 0.2.1rc1
   ```

**Deliverable:** Verified wheel and source distributions

---

### Phase 4: TestPyPI Upload (Estimated: 1-2 hours)

**Goal:** Stage release for community testing

**Prerequisites:**
- ✅ All bugs fixed
- ✅ All local tests passing
- ✅ Packages rebuilt and verified
- ✅ TestPyPI account credentials configured

**Tasks:**

#### 4.1 Configure TestPyPI
```bash
# Ensure ~/.pypirc has testpypi configuration
cat >> ~/.pypirc << 'EOF'
[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = <your-testpypi-token>
EOF
```

#### 4.2 Upload to TestPyPI
```bash
twine upload --repository testpypi dist/*
```

**Expected Output:**
```
Uploading distributions to https://test.pypi.org/legacy/
Uploading taskx-0.2.1rc1-py3-none-any.whl
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 65.0/65.0 kB • 00:00 • ?
Uploading taskx-0.2.1rc1.tar.gz
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 95.0/95.0 kB • 00:00 • ?

View at:
https://test.pypi.org/project/taskx/0.2.1rc1/
```

#### 4.3 Test Installation from TestPyPI
```bash
# Create fresh test environment
python -m venv test_testpypi
source test_testpypi/bin/activate

# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ \
    --extra-index-url https://pypi.org/simple/ \
    taskx==0.2.1rc1

# Verify installation
taskx --version
```

#### 4.4 Run Full Feature Test Suite
Run the complete test suite from Phase 2 again, but this time using the package installed from TestPyPI.

**Pass Criteria:**
- Package installs without errors
- All 10 features work correctly
- No new bugs discovered

#### 4.5 Community Testing (Optional)
- Share TestPyPI link with beta testers
- Monitor for issues
- Gather feedback
- Fix any issues found

**Duration:** 1-3 days for community feedback

**Deliverable:** Verified working package on TestPyPI

---

### Phase 5: Final Verification (Estimated: 1 hour)

**Goal:** Final checks before production release

**Tasks:**

#### 5.1 Documentation Review
- ✅ README.md reflects actual behavior
- ✅ CHANGELOG.md complete
- ✅ RELEASE_NOTES_v0.2.0.md accurate
- ✅ All feature guides tested and accurate
- ✅ Migration guide correct
- ✅ All links work

#### 5.2 Git & GitHub
- ✅ All changes committed
- ✅ Git tag created (v0.2.1-rc1 or v0.2.1)
- ✅ Tag pushed to GitHub
- ✅ Branch is clean

#### 5.3 Final Testing
- ✅ One more complete test suite run
- ✅ Cross-platform verification (if possible)
- ✅ Python version compatibility check (3.8-3.12)

**Deliverable:** Ready for production release

---

### Phase 6: Production PyPI Upload (Estimated: 30 minutes)

**Goal:** Release to production PyPI

**Prerequisites:**
- ✅ TestPyPI testing successful
- ✅ No issues reported
- ✅ All documentation accurate
- ✅ Final verification complete
- ✅ PyPI account credentials configured

**Tasks:**

#### 6.1 Rebuild for Production (if using RC)
If released as 0.2.1-rc1 on TestPyPI, rebuild as 0.2.1 for production:
```bash
# Update version to 0.2.1 (no rc suffix)
# Update in taskx/__init__.py and pyproject.toml

# Clean and rebuild
rm -rf build/ dist/ *.egg-info
python -m build

# Verify
twine check dist/*
```

#### 6.2 Upload to Production PyPI
```bash
twine upload dist/*
```

**Expected Output:**
```
Uploading distributions to https://upload.pypi.org/legacy/
Uploading taskx-0.2.1-py3-none-any.whl
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 65.0/65.0 kB • 00:00 • ?
Uploading taskx-0.2.1.tar.gz
100% ━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 95.0/95.0 kB • 00:00 • ?

View at:
https://pypi.org/project/taskx/0.2.1/
```

#### 6.3 Verify PyPI Publication
```bash
# Wait 2-3 minutes for PyPI to index

# Visit PyPI page
open https://pypi.org/project/taskx/

# Verify:
# - Version 0.2.1 visible
# - Description renders correctly
# - Links work
# - Files available for download
```

#### 6.4 Test Installation from PyPI
```bash
# Create fresh environment
python -m venv test_prod_pypi
source test_prod_pypi/bin/activate

# Install from production PyPI
pip install taskx==0.2.1

# Verify
taskx --version
taskx init --list-templates
```

**Deliverable:** Package live on PyPI!

---

### Phase 7: GitHub Release (Estimated: 30 minutes)

**Goal:** Create official GitHub release

**Tasks:**

#### 7.1 Create GitHub Release
Option A: Using GitHub CLI
```bash
gh release create v0.2.1 \
    --title "v0.2.1: Shell Completion, Aliases, Prompts, Templates" \
    --notes-file RELEASE_NOTES_v0.2.0.md \
    dist/taskx-0.2.1-py3-none-any.whl \
    dist/taskx-0.2.1.tar.gz
```

Option B: Using GitHub Web Interface
1. Go to https://github.com/0xV8/taskx/releases/new
2. Tag version: `v0.2.1`
3. Release title: `v0.2.1: Shell Completion, Aliases, Prompts, Templates`
4. Description: Copy from `RELEASE_NOTES_v0.2.0.md`
5. Attach distribution files
6. Mark as latest release
7. Publish release

#### 7.2 Verify Release
- ✅ Release appears on GitHub
- ✅ Files are downloadable
- ✅ Release notes display correctly
- ✅ Links work

**Deliverable:** Official GitHub release published

---

### Phase 8: Post-Release (Estimated: Ongoing)

**Goal:** Monitor and support the release

**Tasks:**

#### 8.1 First 24 Hours
- 🔍 Monitor PyPI download stats
- 🐛 Watch GitHub issues for bug reports
- 💬 Check for installation problems
- 📣 Respond to community feedback

#### 8.2 First Week
- 📊 Collect user feedback
- 📝 Document common issues
- 🔧 Plan hotfix if needed (v0.2.2)
- ❓ Update FAQ based on questions

#### 8.3 Ongoing
- 📈 Track adoption metrics
- 🎯 Prioritize v0.3.0 features
- 🤝 Engage with community
- 📚 Improve documentation based on feedback

**Deliverable:** Supported release with engaged community

---

## Version Numbering Strategy

### Current Situation
- **v0.2.0** - Built and tested locally, critical bugs found

### Recommended Versions
1. **v0.2.1-rc1** - First release candidate with bug fixes (TestPyPI only)
2. **v0.2.1** - Stable release after TestPyPI validation (Production PyPI)

### Alternative: v0.2.0 Direct Release
If bugs are fixed quickly and testing is thorough:
- Fix bugs
- Keep version 0.2.0
- Release directly to PyPI (skip RC)

**Recommendation:** Use v0.2.1 to indicate bug fixes from original 0.2.0 plan

---

## Risk Assessment & Mitigation

### Risk 1: More Bugs Discovered During Re-Testing

**Probability:** MEDIUM
**Impact:** HIGH (delays release)

**Mitigation:**
- Comprehensive test suite in Phase 2
- Multiple testing rounds
- TestPyPI staging before production

**Contingency:**
- Document all bugs found
- Prioritize by severity
- Fix critical bugs first
- Consider v0.2.2 for minor issues

---

### Risk 2: TestPyPI Upload Issues

**Probability:** LOW
**Impact:** MEDIUM (delays release)

**Mitigation:**
- Verify TestPyPI credentials before starting
- Test `twine` configuration
- Have PyPI API tokens ready

**Contingency:**
- Debug twine/PyPI connection
- Check package metadata
- Verify account permissions

---

### Risk 3: Community Reports Issues After Release

**Probability:** MEDIUM-HIGH
**Impact:** MEDIUM (reputation damage)

**Mitigation:**
- Thorough local testing
- TestPyPI validation
- Clear documentation
- Active monitoring

**Contingency:**
- Quick response to issues
- Hotfix release plan ready
- Clear communication with users
- Yank release if critical bug found

---

### Risk 4: Breaking Changes Discovered

**Probability:** LOW
**Impact:** CRITICAL (breaks backward compatibility claim)

**Mitigation:**
- Test with v0.1.0 configurations
- Verify migration guide accuracy
- Test upgrade scenarios

**Contingency:**
- Update documentation immediately
- Communicate breaking changes
- Provide migration tools
- Consider reverting if too severe

---

## Success Criteria

### Release is Successful If:
1. ✅ All 3 critical bugs fixed
2. ✅ 100% of features work correctly (10/10)
3. ✅ Package installs cleanly from PyPI
4. ✅ Documentation matches actual behavior
5. ✅ No critical bugs reported in first 48 hours
6. ✅ Positive community feedback
7. ✅ Download numbers increasing
8. ✅ GitHub issues are manageable

### Release Needs Hotfix If:
- ❌ Critical bug reported in first 48 hours
- ❌ Installation failures
- ❌ Breaking changes discovered
- ❌ Major feature completely broken
- ❌ Security vulnerability found

---

## Communication Plan

### Pre-Release Announcements
- Update README.md with "v0.2.1 coming soon"
- Post on GitHub Discussions (if enabled)
- Notify early adopters

### Release Day
- Publish GitHub release
- Update PyPI project description
- Share on social media (if applicable)
- Update documentation site

### Post-Release
- Thank contributors
- Share success metrics
- Announce future plans (v0.3.0)
- Engage with community feedback

---

## Rollback Plan

### If Critical Issues Found:

#### Option 1: Yank Release (Minor Issues)
```bash
# Yank the release from PyPI
pip install yank
yank taskx==0.2.1 --reason "Critical bug found, fix coming in 0.2.2"
```

**Impact:** Existing installations keep working, new installations prevented

#### Option 2: Hotfix Release (Fixable Issues)
1. Fix critical bug immediately
2. Version as v0.2.2
3. Release within 24 hours
4. Communicate clearly with users

#### Option 3: Full Rollback (Severe Issues)
1. Yank v0.2.1 from PyPI
2. Recommend users downgrade to v0.1.0
3. Fix issues thoroughly
4. Re-release as v0.3.0 with all fixes

---

## Budget & Resource Allocation

### Time Investment

| Phase | Estimated Time | Priority |
|-------|----------------|----------|
| Bug Fixes | 2-4 hours | HIGH |
| Local Re-Testing | 2-3 hours | HIGH |
| Package Rebuild | 30 minutes | MEDIUM |
| TestPyPI Upload | 1-2 hours | MEDIUM |
| Final Verification | 1 hour | HIGH |
| Production Upload | 30 minutes | HIGH |
| GitHub Release | 30 minutes | MEDIUM |
| Post-Release Monitoring | Ongoing | HIGH |
| **TOTAL** | **8-12 hours** | |

### Critical Path
1. Bug Fixes (blocking)
2. Local Re-Testing (blocking)
3. TestPyPI (optional but recommended)
4. Production PyPI (goal)

**Minimum Time to Release:** 4-6 hours (if skipping TestPyPI)
**Recommended Time:** 8-12 hours (including TestPyPI)

---

## Decision Points

### Decision 1: Version Number
**Options:**
- A) Release as v0.2.0 (original plan)
- B) Release as v0.2.1 (indicates bug fixes)
- C) Release as v0.2.1-rc1 (release candidate)

**Recommendation:** B (v0.2.1) - Clear that bugs were fixed

---

### Decision 2: TestPyPI
**Options:**
- A) Skip TestPyPI, go direct to production
- B) Use TestPyPI for staging

**Recommendation:** B (Use TestPyPI) - Lower risk, catches issues early

---

### Decision 3: Release Timing
**Options:**
- A) Fix bugs and release ASAP
- B) Take time for thorough testing
- C) Wait for community feedback on TestPyPI

**Recommendation:** B (Thorough testing) - Quality over speed

---

## Next Immediate Actions

### Right Now:
1. 🔧 **Start Bug Fixes** - Begin fixing the 3 critical bugs
2. 📝 **Create Bug Fix Branch** - `git checkout -b bugfix/v0.2.1`
3. 🧪 **Set Up Test Environment** - Prepare for re-testing

### After Bug Fixes:
1. 🧪 **Local Re-Testing** - Run complete test suite
2. 📦 **Rebuild Packages** - Create new distributions
3. 🚀 **TestPyPI Upload** - Stage for testing

### Before Production:
1. ✅ **Final Verification** - Triple-check everything
2. 📄 **Update Documentation** - Ensure accuracy
3. 🎯 **Go/No-Go Decision** - Final approval

---

## Conclusion

taskx v0.2.0 is **95% ready for release** but has **3 critical bugs** that must be fixed first. With focused bug fixing and thorough testing, we can have a stable v0.2.1 release ready for PyPI within **8-12 hours** of work.

**Recommended Path:**
1. Fix bugs (v0.2.1)
2. Test locally (2-3 hours)
3. Upload to TestPyPI (validate)
4. Release to Production PyPI
5. Monitor and support

**Confidence Level:** HIGH - Bugs are well-understood and fixable

**Release Quality Target:** 100% feature functionality, zero critical bugs

---

**Strategy Prepared By:** Claude Code
**Date:** October 24, 2025
**Status:** ⚠️ AWAITING BUG FIXES
**Next Step:** Begin fixing 3 critical bugs

---

## Quick Reference: Commands

```bash
# Fix bugs in code
git checkout -b bugfix/v0.2.1

# After fixes, test locally
python -m venv test_local
source test_local/bin/activate
pip install dist/taskx-0.2.1-py3-none-any.whl
# Run full test suite...

# Upload to TestPyPI
twine upload --repository testpypi dist/*

# Test from TestPyPI
pip install --index-url https://test.pypi.org/simple/ \
    --extra-index-url https://pypi.org/simple/ taskx==0.2.1

# Upload to Production
twine upload dist/*

# Create GitHub release
gh release create v0.2.1 \
    --title "v0.2.1: Bug Fixes + Features" \
    --notes-file RELEASE_NOTES_v0.2.0.md \
    dist/*
```

---

**End of PyPI Release Strategy**
