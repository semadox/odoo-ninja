# Odoo Ninja

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)
[![Type checked: mypy](https://img.shields.io/badge/type%20checked-mypy-blue.svg)](http://mypy-lang.org/)

A modern Python CLI tool for accessing Odoo helpdesk tickets with support for reading tickets, posting comments and notes, managing tags, and downloading attachments.

**🤖 AI-First Design**: Designed to be used with Claude Code or similar AI coding assistants to streamline helpdesk workflows through natural language commands.

**🛡️ Safety First**: Built with safety features to prevent accidentally sending messages to customers.

## Features

- 📋 List and view helpdesk tickets
- 💬 Add comments to tickets (with sudo support)
- 🏷️ Manage ticket tags
- 📎 List and download attachments
- 🎨 Rich terminal output with tables
- ⚙️ Flexible configuration via environment variables or config files
- 🔒 Type-safe with mypy strict mode
- 🚀 Modern Python tooling (uv, ruff, mypy)

## Installation

### From PyPI (recommended)

```bash
# Install via pip
pip install odoo-ninja

# Or install via pipx (recommended for CLI tools)
pipx install odoo-ninja

# Or run without installing using uvx (requires uv)
uvx odoo-ninja helpdesk list
```

### From source

This project uses [uv](https://github.com/astral-sh/uv) for dependency management.

```bash
# Clone the repository
git clone https://github.com/semadox/odoo-ninja.git
cd odoo-ninja

# Install dependencies
uv sync

# Install in development mode with dev dependencies
uv sync --all-extras

# Install the CLI tool
uv pip install -e .
```

## Configuration

Create a configuration file with your Odoo credentials. The CLI looks for configuration in these locations (in order):

1. `.odoo-ninja.env` in the current directory
2. `~/.config/odoo-ninja/config.env`
3. `.env` in the current directory

### Configuration File Format

Create a `.env` or `.odoo-ninja.env` file:

```bash
ODOO_URL=https://your-odoo-instance.com
ODOO_DATABASE=your_database
ODOO_USERNAME=your_username
ODOO_PASSWORD=your_password_or_api_key
ODOO_DEFAULT_USER_ID=123  # Optional: default user ID for sudo operations

# Safety: Allow harmful operations (default: false)
# Set to 'true' to enable posting public comments visible to customers
# Internal notes are always allowed (safe operation)
ODOO_ALLOW_HARMFUL_OPERATIONS=false
```

### Environment Variables

All configuration values can also be set via environment variables with the `ODOO_` prefix:

```bash
export ODOO_URL="https://your-odoo-instance.com"
export ODOO_DATABASE="your_database"
export ODOO_USERNAME="your_username"
export ODOO_PASSWORD="your_password"
```

## Usage

### Using with Claude Code or AI Assistants

This CLI is designed to work seamlessly with AI coding assistants like Claude Code. Instead of remembering complex command syntax, you can use natural language:

**Example workflow with Claude Code:**
```
You: "Show me all tickets assigned to me that are in progress"
Claude: [runs: odoo-ninja helpdesk list --assigned-to "Your Name" --stage "In Progress"]

You: "Add an internal note to ticket 123 saying we're waiting for customer response"
Claude: [runs: odoo-ninja helpdesk note 123 "Waiting for customer response"]

You: "Download all attachments from ticket 456"
Claude: [runs: odoo-ninja helpdesk attachments 456, then downloads each]
```

The safety features (like blocking public comments by default) are specifically designed to prevent AI assistants from accidentally exposing internal communications to customers.

### Direct CLI Usage

### List Tickets

```bash
# List all tickets (default limit: 50)
odoo-ninja helpdesk list

# Filter by stage
odoo-ninja helpdesk list --stage "In Progress"

# Filter by partner
odoo-ninja helpdesk list --partner "Acme Corp"

# Filter by assigned user
odoo-ninja helpdesk list --assigned-to "John Doe"

# Set custom limit
odoo-ninja helpdesk list --limit 100
```

### View Ticket Details

```bash
# Show detailed information for a specific ticket
odoo-ninja helpdesk show 123
```

### Add Comments and Notes

**⚠️ Safety Feature**: By default, posting public comments is **disabled** to prevent accidentally sending messages to customers. Internal notes are always allowed.

```bash
# Add an internal note (NOT visible to customers) - ALWAYS ALLOWED
odoo-ninja helpdesk note 123 "This is an internal note for the team"

# Add a note as a specific user
odoo-ninja helpdesk note 123 "Internal update" --user-id 42

# Add a public comment (visible to customers) - REQUIRES ODOO_ALLOW_HARMFUL_OPERATIONS=true
odoo-ninja helpdesk comment 123 "This is a public comment"

# Add a comment as a specific user
odoo-ninja helpdesk comment 123 "Admin comment" --user-id 42
```

To enable public comments, add to your `.env`:
```bash
ODOO_ALLOW_HARMFUL_OPERATIONS=true
```

### Manage Tags

```bash
# List all available tags
odoo-ninja helpdesk tags

# Add a tag to a ticket
odoo-ninja helpdesk tag 123 5
```

### Work with Attachments

```bash
# List attachments for a ticket
odoo-ninja helpdesk attachments 123

# Download an attachment (saves to current directory with original name)
odoo-ninja helpdesk download 456

# Download to a specific path
odoo-ninja helpdesk download 456 --output /path/to/file.pdf

# Download to a specific directory (uses original filename)
odoo-ninja helpdesk download 456 --output /path/to/directory/
```

## Development

### Code Quality

This project uses modern Python tooling:

- **ruff**: Fast linting and formatting
- **mypy**: Static type checking with strict mode
- **uv**: Fast dependency management

```bash
# Run ruff linting
uv run ruff check .

# Auto-fix ruff issues
uv run ruff check --fix .

# Format code
uv run ruff format .

# Run mypy type checking
uv run mypy src/odoo_ninja
```

### Project Structure

```
odoo-ninja/
├── src/
│   └── odoo_ninja/
│       ├── __init__.py
│       ├── main.py       # CLI entry point with Typer commands
│       ├── client.py     # Odoo XML-RPC client wrapper
│       ├── config.py     # Configuration management
│       ├── auth.py       # Authentication and sudo utilities
│       └── helpdesk.py   # Helpdesk operations and display logic
├── pyproject.toml        # Project configuration and dependencies
├── README.md
└── .gitignore
```

## How It Works

### Odoo XML-RPC API

This tool uses Odoo's external XML-RPC API to interact with the Odoo instance. The API provides:

- Authentication via username/password or API keys
- Full CRUD operations on Odoo models
- Search and filtering capabilities
- Support for sudo operations

### Sudo Operations for Comments

Comments are posted using Odoo's `message_post` method with sudo context, allowing you to post messages as a specific user. Configure `ODOO_DEFAULT_USER_ID` to set the default user for comment operations.

### Attachment Handling

Attachments are stored in Odoo's `ir.attachment` model with base64-encoded data. The CLI automatically decodes and saves files when downloading.

## Requirements

- Python 3.12+
- Access to an Odoo instance with XML-RPC enabled
- Valid Odoo credentials (username/password or API key)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup

1. Fork the repository
2. Clone your fork: `git clone https://github.com/YOUR_USERNAME/odoo-ninja.git`
3. Create a feature branch: `git checkout -b feature/my-new-feature`
4. Install development dependencies: `uv sync --all-extras`
5. Make your changes
6. Run tests and checks:
   ```bash
   uv run ruff check .
   uv run ruff format .
   uv run mypy src/odoo_ninja
   ```
7. Commit your changes: `git commit -am 'Add some feature'`
8. Push to the branch: `git push origin feature/my-new-feature`
9. Submit a pull request

### Reporting Issues

Please report issues at: https://github.com/semadox/odoo-ninja/issues

## Publishing to PyPI

This project is configured to automatically publish to PyPI using GitHub Actions with trusted publishing.

### Setup (One-time configuration)

1. **Configure PyPI Trusted Publisher**:
   - Go to https://pypi.org/manage/account/publishing/
   - Add a new pending publisher with these details:
     - PyPI Project Name: `odoo-ninja`
     - Owner: `semadox`
     - Repository name: `odoo-ninja`
     - Workflow name: `publish.yml`
     - Environment name: `pypi`

2. **Configure TestPyPI Trusted Publisher** (optional, for testing):
   - Go to https://test.pypi.org/manage/account/publishing/
   - Add the same configuration with environment name: `testpypi`

3. **Create GitHub Environments**:
   - Go to your repository settings → Environments
   - Create environment `pypi` (add protection rules if desired)
   - Create environment `testpypi` (optional)

### Releasing a new version

1. Update the version in `pyproject.toml` and `src/odoo_ninja/__init__.py`
2. Commit the version bump: `git commit -am "Bump version to X.Y.Z"`
3. Create and push a git tag: `git tag vX.Y.Z && git push origin vX.Y.Z`
4. Create a GitHub release from the tag
5. The GitHub Action will automatically build and publish to PyPI

### Manual testing with TestPyPI

To manually trigger a test publish to TestPyPI:
```bash
# From the GitHub repository, go to Actions → Publish to PyPI → Run workflow
```

### Local build and test

```bash
# Build the package locally
uv build

# Install from local build
pip install dist/odoo_ninja-*.whl

# Or test with TestPyPI
uv build
twine upload --repository testpypi dist/*
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Copyright (c) 2025 Semadox GmbH

## Acknowledgments

Built with:
- [Typer](https://typer.tiangolo.com/) - CLI framework
- [Rich](https://rich.readthedocs.io/) - Terminal formatting
- [Pydantic](https://docs.pydantic.dev/) - Data validation
- [uv](https://github.com/astral-sh/uv) - Package management
- [Ruff](https://github.com/astral-sh/ruff) - Linting and formatting
- [mypy](http://mypy-lang.org/) - Type checking
