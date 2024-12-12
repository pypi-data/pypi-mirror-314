from fastapi.responses import FileResponse

from integra_bridge.adapters import ProcessorAdapter, ConnectorAdapter
from integra_bridge.api_router import APIRouter
from integra_bridge.dto.responces.external_service import ExternalServiceConfigResponse
from integra_bridge.common.dependency_manager import dm

configuration_router = APIRouter(prefix='/configuration', tags=["Работа с конфигурациями внешних сервисов"])


@configuration_router.get(
    path='/',
    response_model=ExternalServiceConfigResponse,
    response_model_exclude_none=True,
    response_model_by_alias=True
)
async def get_configurations():
    processors = ProcessorAdapter.get_adapters()
    processor_views = []
    for processor in processors:
        processor_view = await processor.get_view()
        processor_views.append(processor_view)

    connectors = ConnectorAdapter.get_adapters()
    connector_views = []
    for connector in connectors:
        connector_view = await connector.get_view()
        connector_views.append(connector_view)

    response = ExternalServiceConfigResponse(
        service_name=dm.title,
        service_address=dm.address,
        application_start_date=dm.application_start_date,
        processor_views=processor_views,
        connector_views=connector_views,
        manual_file_name=dm.manual_path.name
    )
    return response


@configuration_router.get(
    path='/manual'
)
async def get_configurations():
    manual_path = dm.manual_path
    if manual_path.exists():
        return FileResponse(manual_path, media_type='application/octet-stream', filename=dm.manual_path.name)
    else:
        return {"error": "File not found"}
