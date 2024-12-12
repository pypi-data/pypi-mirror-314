import json
from abc import ABC
from typing import Any, NoReturn
import httpx
from starlette import status

from integra_bridge.adapters.BaseAdapter import BaseAdapter
from integra_bridge.common.settings import SETTINGS
from integra_bridge.dto import Exchange, ConnectorToBlockView
from integra_bridge.dto.body import Body
from integra_bridge.dto.responces.validation import ValidationResponse
from integra_bridge.entity.connector import Connector
from integra_bridge.entity.output_status import OutputStatus


class ConnectorAdapter(BaseAdapter, ABC):
    _connector_to_block_views: dict[str, ConnectorToBlockView] = {}

    def __init__(self):
        super().__init__()
        ConnectorAdapter.add_adapter(self)

    def __del__(self):
        ConnectorAdapter.remove_adapter(self)

    async def pull_from_integra(self, input_body: dict, params: dict) -> OutputStatus:
        status = OutputStatus()
        return status

    @classmethod
    async def push_to_integra(
            cls,
            input_body: Any,
            connect_to_block_id: str = None
    ) -> int:
        try:
            string_body = json.dumps(input_body)
        except Exception as e:
            raise ValueError(f"input body is not json serializable: {str(e)}")
        if not connect_to_block_id:
            raise ValueError(f"connect to block id  is required")

        connector_to_block_view = ConnectorAdapter._connector_to_block_views.get(connect_to_block_id)
        if not connector_to_block_view:
            raise ValueError(f"connect to block view {connect_to_block_id} not found")

        input_body = Body(stringBody=string_body)
        exchange = Exchange(inputBody=input_body)
        exchange.block_id = connector_to_block_view.block_id
        exchange.input_connect_id = connector_to_block_view.connect_id
        exchange.company_id = connector_to_block_view.company_id

        url = f"{connector_to_block_view.url_integra_service}/api/external/connector/input/{connect_to_block_id}?connectorTitle={connector_to_block_view.connector_title}"
        return await cls.send(exchange, url)

    @classmethod
    async def send(cls, exchange: Exchange, url: str) -> int:
        auth = httpx.BasicAuth(username='admin', password='admin')
        async with httpx.AsyncClient(auth=auth, timeout=SETTINGS.DEFAULT_CONNECTOR_TIMEOUT) as client:
            try:
                response = await client.post(url, json=exchange.model_dump(by_alias=True), timeout=SETTINGS.DEFAULT_CONNECTOR_TIMEOUT)
            except httpx.TimeoutException:
                return status.HTTP_504_GATEWAY_TIMEOUT
            except ValueError as err:
                print('Error while sending to integra: ', str(err))
                return status.HTTP_406_NOT_ACCEPTABLE
            return response.status_code

    async def deploy_input_flow(self, exchange: Exchange, connector_title: str):
        connector_to_block_view = ConnectorToBlockView(
            connector_title=connector_title,
            company_id=exchange.company_id,
            block_id=exchange.block_id,
            connect_id=exchange.input_connect_id,
            url_integra_service=exchange.headers.get('urlIntegra'),
            exchange_deploy=exchange
        )
        connector_to_block_id = await connector_to_block_view.get_id()
        ConnectorAdapter._connector_to_block_views[connector_to_block_id] = connector_to_block_view
        print('!!!!!!!!DEPLOYED:', ConnectorAdapter._connector_to_block_views[connector_to_block_id].connector_title,
              ConnectorAdapter._connector_to_block_views.keys())
        await self.on_after_deploy(
            connection_id=connector_to_block_id,
            connector_params=connector_to_block_view.model_dump()
        )
        return exchange

    async def destroy_input_flow(self, exchange: Exchange, connector_title: str):
        connector_to_block_view = ConnectorToBlockView(
            connector_title=connector_title,
            company_id=exchange.company_id,
            block_id=exchange.block_id,
            connect_id=exchange.input_connect_id,
            exchange_deploy=exchange
        )
        connector_to_block_id = await connector_to_block_view.get_id()
        ConnectorAdapter._connector_to_block_views.pop(connector_to_block_id, None)
        print('!!!!!!!!DESTROYED:', ConnectorAdapter._connector_to_block_views.keys())
        await self.on_after_destroy(
            connection_id=connector_to_block_id,
            connector_params=connector_to_block_view.model_dump()
        )
        return exchange

    async def validate_output(self, connector: Connector) -> ValidationResponse:
        return ValidationResponse(result=True)

    async def validate_input(self, connector: Connector) -> ValidationResponse:
        return ValidationResponse(result=True)

    async def on_after_deploy(self, connection_id: str, connector_params: dict) -> NoReturn:
        ...

    async def on_after_destroy(self, connection_id: str, connector_params: dict) -> NoReturn:
        ...
