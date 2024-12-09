MikroTik RouterOS log exporter
==============================

<p align="center">
  <a href="https://github.com/dinotools/routeros-log-exporter/issues">
    <img alt="GitHub issues" src="https://img.shields.io/github/issues/dinotools/routeros-log-exporter">
  </a>
  <a href="https://github.com/dinotools/routeros-log-exporter/network">
    <img alt="GitHub forks" src="https://img.shields.io/github/forks/dinotools/routeros-log-exporter">
  </a>
  <a href="https://github.com/dinotools/routeros-log-exporter/stargazers">
    <img alt="GitHub stars" src="https://img.shields.io/github/stars/dinotools/routeros-log-exporter">
  </a>
  <a href="https://github.com/DinoTools/routeros-log-exporter/blob/main/LICENSE.md">
    <img alt="GitHub license" src="https://img.shields.io/github/license/dinotools/routeros-log-exporter">
  </a>
  <a href="https://dinotools.github.io/routeros-log-exporter">
    <img alt="Documentation" src="https://github.com/DinoTools/routeros-log-exporter/actions/workflows/docs.yml/badge.svg">
  </a>
  <a href="https://pypi.org/project/routeros-log-exporter/">
    <img alt="PyPI - Downloads" src="https://img.shields.io/pypi/dm/routeros-log-exporter">
  </a>
  <a href="https://pypi.org/project/routeros-log-exporter/">
    <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/routeros-log-exporter">
  </a>
  <a href="https://pypi.org/project/routeros-log-exporter/">
    <img alt="PyPI - Format" src="https://img.shields.io/pypi/format/routeros-log-exporter">
  </a>
  <a href="https://pypi.org/project/routeros-log-exporter/">
    <img alt="PyPI - Status" src="https://img.shields.io/pypi/status/routeros-log-exporter">
  </a>
</p>

> [!WARNING]
> **Proof of Concept**
>
> This project is in an very early stage of development. Don't use it in production.

The Exporter connects to [MikroTik](https://mikrotik.com/) RouterOS devices via API and connects to the log stream to export the logs in realtime.

Requirements
------------

- [Python](https://www.python.org/) >= 3.8 (It might still run with older versions of Python 3)
- Python Packages
    - [Click](https://pypi.org/project/click/)
    - [librouteros](https://pypi.org/project/librouteros/)
    - [pyyaml](https://pypi.org/project/PyYAML/)

Installation
------------

### Docker

```
docker pull ghcr.io/dinotools/routeros-log-exporter:main
docker run --rm -v ./config.yaml:/etc/routeros_log_exporter/config.yaml:ro ghcr.io/dinotools/routeros-log-exporter:main
```

### PIP

If you want to use pip we recommend to use as virtualenv to install the dependencies.

```shell
pip install -r requirements.txt
```

### Debian/Ubuntu

Install the required packages

```shell
sudo apt-get install python3 python3-click python3-librouteros
```

### From PyPI

Install the package from PyPI.

```shell
pip install routeros-log-exporter
```

Usage
-----

```
python3 -m routeros_log_exporter --config config.yaml -vv
```

Resources
---------

- Git-Repository: https://github.com/DinoTools/routeros-log-exporter
- Issues: https://github.com/DinoTools/routeros-log-exporter/issues
- Documentation: https://dinotools.github.io/routeros-log-exporter

License
-------

GPLv3+
