from dataclasses import dataclass
from enum import IntFlag

@dataclass(frozen = True)
class SchemaRef(str):
	pass

@dataclass
class Schema:
	tables: set[str]
