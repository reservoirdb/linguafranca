from .lang import *

_primitive_map: dict[PrimitiveType, str] = {
	PrimitiveType.STRING: 'String',
	PrimitiveType.BOOL: 'bool',
}

class RustLang(Lang):
	def file_extension(self) -> str:
		return '.rs'

	def source_dir(self) -> str:
		return 'src'

	def filename(self) -> str:
		return 'lib'

	def primitive_type(self, t: PrimitiveType) -> str:
		return _primitive_map[t]

	def option_type(self, t: OptionType) -> str:
		return f'Option<{self.type_str(t.t)}>'

	def vec_type(self, t: VecType) -> str:
		return f'Vec<{self.type_str(t.t)}>'

	def map_type(self, t: MapType) -> str:
		return f'std::collections::HashMap<{self.type_str(t.k)}, {self.type_str(t.v)}>'

	def local_type(self, t: TypeDefinition) -> str:
		return t.name

	def _derive_header(self, t: TypeDefinition) -> str:
		props = self.type_properties(t)
		derives = {'Debug', 'serde::Serialize', 'serde::Deserialize'}

		if props.equatable:
			derives |= {'PartialEq'}

		if props.hashable:
			derives |= {'Eq', 'Hash'}

		if props.cloneable:
			derives |= {'Clone'}

		derive_body = ', '.join(sorted(derives))
		return f'#[derive({derive_body})]'

	def make_struct(self, struct: StructDef, type: TypeDefinition) -> str:
		body = ' '.join([f'pub {n}: {self.type_str(f)},' for n, f in struct.fields.items()])

		return f'''
		{self._derive_header(type)}
		pub struct {type.name} {{
			{body}
		}}
		'''

	def make_wrapper(self, wrapper: WrapperDef, type: TypeDefinition) -> str:
		return f'''
		{self._derive_header(type)}
		pub struct {type.name}(pub {self.type_str(wrapper.wraps)});
		'''

	def make_enum(self, enum: EnumDef, type: TypeDefinition) -> str:
		body = ','.join(enum.variants)

		return f'''
		{self._derive_header(type)}
		pub enum {type.name} {{
			{body}
		}}
		'''

	def make_flags(self, flags: FlagsDef, type: TypeDefinition) -> str:
		body = ' '.join([f'const {f} = 1 << {i};' for i, f in enumerate(flags.flags)])

		return f'''
		bitflags::bitflags! {{
			#[derive(Default, serde::Deserialize, serde::Serialize)]
			pub struct {type.name}: u32 {{
				const NONE = 0;
				{body}
				const ALL = u32::MAX;
			}}
		}}
		'''

	def post_build(self) -> list[list[str]]:
		return [
			['cargo', 'check'],
			['cargo', 'fmt', '--all'],
		]
