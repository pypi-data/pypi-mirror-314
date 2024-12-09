#!/usr/bin/env python3
#
#  results.py
"""
Results presented in different formats.
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
import datetime
import string
from collections import defaultdict
from string import ascii_lowercase
from typing import Dict, List

# 3rd party
import pandas  # type: ignore[import-untyped]
from libgunshotmatch.project import Project
from typing_extensions import TypedDict

__all__ = (
		"compounds",
		"compounds_from_matches",
		"machine_learning_data",
		"matches",
		"unknown",
		"unknown_machine_learning_data",
		"MatchesMetadata",
		"MatchesCompounds",
		"Matches",
		)


class MatchesMetadata(TypedDict):
	"""
	Type hint for the ``metadata`` key in :typeddict:`~.Matches`.
	"""

	project: str
	original_filenames: List[str]
	created: str


#: Type hint for the ``compounds`` key in :typeddict:`~.Matches`.
MatchesCompounds = TypedDict(
		"MatchesCompounds",
		{
				"Mean Retention Time": float,  # in minutes
				"Mean Peak Area": float,
				"CAS": str,
				"Retention Times": List[float],
				"Peak Areas": List[float],
				"Hit Numbers": List[int],
				"Match Factors": List[int],
				"Reverse Match Factors": List[int],
				}
		)


class Matches(TypedDict):
	"""
	Return type from :func:`~.matches`.
	"""

	metadata: MatchesMetadata
	compounds: Dict[str, MatchesCompounds]


def matches(project: Project) -> Matches:
	"""
	Returns data on the "best match" for each peak.

	:param project:

	:rtype:

	.. latex:clearpage::
	"""

	matches_json_data: Matches = {
			"metadata": {
					"project": project.name,
					"original_filenames": [
							repeat.datafile.original_filename for repeat in project.datafile_data.values()
							],
					"created": datetime.datetime.now().isoformat()
					},
			"compounds": {}
			}

	assert project.consolidated_peaks is not None
	for peak in project.consolidated_peaks:
		hit = peak.hits[0]
		# TODO: account for multiple peaks with same name
		matches_json_data["compounds"][hit.name] = {
				"Mean Retention Time": peak.rt / 60,  # in minutes
				"Mean Peak Area": peak.area,  # "Peak Number": peak.peak_number,
				"CAS": hit.cas,
				"Retention Times": [rt / 60 for rt in peak.rt_list],
				"Peak Areas": peak.area_list,
				"Hit Numbers": hit.hit_numbers,
				"Match Factors": hit.mf_list,
				"Reverse Match Factors": hit.rmf_list,
				}

	return matches_json_data


_CompoundName = str
_ProjectName = str
_PeakArea = float
_CompoundDataType = Dict[_CompoundName, Dict[_ProjectName, List[_PeakArea]]]
_PropellantNameAndID = str


def compounds_from_matches(*matches_data: Matches, normalize: bool = False) -> _CompoundDataType:
	r"""
	Prepares data on the compounds in each repeat from the output of :func:`~.matches` for each project.

	The output mapping gives the peak areas for each compound in the different projects, grouped by compound.

	:param \*matches_data:
	:param normalize:
	"""

	# Get single array of compound name to 5x peak areas per project
	compound_data: _CompoundDataType = defaultdict(dict)

	for loaded_data in matches_data:

		project_name = loaded_data["metadata"]["project"]

		if normalize:
			data_size = len(loaded_data["metadata"]["original_filenames"])
			df_for_norm = pandas.DataFrame(index=list(string.ascii_lowercase[:data_size]))

			for compound in loaded_data["compounds"]:
				df_for_norm[compound] = loaded_data["compounds"][compound]["Peak Areas"]

			res = df_for_norm.div(df_for_norm.sum(axis=1), axis=0)
			# df_for_norm["total"] = df_for_norm[compounds].sum(axis=1)
			# res["total"] = res[compounds].sum(axis=1)
			# print(res)
			# print(df_for_norm)

			for compound in res.columns:
				compound_data[compound][project_name] = list(res[compound])
		else:
			for compound in loaded_data["compounds"]:
				compound_data[compound][project_name] = loaded_data["compounds"][compound]["Peak Areas"]

	return compound_data


def compounds(*project: Project, normalize: bool = False) -> _CompoundDataType:
	r"""
	Returns data on the compounds in each repeat in the project(s).

	The output mapping gives the peak areas for each compound in the different projects, grouped by compound.

	:param \*project:
	:param normalize:
	"""

	# Get single array of compound name to 5x peak areas per project
	return compounds_from_matches(*(matches(p) for p in project), normalize=normalize)


def unknown(unknown_project: Project, normalize: bool = False) -> _CompoundDataType:
	"""
	Returns results for an unknown sample.

	The output mapping is formatted the same as that from :func:`~.compounds`, but with only one "project".

	:param unknown_project:
	:param normalize:
	"""

	return compounds_from_matches(matches(unknown_project), normalize=normalize)


def machine_learning_data(
		*project: Project,
		normalize: bool = False,
		) -> Dict[_CompoundName, Dict[_PropellantNameAndID, _PeakArea]]:
	r"""
	Returns data formatted for training a decision tree or other machine learning model.

	:param \*project:
	:param normalize:
	"""

	decision_tree_compound_data: Dict[_CompoundName, Dict[_PropellantNameAndID, _PeakArea]] = defaultdict(dict)

	for compound, propellant_peak_areas in compounds(*project, normalize=normalize).items():
		for propellant, peak_areas in propellant_peak_areas.items():
			for identifier, peak_area in zip(ascii_lowercase, peak_areas):
				decision_tree_compound_data[compound][f"{propellant}-{identifier}"] = peak_area

	return decision_tree_compound_data


def unknown_machine_learning_data(
		unknown_project: Project,
		normalize: bool = False,
		) -> Dict[_CompoundName, Dict[_PropellantNameAndID, _PeakArea]]:
	"""
	Returns data formatted for training a decision tree or other machine learning model.

	:param unknown_project:
	:param normalize:
	"""

	decision_tree_compound_data: Dict[_CompoundName, Dict[_PropellantNameAndID, _PeakArea]] = defaultdict(dict)

	for compound, propellant_peak_areas in unknown(unknown_project, normalize=normalize).items():
		assert len(propellant_peak_areas) == 1
		for propellant, peak_areas in propellant_peak_areas.items():
			for peak_area in peak_areas:
				decision_tree_compound_data[compound][f"{propellant}"] = peak_area

	return decision_tree_compound_data
