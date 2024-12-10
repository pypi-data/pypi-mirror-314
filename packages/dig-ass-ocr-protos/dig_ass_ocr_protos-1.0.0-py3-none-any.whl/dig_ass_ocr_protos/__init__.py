__version__ = "1.0.0"

from .DigitalAssistantOCR_pb2 import DigitalAssistantOCRRequest, DigitalAssistantOCRResponse, DocType
from .DigitalAssistantOCR_pb2_grpc import (
    DigitalAssistantOCR,
    DigitalAssistantOCRServicer,
    DigitalAssistantOCRStub
)

from .dto import OcrRequest
from .client import OCRClient