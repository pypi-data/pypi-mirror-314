from typing import Annotated

from fastapi import APIRouter, Request, Query
from starlette import status

from integra_bridge.dto import Exchange
from integra_bridge.dto.responces.validation import ValidationResponse
from integra_bridge.entity.connector import Connector
from integra_bridge.services.connector import ConnectorHandler

connector_router = APIRouter(prefix="/connector", tags=["Коннекторы"])


@connector_router.post(
    path='/output',
    status_code=status.HTTP_200_OK,
    response_model_by_alias=True
)
async def output(
        request: Request,
        title: Annotated[str, Query(alias='connectorTitle')]
):
    return await ConnectorHandler.execute_output_exchange(request=request, title=title)


@connector_router.post(
    path='/validateOutput',
    status_code=status.HTTP_200_OK,
    response_model=ValidationResponse
)
async def validate_output(
        connector: Connector,
        title: Annotated[str, Query(alias='connectorTitle')]
):
    return await ConnectorHandler.validate_output(connector, title=title)


@connector_router.post(
    path='/validateInput',
    status_code=status.HTTP_200_OK,
    response_model=ValidationResponse
)
async def validate_output(
        connector: Connector,
        title: Annotated[str, Query(alias='connectorTitle')]
):
    return await ConnectorHandler.validate_input(connector, title=title)


@connector_router.post(
    path='/deployInput',
    status_code=status.HTTP_200_OK,
    response_model_by_alias=True,
    response_model=Exchange
)
async def deploy_input(
        request: Request,
        title: Annotated[str, Query(alias='connectorTitle')]
):
    return await ConnectorHandler.deploy_input(request=request, title=title)


@connector_router.post(
    path='/destroyInput',
    status_code=status.HTTP_200_OK,
    response_model_by_alias=True,
    response_model=Exchange
)
async def destroy_input(
        request: Request,
        title: Annotated[str, Query(alias='connectorTitle')]
):
    return await ConnectorHandler.destroy_input(request=request, title=title)
