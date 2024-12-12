from pydantic import BaseModel, ConfigDict, StrictStr, Field
from typing import Any
from pydantic.json import pydantic_encoder


class ConnectorToBlockView(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={dict: pydantic_encoder}
    )
    connector_title: StrictStr = Field(None, alias='connectorTitle')
    company_id: StrictStr = Field(None, alias='companyId')
    block_id: StrictStr = Field(None, alias='blockId')
    connect_id: StrictStr = Field(None, alias='connectId')
    url_integra_service: StrictStr | None = Field(None, alias='urlIntegraService')
    exchange_deploy: Any = Field(None, alias='exchangeDeploy')

    async def get_id(self):
        return f'{self.company_id}_{self.block_id}_{self.connect_id}'
