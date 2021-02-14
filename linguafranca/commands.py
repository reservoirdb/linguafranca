from dataclasses import dataclass

from .types import *

@dataclass
class InsertData:
	table: TableRef
	name: str
