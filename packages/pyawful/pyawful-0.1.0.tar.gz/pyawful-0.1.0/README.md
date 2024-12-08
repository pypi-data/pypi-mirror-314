# pyawful

Spend $10 to interact with a dead forum from Python.

> [!CAUTION]
> Using this library without being funny may lead to your account being permanently banned.
> 
> Let's be honest, here: That's probably a net positive.

## Installation

This package is available via [PyPi][pypi-package] as `somethingawful`
and can be installed via your package manager of choice.

## Usage

```python
import os

from pyawful import AuthenticatedAwfulSession

USERNAME = os.environ["SA_USERNAME"]
PASSWORD = os.environ["SA_PASSWORD"]

with AuthenticatedAwfulSession(USERNAME, PASSWORD) as client:
    response = client.get_forum_threads(273)

    for thread in response.threads:
        print(thread.title)
```

## License

Licensed under the [MIT License](./LICENSE).

[pypi-package]: https://pypi.org/project/somethingawful