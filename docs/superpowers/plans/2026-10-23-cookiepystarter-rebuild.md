# CookiePyStarter Rebuild Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking. (superpowers:subagent-driven-development is unavailable in this session — `task` of type `general` is permission-denied.)

**Goal:** Rebuild CookiePyStarter into the definitive modern-Python cookiecutter template: green-on-first-render projects, Apache-2.0, SEO-optimized metadata/docs.

**Architecture:** Single smart cookiecutter template (`{{ cookiecutter.package_name }}/`) with 10 prompts, Jinja conditionals for docker/docs optionals, and two Python hooks (`pre_gen_project.py` validates; `post_gen_project.py` finalizes files + runs uv/pre-commit/git/checks). The template repo gains its own ruff/mypy/pytest tooling plus a render-test CI matrix that renders permutations on ubuntu+windows and verifies the generated output.

**Tech Stack:** cookiecutter ≥2.2 (verify 2.7.1), Jinja2, uv, hatchling, ruff, mypy, pytest, pre-commit, GitHub Actions, mkdocs-material (optional), Docker (optional).

**Spec:** `docs/superpowers/specs/2026-10-23-cookiepystarter-rebuild-design.md`

## Global Constraints
- Brand stays "CookiePyStarter"; repo `mramitdas/CookiePyStarter`.
- Exactly 10 prompts in `cookiecutter.json`; `package_name` is the generated directory name.
- Generated projects: Python `>={{python_version}}` (3.10–3.14 choices), src layout, hatchling, ruff lint+format, mypy, pytest+pytest-cov, pre-commit.
- Template repo dev: Python 3.12+, ruff+mypy+pytest over `hooks/` and `tests/`.
- Hooks are pure Python, Windows-safe (pathlib, no bash); hook failure ⇒ non-zero exit ⇒ cookiecutter deletes output (fail loudly, per design).
- License choices: MIT (default) / Apache-2.0 / BSD-3-Clause / None→CC0-1.0; template repo itself Apache-2.0.
- Workflow process (AGENTS.md): every task = GitHub issue → branch `<type>/<issue#>-<slug>` → PR to default branch → merge with `gh pr merge --merge --delete-branch` after gates (ruff check, ruff format --check, mypy, pytest, no secrets, docs updated). Conventional commits, subject ≤50 chars, body `refs #N`.
- Standing approvals: `STANDING_APPROVALS.md` (autonomous branches/commits/PRs/merge, gh on this repo, uv/pip installs). NOT authorized: force-push, releases/publishing, secrets, disabling gates, other repos (ecosystem PRs deferred to user).

## Review Focus
1. **Jinja vs GitHub Actions `${{ }}` / Dockerfile `${VAR}` collisions** — cookiecutter would eat `${{ matrix.os }}` in generated workflows. Test: render-test asserts generated `ci.yml` contains `${{ runner.os }}` literally (Task 6 step, Task 7 matrix).
2. **Hook failure deletes generated dir** — missing uv/git must produce a clear message, not a traceback; render-test runners must have both. Test: unit tests on the friendly-error path (Task 5), CI installs uv (Task 7).
3. **Windows safety** — hooks and paths must work on windows-latest. Test: render-test matrix runs windows-latest (Task 7).
4. **License/pyproject consistency** — LICENSE text, pyproject `license` field/classifier must agree for all 4 choices. Test: unit test over the license-map + render-test `license=Apache-2.0` (Task 5, Task 7).
5. **Invalid `package_name` from user** (e.g. "My Class", "class") → pre_gen must fail with a clear ERROR line. Test: unit tests incl. keyword rejection (Task 3).

---

### Task 0: Governance files (AGENTS.md, STANDING_APPROVALS.md, spec, plan)

**Files:**
- Create: `AGENTS.md`, `STANDING_APPROVALS.md`, `docs/superpowers/specs/2026-10-23-cookiepystarter-rebuild-design.md`, `docs/superpowers/plans/2026-10-23-cookiepystarter-rebuild.md`

**Interfaces:**
- Produces: repo-wide agent rules; `STANDING_APPROVALS.md` is referenced by AGENTS.md guardrails; branch layout documents `main` as default (cutover happens in Task 10).

- [ ] Step 1: Create issue `chore: land agent governance files` via `gh issue create`.
- [ ] Step 2: Branch `chore/0-governance-files`; write the four files (content: AGENTS.md = user-provided draft with Technical Stack/Commands/Architecture sections as approved 2026-10-23, with `pre_prompt.py` line corrected to `pre_gen_project.py` validation; STANDING_APPROVALS.md = user draft adapted: repo rule → `mramitdas/CookiePyStarter`, gates → ruff/mypy/pytest, drop alembic/uvicorn/bot commands, keep NOT-list verbatim).
- [ ] Step 3: Commit `chore: add agent governance docs refs #0`; push; PR to `prod`; merge with `--merge --delete-branch`.

### Task 1: Repo tooling scaffold

**Files:**
- Create: `pyproject.toml`, `.gitignore`, `.pre-commit-config.yaml`, `tests/__init__.py`, `tests/conftest.py`, `.github/workflows/ci.yml`
- Modify: none

**Interfaces:**
- Produces: `pyproject.toml` dev group (ruff, mypy, pytest, cookiecutter); `tests/conftest.py` helper `load_hook(name: str)` importing `hooks/<name>.py` via importlib for Tasks 3/5.

- [ ] Step 1: Issue + branch `chore/1-repo-tooling`.
- [ ] Step 2: `pyproject.toml`: `[project] name="cookiepystarter-dev" version="0.0.0" requires-python=">=3.12"`, `[dependency-groups] dev = ["cookiecutter>=2.2", "ruff", "mypy", "pytest"]`; `[tool.ruff] target-version="py312" line-length=88`, lint select `["E","F","I","UP","B"]`; `[tool.mypy] strict=true`; `[tool.pytest.ini_options] testpaths=["tests"]`.
- [ ] Step 3: `.gitignore` (python/venv/uv-cache), `.pre-commit-config.yaml` (ruff/ruff-format repos + local mypy hook), `tests/conftest.py` with `load_hook`.
- [ ] Step 4: `.github/workflows/ci.yml`: push/PR → setup-python 3.12, `astral-sh/setup-uv`, `uv sync`, `uv run ruff check hooks/ tests/`, `uv run ruff format --check hooks/ tests/`, `uv run mypy hooks/ tests/`, `uv run pytest`.
- [ ] Step 5: Run gates locally (`uv sync && uv run ruff check hooks/ tests/ && uv run pytest`) — pass (vacuous); commit `chore: add repo dev tooling refs #1`; PR; merge.

### Task 2: cookiecutter.json + template restructure + legacy deletion

**Files:**
- Modify: `cookiecutter.json`
- Rename: `{{ cookiecutter.project_slug }}/` → `{{ cookiecutter.package_name }}/`
- Delete: `{{ cookiecutter.package_name }}/setup.sh`, `requirements/`, `.env`, `src/main.py`, `src/tests/__init__.py`, `docs/installation.rst`, old `.github/` tree inside template, old root `.github/workflows/linting.yml`
- Keep: root `.github/` community files, `media/logo.png`, `LICENSE` (relicensed in this task)

**Interfaces:**
- Produces: 10-prompt `cookiecutter.json` (keys exactly: project_name, package_name, project_description, author, email, github_username, license, python_version, docker, docs); `package_name` default `"{{ cookiecutter.project_name.lower().replace(' ', '_').replace('-', '_') }}"`; `license` choice list `["MIT", "Apache-2.0", "BSD-3-Clause", "None"]`; `python_version` choice list `["3.12", "3.10", "3.11", "3.13", "3.14"]`; docker/docs `["no", "yes"]`.

- [ ] Step 1: Issue + branch `feat/2-template-restructure`.
- [ ] Step 2: Rewrite `cookiecutter.json` to the exact 10-key spec above; rename template dir; delete legacy files listed.
- [ ] Step 3: Replace root `LICENSE` with Apache-2.0 text; verify `uvx cookiecutter . --no-input -o /tmp/r2` renders (dir named from default package_name).
- [ ] Step 4: Commit `feat: restructure template core refs #2`; PR; merge.

### Task 3: pre_gen_project.py validation (TDD)

**Files:**
- Create: `hooks/pre_gen_project.py`, `tests/test_pre_gen.py`

**Interfaces:**
- Produces: `validate_package_name(name: str) -> str` — raises `SystemExit` with message `ERROR: <name> is not a valid Python package name (snake_case identifier, not a keyword).` when `re.fullmatch(r"[_a-zA-Z][_a-zA-Z0-9]*", name)` fails or `keyword.iskeyword(name)`; returns `name` otherwise. Script entry: reads Jinja-rendered `package_name`, calls validator, `sys.exit` accordingly.

- [ ] Step 1: Write failing tests: valid `my_pkg`, `pkg2`; invalid `My Class`, `2pkg`, `class`, empty.
- [ ] Step 2: Run `uv run pytest tests/test_pre_gen.py -v` → FAIL (module missing).
- [ ] Step 3: Implement `hooks/pre_gen_project.py` per signature (module-level `PACKAGE_NAME = "{{ cookiecutter.package_name }}"`, `if __name__ == "__main__"` guard so tests import safely).
- [ ] Step 4: Tests pass; gates green; commit `feat: validate package_name pre-gen refs #3`; PR; merge.

### Task 4: Generated project skeleton

**Files:**
- Create under `{{ cookiecutter.package_name }}/`:
  `pyproject.toml`, `.gitignore`, `README.md`, `CHANGELOG.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, `SECURITY.md`, `.pre-commit-config.yaml`,
  `src/{{ cookiecutter.package_name }}/__init__.py`, `src/{{ cookiecutter.package_name }}/core.py`, `tests/test_core.py`

**Interfaces:**
- Produces: `core.add(a: int, b: int) -> int`; `__init__.py` sets `__version__ = "0.1.0"` and re-exports `add`. `pyproject.toml`: hatchling backend, `[project] name=package_name version=0.1.0 requires-python=">={{ cookiecutter.python_version }}"`, PEP 639 `license` via Jinja conditional (MIT/Apache-2.0/BSD-3-Clause text field), classifiers, `[project.optional-dependencies] docs` when docs=yes; `[tool.ruff]`, `[tool.mypy] strict`, `[tool.pytest.ini_options] testpaths=["tests"] addopts with `--cov=src` only in CI… keep `addopts = ["--cov={{ cookiecutter.package_name }}"]` simple. Generated `.pre-commit-config.yaml`: ruff, ruff-format, mypy revs pinned at implementation time (verify via GitHub API).
- All GitHub-workflow/`{% raw %}` concerns deferred to Tasks 6/7.

- [ ] Step 1: Issue + branch `feat/4-project-skeleton`.
- [ ] Step 2: Write files per spec; `add()` body one line; tests: `test_add_positive`, `test_add_zero`.
- [ ] Step 3: Render `uvx cookiecutter . --no-input -o /tmp/r4`; cd output; `uv sync`; `uv run ruff check .`; `uv run mypy src/`; `uv run pytest` → all pass. (post_gen hook not yet present — render succeeds without setup steps.)
- [ ] Step 4: Commit `feat: add generated project skeleton refs #4`; PR; merge.

### Task 5: License templates + post_gen_project.py (TDD)

**Files:**
- Create: `{{ cookiecutter.package_name }}/.license_templates/MIT.txt`, `APACHE.txt`, `BSD3.txt`, `CC0.txt`; `hooks/post_gen_project.py`; `tests/test_post_gen.py`

**Interfaces:**
- Consumes: `package_name`, `author`, `email`, `license`, `docker`, `docs` from Task 2.
- Produces (importable, unit-tested):
  - `LICENSE_MAP: dict[str, str]` = {"MIT": "MIT.txt", "Apache-2.0": "APACHE.txt", "BSD-3-Clause": "BSD3.txt", "None": "CC0.txt"}
  - `write_license(license_choice: str, author: str, year: str, cwd: Path) -> None` — reads `.license_templates/<mapped>`, substitutes `__YEAR__`, writes `LICENSE`, then removes `.license_templates/`.
  - `remove_optional_paths(paths: list[str], cwd: Path) -> None` — delete files/dirs if exist (docker/docs conditionals).
  - `run_setup() -> None` — subprocess `uv sync`; `uv run pre-commit install`; `git init`; `git add -A`; `git -c user.name=... -c user.email=... commit -m "Initial commit from CookiePyStarter"`; then `uv run ruff check .`, `uv run ruff format --check .`, `uv run mypy src/`, `uv run pytest`; friendly `ERROR: uv is required...` + SystemExit(1) if uv/git missing (`FileNotFoundError` catch).
  - Script entry: renders `author`, `license`, `docker`, `docs`, `email` via Jinja; calls the above; docker!="yes" → remove `Dockerfile`, `.dockerignore`; docs!="yes" → remove `mkdocs.yml`, `docs`.
- Review Focus 4: unit test asserts LICENSE_MAP covers exactly 4 keys; `write_license("None", ...)` writes CC0 text containing "CC0".

- [ ] Step 1: Failing tests (license map, write_license for all 4 choices with tmp_path + `__YEAR__` substitution + `.license_templates` removal, remove_optional_paths on files+dirs).
- [ ] Step 2: Run → FAIL.
- [ ] Step 3: License texts (full MIT/Apache-2.0/BSD-3-Clause/CC0, `__YEAR__` + `{{ cookiecutter.author }}` placeholders); implement hook functions + script entry.
- [ ] Step 4: Tests pass; gates green; commit `feat: post-gen hook + licenses refs #5`; PR; merge.

### Task 6: Generated CI workflow + docker/docs optionals

**Files:**
- Create: `{{ cookiecutter.package_name }}/.github/workflows/ci.yml`, `{{ cookiecutter.package_name }}/Dockerfile`, `{{ cookiecutter.package_name }}/.dockerignore`, `{{ cookiecutter.package_name }}/mkdocs.yml`, `{{ cookiecutter.package_name }}/docs/index.md`

**Interfaces:**
- Consumes: Task 4 pyproject (optional-dependencies docs group), Task 5 removal list (exact paths above).
- Produces: `ci.yml` — name CI; on push/PR; job test: runs-on ubuntu-latest, python `{{ cookiecutter.python_version }}`, `astral-sh/setup-uv`, `uv sync`, ruff check/format, mypy, pytest. **Wrap every `${{ ... }}` in `{% raw %}…{% endraw %}` or use cookiecutter's Jinja with variable names that don't collide** — `{{ cookiecutter.python_version }}` is intended render; GH expressions must survive (Review Focus 1). Dockerfile: multi-stage `python:{{ cookiecutter.python_version }}-slim`, uv-based install, `CMD ["python", "-m", "src..."]` — use `CMD ["python", "-c", "from {{ cookiecutter.package_name }} import print(add(1,2)); print(add(1,2))"]`… simpler: `CMD ["python", "-c", "from {{ cookiecutter.package_name }}.core import add; print(add(1, 2))"]`. mkdocs.yml: `site_name: {{ cookiecutter.project_name }}`, theme material, nav index.

- [ ] Step 1: Issue + branch `feat/6-ci-and-optionals`.
- [ ] Step 2: Write the five files; docker=none render + docker=yes render locally; assert rendered ci.yml contains `${{ runner.os }}`-style expressions intact and `python_version` substituted (grep).
- [ ] Step 3: Commit `feat: generated CI + docker/docs optionals refs #6`; PR; merge.

### Task 7: Template render-test CI matrix

**Files:**
- Create: `.github/workflows/render-test.yml`

**Interfaces:**
- Consumes: whole template + hooks (Tasks 2–6).
- Produces: matrix `os: [ubuntu-latest, windows-latest]` × `config: [default, docker, apache]`; steps: checkout, setup-uv, `uvx cookiecutter . --no-input -o out` (+ `docker=yes` / `license=Apache-2.0` overrides for non-default), enter `out/*`, `uv sync`, ruff/mypy/pytest, grep checks for raw GH expressions (ubuntu only step ok).

- [ ] Step 1: Issue + branch `chore/7-render-matrix`.
- [ ] Step 2: Write workflow; push; watch run green (Review Focus 2/3/5 all exercised here end-to-end: hooks run for real on both OSes).
- [ ] Step 3: Commit `chore: render-test CI matrix refs #7`; PR; merge.

### Task 8: Root README rewrite + CHANGELOG

**Files:**
- Modify: `README.md`
- Create: `CHANGELOG.md`

**Interfaces:**
- Produces: README H1 `CookiePyStarter — Modern Python Cookiecutter Template`; 30s quickstart (`uvx cookiecutter gh:mramitdas/CookiePyStarter`); feature list (uv, ruff, mypy, pytest, pre-commit, CI, Docker, docs, licenses); prompt table; comparison table vs cookiecutter-pypackage; badges (license Apache-2.0, render-test status, Python 3.10–3.14); sponsor section (existing links); docs links (`docs/`); "what you get" file tree. CHANGELOG: Keep-a-Changelog format, `[1.0.0]` unreleased section listing rebuild.

- [ ] Step 1: Issue + branch `docs/8-readme-changelog`.
- [ ] Step 2: Write both; verify all referenced paths exist (anti-hallucination).
- [ ] Step 3: Commit `docs: SEO README + changelog refs #8`; PR; merge.

### Task 9: docs/ guides + GitHub Pages

**Files:**
- Create: `docs/index.md`, `docs/guides/python-cookiecutter-template.md`, `docs/guides/uv-cookiecutter.md`, `docs/guides/modern-python-project-structure.md`, `docs/guides/python-boilerplate-generator.md`

**Interfaces:**
- Produces: 4 keyword-targeted long-form guides (each ≥500 words, internal links, CTA `uvx cookiecutter gh:mramitdas/CookiePyStarter`); index links all. Pages enabled via `gh api` repos/:owner/:repo/pages -f source.branch=main -f source.path=/docs (after Task 10 cutover, or enable on prod now — builder enables on default branch at the time).

- [ ] Step 1: Issue + branch `docs/9-guides-pages`.
- [ ] Step 2: Write guides; enable Pages; verify site URL returns 200.
- [ ] Step 3: Commit `docs: long-tail guides + pages refs #9`; PR; merge.

### Task 10: Repo metadata + default-branch cutover

**Files:** none in tree (gh settings only) + `.github/CODEOWNERS` untouched.

- [ ] Step 1: Issue + branch `chore/10-cutover`.
- [ ] Step 2: Push current `prod` HEAD to `main` (`git push origin prod:main`); `gh repo edit mramitdas/CookiePyStarter --default-branch main`.
- [ ] Step 3: `gh repo edit --description "CookiePyStarter — the modern Python cookiecutter template. uv · ruff · mypy · pytest · pre-commit · Docker · CI. uvx cookiecutter gh:mramitdas/CookiePyStarter"`; `--add-topic` each of: cookiecutter, cookiecutter-template, python, template, boilerplate, uv, ruff, pytest, pre-commit, docker, github-actions; `--remove-topic` none needed.
- [ ] Step 4: Open PR from a trivial branch `chore/10-cutover` targeting `main` (proves cutover); merge; commit `chore: default branch main + metadata refs #10`.

### Task 11: Final verification + release prep (STOP before publishing)

**Files:** none new; verification only + `CHANGELOG.md` finalization.

- [ ] Step 1: Issue + branch `chore/11-final-verify`.
- [ ] Step 2: Full local render: `uvx cookiecutter gh:mramitdas/CookiePyStarter -o /tmp/final` with all four license choices × docker/docs yes/no spot checks; run checks in two renders.
- [ ] Step 3: Verify README/docs links, Pages live, render-test matrix green on latest commit, repo topics/description set.
- [ ] Step 4: Commit any CHANGELOG finalization; PR; merge. **Then STOP and ask the user** to review before: tagging/publishing a GitHub release (NOT pre-authorized) and ecosystem PRs to cookiecutter/awesome-python (other repos, NOT pre-authorized).

---

## Self-review notes (2026-10-23)
- Spec coverage: goals → Tasks 2–7 (template/hooks/CI), SEO → 8–10, licenses → 2+5, branch collapse → 10, bug fixes by replacement → 2/4/8. Ecosystem PRs + release intentionally parked in Task 11 (authorization).
- pre_prompt correction applied everywhere (pre_gen_project).
- Type consistency: `write_license(license_choice: str, author: str, year: str, cwd: Path) -> None`, `remove_optional_paths(paths: list[str], cwd: Path) -> None`, `validate_package_name(name: str) -> str`, `load_hook(name: str)` — used identically across tasks.
