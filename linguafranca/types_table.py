from dataclasses import dataclass
from enum import Enum
from typing import Optional

from .types_schema import *
from . import TxnResult

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
class Table(TxnResult):
	columns: list[Column]
	sort_key: Optional[str]
