__version__ = "1.2.0"

from .DigitalAssistantOCR_pb2 import DigitalAssistantOCRRequest, DigitalAssistantOCRResponse, DocType
from .DigitalAssistantOCR_pb2_grpc import (
    DigitalAssistantOCR,
    DigitalAssistantOCRServicer,
    DigitalAssistantOCRStub
)

from .dto import OcrRequest, OcrHeaders
from .client import OCRClient