from dataclasses import dataclass
from enum import IntFlag

from .types_schema import SchemaRef
from . import TxnResult

@dataclass
class DatabasePermissions(IntFlag):
	MANAGE_ROLES = 1 << 0
	MANAGE_SCHEMAS = 1 << 1

@dataclass
class SchemaPermissions(IntFlag):
	MANAGE_ACCESS = 1 << 0
	MANAGE_TABLES = 1 << 1
	WRITE_TABLE = 1 << 2
	READ_TABLE = 1 << 3

@dataclass(frozen = True)
class UserRef(str):
	pass

@dataclass(frozen = True)
class RoleRef(str):
	pass

@dataclass
class User(TxnResult):
	roles: set[RoleRef]

@dataclass
class Role(TxnResult):
	database_permissions: DatabasePermissions
	global_schema_permissions: SchemaPermissions
	schema_permissions: dict[SchemaRef, SchemaPermissions]
