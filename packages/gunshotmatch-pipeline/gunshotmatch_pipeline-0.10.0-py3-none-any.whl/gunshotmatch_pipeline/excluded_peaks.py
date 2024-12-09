#!/usr/bin/env python3
#
#  config.py
"""
Report excluded peaks from various pipeline steps.

.. versionadded:: 0.10.0
"""
#
#  Copyright © 2024 Dominic Davis-Foster <dominic@davis-foster.co.uk>
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
import io
from collections import deque
from contextlib import redirect_stdout
from typing import Dict, List, MutableSequence, NamedTuple, Optional, Sequence

# 3rd party
import attrs
from libgunshotmatch.consolidate import ConsolidatedPeak, InvertedFilter
from libgunshotmatch.datafile import Repeat
from libgunshotmatch.peak import PeakList, QualifiedPeak, align_peaks
from libgunshotmatch.project import Project, consolidate
from pyms.DPA.Alignment import Alignment
from pyms.Peak.Class import Peak

# this package
from gunshotmatch_pipeline.nist_ms_search import PyMSNISTSearchCfg, engine_on_demand

__all__ = [
		"ExcludedPeaks",
		"PeakCounts",
		"get_excluded_peaks",
		]
"""
Filtering steps:

After Biller-Biemann  (noise and base peak, prior peaks not recorded)
> Filtered peak list saved as Repeat.peaks
During alignment (to minimum peaks)
> Alignment after filtering is saved as Project.alignment
After alignment (to top_n_peaks and min_peak_area)
> Peaks which survive this filtering get qualified and go to Repeat.qualified_peaks
Consolidate process
"""


class PeakCounts(NamedTuple):
	"""
	Counts of peaks at different steps of the pipeline.
	"""

	#: Peak list after Biller-Biemann peak detection and subsequent noise and base peak filtering.
	found_peaks: int

	#: Peaks for which partners were found during alignment (after filtering to `min_peaks`).
	alignment_peaks: int

	#: Peaks which didn't survive alignment step (no/insufficient matching peaks in other datafiles).
	unaligned_peaks: int

	#: Peaks filtered after alignment due to size (``top_n_peaks`` and ``min_peak_area``).
	small_peaks: int


@attrs.define
class ExcludedPeaks:
	"""
	Represents the excluded peaks in a project.
	"""

	#: Partial alignment of peaks.
	alignment: Alignment

	#: Small peaks
	small_peaks: List[Peak]

	#: Peaks filtered during the consolidate process
	filtered_out_consolidated_peaks: List[ConsolidatedPeak]

	#: Stdout from alignment and peak identification process, for debugging.
	debug_stdout: io.StringIO


def get_padded_peak_list(
		qualified_peak_list: List[QualifiedPeak],
		alignment_peak_list: Sequence[Optional[Peak]],
		) -> Sequence[Optional[QualifiedPeak]]:

	padded_qp_list: MutableSequence[Optional[QualifiedPeak]] = []
	qps = deque(qualified_peak_list)
	for ap in alignment_peak_list:
		if ap is None:
			padded_qp_list.append(None)
		else:
			qp = qps.popleft()
			assert qp.rt == ap.rt
			padded_qp_list.append(qp)

	return padded_qp_list


def get_excluded_peaks(
		project: Project,
		pyms_nist_search_config: PyMSNISTSearchCfg,
		peak_filter: InvertedFilter,
		) -> ExcludedPeaks:
	"""
	Determine excluded peaks in a project.

	:param project:
	:param pyms_nist_search_config:
	:param peak_filter:
	"""

	per_repeat_peak_counts: Dict[str, PeakCounts] = {}

	# df = project.alignment.get_peak_alignment(require_all_expr=False)

	all_unaligned_peaks: List[PeakList] = []

	repeat: Repeat
	for repeat in project.datafile_data.values():

		# Peak list after BB and subsequent noise and base peak filtering
		found_peaks = repeat.peaks

		# Peaks for which partners were found during alignment (after filktering to `min_peaks`)
		alignment_peaks = project.alignment.peakpos[project.alignment.expr_code.index(repeat.name)]

		unaligned_peaks = PeakList()
		unaligned_peaks.datafile_name = repeat.name

		assert repeat.qualified_peaks is not None
		qualified_peak_list = get_padded_peak_list(repeat.qualified_peaks, alignment_peaks)
		ap_rt_map = {ap.rt: idx for idx, ap in enumerate(alignment_peaks) if ap is not None}

		assert repeat.qualified_peaks is not None

		for p in repeat.peaks:
			p_rt = p.rt
			if p_rt in ap_rt_map:
				ap = qualified_peak_list[ap_rt_map[p_rt]]
			else:
				ap = None
			ap_rt = ap.rt if ap else None
			if not ap_rt:
				unaligned_peaks.append(p)

		qualified_peaks = PeakList(repeat.qualified_peaks)
		qp_rt_map = {qp.rt: idx for idx, qp in enumerate(qualified_peaks)}

		# Peaks filtered after alignment due to size (``top_n_peaks`` and ``min_peak_area``)
		small_peaks = PeakList(ap for ap in alignment_peaks if ap and ap.rt not in qp_rt_map)

		# Make sure we haven't lost a peak along the way
		assert len(unaligned_peaks) + len(qualified_peaks) + len(small_peaks) == len(found_peaks)

		all_unaligned_peaks.append(unaligned_peaks)

		per_repeat_peak_counts[repeat.name] = PeakCounts(
				found_peaks=len(found_peaks),
				alignment_peaks=len(alignment_peaks),
				unaligned_peaks=len(unaligned_peaks),
				small_peaks=len(small_peaks),
				)

	debug_stdout = io.StringIO()

	with redirect_stdout(debug_stdout):
		A1 = align_peaks(all_unaligned_peaks)

	peaks_to_consolidate_counts = {pc.alignment_peaks - pc.small_peaks for pc in per_repeat_peak_counts.values()}
	assert len(peaks_to_consolidate_counts) == 1
	peaks_to_consolidate_count = next(iter(peaks_to_consolidate_counts))

	with redirect_stdout(debug_stdout):
		with engine_on_demand(pyms_nist_search_config) as search:
			unfiltered_consolidated_peaks, _ = consolidate(project, search.engine)

	filtered_out_consolidated_peaks = peak_filter.filter(unfiltered_consolidated_peaks)

	# print(len(unfiltered_consolidated_peaks))
	# print(len(filtered_out_consolidated_peaks))
	# print(len(project.consolidated_peaks))
	# print(peaks_to_consolidate_count)
	assert len(unfiltered_consolidated_peaks) == peaks_to_consolidate_count

	return ExcludedPeaks(
			alignment=A1,
			debug_stdout=debug_stdout,
			small_peaks=small_peaks,
			filtered_out_consolidated_peaks=filtered_out_consolidated_peaks,
			)
