from dataclasses import dataclass

from .types_table import *

from . import Command

@dataclass
class CreateTable(Command):
	table: TableRef
	table_def: Table

@dataclass
class GetTable(Command):
	table: TableRef

@dataclass
class AlterTable(Command):
	table: TableRef
	new_columns: list[Column]

@dataclass
class DeleteTable(Command):
	table: TableRef

@dataclass
class InsertData(Command):
	table: TableRef
	data_ref: str
