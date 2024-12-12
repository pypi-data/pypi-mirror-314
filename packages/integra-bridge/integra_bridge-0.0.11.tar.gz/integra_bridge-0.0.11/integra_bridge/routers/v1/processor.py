from typing import Annotated

from fastapi import APIRouter, Request, Query
from starlette import status
from integra_bridge.dto import Exchange
from integra_bridge.dto.responces.validation import ValidationResponse
from integra_bridge.entity.processor import Processor
from integra_bridge.services.processor import ProcessorHandler

processor_router = APIRouter(prefix="/processor", tags=["Процессоры"])


@processor_router.post(
    path='/execute',
    status_code=status.HTTP_200_OK,
    response_model=list[Exchange]
)
async def execute(
        request: Request,
        processor_title: Annotated[str, Query(alias='processorTitle')]
):
    exchange = await ProcessorHandler.execute(request=request, processor_title=processor_title)
    return [exchange]


@processor_router.post(
    path='/validation',
    status_code=status.HTTP_200_OK,
    response_model=ValidationResponse
)
async def validate(
        processor: Processor,
        title: Annotated[str, Query(alias='processorTitle')]
):
    return await ProcessorHandler.validate(processor, title=title)
