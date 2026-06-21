# CLAUDE.md

## Project Overview

**Lightener** is a Home Assistant custom integration that creates virtual lights capable of controlling groups of physical lights with independent brightness mapping per light. It enables progressive multi-light room control (e.g., only one lamp at low brightness, all lamps at full brightness).

- **Language**: Python 3.10+
- **Type**: Home Assistant custom integration (HACS-compatible)
- **Integration domain**: `lightener`

## Repository Structure

```
custom_components/lightener/   # Integration source code
  __init__.py                  # Entry setup, migration logic
  light.py                     # Main entity (extends LightGroup)
  config_flow.py               # UI config/options flows
  const.py                     # Domain constant + light types
  util.py                      # Light type detection helper
  manifest.json                # HA integration metadata
  translations/                # i18n strings (en, pt-BR, sk)
tests/components/lightener/    # Test suite
  conftest.py                  # Shared fixtures
  test_init.py                 # Setup/unload/migration tests
  test_config_flow.py          # Config UI flow tests
  test_light.py                # Core entity tests
scripts/                       # Dev helper scripts
  setup                        # Install dev environment
  develop                      # Launch dev HA instance
  lint                         # Run ruff check --fix
config/                        # Dev-only HA configuration
```

## Development Environment Setup

```bash
# One-time setup (installs Python 3.13 via uv, creates .venv, installs deps)
scripts/setup

# Activate virtualenv manually if needed
source .venv/bin/activate
```

The devcontainer (`.devcontainer.json`) runs `scripts/setup` automatically on container creation.

## Common Commands

```bash
# Run tests
pytest

# Lint (auto-fixes in place)
scripts/lint
# or directly:
ruff check . --fix

# Start development Home Assistant instance (port 8123)
scripts/develop
```

## Testing

- Framework: `pytest` with `pytest-asyncio` and `pytest_homeassistant_custom_component`
- Tests live in `tests/components/lightener/`
- All tests are async; `asyncio_mode = auto` is set in `setup.cfg`
- Use fixtures from `conftest.py` when mocking HA light entities

```bash
pytest                         # Run all tests
pytest tests/.../test_light.py # Run specific file
pytest -k "test_brightness"    # Run by name pattern
```

## Code Style

- **Linter/formatter**: Ruff (`ruff check . --fix`)
- **Line length**: 88 characters (Black-compatible)
- **Python target**: 3.10+
- **Docstring style**: D203/D213 ignored; one-line docstrings preferred
- No print statements (T20 rule enforced)
- Complexity limit: 25 (McCabe)

Key Ruff rule groups active: `B, C, D, E, F, T20, UP, W` — see `.ruff.toml` for full config.

## Key Conventions

- All HA entity methods are `async`; follow Home Assistant's async patterns
- `LightenerLight` extends `LightGroup` from `homeassistant.components.light`
- Brightness mapping is stored in config entry options, not state
- Config entry migration is handled in `__init__.py`; bump `SCHEMA_VERSION` when changing the data structure
- Translations must be updated in all files under `translations/` when adding new strings

## CI/CD (GitHub Actions)

| Workflow | Trigger | What it does |
|---|---|---|
| `lint.yml` | push/PR to main | `ruff check .` |
| `validate.yml` | daily + manual | Hassfest + HACS validation |
| `release.yml` | GitHub release publish | Updates version, creates `lightener.zip` |

## Dependencies

Defined in `requirements.txt`:
- `homeassistant==2025.10.1` — pin matches the CI validation target
- `pytest`, `pytest-asyncio`, `pytest_homeassistant_custom_component` — dev/test
- `ruff==0.14.0` — linter (pinned)
- `colorlog>=6.9.0` — runtime dep

When bumping the HA version pin, also update `hacs.json` (`homeassistant` key) and `manifest.json` (`requirements` if any).
