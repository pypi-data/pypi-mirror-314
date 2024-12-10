from pathlib import Path
import sys


_PATH_TYPE_ERROR_MSG =\
	"syspathmodif: A path must be None or of type str or pathlib.Path."


def sp_append(some_path):
	"""
	Appends the given path to the end of list sys.path if it does not already
	contain the path. If the path is of type pathlib.Path, it is converted to a
	string. If the path is None, this method does not change sys.path.

	Args:
		some_path (str or pathlib.Path): the path to append to sys.path.

	Returns:
		bool: True if some_path was appended to sys.path, False otherwise.

	Throws:
		TypeError: if the type of argument some_path is not str or
			pathlib.Path and some_path is not None.
	"""
	some_path = _ensure_path_is_str(some_path)
	was_path_appended = False

	if some_path not in sys.path and some_path is not None:
		sys.path.append(some_path)
		was_path_appended = True

	return was_path_appended


def sp_contains(some_path):
	"""
	Indicates whether list sys.path contains the given path.

	Args:
		some_path (str or pathlib.Path): the path whose presence is verified.

	Returns:
		bool: True if sys.path contains argument some_path, False otherwise.

	Throws:
		TypeError: if the type of argument some_path is not str or
			pathlib.Path and some_path is not None.
	"""
	some_path = _ensure_path_is_str(some_path)
	return some_path in sys.path


def sp_remove(some_path):
	"""
	Removes the given path from list sys.path if it contains the path.

	Args:
		some_path (str or pathlib.Path): the path to remove from sys.path.

	Returns:
		bool: True if some_path was removed from sys.path, False otherwise.

	Throws:
		TypeError: if the type of argument some_path is not str or
			pathlib.Path and some_path is not None.
	"""
	some_path = _ensure_path_is_str(some_path)
	was_path_removed = False

	if some_path in sys.path:
		sys.path.remove(some_path)
		was_path_removed = True

	return was_path_removed


def _ensure_path_is_str(some_path):
	if isinstance(some_path, str) or some_path is None:
		return some_path
	elif isinstance(some_path, Path):
		return str(some_path)
	else:
		raise TypeError(_PATH_TYPE_ERROR_MSG)
