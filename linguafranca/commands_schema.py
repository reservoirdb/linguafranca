from dataclasses import dataclass

from .types_schema import *
from .types_table import *

@dataclass
class CreateSchema:
	name: SchemaRef
