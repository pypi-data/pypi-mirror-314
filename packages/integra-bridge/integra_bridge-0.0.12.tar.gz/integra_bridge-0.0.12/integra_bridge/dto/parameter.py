from enum import Enum
from typing import Any

from pydantic import BaseModel, StrictStr, Field, ConfigDict

from integra_bridge.common.enums import ParameterType


class Parameter(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    name: StrictStr
    label: StrictStr | None = Field(default=None)
    type: Enum = Field(default=ParameterType.TextField)
    # Стиль элемента, где рендерятся внутренние элементы
    children_box_style: dict[str, Any] | None = Field(default=None, alias='childrenBoxStyle')
    # Стиль элемента
    style: dict[str, Any] | None = Field(default=None)
    # Стиль контейнера, где находится элемент
    box_style: dict[str, Any] | None = Field(default=None, alias='boxStyle')
    props: dict[str, Any] | None = Field(default=None)

    description: StrictStr | None = Field(default=None)
    default_value: StrictStr | None = Field(default=None, alias='defaultValue')
    # Для настроек, текущее значение
    value: StrictStr | None = Field(default=None)

    # list of Parameter
    parameters: list['Parameter'] | None = Field(default=None, alias='parameterList')

    default_option: StrictStr | None = Field(default=None, alias='defaultOption')
    options: list[str] | None = Field(default=None)
    object_options: list[Any] | None = Field(default=None, alias='objectOptions')

    bottom_text: StrictStr | None = Field(default=None, alias='bottomText')
    is_add_value: bool | None = Field(default=None, alias='isAddValue')

    is_change: bool = Field(default=True, alias='isChange')
    is_required: bool = Field(default=False, alias='isRequired')
    is_visible: bool = Field(default=True, alias='isVisible')
    is_disabled: bool = Field(default=False, alias='isDisabled')
    is_external: bool = Field(default=False, alias='isExternal')


Parameter.update_forward_refs()

