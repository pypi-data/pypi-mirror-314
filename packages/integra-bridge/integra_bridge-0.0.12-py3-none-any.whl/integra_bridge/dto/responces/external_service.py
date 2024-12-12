from pydantic import BaseModel, StrictStr, Field, ConfigDict
from datetime import datetime

from integra_bridge.dto import ConnectorView
from integra_bridge.dto import ProcessorView


class ExternalServiceConfigResponse(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
    )
    service_name: StrictStr = Field('', alias='serviceName')
    service_address: StrictStr = Field('', alias='serviceAddress')
    application_start_date: datetime | None = Field(None, alias='applicationStartDate')
    connector_views: list[ConnectorView] | None = Field(default_factory=list, alias='connectorViewList')
    processor_views: list[ProcessorView] | None = Field(default_factory=list, alias='processorViewList')
    manual_file_name: StrictStr | None = Field(None, alias='manualFileName')
