from dataclasses import dataclass
from enum import Enum

from .types_schema import *

@dataclass(frozen = True)
class TableRef:
	schema: SchemaRef
	name: str

@dataclass
class ColumnType(str, Enum):
	INT64 = 'Int64'
	STRING = 'String'
	TIMESTAMP = 'Timestamp'

@dataclass
class Column:
	name: str
	ty: ColumnType
	nullable: bool

@dataclass
class Table:
	columns: list[Column]
	sort_key: str
