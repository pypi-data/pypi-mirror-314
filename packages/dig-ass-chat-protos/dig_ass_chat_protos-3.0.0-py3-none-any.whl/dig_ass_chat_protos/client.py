from typing import Any
from uuid import uuid4

from agi_med_protos import HeaderClient
from loguru import logger

from . import DigitalAssistantChatManagerStub
from . import (
    DigitalAssistantChatManagerRequest,
    DigitalAssistantChatManagerResponse,
)

from . import ChatRequest, ChatHeaders

type Metadata = list[tuple[str, int | bool | str]]


class ChatManagerClient(HeaderClient[ChatRequest, ChatHeaders]):
    def __init__(self, address: str) -> None:
        super().__init__(address)
        self._stub = DigitalAssistantChatManagerStub(self._channel)

    def __call__(self, request: ChatRequest) -> str:
        metadata: Metadata = self._generate_metadata(request.headers)
        grpc_request: DigitalAssistantChatManagerRequest = request.to_grpc_request()
        response: DigitalAssistantChatManagerResponse = self._stub.GetTextResponse(grpc_request, metadata=metadata)
        return response.Text

    def _generate_metadata(self, headers: ChatHeaders, **_: Any) -> Metadata:
        if not headers.get("extra_uuid"):
            extra_uuid = str(uuid4())
            logger.warning(f"Forgot extra_uuid in headers. Will be filling {extra_uuid=}")
            headers["extra_uuid"] = extra_uuid
        metadata: Metadata = super()._generate_metadata(headers)
        return metadata
