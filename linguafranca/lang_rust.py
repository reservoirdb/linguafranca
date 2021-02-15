from dataclasses import fields, Field, is_dataclass
from enum import Enum, IntFlag
from typing import Any, get_origin, get_args, Union
from pathlib import Path
import inspect
from collections.abc import Hashable

from .lang import Lang

_type_map: dict[type, str] = {
	str: 'String',
	bool: 'bool',
}

class RustLang(Lang):
	def _derive_header(
		self,
		type_type: type,
		standard_struct: bool = True,
		default: bool = False,
		hashable: bool = False,
	) -> str:
		derives = {
			'serde::Serialize',
			'serde::Deserialize',
		}

		if standard_struct:
			derives |= {'Debug', 'Clone', 'PartialEq'}

		if issubclass(type_type, Hashable):
			derives |= {'Eq', 'Hash'}

		if default:
			derives |= {
				'Default',
			}

		# rustfmt can't keep sort for us because order is semantically useful
		derive_body = ', '.join(sorted(derives))
		return f'#[derive({derive_body})]'

	def _field_type(self, t: type) -> str:
		origin_type = get_origin(t)
		args = get_args(t)

		if origin_type == list:
			return f'Vec<{self._field_type(args[0])}>'

		if origin_type == set:
			return f'std::collections::HashSet<{self._field_type(args[0])}>'

		if origin_type == dict:
			# only strings or things that can be treated as strings in JSON
			assert args[0] == str or inspect.getmro(args[0])[1] == str
			return f'std::collections::HashMap<{self._field_type(args[0])}, {self._field_type(args[1])}>'

		if origin_type == Union:
			if len(args) == 2 and args[1] == type(None):
				return f'Option<{self._field_type(args[0])}>'

		if is_dataclass(t):
			return f'crate::types::{t.__name__}'

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
				{self._derive_header(type_type, default = True, standard_struct = False)}
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
			{self._derive_header(type_type)}
			pub enum {type_type.__name__} {{
				{variants}
			}}
			'''
		elif issubclass(type_type, (str, )):
			return f'''
			{self._derive_header(type_type)}
			pub struct {type_type.__name__}(pub {self._field_type(inspect.getmro(type_type)[1])});
			'''
		else:
			body = ' '.join([self._field(field) for field in fields(type_type)])
			return f'''
			{self._derive_header(type_type)}
			pub struct {type_type.__name__} {{
				{body}
			}}
			'''

	def post_build(self) -> list[list[str]]:
		return [
			['cargo', 'check'],
			['cargo', 'fmt', '--all'],
		]
