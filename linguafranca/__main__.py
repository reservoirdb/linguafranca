from typing import cast
from types import ModuleType
import importlib
import textwrap
import os
import shutil
from collections import defaultdict
from pathlib import Path
import subprocess
import sys

from .lang import Lang
from .lang_rust import RustLang

def get_all_exported_types(module: ModuleType) -> list[type]:
	return [obj for obj in module.__dict__.values() if isinstance(obj, type) and obj.__module__ == module.__name__]

types = get_all_exported_types(importlib.import_module('.types', package = __package__))
commands = get_all_exported_types(importlib.import_module('.commands', package = __package__))

def process_lang(lang_name: str) -> None:
	lang_dir = Path('out', lang_name)
	shutil.rmtree(lang_dir, ignore_errors = True)
	lang_dir.mkdir(parents = True)
	shutil.copytree(Path('static', lang_name), lang_dir, dirs_exist_ok = True)

	lang_types = get_all_exported_types(importlib.import_module(f'.lang_{lang_name}', package = __package__))
	lang = lang_types[0]()
	assert isinstance(lang, Lang)

	output_files: dict[Path, list[str]] = defaultdict(list)
	for command in commands:
		output_files[lang_dir / lang.command_file(command)].append(textwrap.dedent(lang.gen_command(command)))

	for t in types:
		output_files[lang_dir / lang.type_file(command)].append(textwrap.dedent(lang.gen_type(t)))

	for folder in set([p.parent for p in output_files.keys()]):
		os.makedirs(folder, exist_ok = True)

	for path, contents in output_files.items():
		path.write_text('\n'.join(contents))

	for args in lang.post_build():
		subprocess.run(args, cwd = lang_dir, check = True)

target_langs = sys.argv[1:]
for lang in target_langs:
	process_lang(lang)
