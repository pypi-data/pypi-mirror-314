```bash
python3 -m pip install --upgrade distcrab
```

```bash
python3 -m distcrab --host=[HOST] --branch=[BRANCH]
python3 -m distcrab --host=[HOST] --version=[VERSION]
```

```python
from distcrab import Distcrab
Distcrab(host, port, username, password, version, branch)
```
