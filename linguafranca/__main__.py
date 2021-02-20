import textwrap
import shutil
from collections import defaultdict
from pathlib import Path
import subprocess
from argparse import ArgumentParser
from enum import Enum

import yaml
from dacite.core import from_dict
from dacite.config import Config

from .lang import Lang, TypeDefinition, StructDef, EnumDef, FlagsDef, WrapperDef
from .lang_rust import RustLang
from .lang_python import PythonLang

def process_lang(
	lang: Lang,
	type_defs: list[TypeDefinition],
	clean: bool,
	out_dir: str,
) -> None:
	lang_dir = Path(out_dir, lang_name)
	if clean:
		shutil.rmtree(lang_dir)

	lang_dir.mkdir(parents = True, exist_ok = True)
	shutil.copytree(Path('static', lang_name), lang_dir, dirs_exist_ok = True)

	output_files = defaultdict(list)

	for type_def in type_defs:
		full_path = lang_dir / lang.source_dir() / ((lang.filename() or 'default') + lang.file_extension())

		if isinstance(type_def.type, StructDef):
			type_text = lang.make_struct(type_def.type, type_def)
		elif isinstance(type_def.type, EnumDef):
			type_text = lang.make_enum(type_def.type, type_def)
		elif isinstance(type_def.type, FlagsDef):
			type_text = lang.make_flags(type_def.type, type_def)
		elif isinstance(type_def.type, WrapperDef):
			type_text = lang.make_wrapper(type_def.type, type_def)

		output_files[full_path].append(textwrap.dedent(type_text))

	for folder in set([p.parent for p in output_files.keys()]):
		folder.mkdir(parents = True, exist_ok = True)

	for path, contents in output_files.items():
		path.write_text('\n'.join([textwrap.dedent(lang.file_header())] + contents))

	for args in lang.post_build():
		subprocess.run(args, cwd = lang_dir, check = True)

def load_types(dir: Path) -> list[TypeDefinition]:
	ret = []
	for file in sorted(dir.glob('*.yml')):
		contents = yaml.safe_load(file.read_text())
		ret += [from_dict(TypeDefinition, t) for t in contents]

	return ret

parser = ArgumentParser()
parser.add_argument('--clean', action = 'store_true')
parser.add_argument('--outdir', type = str, default = 'out')
parser.add_argument('sourcedir')
parser.add_argument('lang', nargs = '+')
args = parser.parse_args()

all_types = load_types(Path(args.sourcedir))
types_by_name = {t.name: t for t in all_types}

langs = {
	'rust': RustLang(types_by_name),
	'python': PythonLang(types_by_name),
}

for lang_name in args.lang:
	lang = langs[lang_name]
	process_lang(lang, all_types, args.clean, args.outdir)
