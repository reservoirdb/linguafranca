from dataclasses import fields, Field, is_dataclass
from enum import Enum, IntFlag
from typing import Any, get_origin, get_args
from pathlib import Path
import inspect

from .lang import Lang

_type_map: dict[type, str] = {
	str: 'String',
	bool: 'bool',
}

class RustLang(Lang):
	def _field_type(self, t: type) -> str:
		origin_type = get_origin(t)
		args = get_args(t)

		if origin_type == list:
			return f'Vec<{self._field_type(args[0])}>'
		elif origin_type == set:
			return f'std::collections::HashSet<{self._field_type(args[0])}>'
		elif is_dataclass(t):
			return f'crate::types::{t.__name__}'
		else:
			return _type_map[t]

	def _field(self, field: Field[Any]) -> str:
		return f'pub {field.name}: {self._field_type(field.type)},'

	def file_extension(self) -> str:
		return '.rs'

	def source_dir(self) -> str:
		return 'src'

	def gen_type(self, type_type: type) -> str:
		if issubclass(type_type, IntFlag):
			variants = ' '.join([f'const {t.name} = {t.value};' for t in type_type])
			return f'''
			bitflags::bitflags! {{
				#[derive(Default, serde::Serialize, serde::Deserialize)]
				pub struct {type_type.__name__}: u32 {{
					const NONE = 0;
					{variants}
					const ALL = u32::MAX;
				}}
			}}
			'''
		elif issubclass(type_type, Enum):
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
