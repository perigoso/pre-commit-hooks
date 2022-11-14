pre-commit-hooks
================

Some hooks for pre-commit.

See also: [pre-commit/pre-commit](https://github.com/pre-commit/pre-commit)

### Using pre-commit-hooks with pre-commit

Add this to your `.pre-commit-config.yaml`

```yaml
-   repo: https://github.com/perigoso/pre-commit-hooks
    rev: v0.1.0  # Use the ref you want to point at
    hooks:
    - id: check-hex-case
    #   ...
    - id: check-include-guards
    #   ...
    # - id: ...
```

### Hooks available

#### `check-include-guards`

Checks for unique relative named C header include guards.
Naming is the file path relative to a specific directory, all upper case, with no prefix or suffix underscores.

- Specify what relative path with `args: ['--relative-path=src']`

#### `check-hex-case`

Checks for Checks and fixes hex number declarion case, as in upper/lower.
By default it fixes hex number declarations to lower case prefix, upper case digits (`0x55AA`)
Flags can be used to change this bahaviour (`0X55AA`, `0x55aa`, `0X55aa`):

- Set preffix to upper case with `args: ['--upper-preffix']`
- Set digits to lower case with `args: ['--lower-digits']`
