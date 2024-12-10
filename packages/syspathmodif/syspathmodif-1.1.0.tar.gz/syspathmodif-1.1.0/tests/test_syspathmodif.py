import pytest

from pathlib import Path
import sys


_INIT_SYS_PATH = list(sys.path)

_LOCAL_DIR = Path(__file__).resolve().parent
_REPO_ROOT = _LOCAL_DIR.parent
_LIB_DIR = _REPO_ROOT/"syspathmodif"


def _reset_sys_path():
	# Copying the list is necessary to preserve the initial state.
	sys.path = list(_INIT_SYS_PATH)


sys.path.append(str(_REPO_ROOT))
from syspathmodif import\
	sp_append,\
	sp_contains,\
	sp_remove
_reset_sys_path()


def test_sp_contains_true_str():
	# This test does not change the content of sys.path.
	dir0 = str(sys.path[0])
	assert sp_contains(dir0)


def test_sp_contains_true_pathlib():
	# This test does not change the content of sys.path.
	dir0 = Path(sys.path[0])
	assert sp_contains(dir0)


def test_sp_contains_false_str():
	# This test does not change the content of sys.path.
	assert not sp_contains(str(_LIB_DIR))


def test_sp_contains_false_pathlib():
	# This test does not change the content of sys.path.
	assert not sp_contains(_LIB_DIR)


def test_sp_contains_none():
	# This test does not change the content of sys.path.
	assert not sp_contains(None)


def test_sp_contains_exception():
	# This test does not change the content of sys.path.
	except_msg =\
		"syspathmodif: A path must be None or of type str or pathlib.Path."
	with pytest.raises(TypeError, match=except_msg):
		sp_contains(3.14159)


def test_sp_append_str():
	try:
		success = sp_append(str(_LIB_DIR))
		assert success
		assert sp_contains(str(_LIB_DIR))
	finally:
		_reset_sys_path()


def test_sp_append_pathlib():
	try:
		success = sp_append(_LIB_DIR)
		assert success
		assert sp_contains(_LIB_DIR)
	finally:
		_reset_sys_path()


def test_sp_append_no_success():
	try:
		sys.path.append(str(_LIB_DIR))
		success = sp_append(_LIB_DIR)
		assert not success
		assert sp_contains(_LIB_DIR)
	finally:
		_reset_sys_path()


def test_sp_append_none():
	try:
		success = sp_append(None)
		assert not success
		assert sys.path == _INIT_SYS_PATH
	finally:
		_reset_sys_path()


def test_sp_remove_str():
	try:
		sys.path.append(str(_LIB_DIR))
		success = sp_remove(str(_LIB_DIR))
		assert success
		assert not sp_contains(str(_LIB_DIR))
	finally:
		_reset_sys_path()


def test_sp_remove_pathlib():
	try:
		sys.path.append(str(_LIB_DIR))
		success = sp_remove(_LIB_DIR)
		assert success
		assert not sp_contains(_LIB_DIR)
	finally:
		_reset_sys_path()


def test_sp_remove_no_success():
	try:
		# sys.path does not contain _LIB_DIR.
		success = sp_remove(_LIB_DIR)
		assert not success
		assert not sp_contains(_LIB_DIR)
	finally:
		_reset_sys_path()


def test_sp_remove_none_no_success():
	try:
		success = sp_remove(None)
		assert not success
		assert sys.path == _INIT_SYS_PATH
	finally:
		_reset_sys_path()


def test_sp_remove_none_success():
	try:
		sys.path.append(None)
		success = sp_remove(None)
		assert success
		assert sys.path == _INIT_SYS_PATH
	finally:
		_reset_sys_path()
