# Contributing

Thank you for your interest in contributing to this repository! Contributions that improve the educational value, fix bugs, or add useful cybersecurity exercises are welcome.

---

## Getting Started

1. **Fork** the repository
2. **Clone** your fork locally:
   ```bash
   git clone https://github.com/your-username/ICC-03-Personal-Repo.git
   ```
3. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Make your changes**, following the guidelines below
5. **Commit** with a clear message
6. **Push** to your fork and open a **Pull Request**

---

## What to Contribute

| Type | Welcome? | Notes |
|------|----------|-------|
| Bug fixes | Yes | Fix broken scripts, incorrect commands, or bad links |
| New exercises | Yes | Must follow the module structure and include a README |
| New cheat sheet notes | Yes | Must be accurate and well-formatted |
| New scripts/tools | Yes | Must include a README with usage instructions |
| Spelling/grammar fixes | Yes | Always appreciated |
| Security improvements | Yes | Safer practices in existing code |
| Malicious code | No | Any harmful or unethical content will be rejected |

---

## Code Style

### Python
- Use **snake_case** for file and variable names
- Add a module docstring at the top of every script explaining its purpose
- Use `try/except` for error handling at I/O boundaries
- No hardcoded credentials or sensitive data

### Bash
- Use `#!/bin/bash` shebang
- Quote all variables: `"$variable"`
- Use `[[ ]]` for conditionals in Bash (not `[ ]`)

### Markdown
- Use `##` sections with `---` dividers between them
- Use tables for structured information
- Add a blank line between headings and content

---

## Repository Structure

New content should follow the existing structure. Folder names are lowercase, use hyphens instead of spaces, and modules are numbered in the order the course covers them.

```
NN-module-name/
├── notes/
│   └── topic/README.md        ← cheat sheet
└── exercises/
    └── exercise-name/
        ├── README.md          ← required
        └── script.py / script.sh

tools/
└── tool-name/
    ├── README.md              ← required
    ├── tool_name.py / .sh
    └── requirements.txt       ← if external packages are used
```

Modules:
- `00-foundations/`
- `01-networking-and-sysadmin/`
- `02-grc/`
- `03-data-security/`
- `04-security-operations/`
- `05-cloud-security/`
- `06-threat-hunting/`
- `07-appsec/`
- `08-penetration-testing/`

---

## Running the checks locally

CI runs the same three checks on every pull request. To run them before you push:

```bash
pip install ruff pytest
ruff check .
pytest -q
shellcheck -S error tools/*/*.sh
```

If you add a Python exercise with logic that can be tested without a network or a GUI, add a test for it in `tests/`.

---

## Pull Request Checklist

Before submitting a PR, make sure:

- [ ] Your code runs without errors
- [ ] `ruff check .` and `pytest -q` pass
- [ ] A `README.md` is included for any new exercise or script
- [ ] No sensitive data (credentials, keys, personal info) is included
- [ ] Links in README files are correct and relative
- [ ] Commit messages are clear and descriptive

---

## Code of Conduct

All contributors are expected to follow the [Code of Conduct](./CODE_OF_CONDUCT.md).
