from dataclasses import dataclass
from enum import IntFlag

from . import TxnResult

@dataclass(frozen = True)
class SchemaRef(str):
	pass

@dataclass
class Schema(TxnResult):
	tables: set[str]
