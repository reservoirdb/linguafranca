import os
from .lang import *

_primitive_map: dict[PrimitiveType, str] = {
	PrimitiveType.STRING: 'string',
	PrimitiveType.BOOL: 'boolean',
}

npm_cmd = 'npm'

if os.name == 'nt':
	npm_cmd += '.cmd'

class TypeScriptLang(Lang):
	def file_extension(self) -> str:
		return '.ts'

	def source_dir(self) -> str:
		return 'src'

	def filename(self) -> str:
		return 'main'

	def primitive_type(self, t: PrimitiveType) -> str:
		return _primitive_map[t]

	def option_type(self, t: OptionType) -> str:
		return f'({self.type_str(t.t)} | undefined)'

	def vec_type(self, t: VecType) -> str:
		return f'{self.type_str(t.t)}[]'

	def map_type(self, t: MapType) -> str:
		# typescript index exprs require string | number keys
		# can't type this properly with wrapper type aliases :(
		return f'{{ [key: string]: {self.type_str(t.v)} }}'

	def set_type(self, t: SetType) -> str:
		return f'{self.type_str(t.t)}[]'

	def local_type(self, t: TypeDefinition) -> str:
		return t.name

	def _field(self, name: str, field_type_expr: str, struct: StructDef) -> str:
		optional_flag = ''
		if not struct.required or (isinstance(struct.required, list) and name not in struct.required):
			optional_flag += '?'

		return f'{name}{optional_flag}: {self.type_str(field_type_expr)}'

	def make_struct(self, struct: StructDef, type: TypeDefinition) -> str:
		body = '; '.join([self._field(n, f, struct) for n, f in struct.fields.items()])

		return f'''
		export interface {type.name} {{
			type: '{type.name}',
			{body}
		}}
		'''

	def make_wrapper(self, wrapper: WrapperDef, type: TypeDefinition) -> str:
		return f'''
		export type {type.name} = {self.type_str(wrapper.wraps)}
		'''

	def make_enum(self, enum: EnumDef, type: TypeDefinition) -> str:
		body = ', '.join([f'{v} = \'{v}\'' for v in enum.variants])
		return f'''
		export enum {type.name} {{
			{body}
		}}
		'''

	def make_flags(self, flags: FlagsDef, type: TypeDefinition) -> str:
		body = ' '.join([f'{f} = 1 << {i},' for i, f in enumerate(flags.flags)])
		return f'''
		export enum {type.name} {{
			NONE = 0,
			{body}
			ALL = 0xffffffff,
		}}
		'''

	def make_interface(self, interface: InterfaceDef, type: TypeDefinition) -> str:
		implementations = ' | '.join([t.name for t in self.implementations_of(type.name)])

		return f'''
		export type {type.name} = ({implementations})
		'''

	def post_build(self) -> list[list[str]]:
		return [
			[npm_cmd, 'install'],
			[npm_cmd, 'run', 'build'],
		]
