from dataclasses import fields, Field
from enum import Enum
from typing import Any, get_origin, get_args
from pathlib import Path
import inspect

from .lang import Lang
from . import types

_type_map: dict[type, str] = {
	str: 'String',
	bool: 'bool',
}

class RustLang(Lang):
	def _field_type(self, t: type) -> str:
		origin_type = get_origin(t)
		args = get_args(t)

		if origin_type == list:
			type_name = f'Vec<{self._field_type(args[0])}>'
		elif t.__module__ == types.__name__:
			type_name = f'crate::types::{t.__name__}'
		else:
			type_name = _type_map[t]

		return type_name

	def _field(self, field: Field[Any]) -> str:
		return f'pub {field.name}: {self._field_type(field.type)},'

	def command_file(self, command_type: type) -> Path:
		return Path('src', 'commands.rs')

	def type_file(self, type_type: type) -> Path:
		return Path('src', 'types.rs')

	def gen_command(self, command_type: type) -> str:
		body = ' '.join([self._field(field) for field in fields(command_type)])
		return f'''
		#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize)]
		pub struct {command_type.__name__} {{
			{body}
		}}
		'''

	def gen_type(self, type_type: type) -> str:
		if issubclass(type_type, Enum):
			variants = ','.join([v.value for v in type_type])
			return f'''
			#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize)]
			pub enum {type_type.__name__} {{
				{variants}
			}}
			'''
		else:
			body = ' '.join([self._field(field) for field in fields(type_type)])
			return f'''
			#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize)]
			pub struct {type_type.__name__} {{
				{body}
			}}
			'''

	def post_build(self) -> list[list[str]]:
		return [
			['cargo', 'fmt', '--all'],
			['cargo', 'check'],
		]
