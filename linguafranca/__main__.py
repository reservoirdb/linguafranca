from types import ModuleType
from typing import TypeVar
import importlib
import textwrap
import shutil
from collections import defaultdict
from pathlib import Path
import subprocess
import sys
from argparse import ArgumentParser

from .lang import Lang
from .lang_rust import RustLang

T = TypeVar('T', covariant = True)

def get_exported_types(export_type: type[T], *module_names: str) -> list[type[T]]:
	modules = [importlib.import_module(m, package = __package__) for m in module_names]
	return [
		obj for module in modules for obj in module.__dict__.values()
		if isinstance(obj, type) and obj.__module__ == module.__name__ and issubclass(obj, export_type)
	]

target_types = {
	'types': get_exported_types(object, '.types_table', '.types_user'),
	'commands': get_exported_types(object, '.commands'),
}

def process_lang(lang_name: str, clean: bool, out_dir: str) -> None:
	lang_dir = Path(out_dir, lang_name)
	if clean:
		shutil.rmtree(lang_dir)

	lang_dir.mkdir(parents = True, exist_ok = True)
	shutil.copytree(Path('static', lang_name), lang_dir, dirs_exist_ok = True)

	lang_types = get_exported_types(Lang, f'.lang_{lang_name}') # type: ignore
	lang = lang_types[0]()

	output_files = {
		lang_dir / lang.source_dir() / (filename + lang.file_extension()):
		[textwrap.dedent(lang.gen_type(t)) for t in types]
		for filename, types in target_types.items()
	}

	for folder in set([p.parent for p in output_files.keys()]):
		folder.mkdir(parents = True, exist_ok = True)

	for path, contents in output_files.items():
		path.write_text('\n'.join(contents))

	for args in lang.post_build():
		subprocess.run(args, cwd = lang_dir, check = True)

parser = ArgumentParser()
parser.add_argument('--clean', action = 'store_true')
parser.add_argument('--outdir', type = str, default = 'out')
parser.add_argument('lang', nargs = '+')
args = parser.parse_args()

for lang in args.lang:
	process_lang(lang, args.clean, args.outdir)
