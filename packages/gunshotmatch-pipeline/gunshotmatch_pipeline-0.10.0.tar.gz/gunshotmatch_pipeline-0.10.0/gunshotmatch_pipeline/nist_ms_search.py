#!/usr/bin/env python3
#
#  nist_ms_search.py
"""
Configuration for :mod:`pyms_nist_search` and NIST MS Search.
"""
#
#  Copyright © 2023 Dominic Davis-Foster <dominic@davis-foster.co.uk>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
#  EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
#  MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
#  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR
#  OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE
#  OR OTHER DEALINGS IN THE SOFTWARE.
#

# stdlib
from contextlib import contextmanager
from tempfile import TemporaryDirectory
from typing import Any, Dict, Iterator, Optional

# 3rd party
import attrs
import pyms_nist_search
from domdf_python_tools.typing import PathLike
from libgunshotmatch.method import MethodBase
from libgunshotmatch.method._fields import Boolean, String
from libgunshotmatch.utils import _fix_init_annotations

__all__ = ("PyMSNISTSearchCfg", "nist_ms_search_engine", "LazyEngine", "engine_on_demand")


@_fix_init_annotations
@attrs.define
class PyMSNISTSearchCfg(MethodBase):
	"""
	Configuration for :mod:`pyms_nist_search`.

	.. autosummary-widths:: 40/100
	"""

	#: Absolute path to the NIST library (mainlib or user).
	library_path: str = String.field(default=attrs.NOTHING)

	#: :py:obj:`True` for user libraries; :py:obj:`False` for the NIST mainlib.
	user_library: bool = Boolean.field(default=False)


def _create_engine(config: PyMSNISTSearchCfg, workdir: PathLike, **kwargs) -> pyms_nist_search.Engine:
	if config.user_library:
		library_type = pyms_nist_search.NISTMS_USER_LIB
	else:
		library_type = pyms_nist_search.NISTMS_MAIN_LIB

	return pyms_nist_search.Engine(config.library_path, library_type, workdir, **kwargs)


@contextmanager
def nist_ms_search_engine(config: PyMSNISTSearchCfg, **kwargs) -> Iterator[pyms_nist_search.Engine]:
	r"""
	Initialize the NIST MS Serch engine from :mod:`pyms_nist_search`.

	:param config:
	:param \*\*kwargs: Keyword arguments for :class:`pyms_nist_search.win_engine.Engine`
	"""

	with TemporaryDirectory() as workdir:

		with _create_engine(config, workdir, **kwargs) as search:
			# with pyms_nist_search.Engine(config.library_path, library_type, workdir, **kwargs) as search:
			yield search


class LazyEngine:
	r"""
	Initialize the NIST MS Serch engine on demand.

	:param config:
	:param \*\*kwargs: Keyword arguments for :class:`pyms_nist_search.win_engine.Engine`

	.. versionadded:: 0.2.0
	"""

	def __init__(self, config: PyMSNISTSearchCfg, **kwargs):
		self.config: PyMSNISTSearchCfg = config
		self.kwargs: Dict[str, Any] = kwargs
		self._engine: Optional[pyms_nist_search.Engine] = None
		self._workdir = TemporaryDirectory()

	def deinit(self) -> None:
		"""
		Cleanup the underlying engine and temporary directory.
		"""

		if self._engine is not None:
			self._engine.uninit()
		self._workdir.cleanup()

	@property
	def engine(self) -> pyms_nist_search.Engine:
		"""
		The NIST MS Search engine.

		The engine is created the first time this property is accessed.
		"""

		if self._engine is None:
			self._engine = _create_engine(self.config, self._workdir.name, **self.kwargs)

		return self._engine


@contextmanager
def engine_on_demand(config: PyMSNISTSearchCfg, **kwargs) -> Iterator[LazyEngine]:
	r"""
	Defer initialization of the NIST MS Serch engine until required (if at all).

	:param config:
	:param \*\*kwargs: Keyword arguments for :class:`pyms_nist_search.win_engine.Engine`

	:rtype:

	.. versionadded:: 0.2.0
	"""

	le = LazyEngine(config, **kwargs)
	yield le
	le.deinit()
