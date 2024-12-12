from .connector import Connector
from .processor import Processor
from pydantic import BaseModel, StrictStr, Field, ConfigDict


class Block(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )

    id: StrictStr
    name: StrictStr | None = None
    description: StrictStr | None = None
    flow_id: StrictStr | None = Field(None, alias='flowId')
    company_id: StrictStr | None = Field(None, alias='companyId')
    flow_name: StrictStr | None = Field(None, alias='flowName')
    is_active: bool | None = Field(None, alias='isActive')
    is_guaranteed_order: bool | None = Field(None, alias='isGuaranteedOrder')
    is_guaranteed_delivery: bool | None = Field(None, alias='isGuaranteedDelivery')
    is_active_guaranteed_delivery: bool | None = Field(None, alias='isActiveGuaranteedDelivery')
    is_limited_count_delivery: bool | None = Field(None, alias='isLimitedCountDelivery')
    limited_count: int | None = Field(None, alias='limitedCount')
    input_list: list[Connector] | None = Field(None, alias='inputList')
    enriched_inputs: list[Connector] | None = Field(None, alias='enrichedInputList')
    processors: list[Processor] | None = Field(None, alias='processorList')
    enriched_processors: list[Processor] | None = Field(None, alias='enrichedProcessorList')
    outputs: list[Connector] | None = Field(None, alias='outputList')
    enriched_outputs: list[Connector] | None = Field(None, alias='enrichedOutputList')
