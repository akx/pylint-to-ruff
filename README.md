# pylint-to-ruff

A friend of [flake8-to-ruff](https://pypi.org/project/flake8-to-ruff/),
this project attempts to introspect your Pylint configuration and figure out
what Ruff rules to enable or disable.

## Compatibility

Ruff versions 0.1.4 (November 2023) and newer are supported.

## Usage

You need to be in an environment where both your target Pylint version and
your target Ruff version are available to execute.

Then, run the program – easiest is `pipx`:

```bash
pipx run pylint-to-ruff
```

or if you have installed the package already with Pip, simply

```bash
pylint-to-ruff
```

The tool will output a TOML segment you can paste or interpolate into your
Ruff configuration file.
