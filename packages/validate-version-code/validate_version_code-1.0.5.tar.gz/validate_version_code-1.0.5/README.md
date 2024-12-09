# validate_version_code

[![PyPI](https://badge.fury.io/py/validate-version-code.svg)](https://pypi.org/project/validate-version-code/)
[![Downloads](https://pepy.tech/badge/validate-version-code)](https://pepy.tech/project/validate-version-code)
[![License](https://img.shields.io/github/license/LucaCappelletti94/validate_version_code)](https://github.com/LucaCappelletti94/validate_version_code/blob/master/LICENSE)
[![Github Actions](https://github.com/LucaCappelletti94/validate_version_code/actions/workflows/python.yml/badge.svg)](https://github.com/LucaCappelletti94/validate_version_code/actions/)

Python package to validate version codes.

## How do I install this package?

As usual, just download it using pip:

```bash
pip install validate_version_code
```

## Usage Example

Here’s a basic how-to:

```python
from validate_version_code import validate_version_code

valid_version_code = "1.2.3"
invalid_version_code = "beta.3"

assert validate_version_code(valid_version_code)
assert not validate_version_code(invalid_version_code)
```

## License

This package is distributed under the MIT license. This license can be found [here](LICENSE).
