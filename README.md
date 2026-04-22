# Modern-Python-Cookbook-Third-Edition
Code Repository for Modern Python Cookbook Third Edition, Published by Packt

The code examples all require Python 3.12.

It's often easiest to build this by starting with a tool like ``conda`` to
install Python and create virtual environments.
Conda is not required; it's only suggested.

Using Conda:

```bash
    conda create --name cookbook3 python=3.12 --channel=conda-forge
    conda activate cookbook3
    python -m pip install -r requirements.txt
```

After this setup, the test suite is run as follows:

```bash
tox
```

Since each chapter is tested in a separate virtual environment,
the first run will take several minutes to download and install the packages.
After that, the cached virtual environments will be reused.
