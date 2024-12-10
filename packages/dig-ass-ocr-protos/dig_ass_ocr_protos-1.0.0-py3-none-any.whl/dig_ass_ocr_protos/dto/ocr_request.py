from dataclasses import dataclass

from agi_med_protos.dto import RequestWithHeaders, Headers

from .. import DocType, DigitalAssistantOCRRequest


@dataclass
class OcrRequest(RequestWithHeaders[Headers]):
    document: bytes
    type: DocType

    def to_grpc_request(self) -> DigitalAssistantOCRRequest:
        grpc_request = DigitalAssistantOCRRequest(
            Document=self.document,
            Type=self.type
        )
        return grpc_request
