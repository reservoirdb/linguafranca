from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional, Literal, TypedDict, Union, NewType
from dataclasses import dataclass, replace, fields
from enum import Enum
from functools import reduce

from pyparsing import nestedExpr

class PrimitiveType(Enum):
	STRING = 'string'
	I64 = 'i64'
	BOOL = 'bool'

_primitive_reverse_map = {v.value: v for v in PrimitiveType}

@dataclass
class OptionType:
	t: 'ResolvedType'

@dataclass
class VecType:
	t: 'ResolvedType'

@dataclass
class SetType:
	t: 'ResolvedType'

@dataclass
class MapType:
	k: 'ResolvedType'
	v: 'ResolvedType'

ResolvedType = Union[PrimitiveType, OptionType, VecType, SetType, MapType, 'TypeDefinition']

@dataclass
class StructDef:
	fields: dict[str, str]

@dataclass
class WrapperDef:
	wraps: str

@dataclass
class EnumDef:
	variants: list[str]

@dataclass
class FlagsDef:
	flags: list[str]

@dataclass
class InterfaceDef:
	type_name: str
	content_name: str

@dataclass
class TypeDefinition:
	name: str
	type: Union[StructDef, WrapperDef, EnumDef, FlagsDef, InterfaceDef]
	implements: Optional[list[str]]

@dataclass
class TypeProperties:
	hashable: bool = False
	equatable: bool = False
	cloneable: bool = False

def _merge_type_props(*props: TypeProperties) -> TypeProperties:
	ret = TypeProperties()

	for k in [f.name for f in fields(TypeProperties)]:
		setattr(ret, k, all([getattr(p, k) for p in props]))

	return ret

class Lang(ABC):
	def __init__(self, types_by_name: dict[str, TypeDefinition]):
		self.types_by_name = types_by_name

	def type_properties(self, t: Union[str, ResolvedType]) -> TypeProperties:
		if isinstance(t, str):
			t = self._resolve_type(t)

		if isinstance(t, PrimitiveType):
			return TypeProperties(hashable = True, equatable = True, cloneable = True)
		elif isinstance(t, OptionType):
			return self.type_properties(t.t)
		elif isinstance(t, (SetType, VecType)):
			list_props = TypeProperties(equatable = True, cloneable = True)
			return _merge_type_props(list_props, self.type_properties(t.t))
		elif isinstance(t, MapType):
			map_props = TypeProperties(equatable = True, cloneable = True)
			return _merge_type_props(map_props, self.type_properties(t.k), self.type_properties(t.v))
		elif isinstance(t, TypeDefinition):
			if isinstance(t.type, StructDef):
				return _merge_type_props(*[self.type_properties(t) for t in t.type.fields.values()])
			elif isinstance(t.type, WrapperDef):
				return self.type_properties(t.type.wraps)
			elif isinstance(t.type, (EnumDef, FlagsDef)):
				return TypeProperties(hashable = True, equatable = True, cloneable = True)
			elif isinstance(t.type, InterfaceDef):
				return TypeProperties()

	def _resolve_type(self, type_expr: str) -> ResolvedType:
		if prim_resolved := _primitive_reverse_map.get(type_expr):
			return prim_resolved

		if local_resolved := self.types_by_name.get(type_expr):
			return local_resolved

		if '<' in type_expr:
			generic_type, generic_arg_strings = nestedExpr('<', '>').parseString(f'<{type_expr}>')[0]
			generic_args = [self._resolve_type(a.removesuffix(',')) for a in generic_arg_strings]
			if generic_type == 'vec':
				return VecType(generic_args[0])
			if generic_type == 'option':
				return OptionType(generic_args[0])
			if generic_type == 'set':
				return SetType(generic_args[0])
			if generic_type == 'map':
				return MapType(generic_args[0], generic_args[1])

		raise Exception(f'failed to resolve type: {type_expr}')

	def type_str(self, t: Union[str, ResolvedType]) -> str:
		if isinstance(t, str):
			t = self._resolve_type(t)

		if isinstance(t, PrimitiveType):
			return self.primitive_type(t)
		elif isinstance(t, OptionType):
			return self.option_type(t)
		elif isinstance(t, VecType):
			return self.vec_type(t)
		elif isinstance(t, MapType):
			return self.map_type(t)
		elif isinstance(t, SetType):
			return self.set_type(t)
		elif isinstance(t, TypeDefinition):
			return self.local_type(t)

	@abstractmethod
	def file_extension(self) -> str:
		...

	@abstractmethod
	def source_dir(self) -> str:
		...

	@abstractmethod
	def filename(self) -> str:
		...

	@abstractmethod
	def make_struct(self, struct: StructDef, type: TypeDefinition) -> str:
		...

	@abstractmethod
	def make_wrapper(self, wrapper: WrapperDef, type: TypeDefinition) -> str:
		...

	@abstractmethod
	def make_enum(self, enum: EnumDef, type: TypeDefinition) -> str:
		...

	@abstractmethod
	def make_flags(self, flags: FlagsDef, type: TypeDefinition) -> str:
		...

	@abstractmethod
	def make_interface(self, interface: InterfaceDef, type: TypeDefinition) -> str:
		...

	@abstractmethod
	def primitive_type(self, t: PrimitiveType) -> str:
		...

	@abstractmethod
	def option_type(self, t: OptionType) -> str:
		...

	@abstractmethod
	def vec_type(self, t: VecType) -> str:
		...

	@abstractmethod
	def set_type(self, t: SetType) -> str:
		...

	@abstractmethod
	def map_type(self, t: MapType) -> str:
		...

	@abstractmethod
	def local_type(self, t: TypeDefinition) -> str:
		...

	def post_build(self) -> list[list[str]]:
		return []

	def file_header(self) -> str:
		return ''
