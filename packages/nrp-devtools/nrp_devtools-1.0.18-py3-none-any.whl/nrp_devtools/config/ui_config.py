import dataclasses
from typing import Optional


@dataclasses.dataclass
class UIConfig:
    name: str
    endpoint: str

    # for model UIs
    model: Optional[str] = None
    api_service: Optional[str] = None
    ui_serializer_class: Optional[str] = None
