from __future__ import annotations

import dataclasses
import json
from dataclasses import dataclass


def loads(data: str) -> TokenFile:
    d = json.loads(data)
    return TokenFile(name=d["name"], token=d["token"], created=d["created"], expires=d["expires"])


def dumps(token: TokenFile) -> str:
    return json.dumps(dataclasses.asdict(token), default=str)


@dataclass
class TokenFile:
    name: str
    token: str
    created: str
    expires: str
