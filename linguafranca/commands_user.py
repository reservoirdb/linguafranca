from dataclasses import dataclass

from .types_schema import *
from .types_user import *
from .types_compute import *

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
class GrantComputeClusterPermissions(Command):
	role: RoleRef
	compute_cluster: ComputeClusterRef
	permissions: ComputeClusterPermissions

@dataclass
class GrantGlobalComputeClusterPermissions(Command):
	role: RoleRef
	permissions: ComputeClusterPermissions

@dataclass
class GrantDatabasePermissions(Command):
	role: RoleRef
	permissions: DatabasePermissions
