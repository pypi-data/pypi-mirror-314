#!/usr/bin/env python3
#
#  decision_tree.py
"""
Prepare data and train decision trees.

.. autosummary-widths:: 53/100
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
import string
from statistics import mean, stdev
from string import ascii_lowercase
from typing import Collection, Iterator, List, Tuple, Type

# 3rd party
import attrs
import graphviz  # type: ignore[import-untyped]
import numpy
import pandas  # type: ignore[import-untyped]
import sklearn.tree  # type: ignore[import-untyped]
from domdf_python_tools.paths import PathPlus
from libgunshotmatch.project import Project
from libgunshotmatch.utils import get_truncated_normal
from sklearn.base import ClassifierMixin  # type: ignore[import-untyped]
from sklearn.ensemble import RandomForestClassifier  # type: ignore[import-untyped]

# this package
import gunshotmatch_pipeline.results
from gunshotmatch_pipeline.projects import Projects
from gunshotmatch_pipeline.results import unknown_machine_learning_data
from gunshotmatch_pipeline.unknowns import UnknownSettings
from gunshotmatch_pipeline.utils import friendly_name_mapping

__all__ = (
		"data_from_projects",
		"fit_decision_tree",
		"simulate_data",
		"visualise_decision_tree",
		"DecisionTreeVisualiser",
		"get_feature_names",
		"data_from_unknown",
		"dotsafe_name",
		"predict_unknown",
		)

# Columns which don't correspond to compounds (features); i.e. metadata columns
_non_feature_columns = {"class", "member_id", "class-id"}


def data_from_projects(
		projects: Projects,
		normalize: bool = False,
		) -> Tuple[pandas.DataFrame, List[str]]:
	"""
	Returns a :class:`~pandas.DataFrame` containing decision tree data for the given projects.

	:param projects:
	:param normalize:
	"""

	# data = pandas.DataFrame.from_dict(_machine_learning_data(projects, normalize))
	data = pandas.DataFrame.from_dict(
			gunshotmatch_pipeline.results.machine_learning_data(
					*projects.iter_loaded_projects(), normalize=normalize
					)
			)

	data = data.rename(friendly_name_mapping, axis=1).fillna(0.0)
	# feature_names = list(data.columns)
	data["class"] = [name[:-2] for name in data.index]
	data["member_id"] = [name[-1] for name in data.index]
	data["class-id"], factorize_map = pandas.factorize(pandas.Categorical(data["class"]), sort=True)

	# feature_names = get_feature_names(data)
	return data, list(factorize_map)


def data_from_unknown(
		unknown: UnknownSettings,
		feature_names: Collection[str],
		normalize: bool = False,  # ) -> Tuple[pandas.DataFrame, List[str]]:
		) -> pandas.DataFrame:
	"""
	Returns a :class:`~pandas.DataFrame` containing decision tree data for the given unknown.

	:param unknown:
	:param feature_names: The compounds the decision tree was trained on. Extra compounds in the unknown will be excluded.
	:param normalize:
	"""

	project = Project.from_file(PathPlus(unknown.output_directory) / f"{unknown.name}.gsmp")
	data = pandas.DataFrame.from_dict(unknown_machine_learning_data(project, normalize))
	data = data.rename(friendly_name_mapping, axis=1).fillna(0.0)

	zeroes_padding_dict = {compound: 0.0 for compound in set(feature_names).difference(data.columns)}
	zeroes_padding = pandas.DataFrame(zeroes_padding_dict, index=data.index)
	data = pandas.concat((data, zeroes_padding), axis=1)

	return data[feature_names]


def simulate_data(
		project: Project,
		normalize: bool = False,
		n_simulated: int = 10,
		) -> pandas.DataFrame:
	"""
	Generate simulated peak area data for a project.

	:param project:
	:param normalize:
	:param n_simulated: The number of values to simulate.

	:rtype:

	.. latex:clearpage::
	"""

	propellant_data = gunshotmatch_pipeline.results.matches(project)

	real_data_size = len(propellant_data["metadata"]["original_filenames"])
	df_for_norm = pandas.DataFrame(index=list(string.ascii_lowercase[:real_data_size]))

	compounds_data = propellant_data["compounds"]

	for compound in compounds_data:
		df_for_norm[compound] = compounds_data[compound]["Peak Areas"]

	compounds = list(df_for_norm.columns)

	new_data: List[List[float]] = []

	for sample_idx in range(1, n_simulated + 1):
		new_data.append([])

	for compound in df_for_norm.columns:
		real_values = list(df_for_norm[compound])
		real_mean = mean(real_values)
		real_stdev = stdev(real_values)

		simulated_values = get_truncated_normal(
				real_mean,
				real_stdev,
				min(real_values),
				max(real_values),
				n_simulated,
				random_state=20230703,
				)

		# print(compound, simulated_values)

		for sample_idx, value in enumerate(simulated_values):
			new_data[sample_idx].append(value)

	for sample_idx in range(n_simulated):
		# print(sample_idx, real_data_size+sample_idx)
		df_for_norm.loc[ascii_lowercase[real_data_size + sample_idx]] = new_data[sample_idx]

	if normalize:
		df_for_norm = df_for_norm.div(df_for_norm.sum(axis=1), axis=0)
		df_for_norm["total"] = df_for_norm[compounds].sum(axis=1)
		for x in df_for_norm["total"]:
			assert abs(x - 1) < 1e-10, x

	return df_for_norm


def fit_decision_tree(
		data: pandas.DataFrame,
		classifier: ClassifierMixin,
		) -> List[str]:
	"""
	Fit the classifier to the data.

	:param data:
	:param classifier:

	:returns: List of feature names
	"""

	feature_names = get_feature_names(data)
	classifier.fit(data[feature_names], data["class-id"])
	return feature_names


def get_feature_names(data: pandas.DataFrame) -> List[str]:
	"""
	Return the feature names for the given data.

	:param data:
	"""

	return list(data.columns[~data.columns.isin(_non_feature_columns)])


_dotsafe_transmap = str.maketrans({
		'<': "&lt;",
		'>': "&gt;",
		'&': "&amp;",
		"'": "&apos;",
		'"': "&quot;",
		})


def dotsafe_name(name: str) -> str:
	"""
	Return a dot (graphviz) suitable name for a sample, with special characters escaped.

	:param name:

	:rtype:

	.. versionadded:: 0.5.0

	.. latex:clearpage::
	"""

	return name.translate(_dotsafe_transmap)


def visualise_decision_tree(
		data: pandas.DataFrame,
		classifier: ClassifierMixin,
		factorize_map: List[str],
		filename: str = "decision_tree_graphivz",
		filetype: str = "svg",
		) -> None:
	"""
	Visualise a decision tree with graphviz.

	:param data:
	:param classifier:
	:param factorize_map: List of class names in the order they appear as classes in the classifier.
	:param filename: Output filename without extension; for random forest, the base filename (followed by ``-tree-n``).
	:param filetype: Output filetype (e.g. svg, png, pdf).
	"""

	visualiser = DecisionTreeVisualiser.from_data(data, classifier, factorize_map)
	return visualiser.visualise_tree(filename, filetype)


@attrs.define
class DecisionTreeVisualiser:
	"""
	Class for exporting visualisations of a decision tree or random forest.

	.. versionadded:: 0.8.0
	"""

	#: Decision tree or random forest classifier.
	classifier: ClassifierMixin

	#: The compounds the decision tree was trained on.
	feature_names: List[str]

	#: List of class names in the order they appear as classes in the classifier.
	factorize_map: List[str] = attrs.field(on_setattr=attrs.setters.validate)

	# Cached names for graphvis
	_dotsafe_class_names: List[str] = attrs.field(init=False, default=None)

	@factorize_map.validator
	def _dotsafe_factorize_map(self, attribute: attrs.Attribute, value: List[str]) -> None:
		self._dotsafe_class_names = list(map(dotsafe_name, value))

	@classmethod
	def from_data(
			cls: Type["DecisionTreeVisualiser"],
			data: pandas.DataFrame,
			classifier: ClassifierMixin,
			factorize_map: List[str],
			) -> "DecisionTreeVisualiser":
		"""
		Alternative constructor from the pandas dataframe the classifier was trained on.
		"""

		feature_names = get_feature_names(data)
		return cls(classifier, feature_names, factorize_map)

	# def get_text_tree(self) -> str:
	# 	"""
	# 	Return a text representation of the tree.
	# 	"""

	# 	if isinstance(self.classifier, RandomForestClassifier):
	# 		raise NotImplementedError
	# 	else:
	# 		# Get text representation of decision tree
	# 		return sklearn.tree.export_text(self.classifier, feature_names=self.feature_names)

	def _get_graphviz(self, tree: ClassifierMixin) -> graphviz.Source:
		# DOT data
		dot_data = sklearn.tree.export_graphviz(
				tree,
				out_file=None,
				feature_names=self.feature_names,
				class_names=self._dotsafe_class_names,
				filled=False,
				special_characters=True,
				)

		return graphviz.Source(dot_data)

	def visualise_tree(
			self,
			filename: str = "decision_tree_graphivz",
			filetype: str = "svg",
			) -> None:
		"""
		Visualise the decision tree or random forest as an image.

		:param filename: Output filename without extension; for random forest, the base filename (followed by ``-tree-n``).
		:param filetype: Output filetype (e.g. svg, png, pdf).
		"""

		# TODO: handle PathLike for filename

		if isinstance(self.classifier, RandomForestClassifier):
			for idx, tree in enumerate(self.classifier.estimators_):
				graph = self._get_graphviz(tree)
				graph.render(
						f"{filename}-tree-{idx}.dot",
						outfile=f"{filename}-tree-{idx}.{filetype}",
						format=filetype,
						)
		else:
			graph = self._get_graphviz(self.classifier)
			graph.render(f"{filename}.dot", outfile=f"{filename}.{filetype}", format=filetype)


def predict_unknown(
		unknown: UnknownSettings,
		classifier: ClassifierMixin,
		factorize_map: List[str],
		feature_names: List[str],
		) -> Iterator[Tuple[str, float]]:
	"""
	Predict classes for an unknown sample from a decision tree or random forest.

	:param unknown:
	:param classifier:
	:param factorize_map: List of class names in the order they appear as classes in the classifier.
	:param feature_names: The compounds the decision tree was trained on. Extra compounds in the unknown will be excluded.

	:returns: An iterator of predicted class names and their probabilities, ranked from most to least likely.

	.. versionadded:: 0.9.0
	"""

	unknown_sample = data_from_unknown(unknown, feature_names=feature_names)
	proba = classifier.predict_proba(unknown_sample)
	argsort = numpy.argsort(proba, axis=1)

	class_names = [factorize_map[cls] for cls in reversed(argsort.tolist()[0])]
	probabilities = sorted(classifier.predict_proba(unknown_sample)[0], reverse=True)

	assert len(probabilities) == len(class_names)
	yield from zip(class_names, probabilities)
