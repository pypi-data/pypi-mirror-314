# ~/clientfactory/session/base.py
from __future__ import annotations
import typing as t
import requests as rq
from dataclasses import dataclass, field
from clientfactory.utils.request import Request, RequestError
from clientfactory.utils.response import Response
from clientfactory.auth.base import BaseAuth
from loguru import logger as log

class SessionError(Exception):
    """Base exception for session errors"""
    pass

@dataclass
class SessionConfig:
    """Configuration for session behavior"""
    headers: dict = field(default_factory=dict)
    cookies: dict = field(default_factory=dict)
    auth: t.Optional[t.Tuple[str, str]] = None
    proxies: dict = field(default_factory=dict)
    verify: bool = True


class BaseSession:
    """
    Base session class that handles request execution and lifecycle management.
    Provides hooks for authentication and request/response processing.
    """
    def __init__(self, config: t.Optional[SessionConfig]=None, auth: t.Optional[BaseAuth]=None):
        self.config = config or SessionConfig()
        self.auth = auth
        self._session = self.__session__()

    def __session__(self) -> rq.Session:
        """Create and configure requests session"""
        session = rq.Session()
        session.headers.update(self.config.headers) # set default headers
        session.cookies.update(self.config.cookies)
        if self.config.auth:
            session.auth = self.config.auth
        if self.config.proxies:
            session.proxies.update(self.config.proxies)
        session.verify = self.config.verify
        return session

    def __prep__(self, request: Request) -> rq.Request:
        request = request.prepare()

        log.debug(f"BaseSession.__prep__ | received request headers[{request.headers}]")
        log.debug(f"BaseSession.__prep__ | session config headers[{self.config.headers}]")
        # merge headers -- session defaults with request specifics
        headers = self.config.headers.copy()
        headers.update(request.headers)

        return rq.Request(
            method=request.method.value,
            url=request.url,
            params=request.params,
            headers=headers,
            cookies=request.cookies,
            json=request.json,
            data=request.data,
            files=request.files
        )

    def execute(self, request:Request) -> Response:
        prepped = self.__prep__(request)
        log.debug(f"BaseSession.execute | executing prepared request[{prepped.__dict__}]")
        lasterror = None
        for attempt in range(request.config.maxretries):
            try:
                resp = self._session.send(
                    prepped.prepare(),
                    timeout=request.config.timeout,
                    allow_redirects=request.config.allowredirects,
                    stream=request.config.stream
                )
                return Response(
                    status_code=resp.status_code,
                    headers=dict(resp.headers),
                    raw_content=resp.content,
                    request=request
                )
            except rq.RequestException as e:
                lasterror = e
                # could add backoff logic here
                continue
        raise SessionError(f"Failed after {request.config.maxretries} attempts: {lasterror}")

    def send(self, request: Request) -> Response:
        return self.execute(request)

    def close(self):
        self._session.close()

    def __enter__(self) -> BaseSession:
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
