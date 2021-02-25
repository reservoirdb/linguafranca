from .lang import *

_primitive_map: dict[PrimitiveType, str] = {
	PrimitiveType.STRING: 'str',
	PrimitiveType.BOOL: 'bool',
}

class PythonLang(Lang):
	def file_extension(self) -> str:
		return '.py'

	def source_dir(self) -> str:
		return 'reservoirdb_protocol'

	def filename(self) -> str:
		return '__init__'

	def file_header(self) -> str:
		return '''
		import dataclasses
		import typing
		import typing_extensions
		import enum
		'''

	def primitive_type(self, t: PrimitiveType) -> str:
		return _primitive_map[t]

	def option_type(self, t: OptionType) -> str:
		return f'typing.Optional[{self.type_str(t.t)}]'

	def vec_type(self, t: VecType) -> str:
		return f'typing.List[{self.type_str(t.t)}]'

	def map_type(self, t: MapType) -> str:
		return f'typing.Dict[{self.type_str(t.k)}, {self.type_str(t.v)}]'

	def set_type(self, t: SetType) -> str:
		return f'typing.Set[{self.type_str(t.t)}]'

	def local_type(self, t: TypeDefinition) -> str:
		return f'\'{t.name}\''

	def make_struct(self, struct: StructDef, type: TypeDefinition) -> str:
		body = ';'.join([f'{n}: {self.type_str(f)}' for n, f in struct.fields.items()])

		return f'''
		@dataclasses.dataclass
		class {type.name}:
			{body}
			type: typing.Literal['{type.name}'] = '{type.name}'
		'''

	def make_wrapper(self, wrapper: WrapperDef, type: TypeDefinition) -> str:
		return f'''
		class {type.name}({self.type_str(wrapper.wraps)}):
			pass
		'''

	def make_enum(self, enum: EnumDef, type: TypeDefinition) -> str:
		body = '; '.join([f'{v.upper()} = \'{v}\'' for v in enum.variants])
		return f'''
		class {type.name}(str, enum.Enum):
			{body}
		'''

	def make_flags(self, flags: FlagsDef, type: TypeDefinition) -> str:
		body = ' '.join([f'{f} = 1 << {i};' for i, f in enumerate(flags.flags)])

		return f'''
		class {type.name}(enum.IntFlag):
			{body}
		'''

	def make_interface(self, interface: InterfaceDef, type: TypeDefinition) -> str:
		implementations = ', '.join([t.name for t in self.implementations_of(type.name)])
		return f'''
		{type.name} = typing.Union[{implementations}]
		'''

	def post_build(self) -> list[list[str]]:
		return [
			['mypy', '.'],
			['yapf', '-ir', 'reservoirdb_protocol'],
		]
