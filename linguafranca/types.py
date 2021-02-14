from dataclasses import dataclass
from enum import Enum

@dataclass
class TableRef:
	schema: str
	name: str

@dataclass
class ColumnType(str, Enum):
	INT64 = 'Int64'
	STRING = 'String'

@dataclass
class Column:
	name: str
	ty: ColumnType
	nullable: bool

@dataclass
class Table:
	columns: list[Column]
