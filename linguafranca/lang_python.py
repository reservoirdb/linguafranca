from dataclasses import fields, Field, is_dataclass
from enum import Enum, IntFlag
from typing import Any, get_origin, get_args, Union, Protocol, Optional
from pathlib import Path
import inspect
from collections.abc import Hashable

from .lang import Lang

class PythonLang(Lang):
	def file_extension(self) -> str:
		return '.py'

	def source_dir(self) -> str:
		return 'reservoirdb_protocol'

	def filename(self) -> Optional[str]:
		return 'types'

	def _first_mro_or_none(self, ty: type) -> Optional[type]:
		mro = inspect.getmro(ty)
		if len(mro) >= 2:
			return mro[1]
		return None

	def _is_protocol(self, ty: type) -> bool:
		return self._first_mro_or_none(ty) == Protocol # type: ignore

	def _field_type(self, t: type) -> str:
		origin_type = get_origin(t)
		args = get_args(t)

		if origin_type == list:
			return f'typing.List[{self._field_type(args[0])}]'

		if origin_type == set:
			return f'typing.Set[{self._field_type(args[0])}]'

		if origin_type == dict:
			# only strings or things that can be treated as strings in JSON
			assert args[0] == str or inspect.getmro(args[0])[1] == str
			return f'typing.Dict[{self._field_type(args[0])}, {self._field_type(args[1])}]'

		if origin_type == Union:
			if len(args) == 2 and args[1] == type(None):
				return f'typing.Optional[{self._field_type(args[0])}]'

		if is_dataclass(t):
			return f'\'{t.__name__}\''

		if self._is_protocol(t):
			return f'\'Tagged{t.__name__}\''

		return t.__name__

	def gen_type(self, type_type: type) -> str:
		if issubclass(type_type, IntFlag):
			variants = '; '.join([f'{t.name} = \'{t.value}\'' for t in type_type])
			return f'''
			@dataclass
			class {type_type.__name__}(enum.IntFlag):
				{variants}
			'''
		elif issubclass(type_type, Enum):
			variants = '; '.join([f'{t.name} = \'{t.value}\'' for t in type_type])
			return f'''
			@dataclass
			class {type_type.__name__}(enum.Enum):
				{variants}
			'''
		elif issubclass(type_type, (str, )):
			return f'''
			@dataclass
			class {type_type.__name__}({inspect.getmro(type_type)[1].__name__}):
				pass
			'''
		else:
			traits_to_impl = [base for base in inspect.getmro(type_type)[1:] if self._is_protocol(base)]
			class_fields = [f'{f.name}: {self._field_type(f.type)}' for f in fields(type_type)]
			body = '; '.join(class_fields) if class_fields else 'pass'
			inherits = '(' + ', '.join([t.__name__ for t in traits_to_impl]) + ')' if traits_to_impl else ''
			return f'''
			@dataclass
			class {type_type.__name__}{inherits}:
				{body}
			'''

	def file_header(self) -> str:
		return '''
		import typing
		import enum
		from dataclasses import dataclass

		from . import Command, TxnResult, TaggedCommand, TaggedTxnResult
		'''

	def post_build(self) -> list[list[str]]:
		return [
			['mypy', '.'],
		]
