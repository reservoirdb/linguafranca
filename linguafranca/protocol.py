from dataclasses import dataclass

from .types_user import *

@dataclass
class AuthLoginResponse:
	token: str

@dataclass
class AuthLoginRequest:
	account: str
	user: UserRef
	password: str
