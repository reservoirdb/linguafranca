from dataclasses import dataclass
from enum import IntFlag

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
class User:
	roles: set[str]
