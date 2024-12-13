from typing import Any, Optional

from pydantic import BaseModel


class CallToAction(BaseModel):
    type: str = "NONE"
    value: Optional[Any] = None
