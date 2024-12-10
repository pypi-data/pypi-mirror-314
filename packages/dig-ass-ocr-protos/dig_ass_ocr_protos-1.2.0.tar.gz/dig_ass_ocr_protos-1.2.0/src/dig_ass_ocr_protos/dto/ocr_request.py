from dataclasses import dataclass

from agi_med_protos.dto import RequestWithHeaders, Headers

from . import OcrHeaders
from .. import DocType, DigitalAssistantOCRRequest


@dataclass
class OcrRequest(RequestWithHeaders[OcrHeaders]):
    document: bytes
    type: DocType

    def to_grpc_request(self) -> DigitalAssistantOCRRequest:
        grpc_request = DigitalAssistantOCRRequest(
            Document=self.document,
            Type=self.type
        )
        return grpc_request
