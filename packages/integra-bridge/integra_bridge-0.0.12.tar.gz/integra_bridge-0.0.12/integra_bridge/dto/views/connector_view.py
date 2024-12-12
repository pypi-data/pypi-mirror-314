import uuid
from pydantic import BaseModel, UUID4, Field, StrictStr, ConfigDict
from integra_bridge.dto.skeletons.connector import SkeletonConnector


class ConnectorView(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    connector_id: UUID4 = Field(default_factory=uuid.uuid4, alias='connectorID')
    title: StrictStr = Field(alias='connectorTitle')
    input_description: StrictStr = Field('', alias='inputConnectorDescription')
    output_description: StrictStr = Field('', alias='outputConnectorDescription')
    skeleton_input_connect: SkeletonConnector | None = Field(None, alias='skeletonInputConnector')
    skeleton_output_connect: SkeletonConnector | None = Field(None, alias='skeletonOutputConnector')
