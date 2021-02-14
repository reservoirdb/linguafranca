from abc import ABC, abstractmethod
from pathlib import Path

class Lang(ABC):
	def command_name(self, command_type: type) -> str:
		return command_type.__name__

	@abstractmethod
	def command_file(self, command_type: type) -> Path:
		...

	@abstractmethod
	def gen_command(self, command_type: type) -> str:
		...

	@abstractmethod
	def gen_type(self, type_type: type) -> str:
		...

	def post_build(self) -> list[list[str]]:
		return []
