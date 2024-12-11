# autodiscovery

`autodiscovery` is a Python library designed to facilitate the discovery of Python applications across a network. This tool makes it easy to locate and interact with other instances of Python-based services or applications within a defined network range.

## Features
- **Seamless autodiscovery**: Automatically detects Python applications on the same network.
- **Lightweight and easy to use**: Minimal setup required.
- **Cross-platform**: Works on Windows, macOS, and Linux.

---

## Installation

Install `autodiscovery` via pip:

```bash
pip install autodiscovery
```

---

## Quick Start

Here’s how to get started with `autodiscovery` in your Python application:

### Setting Up a Discoverable Application


```python
from autodiscovery import AutoDiscovery

auto = AutoDiscovery()
auto.run_announcement()
```

### Discovering Applications on the Network

```python
from autodiscovery import AutoDiscovery

auto = AutoDiscovery()
auto.run_announcement()

print(auto.peers)
```
```
{"127.0.0.1": 1733868108.392893}
```
Peers are removed after 10 seconds when the peer stops broadcasting

---



## Example Use Case

### Use Case: Connecting Microservices
Imagine you have a distributed system with multiple microservices running in your local network. Using `autodiscovery`, you can:

1. Start a `AutoDiscovery` announcement in each microservice to announce its presence.
2. Use a `AutoDiscovery` discovery in your central service to find and communicate with all active microservices.

---

## Contributing

Contributions are welcome! If you'd like to contribute to `autodiscovery`, please:

1. Fork the repository on GitHub.
2. Create a new feature branch.
3. Commit your changes and submit a pull request.

---

## License

`autodiscovery` is licensed under the MIT License. See the LICENSE file for details.
