from fastapi import HTTPException, Request
from orjson import orjson
from pydantic import ValidationError
from starlette import status

from integra_bridge.dto import Exchange
from integra_bridge.adapters import ConnectorAdapter
from integra_bridge.dto.responces.validation import ValidationResponse
from integra_bridge.entity.connector import Connector


class ConnectorHandler:
    @classmethod
    async def execute_output_exchange(cls, request: Request, title: str):
        connector_adapter = await cls.get_connector_by_title(title)
        try:
            exchange = await request.json()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Output body is not JSON serializable")
        output_body = exchange.get("outputBody", {}).get("stringBody", {})
        try:
            inner_body = orjson.loads(output_body)
        except ValueError:
            inner_body = output_body
        params = exchange.get("outputConnect", {}).get("params", {})
        inner_params = params
        try:
            output_status = await connector_adapter.pull_from_integra(inner_body, inner_params)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f'Connector error: {str(e)}')
        if output_status.error_message:
            exchange['exception'] = output_status.error_message
        return exchange

    @classmethod
    async def deploy_input(cls, request: Request, title: str) -> Exchange:
        exchange = await cls.get_exchange_object(request)
        connector = await ConnectorHandler.get_connector_by_title(title)
        await connector.deploy_input_flow(exchange=exchange, connector_title=title)
        return exchange

    @classmethod
    async def destroy_input(cls, request: Request, title: str) -> Exchange:
        exchange = await cls.get_exchange_object(request)
        connector = await ConnectorHandler.get_connector_by_title(title)
        await connector.destroy_input_flow(exchange=exchange, connector_title=title)
        return exchange

    @classmethod
    async def validate_output(cls, connector: Connector, title: str) -> ValidationResponse:
        try:
            connector_adapter = await cls.get_connector_by_title(title)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        return await connector_adapter.validate_output(connector)

    @classmethod
    async def validate_input(cls, connector: Connector, title: str) -> ValidationResponse:
        try:
            connector_adapter = await cls.get_connector_by_title(title)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        return await connector_adapter.validate_input(connector)

    @staticmethod
    async def get_exchange_object(request: Request) -> Exchange:
        try:
            exchange_dict = await request.json()
            exchange = Exchange(**exchange_dict)
        except ValidationError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Exchange structure is unvalid: {e}")
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=f"Input body is not JSON serializable: {e}")
        return exchange

    @staticmethod
    async def get_connector_by_title(title: str) -> ConnectorAdapter:
        for connector_adapter in ConnectorAdapter.get_adapters():
            connector_view = await connector_adapter.get_view()
            if connector_view.title.lower() == title.lower():
                return connector_adapter
        raise HTTPException(status_code=404, detail=f'Connector not found: {title}')
