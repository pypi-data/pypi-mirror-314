#!/usr/bin/env python3
#
#  exporters.py
"""
Functions and classes for export to disk, and verification of saved data.
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
from typing import List

# 3rd party
import sdjson
from domdf_python_tools.paths import PathPlus
from libgunshotmatch.datafile import Datafile, Repeat
from libgunshotmatch.peak import QualifiedPeak
from libgunshotmatch.project import Project
from numpy import allclose, array_equal

# this package
import gunshotmatch_pipeline.results

__all__ = ("verify_saved_datafile", "verify_saved_project", "write_combined_csv", "write_matches_json")


def verify_saved_datafile(in_process: Datafile, from_file: Datafile) -> None:
	"""
	Verify the data in a saved :class:`~libgunshotmatch.datafile.Datafile` matches the data in memory.

	Will raise an :exc:`AssertionError` if the data do not match.

	:param in_process: The :class:`~libgunshotmatch.datafile.Datafile` already in memory.
	:param from_file: A :class:`~libgunshotmatch.datafile.Datafile` loaded from disk.
	"""

	assert in_process.intensity_matrix is not None
	assert from_file.intensity_matrix is not None
	assert allclose(in_process.intensity_matrix.time_list, from_file.intensity_matrix.time_list)
	assert allclose(in_process.intensity_matrix.mass_list, from_file.intensity_matrix.mass_list)
	assert allclose(in_process.intensity_matrix.intensity_array, from_file.intensity_matrix.intensity_array)
	assert from_file.name == in_process.name
	assert from_file.user == in_process.user
	assert from_file.device == in_process.device
	assert from_file.date_created == in_process.date_created
	assert from_file.date_modified == in_process.date_modified
	assert from_file.version == in_process.version
	assert from_file.original_filename == in_process.original_filename
	assert from_file.original_filetype == in_process.original_filetype
	assert from_file.description == in_process.description


def verify_saved_project(in_process: Project, from_file: Project) -> None:
	"""
	Verify the data in a saved :class:`~libgunshotmatch.project.Project` matches the data in memory.

	Will raise an :exc:`AssertionError` if the data do not match.

	:param in_process: The :class:`~libgunshotmatch.project.Project` already in memory.
	:param from_file: A :class:`~libgunshotmatch.project.Project` loaded from disk.
	"""

	# TODO: consolidated_peaks

	assert in_process.name == from_file.name
	assert in_process.alignment.peakpos == from_file.alignment.peakpos
	assert in_process.alignment.expr_code == from_file.alignment.expr_code
	assert array_equal(in_process.alignment.peakalgt, from_file.alignment.peakalgt)  # type: ignore[arg-type]
	assert in_process.alignment.similarity == from_file.alignment.similarity
	assert in_process.datafile_data.keys() == from_file.datafile_data.keys()

	left_dd = in_process.datafile_data
	right_dd = from_file.datafile_data
	for datafile_id in left_dd:
		verify_saved_datafile(left_dd[datafile_id].datafile, right_dd[datafile_id].datafile)

		assert left_dd[datafile_id].peaks == right_dd[datafile_id].peaks
		assert left_dd[datafile_id].qualified_peaks == right_dd[datafile_id].qualified_peaks


def write_matches_json(project: Project, output_dir: PathPlus) -> None:
	"""
	Write the JSON output file listing the determined "best match" for each peaks.

	:param project:
	:param output_dir: The directory to write the ``<project.name>.json`` file to.
	"""

	(output_dir / f"{project.name}.json").dump_json(
			gunshotmatch_pipeline.results.matches(project),
			indent=2,
			json_library=sdjson,  # type: ignore[arg-type]
			)


def write_combined_csv(repeat: Repeat, output_dir: PathPlus) -> None:
	"""
	Write a CSV file listing the top hits for each peak in the :class:`~.libgunshotmatch.datafile.Repeat`, with associated data.

	:param project:
	:param output_dir: Directory to save the file in

	:rtype:

	.. latex:clearpage::
	"""

	csv_header_row = "Retention Time;Peak Area;;Match;R Match;Name;CAS Number;Notes"

	# qualified_peaks = repeat["qualified_peaks"]
	qualified_peaks = repeat.qualified_peaks
	assert qualified_peaks is not None

	combined_csv_file = output_dir / f"{repeat.datafile.name}_COMBINED.csv"

	# Write output to CSV file
	with combined_csv_file.open('w') as combine_csv:

		# Sample name and header row
		combine_csv.write(f"{repeat.datafile.name}\n{csv_header_row}\n")

		def to_csv(peak: QualifiedPeak) -> List[List[str]]:
			assert peak.area is not None
			area = f"{peak.area / 60:,}"
			csv = [[str(peak.rt / 60), area, '', '', '', '', '', '']]
			for hit in peak.hits:
				csv.append([
						'',
						'',
						'',
						str(hit.match_factor),
						str(hit.reverse_match_factor),
						hit.name,
						hit.cas,
						])
			return csv

		for peak in qualified_peaks:
			for row in to_csv(peak):
				combine_csv.write(f'{";".join(row)}\n')
