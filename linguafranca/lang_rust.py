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

	def set_type(self, t: SetType) -> str:
		return f'std::collections::HashSet<{self.type_str(t.t)}>'

	def local_type(self, t: TypeDefinition) -> str:
		if isinstance(t.type, InterfaceDef):
			return f'Box<dyn {t.name}>'
		return t.name

	def _derive_header(self, t: TypeDefinition) -> str:
		props = self.type_properties(t)
		derives = {'serde::Serialize', 'serde::Deserialize'}

		if props.debuggable:
			derives |= {'Debug'}

		if props.equatable:
			derives |= {'PartialEq'}

		if props.hashable:
			derives |= {'Eq', 'Hash'}

		if props.cloneable:
			derives |= {'Clone'}

		derive_body = ', '.join(sorted(derives))
		return f'#[derive({derive_body})]'

	def _trait_impl(self, type_name: str, interface_name: str) -> str:
		return f'''
		#[typetag::serde]
		impl {interface_name} for {type_name} {{
			fn as_any(&self) -> &dyn std::any::Any {{
				self
			}}
		}}
		'''

	def _trait_impls(self, type: TypeDefinition) -> str:
		return '\n'.join([self._trait_impl(type.name, t) for t in type.implements]) if type.implements else ''

	def _field(self, name: str, field_type_expr: str, struct: StructDef) -> str:
		prefix = ''
		if not struct.required or (isinstance(struct.required, list) and name not in struct.required):
			prefix += '#[serde(default)] '

		return f'{prefix}pub {name}: {self.type_str(field_type_expr)},'

	def make_struct(self, struct: StructDef, type: TypeDefinition) -> str:
		body = ' '.join([self._field(n, f, struct) for n, f in struct.fields.items()])

		return f'''
		{self._derive_header(type)}
		pub struct {type.name} {{
			{body}
		}}
		''' + self._trait_impls(type)

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
			#[derive(Default)]
			pub struct {type.name}: u32 {{
				const NONE = 0;
				{body}
				const ALL = u32::MAX;
			}}
		}}

		bitflags_serde_shim::impl_serde_for_bitflags!({type.name});
		'''

	def make_interface(self, interface: InterfaceDef, type: TypeDefinition) -> str:
		return f'''
		#[typetag::serde(tag = "type")]
		pub trait {type.name}: 'static {{
			fn as_any(&self) -> &dyn std::any::Any;
		}}
		'''

	def post_build(self) -> list[list[str]]:
		return [
			['cargo', 'check'],
			['cargo', 'fmt', '--all'],
		]
