#!/usr/bin/env python3
#
#  config.py
"""
Configuration for GunShotMatch analysis.
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
import json
from typing import Type

# 3rd party
import attrs
import tomli_w
from libgunshotmatch.method import MethodBase
from libgunshotmatch.utils import _fix_init_annotations

# this package
from gunshotmatch_pipeline.nist_ms_search import PyMSNISTSearchCfg
from gunshotmatch_pipeline.utils import tomllib

__all__ = ("Configuration", )


@_fix_init_annotations
@attrs.define
class Configuration(MethodBase):
	"""
	Overall GunShotMatch configuration.
	"""

	#: Configuration for :mod:`pyms_nist_search`.
	pyms_nist_search: PyMSNISTSearchCfg = attrs.field(converter=PyMSNISTSearchCfg._coerce)  # type: ignore[misc]

	@classmethod
	def from_toml(cls: Type["Configuration"], toml_string: str) -> "Configuration":
		"""
		Parse a :class:`~.Configuration` from a TOML string.

		:param toml_string:
		"""

		parsed_toml = tomllib.loads(toml_string)
		# print(dict(zip(map(str.lower,parsed_toml.keys()),parsed_toml.values())))
		return cls(**parsed_toml["gunshotmatch"])

	@classmethod
	def from_json(cls: Type["Configuration"], json_string: str) -> "Configuration":
		"""
		Parse a :class:`~.Configuration` from a JSON string.

		:param json_string:
		"""

		parsed_json = json.loads(json_string)
		return cls(**parsed_json["gunshotmatch"])

	def to_toml(self) -> str:
		"""
		Convert a :class:`~.Configuration` to a TOML string.
		"""

		return tomli_w.dumps({"gunshotmatch": self.to_dict()})
