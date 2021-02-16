from dataclasses import dataclass

from .types_user import *

@dataclass
class AuthLoginResponse:
	token: str

@dataclass
class AuthLoginRequest:
	user: UserRef
	password: str
