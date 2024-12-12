# ~/clientfactory/auth/base.py
from __future__ import annotations
import typing as t
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from clientfactory.utils.request import Request
from clientfactory.utils.response import Response

class AuthError(Exception):
    """Base exception for authentication errors"""
    pass

@dataclass
class AuthState:
    """Represents the current state of authentication"""
    authenticated: bool = False
    token: t.Optional[str] = None
    expires: t.Optional[float] = None
    metadata: dict = field(default_factory=dict)

class BaseAuth(ABC):
    """
    Base authentication handler.
    Defines interface for different auth methods.
    """
    def __init__(self):
        self.state = AuthState()

    @abstractmethod
    def authenticate(self) -> AuthState:
        """
        Perform initial authentication.
        Should set and return AuthState.
        """
        pass

    @abstractmethod
    def prepare(self, request: Request) -> Request:
        """
        Add authentication to request.
        e.g., add tokens, keys, signatures etc.
        """
        pass

    def handle(self, response: Response) -> Response:
        """
        Process response, handle auth-related errors.
        Default implementation just checks status.
        """
        if response.status_code == 401:
            self.state.authenticated = False
            raise AuthError("Authentication failed")
        elif response.status_code == 403:
            raise AuthError("Not authorized")
        return response

    def refresh(self) -> bool:
        """
        Refresh authentication if supported.
        Returns True if refresh was successful.
        Default implementation does nothing.
        """
        return False

    @property
    def isauthenticated(self) -> bool:
        """Check if currently authenticated"""
        return self.state.authenticated

    def __call__(self, request: Request) -> Request:
        """
        Convenience method to prepare requests.
        Allows auth to be used as a callable.
        """
        return self.prepare(request)

class NoAuth(BaseAuth):
    """Authentication handler for APIs that don't require auth"""

    def authenticate(self) -> AuthState:
        self.state.authenticated = True
        return self.state

    def prepare(self, request: Request) -> Request:
        return request

class TokenAuth(BaseAuth):
    """Simple token-based authentication"""

    def __init__(self, token: str, scheme: str = "Bearer"):
        super().__init__()
        self.token = token
        self.scheme = scheme
        self.state.token = token

    def authenticate(self) -> AuthState:
        self.state.authenticated = bool(self.token)
        return self.state

    def prepare(self, request: Request) -> Request:
        if not self.token:
            raise AuthError("No token provided")

        return request.WITH(
            headers={"Authorization": f"{self.scheme} {self.token}"}
        )

class BasicAuth(BaseAuth):
    """Basic authentication using username/password"""

    def __init__(self, username: str, password: str):
        super().__init__()
        self.username = username
        self.password = password

    def authenticate(self) -> AuthState:
        self.state.authenticated = bool(self.username and self.password)
        return self.state

    def prepare(self, request: Request) -> Request:
        if not (self.username and self.password):
            raise AuthError("Username and password required")

        import base64
        auth = base64.b64encode(
            f"{self.username}:{self.password}".encode()
        ).decode()

        return request.WITH(
            headers={"Authorization": f"Basic {auth}"}
        )
