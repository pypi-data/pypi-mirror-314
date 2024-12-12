from pydantic import BaseModel, StrictStr, Field

from integra_bridge.common.enums import DataSendingStatus


class OutputStatus(BaseModel):
    status: DataSendingStatus = Field(default=DataSendingStatus.success.value)
    error_message: StrictStr | None = None
