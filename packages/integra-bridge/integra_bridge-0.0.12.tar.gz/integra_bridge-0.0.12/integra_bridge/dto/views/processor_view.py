from pydantic import BaseModel, StrictStr, Field, ConfigDict
from integra_bridge.dto import SkeletonProcessor


class ProcessorView(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    title: StrictStr | None = Field("", alias='processorTitle')
    description: StrictStr | None = Field("", alias='processorDescription')
    skeleton: SkeletonProcessor = Field("", alias='skeletonProcessor')
