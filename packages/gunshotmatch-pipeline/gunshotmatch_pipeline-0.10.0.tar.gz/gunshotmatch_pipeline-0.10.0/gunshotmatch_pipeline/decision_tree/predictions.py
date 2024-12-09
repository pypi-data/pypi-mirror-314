#!/usr/bin/env python3
#
#  predictions.py
"""
Represents random forest classifier predictions for testing classifier performance.

.. versionadded:: 0.9.0
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
from typing import List, NamedTuple, Optional, Tuple

__all__ = ["PredictionResult", "dump_predictions", "load_predictions"]


class PredictionResult(NamedTuple):
	"""
	Represents the predicted classes from a random forest classifier.
	"""

	#: the sample name e.g. "Unknown Western Double A"
	name: str

	#: i.e. the ammo type e.g. "Western Double A"
	class_name: str

	#: Tuples of ``(<class name>, <probability>)``.
	predictions: Tuple[Tuple[str, float], ...]

	@property
	def correct(self) -> bool:
		"""
		Returns whether the top prediction matches the actual class name.
		"""

		return self.class_name == self.predictions[0][0]


def dump_predictions(predictions: List[PredictionResult], indent: Optional[int] = 2) -> str:
	"""
	Return a JSON representation of the predictions.

	:param predictions:
	:param indent:
	"""

	return json.dumps([pr._asdict() for pr in predictions], indent=indent)


def load_predictions(predictions_json: str) -> List[PredictionResult]:
	"""
	Load predictions from the given JSON string.

	:param predictions_json:
	"""

	predictions: List[PredictionResult] = [PredictionResult(**pr) for pr in json.loads(predictions_json)]
	return predictions
