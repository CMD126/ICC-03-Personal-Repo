# Contributing

Contributions that improve educational value, fix bugs, or add useful cybersecurity content are welcome.

---

## How to Contribute

1. **Fork** the repository
2. **Create a branch:** `git checkout -b feature/your-feature-name`
3. **Make your changes** following the guidelines below
4. **Commit** with a clear message
5. **Open a Pull Request**

---

## What is Welcome

| Type | Notes |
|------|-------|
| Bug fixes | Broken scripts, bad links, incorrect commands |
| New exercises | Must be in the correct module folder with a `README.md` |
| New cheat sheet notes | Accurate, well-formatted Markdown |
| New scripts | Must include a `README.md` with usage instructions |
| Spelling/grammar | Always appreciated |
| Security improvements | Safer practices in existing code |

---

## Folder Structure

New exercises go inside the relevant module:

```
<Topic Name>/
└── exercises/
    └── exercise-name/
        ├── README.md       ← required
        └── script.py / script.sh
```

New scripts go under `/Scripts`:

```
Scripts/
└── tool-name/
    ├── README.md           ← required
    ├── tool_name.py / .sh
    └── requirements.txt    ← if external packages are used
```

---

## Code Style

- **Python:** snake_case filenames, docstring at top, `try/except` at I/O boundaries
- **Bash:** `#!/usr/bin/env bash`, quote all variables, use `[[ ]]` for conditionals
- **Markdown:** `##` sections, `---` dividers, tables for structured info

---

→ [View full CONTRIBUTING.md](../CONTRIBUTING.md) | [← Home](Home)
