from typing import Any
from uuid import uuid4

from agi_med_protos import HeaderClient
from loguru import logger

from . import DigitalAssistantTextRequest, DigitalAssistantTextResponse, DigitalAssistantTextStub
from .dto import TextRequest, TextHeaders

type Metadata = list[tuple[str, int | bool | str]]


class TextClient(HeaderClient[TextRequest, TextHeaders]):
    def __init__(self, address: str) -> None:
        super().__init__(address)
        self._stub = DigitalAssistantTextStub(self._channel)  # type: ignore[no-untyped-call]

    def __call__(self, request: TextRequest) -> str:
        metadata: Metadata = self._generate_metadata(request.headers)
        grpc_request: DigitalAssistantTextRequest = request.to_grpc_request()
        response: DigitalAssistantTextResponse = self._stub.GetTextResponse(grpc_request, metadata=metadata)
        return response.Text

    def _generate_metadata(self, headers: TextHeaders, **_: Any) -> Metadata:
        if not headers.get("extra_uuid"):
            extra_uuid = str(uuid4())
            logger.warning(f"Forgot extra_uuid in headers. Will be filling {extra_uuid=}")
            headers["extra_uuid"] = extra_uuid
        metadata: Metadata = super()._generate_metadata(headers)
        return metadata
