Adds packaging (pyproject/setup.cfg), a build-and-publish workflow (builds sdist/wheel, optional PyPI/GitHub Packages publish), and a deploy-to-pi workflow (builds wheel, SCP to Raspberry Pi and installs inside a venv).

Files added:
- .github/workflows/build-and-publish.yml
- .github/workflows/deploy-to-pi.yml
- pyproject.toml
- setup.cfg
- .gitignore
- config.example.yml

Notes for reviewers:
- SMTP credentials and other secrets must be provided via GitHub Secrets (see README suggestions).
- Deploy workflow expects secrets: `PI_HOST`, `PI_USER`, `PI_SSH_KEY`, `PI_SSH_PORT`.
- The package is currently a single-module package (`py_modules = martina`). Consider refactoring into a package if desired.

Suggested tests before merge:
- Validate that `build-and-publish` builds artifacts successfully (check `dist/`).
- Validate `deploy-to-pi` in a safe environment with a test Pi (ensure SSH key + user work).
