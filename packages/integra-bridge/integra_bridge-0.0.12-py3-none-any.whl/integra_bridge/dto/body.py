import json

from pydantic import BaseModel, Field, StrictStr, ConfigDict
from typing import Any
from pydantic.json import pydantic_encoder


class Body(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={dict: pydantic_encoder}
    )
    packet_id: StrictStr | None = Field(None, alias='packetId')
    type: StrictStr | None = None
    string_body: StrictStr = Field(alias='stringBody')
    object_string: StrictStr | None = Field(None, alias='objectString', exclude=True)
    object: Any | None = Field(None, exclude=True)
    output_body: StrictStr | None = Field(None, alias='outputBody')
    output_type: StrictStr | None = Field(None, alias='outputType')

    def __init__(self, **data):
        super().__init__(**data)
        self.object = self.parse_object()

    def parse_object(self):
        if not self.string_body or not self.string_body.strip():
            self.string_body = "{}"
        try:
            obj = json.loads(self.string_body)
            self.type = "json"
        except json.JSONDecodeError:
            obj = self.string_body
            self.type = "string"
        self.object_string = self.string_body
        return obj

    def get_type(self):
        self.parse_object()
        return self.type

    def set_string_body(self, string_body: str):
        self.string_body = string_body
        self.object = None
        self.object_string = None

    def get_output_body(self):
        try:
            obj = self.parse_object()
            return json.dumps(obj, default=pydantic_encoder)
        except Exception:
            return self.string_body

    def __str__(self):
        return (f"Body(packet_id={self.packet_id}, type={self.type}, string_body={self.string_body}, "
                f"object_string={self.object_string}, object={self.object}, output_body={self.output_body}, "
                f"output_type={self.output_type})")
