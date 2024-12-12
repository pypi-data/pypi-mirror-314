from pydantic import BaseModel, Field, StrictStr, ConfigDict


class ValidationResponse(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    result: bool = True
    # Блокирующие ошибки
    params_description: dict[StrictStr, list[StrictStr]] = Field(default_factory=dict, alias='paramsDescription')
    query_params_description: dict[StrictStr, list[StrictStr]] = Field(default_factory=dict,
                                                                       alias='queryParamsDescription'
                                                                       )
    filter_description: dict[StrictStr, list[StrictStr]] = Field(default_factory=dict, alias='filterDescription')

    # Неблокирующие
    warning_params_description: dict[StrictStr, list[StrictStr]] = Field(default_factory=dict,
                                                                         alias='warningParamsDescription')
    warning_query_params_description: dict[StrictStr, list[StrictStr]] = Field(default_factory=dict,
                                                                               alias='warningQueryParamsDescription')
    warning_filter_description: dict[StrictStr, list[StrictStr]] = Field(default_factory=dict,
                                                                         alias='warningFilterDescription')
