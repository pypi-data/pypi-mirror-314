#!/usr/bin/env python3
#
#  utils.py
"""
General utility functions.
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
from typing import Dict

# 3rd party
from domdf_python_tools.words import Plural

try:
	# stdlib
	import tomllib  # type: ignore[import-not-found]
except ImportError:
	# 3rd party
	import tomli as tomllib

__all__ = ("project_plural", "unknown_plural", "friendly_name_mapping", "tomllib", "NameMapping")

#: :class:`domdf_python_tools.words.Plural` for ``project``.
project_plural = Plural("project", "projects")

unknown_plural = Plural("unknown", "unknowns")
"""
:class:`domdf_python_tools.words.Plural` for ``unknown``.

.. versionadded:: 0.9.0
"""


class NameMapping(Dict[str, str]):
	"""
	Class for mapping IUPAC preferred names to more common, friendlier names.

	On lookup, if the name has no known alias the looked-up name is returned.

	.. versionadded:: 0.4.0
	"""

	def __missing__(self, key: str) -> str:
		return key


#: Mapping of IUPAC preferred names to more common, friendlier names.
friendly_name_mapping = NameMapping({
		# IUPAC: Friendly
		"Benzenamine, 4-nitro-N-phenyl-": "4-NDPA",
		"Benzenamine, 2-nitro-N-phenyl-": "2-NDPA",
		"Urea, N,N'-dimethyl-N,N'-diphenyl-": "Methyl centralite",
		"N,N'-Diethyl-N,N'-diphenylurea": "Ethyl Centralite",
		"Benzene, nitro-": "Nitrobenzene",
		"Benzene, 2-methyl-1,3-dinitro-": "2,6-DNT",
		"Benzene, 1-methyl-2,3-dinitro-": "2,3-DNT",
		"Benzene, 1-methyl-2,4-dinitro-": "2,4-DNT",
		"Phenol, 2-nitro-": "2-Nitrophenol",
		"Benzene, 1-methyl-2-nitro-": "2-Nitrotoluene",
		"Benzene, 1-methyl-4-nitro-": "4-Nitrotoluene",
		"Benzene, 1-methyl-3-nitro-": "3-Nitrotoluene",
		"Benzenamine, N-ethyl-N-nitroso-": "N-Nitroso-N-ethylaniline",
		"Phenol, 4-methyl-2-nitro-": "4-Methyl-2-nitrophenol",
		"2,5-Cyclohexadiene-1,4-dione, 2,5-dimethyl-": "2,5-Dimethyl-p-benzoquinone",
		"2,5-Cyclohexadiene-1,4-dione, 2,5-diphenyl-": "2,5-Diphenyl-p-benzoquinone",
		"2,5-Cyclohexadiene-1,4-dione, 2,6-bis(1,1-dimethylethyl)-": "2,6-Di-tert-butyl-p-benzoquinone",
		"1,2-Benzenedicarboxylic acid, butyl 2-methylpropyl ester": "Butyl isobutyl phthalate",
		"1,2-Benzenedicarboxylic acid, butyl 2-ethylhexyl ester": "Butyl 2-ethylhexyl phthalate",
		"1,2-Benzenedicarboxylic acid, diheptyl ester": "Diheptyl phthalate",
		"1,2-Benzenedicarboxylic acid, butyl octyl ester": "Butyl octyl phthalate",
		"1,6-Anhydro-β-D-glucopyranose (levoglucosan)": "Levoglucosan",
		"Bicyclo[2.2.1]heptan-2-one, 1,7,7-trimethyl-, (1S)-": "(-)-Camphor",
		"Pentaerythritol Tetranitrate": "PETN",
		"Benzene, 1,3-dimethyl-": "m-Xylene",
		})
