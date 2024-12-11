from dataclasses import dataclass
from typing import Any

from agi_med_common.models import OuterContextItem
from agi_med_protos.dto import RequestWithHeaders
from google.protobuf.json_format import ParseDict

from . import ChatHeaders
from .. import DigitalAssistantChatManagerRequest


@dataclass
class ChatRequest(RequestWithHeaders[ChatHeaders]):
    text: str
    outer_context: OuterContextItem

    def to_grpc_request(self) -> DigitalAssistantChatManagerRequest:
        grpc_request = DigitalAssistantChatManagerRequest()
        req_dict: dict[str, Any] = {"Text": self.text, "OuterContext": self.outer_context.model_dump(by_alias=True)}
        ParseDict(req_dict, grpc_request, ignore_unknown_fields=True)
        return grpc_request
