# taskx Examples

This directory contains example projects demonstrating various use cases for taskx.

## Examples

### 1. Simple Python Project (`simple-python/`)

Demonstrates basic taskx usage for a Python library or CLI tool.

**Features:**
- Code formatting with black
- Linting with ruff
- Type checking with mypy
- Testing with pytest
- Parallel quality checks
- Watch mode for TDD

**Try it:**
```bash
cd simple-python
taskx list           # See all available tasks
taskx check          # Run all checks in parallel
taskx dev            # Watch and run tests on file changes
taskx graph          # Visualize task dependencies
```

### 2. Flask Web Application (`flask-app/`)

Demonstrates taskx for web development workflows.

**Features:**
- Development server with auto-reload
- Database migration management
- Docker build and deployment
- Environment-based deployment targets
- Security scanning
- Parallel build checks

**Try it:**
```bash
cd flask-app
taskx dev                    # Start development server with watch mode
taskx db-init && taskx db-migrate  # Database setup
taskx docker-run            # Run in container
taskx deploy-staging        # Deploy to staging (after build checks)
```

### 3. Data Science Project (`data-science/`)

Demonstrates taskx for ML/data science workflows.

**Features:**
- Complete ML pipeline with dependencies
- Parallel hyperparameter tuning
- GPU training support
- Jupyter notebook integration
- MLflow tracking
- Data validation

**Try it:**
```bash
cd data-science
taskx pipeline              # Run complete ML pipeline (download → train → evaluate)
taskx tune                  # Run parallel hyperparameter tuning
taskx notebook              # Start Jupyter Lab
taskx graph --format mermaid > pipeline.mmd  # Export pipeline diagram
```

## Common Patterns

### Parallel Execution

Run multiple commands concurrently:

```toml
[tool.taskx.tasks]
check = {
    parallel = ["ruff check .", "mypy .", "pytest -q"],
    description = "Run all checks in parallel"
}
```

### Watch Mode

Auto-restart tasks on file changes:

```toml
[tool.taskx.tasks]
dev = {
    cmd = "python app.py",
    watch = ["*.py", "templates/**/*"],
    description = "Dev server with auto-reload"
}
```

### Task Dependencies

Chain tasks with automatic ordering:

```toml
[tool.taskx.tasks]
test = { cmd = "pytest tests/" }
build = { cmd = "python -m build" }
deploy = {
    depends = ["test", "build"],  # Runs test → build → deploy
    cmd = "sh scripts/deploy.sh"
}
```

### Environment Variables

Use environment variables for configuration:

```toml
[tool.taskx.env]
APP_NAME = "myapp"
PORT = "8000"

[tool.taskx.tasks]
dev = { cmd = "uvicorn ${APP_NAME}:app --port ${PORT} --reload" }
```

## Learning Path

1. **Start with** `simple-python` to learn basic taskx concepts
2. **Move to** `flask-app` to see how taskx handles web development
3. **Explore** `data-science` for complex dependency pipelines

## Tips

- Use `taskx graph` to visualize dependencies
- Use `taskx watch <task>` for rapid development
- Set `parallel` for independent tasks to speed up workflows
- Use environment variables for configuration
- Add descriptions to make `taskx list` more helpful

## Creating Your Own

To use taskx in your project:

```bash
# Initialize configuration
taskx init

# Edit pyproject.toml to add your tasks
# Then run with:
taskx <task-name>
```

See the [main README](../README.md) for full documentation.
