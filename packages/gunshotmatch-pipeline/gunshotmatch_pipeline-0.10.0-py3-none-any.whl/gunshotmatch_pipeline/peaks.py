#!/usr/bin/env python3
#
#  peaks.py
"""
Peak detection and alignment functions.
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

# 3rd party
import pandas  # type: ignore[import-untyped]
from libgunshotmatch.datafile import Datafile
from libgunshotmatch.method import Method
from libgunshotmatch.peak import PeakList, align_peaks, filter_aligned_peaks, filter_peaks
from libgunshotmatch.project import Project
from pyms.BillerBiemann import BillerBiemann
from pyms.GCMS.Class import GCMS_data
from pyms.Peak.Function import peak_sum_area

__all__ = ("align_and_filter_peaks", "prepare_peak_list")


def prepare_peak_list(
		datafile: Datafile,
		gcms_data: GCMS_data,
		method: Method,
		) -> PeakList:
	"""
	Construct and filter the peak list.

	:param datafile:
	:param gcms_data:
	:param method:
	"""

	im = datafile.intensity_matrix
	assert im is not None

	peak_list: PeakList = PeakList(
			BillerBiemann(
					im,
					points=method.peak_detection.points,
					scans=method.peak_detection.scans,
					)
			)
	print(" Peak list before filtering:", peak_list)

	filtered_peak_list: PeakList = filter_peaks(
			peak_list,
			gcms_data.tic,
			noise_filter=method.peak_filter.noise_filter,
			noise_threshold=method.peak_filter.noise_filter,
			base_peak_filter=method.peak_filter.base_peak_filter,
			rt_range=method.peak_filter.rt_range,
			)
	print(" Peak list after filtering:", filtered_peak_list)

	for peak in filtered_peak_list:
		peak.area = peak_sum_area(im, peak)

	filtered_peak_list.datafile_name = datafile.name
	return filtered_peak_list


def align_and_filter_peaks(project: Project, method: Method) -> pandas.DataFrame:
	"""
	Perform peak alignment and peak filtering for the project, with the given method.

	:param project:
	:param method:
	"""

	project.alignment = align_peaks(
			[r.peaks for r in project.datafile_data.values()],
			rt_modulation=method.alignment.rt_modulation,
			gap_penalty=method.alignment.gap_penalty,
			min_peaks=method.alignment.min_peaks,
			)

	peaks_to_identify = filter_aligned_peaks(
			project.alignment,
			top_n_peaks=method.alignment.top_n_peaks,
			min_peak_area=method.alignment.min_peak_area,
			)

	return peaks_to_identify
