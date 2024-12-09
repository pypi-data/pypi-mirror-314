# pyawful

Spend $10 to interact with a dead forum from Python.

> [!CAUTION]
> Using this library without being funny may lead to your account being permanently banned.
> 
> Let's be honest, here: That's probably a net positive.

## Installation

This package is available via [PyPi][pypi-package] as `pyawful`
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

### Caching Authentication Session

> [!WARNING]
> Ignore this advice if you want to pay $10 again

Limit the number of sessions you create - if you're making lots
of requests or otherwise doing something regularly you should
persist the session cookies and restore them.

```python
from datetime import datetime
import json
import os

from pyawful import AuthenticatedAwfulSession, AwfulCookies

USERNAME = os.environ["SA_USERNAME"]
PASSWORD = os.environ["SA_PASSWORD"]

session = AuthenticatedAwfulSession(USERNAME, PASSWORD)

try:
    with open("./session.json", "r") as session_file:
        cached_session = json.load(session_file)
        cookies = AwfulCookies(**cached_session["cookies"])
        expiration = datetime.fromtimestamp(cached_session["expiration"])
        session.resume_session(cookies, expiration)
except Exception:
    pass

with session as client:
    cookies = session.get_cookies()
    expiration = session.get_expiration().timestamp()
    with open("./session.json", "w") as session_file:
        json.dump(
            { "cookies": cookies, "expiration": expiration },
            session_file
        )
```

## License

Licensed under the [MIT License](./LICENSE).

[pypi-package]: https://pypi.org/project/pyawful
