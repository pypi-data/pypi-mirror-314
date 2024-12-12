from pydantic import BaseModel, Field, StrictStr, ConfigDict
from typing import Any


class Connector(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )

    id: Any
    company_id: Any | None = Field(None, alias='companyId')
    name: StrictStr | None = None
    description: StrictStr | None = None
    number: int | None = None
    type_connect: StrictStr | None = Field(None, alias='typeConnect')
    input_type_format: StrictStr | None = Field(None, alias='inputTypeFormat')
    output_type_format: StrictStr | None = Field(None, alias='outputTypeFormat')
    params: dict[StrictStr, StrictStr] | None = None
    query_params: dict[StrictStr, StrictStr] | None = Field(None, alias='queryParams')
    #  массивы, объекты
    params_object: dict[StrictStr, Any] | None = Field(None, alias='paramsObject')
