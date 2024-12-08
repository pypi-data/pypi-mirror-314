[![Build][github-ci-image]][github-ci-link]
[![Coverage Status][codecov-image]][codecov-link]
[![PyPI Version][pypi-image]][pypi-link]
[![PyPI - Python Version][python-image]][pypi-link]
![License][license-image]

# Kajihs Utils

Various, fully typed, hopefully sanely implemented and somewhat random utilities.

## ⬇️ Installation

You can install **kajihs_utils** via pip:

```bash
pip install kajihs-utils
```

## 🏃 Getting Started

```python:dev/readme_snippets/formatted/features_demo.py
from kajihs_utils import batch, get_first

# Get first key existing in a dict:
d = {"a": 1, "b": 2, "c": 3}
print(get_first(d, ["x", "a", "b"]))  # Output: 1

# Batch a sequence:
seq = list(range(10))
print(list(batch(seq, 3)))  # Output: [[0, 1, 2], [3, 4, 5], [6, 7, 8], [9]]
```

## 🧾 License

[MIT license](LICENSE)

<!-- Links -->
[github-ci-image]: https://github.com/Kajiih/kajihs_utils/actions/workflows/build.yml/badge.svg?branch=main
[github-ci-link]: https://github.com/Kajiih/kajihs_utils/actions?query=workflow%3Abuild+branch%3Amain

[codecov-image]: https://img.shields.io/codecov/c/github/Kajiih/kajihs_utils/main.svg?logo=codecov&logoColor=aaaaaa&labelColor=333333
[codecov-link]: https://codecov.io/github/Kajiih/kajihs_utils

[pypi-image]: https://img.shields.io/pypi/v/kajihs-utils.svg?logo=pypi&logoColor=aaaaaa&labelColor=333333
[pypi-link]: https://pypi.python.org/pypi/kajihs-utils

[python-image]: https://img.shields.io/pypi/pyversions/kajihs-utils?logo=python&logoColor=aaaaaa&labelColor=333333
[license-image]: https://img.shields.io/badge/license-MIT_license-blue.svg?labelColor=333333
