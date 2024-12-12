from fastapi import APIRouter

from integra_bridge.common.settings import SETTINGS
from integra_bridge.routers.v1.configuration import configuration_router
from integra_bridge.routers.v1.connector import connector_router
from integra_bridge.routers.v1.processor import processor_router
from integra_bridge.routers.v1.service import service_router

base_router = APIRouter(prefix=SETTINGS.API_PREFIX)

base_router.include_router(configuration_router)
base_router.include_router(processor_router)
base_router.include_router(connector_router)
base_router.include_router(service_router)
