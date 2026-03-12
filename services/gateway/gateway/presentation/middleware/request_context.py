from dataclasses import dataclass
from uuid import uuid4


@dataclass
class RequestContext:
    request_id: str


def build_request_context() -> RequestContext:
    return RequestContext(request_id=str(uuid4()))
