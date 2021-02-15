from dataclasses import dataclass

from .types_schema import *
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

@dataclass
class CreateRole:
	role: RoleRef

@dataclass
class GrantSchemaPermissions:
	role: RoleRef
	schema: SchemaRef
	permissions: SchemaPermissions

@dataclass
class GrantGlobalSchemaPermissions:
	role: RoleRef
	permissions: SchemaPermissions

@dataclass
class GrantDatabasePermissions:
	role: RoleRef
	permissions: DatabasePermissions
