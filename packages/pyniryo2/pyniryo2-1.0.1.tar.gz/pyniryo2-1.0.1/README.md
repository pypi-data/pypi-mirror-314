## 🚨 **Project Deprecated** 🚨

**This project is officially marked as deprecated and will no longer be maintained or receive updates starting 1st June 2025. We recommend users migrate to [PyNiryo](https://github.com/NiryoRobotics/pyniryo) or fork this repository if needed.**

# pyniryo2

## Table of Contents
- [Installation](#installation)
- [Documentation](#documentation)
- [License](#license)

## Installation

PyNiryo is distributed on [PyPI](https://pypi.org) as a universal
wheel and is available on Linux/macOS and Windows and supports
Python 2.7/3.5+

```bash
$ pip install pyniryo2
```

## Documentation

PyNiryo2 allows to write simple script in Python in order to control Ned

```python
from pyniryo2 import *

ned = NiryoRobot("10.10.10.10")

ned.arm.calibrate_auto()

ned.arm.move_joints([0.2, -0.3, 0.1, 0.0, 0.5, -0.8])
```

To see more examples or learn more about the available functions, full documentation is available at https://niryorobotics.github.io/pyniryo2

License
-------

PyNiryo2 is distributed under the terms of GNU General [Public License v3.0](https://choosealicense.com/licenses/gpl-3.0)