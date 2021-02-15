from dataclasses import dataclass
from enum import IntFlag

@dataclass
class SchemaRef(str):
	pass

@dataclass
class Schema:
	tables: set[str]
