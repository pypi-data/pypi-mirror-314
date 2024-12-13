# pyisg

[![PyPI - Version](https://img.shields.io/pypi/v/pyisg?logo=PyPI&label=PyPI)](https://pypi.org/project/pyisg/)
![Python Version from PEP 621 TOML](https://img.shields.io/python/required-version-toml?logo=Python&label=Python&&tomlFilePath=https%3A%2F%2Fraw.githubusercontent.com%2Fpaqira%2Fpyisg%2Fmain%2Fpyproject.toml)
![GitHub Actions Workflow Status](https://img.shields.io/github/actions/workflow/status/paqira/pyisg/CI.yml?logo=GitHub)
[![Read the Docs](https://img.shields.io/readthedocs/pyisg?logo=readthedocs)](https://pyisg.readthedocs.io)
![PyPI - License](https://img.shields.io/pypi/l/pyisg?color=blue)

Library reading/writing the [ISG 2.0 format][SPEC].

This provides APIs, such as `load`, `loads`, `dump` and `dumps`.

```python
import pyisg

# serialize to ISG 2.0 format str to dict
with open("file.isg") as fs:
    obj = pyisg.load(fs)

# deserialize to ISG 2.0 format str
s = pyisg.dumps(obj)
```

One can install `pyisg` from PyPI

```shell
pip install pyisg
```

## Licence

MIT or Apache-2.0

## Reference

Specification: https://www.isgeoid.polimi.it/Geoid/format_specs.html


[SPEC]: https://www.isgeoid.polimi.it/Geoid/format_specs.html
