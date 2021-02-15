from dataclasses import dataclass

from .types_user import *

@dataclass
class CreateUser:
	user: UserRef
	password: str

@dataclass
class GetUser:
	user: UserRef

@dataclass
class AssignUserRoles:
	user: UserRef
	roles: list[RoleRef]
