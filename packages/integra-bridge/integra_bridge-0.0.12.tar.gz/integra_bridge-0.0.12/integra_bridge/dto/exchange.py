from pydantic import BaseModel, Field, StrictStr, ConfigDict
from typing import Any

from .body import Body
from integra_bridge.entity.block import Block
from integra_bridge.entity.connector import Connector
from integra_bridge.entity.processor import Processor


class Exchange(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    id_executor_history: Any | None = Field(None, alias='idExecutorHistory')
    id: Any | None = None
    company_id: Any | None = Field(None, alias='companyId')
    input_headers: dict[StrictStr, StrictStr] | None = Field(default_factory=dict, alias='inputHeaders')
    headers: dict[StrictStr, StrictStr] | None = {}
    output_headers: dict[StrictStr, StrictStr] | None = Field(default_factory=dict, alias='outputHeaders')
    input_path_params: dict[StrictStr, StrictStr] | None = Field(default_factory=dict, alias='inputPathParams')
    input_query_params: dict[StrictStr, StrictStr] | None = Field(default_factory=dict, alias='inputQueryParams')
    input_body: Body | None = Field(None, alias='inputBody')
    body: Body | None = None
    output_body: Body | None = Field(None, alias='outputBody')

    # Exchange
    exchange: Any | None = None

    block_id: Any | None = Field(None, alias='blockId')
    block: Block | None = None
    input_connect_id: Any | None = Field(None, alias='inputConnectId')
    input_connect: Connector | None = Field(None, alias='inputConnect')
    type_input_connect: Any | None = Field(None, alias='typeInputConnect')

    # Если true то будет принудительно передеплоин
    is_forcible: bool | None = Field(None, alias='isForcible')

    # Если true то принудительно будет отработан, даже если блок не активен
    is_execute_block_forcible: bool | None = Field(None, alias='isExecuteBlockForcible')

    # Если null == все процессоры используем
    use_processor_ids: list[StrictStr] | None = Field(None, alias='useProcessorIdList')

    processor_id: Any | None = Field(None, alias='processorId')
    processor: Processor | None = None
    is_skip: bool | None = Field(None, alias='isSkip')

    # Если false = то отфильтрофан, далее не идет.
    is_filtered: bool | None = Field(None, alias='isFiltered')

    # Если null - то отправляем.
    is_send_output_connect: bool | None = Field(None, alias='isSendOutputConnect')

    # Если true - то выполняется интеграционный тест
    is_integration_test: bool | None = Field(None, alias='isIntegrationTest')

    output_connect_id: Any | None = Field(None, alias='outputConnectId')
    output_connect: Connector | None = Field(None, alias='outputConnect')
    input_object_map: dict[StrictStr, Any] | None = Field(default_factory=dict, alias='inputObjectMap')
    object_map: dict[StrictStr, Any] | None = Field(default_factory=dict, alias='objectMap')
    output_object_map: dict[StrictStr, Any] | None = Field(default_factory=dict, alias='outputObjectMap')

    # Обработка ошибок,логика по переотправке
    error_packet_id: Any | None = Field(None, alias='errorPacketId')

    # Если true, то запущен из ErrorPacketService
    is_run_error_packet: bool | None = Field(None, alias='isRunErrorPacket')

    is_finish: bool | None = Field(None, alias='isFinish')
    is_exist_error_packet: bool | None = Field(None, alias='isExistErrorPacket')
    is_guaranteed_order: bool | None = Field(None, alias='isGuaranteedOrder')
    is_guaranteed_delivery: bool | None = Field(None, alias='isGuaranteedDelivery')
    is_limited_count_delivery: bool | None = Field(None, alias='isLimitedCountDelivery')
    limited_count: int | None = Field(None, alias='limitedCount')
    processor_id_exception: Any = Field(None, alias='processorIdException')
    status: Any | None = None
    exception: Any | None = None
    stackTrace: Any | None = None
