from dataclasses import dataclass

from .types_user import *
from . import Command, TxnResult

@dataclass
class AuthLoginResponse:
	token: str

@dataclass
class AuthLoginRequest:
	account: str
	user: UserRef
	password: str

@dataclass(eq = False)
class TxnRequest:
	commands: list[Command]

@dataclass(eq = False)
class TxnResponse:
	results: list[TxnResult]

@dataclass
class QueryRequest:
	query: str
