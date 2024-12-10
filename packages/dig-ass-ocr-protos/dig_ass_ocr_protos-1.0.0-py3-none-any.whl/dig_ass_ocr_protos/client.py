from typing import Any
from uuid import uuid4

from agi_med_protos import HeaderClient
from agi_med_protos.dto import Headers
from loguru import logger

from . import DigitalAssistantOCRStub
from . import DigitalAssistantOCRResponse
from .dto import OcrRequest

type Metadata = list[tuple[str, int | bool | str]]


class OCRClient(HeaderClient):
    def __init__(self, address: str) -> None:
        super().__init__(address)
        self._stub = DigitalAssistantOCRStub(self._channel)

    def __call__(self, request: OcrRequest) -> str:
        response: DigitalAssistantOCRResponse = self._stub.GetTextResponse(request.to_grpc_request())
        return response.Text

    def _generate_metadata(self, headers: Headers, **_: Any) -> Metadata:
        if not headers.get("extra_uuid"):
            extra_uuid = str(uuid4())
            logger.warning(f"Forgot extra_uuid in headers. Will be filling {extra_uuid=}")
            headers["extra_uuid"] = extra_uuid
        metadata: Metadata = super()._generate_metadata(headers)
        return metadata
