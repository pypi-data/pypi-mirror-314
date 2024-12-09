#!/usr/bin/env python3
#
#  unknowns.py
"""
Metadata and pipeline for unknown samples.
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
from operator import itemgetter
from typing import Dict, List, Tuple, Type

# 3rd party
import attrs
import pyms_nist_search
import tomli_w
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.typing import PathLike
from libgunshotmatch.consolidate import ConsolidatedPeakFilter
from libgunshotmatch.datafile import Repeat
from libgunshotmatch.method import Method, MethodBase
from libgunshotmatch.method._fields import String
from libgunshotmatch.project import Project
from libgunshotmatch.search import identify_peaks
from libgunshotmatch.utils import _fix_init_annotations
from pyms.DPA.Alignment import exprl2alignment
from pyms.Experiment import Experiment

# this package
from gunshotmatch_pipeline import prepare_datafile
from gunshotmatch_pipeline.nist_ms_search import engine_on_demand
from gunshotmatch_pipeline.projects import LoaderMixin
from gunshotmatch_pipeline.utils import tomllib

__all__ = ("UnknownSettings", "filter_and_identify_peaks", "process_unknown")


@_fix_init_annotations
@attrs.define
class UnknownSettings(MethodBase, LoaderMixin):
	"""
	Settings for an unknown propellant or OGSR sample.

	.. autosummary-widths:: 28/100
	"""

	#: The unknown sample's name or identifier.
	name: str = String.field(default=attrs.NOTHING)

	#: The input datafile
	datafile: str = String.field(default=attrs.NOTHING)

	#: Relative or absolute filename to the method TOML file. The table name is "method".
	method: str = String.field(default=attrs.NOTHING)

	#: Relative or absolute filename to the configuration TOML file. The table name is "config".
	config: str = String.field(default=attrs.NOTHING)

	#: Relative or absolute path to the directory the output files should be placed in.
	output_directory: str = String.field(default=attrs.NOTHING)

	#: Relative or absolute path to the directory containing the data files.
	data_directory: str = String.field(default='')

	@property
	def datafile_path(self) -> PathPlus:
		"""
		The absolute path to the datafile.
		"""

		return (PathPlus(self.data_directory) / self.datafile).abspath()

	@classmethod
	def from_toml(cls: Type["UnknownSettings"], toml_string: str) -> "UnknownSettings":
		"""
		Parse an :class:`~.UnknownSettings` from a TOML string.

		:param toml_string:
		"""

		parsed_toml: Dict[str, str] = tomllib.loads(toml_string)
		understood_keys = {"name", "datafile", "method", "config", "output_directory", "data_directory"}
		toml_subset = {k: v for k, v in parsed_toml.items() if k in understood_keys}
		return cls(**toml_subset)

	@classmethod
	def from_json(cls: Type["UnknownSettings"], json_string: str) -> "UnknownSettings":
		"""
		Parse an :class:`~.UnknownSettings` from a JSON string.

		:param json_string:
		"""

		parsed_json = json.loads(json_string)
		return cls(**parsed_json)

	def to_toml(self) -> str:
		"""
		Convert an :class:`~.UnknownSettings` to a TOML string.
		"""

		return tomli_w.dumps(self.to_dict())


def filter_and_identify_peaks(
		repeat: Repeat,
		method: Method,
		engine: pyms_nist_search.Engine,
		) -> None:
	"""
	Filter peaks by minimum peak area, then identify compounds.

	:param repeat:
	:param method:
	:param engine: NIST MS Search engine.
	"""

	top_n_peaks = method.alignment.top_n_peaks
	min_peak_area = method.alignment.min_peak_area

	peak_index_area_map: List[Tuple[float, float]] = []
	for peak in repeat.peaks:
		assert peak.area is not None
		peak_index_area_map.append((peak.area, peak.rt))

	if top_n_peaks:  # If ``0`` all peaks are included.
		print(f"Filtering to the largest {top_n_peaks} peaks with a peak area above {min_peak_area}")

		peak_index_area_map.sort(key=itemgetter(0), reverse=True)
		peak_index_area_map = peak_index_area_map[:top_n_peaks]
	else:
		print(f"Filtering to peaks with an average peak area above {min_peak_area}")

	top_peaks_times = [rt / 60 for area, rt in peak_index_area_map if area >= min_peak_area]

	# peak_index_area_map = [(idx, peak.area, peak.rt) for idx, peak in enumerate(repeat.peaks)]
	# peak_index_area_map.sort(key=itemgetter(1), reverse=True)

	# # Get indices of largest n peaks based on `ident_top_peaks`
	# # top_peaks_indices = []
	# top_peaks_times = []
	# # print("tail of area_alignment=", area_alignment.tail(top_n_peaks))

	# # Limit to the largest `ident_top_peaks` peaks
	# for peak_no, area, rt in peak_index_area_map[:top_n_peaks]:
	# 	# Ignore peak if average peak area is less then min_peak_area
	# 	if area >= min_peak_area:
	# 		# top_peaks_indices.append(peak_no)
	# 		top_peaks_times.append(rt / 60)
	# 		# top_peaks_times.append(round_rt(rt / 60))

	print(f"Identifying Compounds for {repeat.name}")
	qualified_peaks = identify_peaks(
			engine,
			top_peaks_times,
			repeat.peaks,  # verbose=True,
			)
	repeat.qualified_peaks = qualified_peaks


def process_unknown(
		unknown: UnknownSettings,
		output_dir: PathLike,
		recreate: bool = False,
		) -> Project:
	"""
	Process an "unknown" sample.

	:param unknown:
	:param output_dir:
	:param recreate: Force regeneration of ``.gsmr`` and ``.gsmp`` files.
	"""

	output_dir = PathPlus(output_dir)
	output_dir.maybe_make()

	method = unknown.load_method()
	config = unknown.load_config()

	gsmp_filename = output_dir / f"{unknown.name}.gsmp"
	# print(gsmp_filename)
	if gsmp_filename.exists() and not recreate:
		print(f"Loading Unknown from file {gsmp_filename.as_posix()!r}")
		project = Project.from_file(gsmp_filename)
	else:

		with engine_on_demand(config.pyms_nist_search) as search:

			gsmr_filename = (output_dir / unknown.datafile).with_suffix(".gsmr")
			# print(gsmr_filename)
			if gsmr_filename.exists() and not recreate:
				print(f"Loading Repeat from file {gsmr_filename.as_posix()!r}")
				repeat = Repeat.from_file(gsmr_filename)
				repeat.peaks.datafile_name = repeat.name
			else:
				print("\nParsing", unknown.datafile_path)
				repeat, gcms_data = prepare_datafile(unknown.datafile_path, method)
				filter_and_identify_peaks(repeat, method, engine=search.engine)
				repeat.export(output_dir)

			alignment = exprl2alignment([Experiment(repeat.name, repeat.peaks)])[0]

			project = Project(name=unknown.name, alignment=alignment, datafile_data={repeat.name: repeat})

			if not project.consolidated_peaks:
				# ms_comparison_df = project.consolidate()

				cp_filter = ConsolidatedPeakFilter(
						name_filter=method.consolidate.name_filter,
						min_match_factor=int(method.consolidate.min_match_factor * 0.8),
						min_appearances=1,  # verbose=True,
						)

			ms_comparison_df = project.consolidate(search.engine, cp_filter)
		# assert project.consolidated_peaks is not None
		# print(len(project.consolidated_peaks))

		# print(ms_comparison_df)

		# export_filename = project.export(output_dir)
		export_filename = project.export(output_dir)
		print(f"Project saved to {export_filename!r}")

	return project
