from dataclasses import dataclass

from .types_schema import *
from .types_user import *

from . import Command

@dataclass
class CreateUser(Command):
	user: UserRef
	password: str

@dataclass
class GetUser(Command):
	user: UserRef

@dataclass
class AssignUserRoles(Command):
	user: UserRef
	roles: list[RoleRef]

@dataclass
class CreateRole(Command):
	role: RoleRef

@dataclass
class GrantSchemaPermissions(Command):
	role: RoleRef
	schema: SchemaRef
	permissions: SchemaPermissions

@dataclass
class GrantGlobalSchemaPermissions(Command):
	role: RoleRef
	permissions: SchemaPermissions

@dataclass
class GrantDatabasePermissions(Command):
	role: RoleRef
	permissions: DatabasePermissions
