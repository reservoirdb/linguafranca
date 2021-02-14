from dataclasses import fields, Field
from typing import Any
from pathlib import Path

from .lang import Lang

_type_map: dict[type, str] = {
	str: 'String',
}

class RustLang(Lang):
	def _command_field(self, field: Field[Any]) -> str:
		type_name = _type_map.get(field.type, field.type.__name__)
		return f'pub {field.name}: {type_name},'

	def command_file(self, command_type: type) -> Path:
		return Path('src', 'commands.rs')

	def gen_command(self, command_type: type) -> str:
		command_fields = fields(command_type)
		body = ' '.join([self._command_field(field) for field in command_fields])
		return f'''
		#[derive(Debug, Clone, PartialEq, serde::Serialize, serde::Deserialize)]
		pub struct {self.command_name(command_type)} {{
			{body}
		}}
		'''

	def gen_type(self, type_type: type) -> str:
		...

	def post_build(self) -> list[list[str]]:
		return [
			['cargo', 'fmt', '--all'],
		]
