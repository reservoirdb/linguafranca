from dataclasses import dataclass

from .types_table import *
from .types_user import *

@dataclass
class InsertData:
	table: TableRef
	name: str
