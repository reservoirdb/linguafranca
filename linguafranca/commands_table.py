from dataclasses import dataclass

from .types_table import *

@dataclass
class CreateTable:
	table: TableRef
	table_def: Table

@dataclass
class GetTable:
	table: TableRef

@dataclass
class AlterTable:
	table: TableRef
	new_columns: list[Column]

@dataclass
class DeleteTable:
	table: TableRef

@dataclass
class InsertData:
	table: TableRef
	name: str
