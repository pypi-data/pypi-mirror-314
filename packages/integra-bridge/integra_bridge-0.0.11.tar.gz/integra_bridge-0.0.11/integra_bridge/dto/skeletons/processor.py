from pydantic import BaseModel, Field, ConfigDict
from integra_bridge.dto.parameter import Parameter


class SkeletonProcessor(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    type_processor: str = Field("", alias='typeProcessor')
    parameters: list[Parameter] = Field(default_factory=list, alias='parameterList')
