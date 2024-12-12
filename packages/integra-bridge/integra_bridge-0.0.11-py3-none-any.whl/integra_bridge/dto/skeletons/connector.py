from typing import Any

from pydantic import BaseModel, Field, StrictStr, ConfigDict

from integra_bridge.dto.parameter import Parameter


class SkeletonConnector(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )

    type_connect: StrictStr = Field('', alias='typeConnect')
    style_form: dict[str, Any] = Field(default_factory=dict, alias='styleForm')
    relation_text: StrictStr = Field('', alias='relationText')
    parameters: list[Parameter] = Field(default_factory=list, alias='parameterList')
