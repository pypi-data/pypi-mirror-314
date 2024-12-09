#!/usr/bin/env python3
#
#  __init__.py
"""
GunShotMatch Pipeline.

.. autosummary-widths:: 54/100
"""
#
#  Copyright © 2020-2023 Dominic Davis-Foster <dominic@davis-foster.co.uk>
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
from typing import List, Tuple

# 3rd party
import pyms_nist_search
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.typing import PathLike
from libgunshotmatch.datafile import Datafile, Repeat, get_info_from_gcms_data
from libgunshotmatch.method import Method
from libgunshotmatch.project import Project
from libgunshotmatch.search import identify_peaks
from pyms.GCMS.Class import GCMS_data

# this package
from gunshotmatch_pipeline.peaks import align_and_filter_peaks, prepare_peak_list

__all__ = ("prepare_datafile", "project_from_repeats")

__author__: str = "Dominic Davis-Foster"
__copyright__: str = "2020-2023 Dominic Davis-Foster"
__license__: str = "MIT License"
__version__: str = "0.10.0"
__email__: str = "dominic@davis-foster.co.uk"


def prepare_datafile(
		filename: PathLike,
		method: Method,
		verbose: bool = False,
		) -> Tuple[Repeat, GCMS_data]:
	"""
	Pipeline from raw datafile to a :class:`~libgunshotmatch.datafile.Datafile`.

	:param filename:
	:param method:
	:param verbose: If :py:obj:`True` information about the GC-MS data in each datafile will be printed.
	"""

	raw_datafile = PathPlus(filename)
	print(f"\nPreparing datafile {raw_datafile.as_posix()!r}")
	datafile = Datafile.new(raw_datafile.stem, filename)
	gcms_data: GCMS_data = datafile.load_gcms_data()

	datafile.prepare_intensity_matrix(
			gcms_data,
			savitzky_golay=method.intensity_matrix.savitzky_golay,
			tophat=method.intensity_matrix.tophat,
			tophat_structure_size=method.intensity_matrix.tophat_structure_size,
			crop_mass_range=method.intensity_matrix.crop_mass_range,
			)

	if verbose:
		print(datafile)
		print(get_info_from_gcms_data(gcms_data))

	peak_list = prepare_peak_list(datafile, gcms_data, method)

	return Repeat(datafile, peak_list), gcms_data


def project_from_repeats(
		repeats: List[Repeat],
		name: str,
		method: Method,
		engine: pyms_nist_search.Engine,
		) -> Project:
	"""
	Construct a project from the given :class:`~libgunshotmatch.datafile.Repeat` objects, using the given method.

	:param repeats:
	:param name: The project name.
	:param method:
	:param engine: NIST MS Search engine.
	"""

	datafile_data = {repeat.name: repeat for repeat in repeats}

	# datafile_data = {}

	# for repeat in repeats:
	# 	datafile_data[repeat.name] = repeat

	project = Project(name=name, alignment=None, datafile_data=datafile_data)  # type: ignore[arg-type]
	print(project)

	# print("\n=================")
	# print(datafile_data)

	peaks_to_identify = align_and_filter_peaks(project, method)

	# for experiment in A1.expr_code:
	for experiment in datafile_data.keys():
		print(f"Identifying Compounds for {experiment}")
		# qualified_peaks = identify_peaks(peaks_to_identify[experiment], datafile_data[experiment]["peak_list"])
		# datafile_data[experiment]["qualified_peaks"] = qualified_peaks
		qualified_peaks = identify_peaks(
				engine,
				peaks_to_identify[experiment],
				datafile_data[experiment].peaks,  # verbose=True,
				)
		datafile_data[experiment].qualified_peaks = qualified_peaks

	return project
