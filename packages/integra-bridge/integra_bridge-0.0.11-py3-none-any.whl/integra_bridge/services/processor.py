import json
import traceback

from orjson import orjson
from pydantic import ValidationError

from integra_bridge.adapters.ProcessorAdapter import ProcessorAdapter
from fastapi import HTTPException, Request
from starlette import status

from integra_bridge.dto import Exchange
from integra_bridge.dto.responces.validation import ValidationResponse
from integra_bridge.entity.processor import Processor


class ProcessorHandler:
    @classmethod
    async def execute(cls, request: Request, processor_title: str) -> Exchange:
        processor_adapter = await cls.get_processor_by_title(processor_title)

        try:
            exchange = await request.json()
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Input body is not JSON serializable")
        input_body = exchange.get("body", {}).get("stringBody", {})
        try:
            inner_body = orjson.loads(input_body)
        except ValueError:
            inner_body = input_body

        params = exchange.get("processor", {}).get("params", {})
        try:
            updated_body = await processor_adapter.execute(inner_body, params)
        except Exception as e:
            exception = traceback.format_exc()
            exception_lines = exception.splitlines()[3:]
            formatted_exception = "\n".join(exception_lines).strip()
            formatted_exception = formatted_exception[2:]
            exchange["exception"] = str(e)
            exchange['stackTrace'] = formatted_exception
            updated_body = inner_body
        try:
            updated_body = json.dumps(updated_body, ensure_ascii=False)
            body_type = "json"
        except Exception:
            body_type = "string"
        exchange["body"]["type"] = body_type
        exchange["body"]["stringBody"] = updated_body
        try:
            exchange = Exchange(**exchange)
        except ValidationError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        return exchange

    @classmethod
    async def validate(cls, processor: Processor, title: str) -> ValidationResponse:
        try:
            processor_adapter = await cls.get_processor_by_title(title)
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        return await processor_adapter.validate(processor)

    @classmethod
    async def get_processor_by_title(cls, title: str) -> ProcessorAdapter:
        for processor_adapter in ProcessorAdapter.get_adapters():
            processor_view = await processor_adapter.get_view()
            if processor_view.title.lower() == title.lower():
                return processor_adapter
        raise HTTPException(status_code=404, detail=f'Processor not found: {title} ')
