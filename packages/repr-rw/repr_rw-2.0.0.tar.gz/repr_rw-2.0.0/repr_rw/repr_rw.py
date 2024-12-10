from pathlib import\
	Path
import re

from syspathmodif import\
	sp_append,\
	sp_remove


_ENCODING_UTF8 = "utf-8"
_MODE_R = "r"
_MODE_W = "w"
_NEW_LINE = "\n"

_REGEX_IMPORT = "import .+"
_REGEX_FROM_IMPORT = "from .+ import .+"


def _ensure_is_path(obj):
	if isinstance(obj, Path):
		return obj

	elif isinstance(obj, str):
		return Path(obj)

	else:
		raise TypeError(
			"An argument of type str or pathlib.Path is expected.")


def _is_import_statement(some_str):
	if re.match(_REGEX_IMPORT, some_str) is not None:
		return True

	if re.match(_REGEX_FROM_IMPORT, some_str) is not None:
		return True

	return False


def read_reprs(file_path, importations=None, ignore_except=False):
	"""
	If a text file contains the representation of Python objects, this
	generator can read it to recreate those objects. Each line in the file
	must be a string returned by function repr. Empty lines are ignored. Each
	iteration of this generator yields one object.

	Recreating objects requires to import their class. For this purpose, you
	need to provide a dictionary mapping the appropriate import statements
	(keys, type str) to the path (value, type str or pathlib.Path) to the
	parent directory of the class's module or package. However, if the imported
	class is from a built-in module or the standard library, set the value to
	None. Statements that are not importations will not be executed.

	Parameters:
		file_path (str or pathlib.Path): the path to a text file that contains
			object representations.
		importations (dict): the import statements (keys, type str) and the
			paths (values, type str or pathlib.Path) required to perform the
			importations. Defaults to None.
		ignore_except (bool): If it is True, exceptions raised upon the parsing
			of object representations will be ignored, and the involved objects
			will not be recreated. Defaults to False.

	Yields:
		an object recreated from its representation.

	Raises:
		FileNotFoundError: if argument file_path does not exist.
		ModuleNotFoundError: if an importation statement is missing or
			contains a fault.
		TypeError: if argument file_path is not of type str or pathlib.Path.
		Exception: any exception raised upon the parsing of an object
			representation if ignore_except is False.
	"""
	if importations is not None:
		for importation, path in importations.items():
			if _is_import_statement(importation):
				was_path_appended = sp_append(path)
				exec(importation)

				if was_path_appended:
					sp_remove(path)

	file_path = _ensure_is_path(file_path)

	with file_path.open(mode=_MODE_R, encoding=_ENCODING_UTF8) as file:
		for obj_repr in file: # The iterator yields one line at the time.
			if len(obj_repr) >= 1:
				try:
					yield eval(obj_repr)
				except Exception as e:
					if not ignore_except:
						raise e


def write_reprs(file_path, objs):
	"""
	Writes the representation of Python objects in a text file. Each line is a
	string returned by function repr. If the file already exists, this function
	overwrites it.

	Parameters:
		file_path (str or pathlib.Path): the path to the text file that will
			contain the object representations.
		objs (generator, list, set or tuple): the objects whose representation
			will be written.

	Raises:
		TypeError: if argument file_path is not of type str or pathlib.Path.
	"""
	file_path = _ensure_is_path(file_path)

	with file_path.open(mode=_MODE_W, encoding=_ENCODING_UTF8) as file:
		for obj in objs:
			file.write(repr(obj) + _NEW_LINE)
