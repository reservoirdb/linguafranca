from abc import ABC, abstractmethod
from pathlib import Path

class Lang(ABC):
	@abstractmethod
	def file_extension(self) -> str:
		...

	@abstractmethod
	def source_dir(self) -> str:
		...

	@abstractmethod
	def gen_type(self, type_type: type) -> str:
		...

	def post_build(self) -> list[list[str]]:
		return []
