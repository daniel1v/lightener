# AGENTS.md

## Project Overview

**Lightener** is a Home Assistant custom integration written in Python. It creates virtual light entities that control groups of real lights with per-light independent brightness mapping, enabling progressive multi-light scenes (e.g., activate lights one by one as brightness increases).

- **Language**: Python 3.10+
- **Integration domain**: `lightener`
- **Distribution**: HACS (Home Assistant Community Store)

## Repository Layout

```
custom_components/lightener/   # All integration source code
tests/components/lightener/    # Pytest test suite
scripts/                       # setup · develop · lint
config/                        # Dev-only HA YAML config (not shipped)
.github/workflows/             # CI: lint, validate, release
```

## Setup

```bash
scripts/setup          # Install Python (via uv), create .venv, install all deps
source .venv/bin/activate
```

## Running Tests

```bash
pytest                 # Run full suite (config in setup.cfg)
pytest -k "test_name"  # Filter by test name
```

All tests are async. The framework is `pytest-asyncio` + `pytest_homeassistant_custom_component`. Do not add `@pytest.mark.asyncio` individually — `asyncio_mode = auto` is already set.

## Linting

```bash
scripts/lint           # Equivalent to: ruff check . --fix
```

Linting **must pass** before submitting changes. The CI workflow (`lint.yml`) enforces `ruff check .` on every push and PR to `main`.

## Code Conventions

- All Home Assistant callbacks and entity methods must be `async def`
- `LightenerLight` in `light.py` extends `LightGroup` — keep it compatible with the HA light platform interface
- Brightness mapping logic lives in `LightenerControlledLight`; do not scatter it elsewhere
- Config data is stored in Home Assistant config entry options (not entity state)
- When changing the config entry data structure, increment `SCHEMA_VERSION` in `__init__.py` and add a migration branch
- Strings shown in the UI must be added to **all** files in `translations/` (`en.json`, `pt-BR.json`, `sk.json`)
- No `print()` statements — use `logging` (enforced by Ruff rule T20)
- Line length: 88 characters

## Important Files

| File | Purpose |
|---|---|
| `custom_components/lightener/light.py` | Core entity implementation |
| `custom_components/lightener/__init__.py` | Entry setup, teardown, migration |
| `custom_components/lightener/config_flow.py` | Config and options UI flows |
| `custom_components/lightener/const.py` | `DOMAIN`, light type constants |
| `custom_components/lightener/manifest.json` | HA integration metadata (version, dependencies) |
| `tests/components/lightener/conftest.py` | Shared test fixtures |

## What Not to Touch

- `.venv/` — generated, not committed
- `config/` — local dev HA config only, not part of the integration
- `hacs.json` — only update `homeassistant` field when bumping the minimum HA version

## Validation

In addition to unit tests and lint, the integration is validated against:

- **Hassfest** — Home Assistant's official manifest/integration validator
- **HACS** — checks repo structure and metadata

Both run in CI (`validate.yml`). You can trigger them manually via GitHub Actions.

## Release Process

Releases are created via a GitHub release tag. The `release.yml` workflow automatically:
1. Updates `manifest.json` with the release version
2. Packages the integration as `lightener.zip`
3. Uploads the ZIP to the release assets

Do not manually edit the version in `manifest.json`.
