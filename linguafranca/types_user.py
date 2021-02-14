from dataclasses import dataclass
from enum import IntFlag

@dataclass
class DatabasePermissions(IntFlag):
	NONE = 0
	MANAGE_ROLES = 1 << 0
	MANAGE_SCHEMAS = 1 << 1

@dataclass
class SchemaPermissions(IntFlag):
	NONE = 0
	MANAGE_ACCESS = 1 << 0
	MANAGE_TABLES = 1 << 1
	WRITE_TABLE = 1 << 2
	READ_TABLE = 1 << 3

@dataclass
class UserRef:
	name: str

@dataclass
class RoleRef:
	name: str

@dataclass
class User:
	roles: set[str]
