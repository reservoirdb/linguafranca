from abc import ABC, abstractmethod
from pathlib import Path
from typing import Optional

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

	def filename(self) -> Optional[str]:
		return None

	def post_build(self) -> list[list[str]]:
		return []

	def file_header(self) -> str:
		return ''
