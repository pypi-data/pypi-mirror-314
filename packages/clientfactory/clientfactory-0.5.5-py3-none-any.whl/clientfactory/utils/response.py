# ~/clientfactory/utils/response.py
from __future__ import annotations
import typing as t
import json
from dataclasses import dataclass, field
from http import HTTPStatus

class ResponseError(Exception):
    """Base exception for response-related errors"""
    pass

class HTTPError(ResponseError):
    """Raised when response indicates HTTP error"""
    def __init__(self, response: Response):
        self.response = response
        super().__init__(
            f"HTTP {response.status_code} {response.reason}: {response.url}"
        )

@dataclass
class Response:
    """HTTP Response representation"""
    status_code: int
    headers: dict
    raw_content: bytes
    request: "Request"  # from request.py
    _parsedjson: t.Optional[t.Any] = field(default=None, repr=False)

    @property
    def ok(self) -> bool:
        """Whether the request was successful"""
        return 200 <= self.status_code < 300

    @property
    def reason(self) -> str:
        """HTTP status reason"""
        return HTTPStatus(self.status_code).phrase

    @property
    def url(self) -> str:
        """URL that was requested"""
        return self.request.url

    @property
    def content(self) -> bytes:
        """Raw response content"""
        return self.raw_content

    @property
    def text(self) -> str:
        """Response content as text"""
        return self.raw_content.decode('utf-8')

    def json(self, **kwargs) -> t.Any:
        """
        Parse response content as JSON
        Results are cached after first call
        """
        if self._parsedjson is None:
            try:
                self._parsedjson = json.loads(self.text, **kwargs)
            except json.JSONDecodeError as e:
                raise ResponseError(f"Invalid JSON response: {e}")
        return self._parsedjson

    def raise_for_status(self) -> None:
        """Raise HTTPError if status indicates error"""
        if not self.ok:
            raise HTTPError(self)

    def __bool__(self) -> bool:
        """Truth value is based on ok property"""
        return self.ok

    def WITH(self, **updates) -> Response:
        """Create new response with updates"""
        fields = {
            'status_code': self.status_code,
            'headers': self.headers.copy(),
            'raw_content': self.raw_content,
            'request': self.request,
            '_parsedjson': self._parsedjson
        }

        UPDATEABLE = {'headers'}
        for k, v in updates.items():
            if k.lower() in UPDATEABLE and v is not None:
                fields[k].update(v)  # merge dicts for updateable fields
            else:
                fields[k] = v  # replace for other fields

        return self.__class__(**fields)
