# pyisg

Library reading/writing the [ISG 2.0 format][SPEC].

This provides APIs, such as {py:func}`.load`, {py:func}`.loads`, {py:func}`.dump` and {py:func}`.dumps`.

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

[SPEC]: https://www.isgeoid.polimi.it/Geoid/format_specs.html

Licence
: MIT or Apache-2.0

Reference
: Specification: [https://www.isgeoid.polimi.it/Geoid/format_specs.html][SPEC]

## `pyisg` package

### Submodules

```{eval-rst}
.. toctree::
   :maxdepth: 1

   pyisg.types
```

### Module contents

```{eval-rst}
.. automodule:: pyisg
   :members:
   :undoc-members:
   :show-inheritance:
```

### `pyisg.types` module

```{eval-rst}
.. automodule:: pyisg.types
   :members:
   :undoc-members:
   :show-inheritance:
```

## Indices and tables

* {ref}`genindex`
* {ref}`modindex`
* {ref}`search`

