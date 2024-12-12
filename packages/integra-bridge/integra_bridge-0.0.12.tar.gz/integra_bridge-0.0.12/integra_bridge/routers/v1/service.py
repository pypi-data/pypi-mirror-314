from starlette import status
from integra_bridge.api_router import APIRouter

from fastapi import Response

service_router = APIRouter(prefix='/service', tags=["Обслуживание сервиса"])


@service_router.get('/checkhealth')
async def checkhealth():
    return Response(status_code=status.HTTP_200_OK)
