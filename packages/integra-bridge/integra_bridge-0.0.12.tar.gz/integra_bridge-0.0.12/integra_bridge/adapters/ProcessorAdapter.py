from abc import abstractmethod

from integra_bridge.adapters.BaseAdapter import BaseAdapter
from integra_bridge.dto import Exchange
from integra_bridge.dto.responces.validation import ValidationResponse
from integra_bridge.entity.processor import Processor


class ProcessorAdapter(BaseAdapter):
    def __init__(self):
        super().__init__()
        ProcessorAdapter.add_adapter(self)

    def __del__(self):
        ProcessorAdapter.remove_adapter(self)

    @abstractmethod
    async def execute(self, input_body: dict, params: dict) -> Exchange:
        ...

    async def validate(self, processor: Processor) -> ValidationResponse:
        return ValidationResponse(result=True)
