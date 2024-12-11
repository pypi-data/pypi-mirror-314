# Runtime Dataclass Enforcer 

```python

from rtdce import enforce 

from dataclasses import dataclass
from typing import Dict

@dataclass
class Test:
    hello: Dict[str, int]

t = Test(hello={'world': 123})

enforce(t)

```