from pydantic import BaseModel, StrictStr, Field, ConfigDict
from typing import Any


class Processor(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )

    id: Any
    name: StrictStr | None = None
    description: StrictStr | None = None
    number: int | None = None
    type_processor: StrictStr | None = Field(None, alias='typeProcessor')
    params: dict[StrictStr, StrictStr] | None = None
    params_object: dict[StrictStr, Any] | None = Field(None, alias='paramsObject')
