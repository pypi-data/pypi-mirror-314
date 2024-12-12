import json
from typing import Any, Optional

from pydantic_core import to_jsonable_python
from temporalio.api.common.v1 import Payload
from temporalio.converter import (
    CompositePayloadConverter,
    DataConverter,
    DefaultPayloadConverter,
    JSONPlainPayloadConverter,
)

class PydanticJSONPayloadConverter(JSONPlainPayloadConverter):
    """Pydantic JSON payload converter.

    This extends the :py:class:`JSONPlainPayloadConverter` to override
    :py:meth:`to_payload` using the Pydantic encoder.
    """

    def to_payload(self, value: Any) -> Optional[Payload]:
        """Convert values with Pydantic encoder, fallback to default if fails."""
        try:
            # Attempt to convert using Pydantic
            return Payload(
                metadata={"encoding": self.encoding.encode()},
                data=json.dumps(value, separators=(",", ":"), sort_keys=True, default=to_jsonable_python).encode(),
            )
        except (TypeError, ValueError):
            # Fallback to default JSON conversion
            return super().to_payload(value)


class PydanticPayloadConverter(CompositePayloadConverter):
    """Payload converter that replaces Temporal JSON conversion with Pydantic
    JSON conversion.
    """

    def __init__(self) -> None:
        super().__init__(
            *(
                c
                if not isinstance(c, JSONPlainPayloadConverter)
                else PydanticJSONPayloadConverter()
                for c in DefaultPayloadConverter.default_encoding_payload_converters
            )
        )


pydantic_data_converter = DataConverter(
    payload_converter_class=PydanticPayloadConverter
)
"""Data converter using Pydantic JSON conversion."""