from typing import cast
from types import ModuleType
import importlib
import textwrap
import os
import shutil
from collections import defaultdict
from pathlib import Path
import subprocess

from .lang import Lang
from .lang_rust import RustLang

def get_all_exported_types(module: ModuleType) -> list[type]:
	return [obj for obj in module.__dict__.values() if isinstance(obj, type) and obj.__module__ == module.__name__]

commands = get_all_exported_types(importlib.import_module('.commands', package = __package__))

def process_lang(lang_name: str) -> None:
	lang_dir = Path('out', lang_name)
	shutil.rmtree(lang_dir, ignore_errors = True)
	lang_dir.mkdir(parents = True)
	shutil.copytree(Path('static', lang_name), lang_dir, dirs_exist_ok = True)

	lang_types = get_all_exported_types(importlib.import_module(f'.lang_{lang_name}', package = __package__))
	lang = lang_types[0]()
	assert isinstance(lang, Lang)

	command_files: dict[Path, list[str]] = defaultdict(list)
	for command in commands:
		command_files[lang_dir / lang.command_file(command)].append(textwrap.dedent(lang.gen_command(command)))

	for folder in set([p.parent for p in command_files.keys()]):
		os.makedirs(folder, exist_ok = True)

	for path, contents in command_files.items():
		path.write_text('\n'.join(contents))

	for args in lang.post_build():
		subprocess.run(args, cwd = lang_dir, check = True)

process_lang('rust')
