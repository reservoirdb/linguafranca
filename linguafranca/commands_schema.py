from dataclasses import dataclass

from .types_schema import *
from .types_table import *

from . import Command

@dataclass
class CreateSchema(Command):
	name: SchemaRef
