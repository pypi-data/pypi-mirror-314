#!/usr/bin/env python3
#
#  projects.py
"""
Metadata for project pipelines.
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
from collections.abc import Iterable
from typing import Any, Dict, Iterator, List, Mapping, MutableMapping, Optional, Type

# 3rd party
import attrs
import tomli_w
from domdf_python_tools.paths import PathPlus
from domdf_python_tools.typing import PathLike
from libgunshotmatch.consolidate import ConsolidatedPeakFilter
from libgunshotmatch.datafile import Repeat
from libgunshotmatch.method import Method, MethodBase, _submethod_field
from libgunshotmatch.method._fields import String
from libgunshotmatch.project import Project
from libgunshotmatch.utils import _fix_init_annotations

# this package
from gunshotmatch_pipeline import prepare_datafile, project_from_repeats
from gunshotmatch_pipeline.config import Configuration
from gunshotmatch_pipeline.nist_ms_search import engine_on_demand
from gunshotmatch_pipeline.utils import tomllib

__all__ = ("GlobalSettings", "LoaderMixin", "ProjectSettings", "Projects", "process_projects")


def _convert_datafiles(datafiles: Any) -> List[str]:
	if not isinstance(datafiles, Iterable):
		raise TypeError("'datafiles' must be an iterable.")
	return [str(x) for x in datafiles]


class LoaderMixin:
	"""
	Mixin class providing ``load_method()`` and ``load_config()`` methods.
	"""

	# Relative or absolute filename to the method TOML file. The table name is "method".
	method: Optional[str]

	# Relative or absolute filename to the configuration TOML file. The table name is "gunshotmatch".
	config: Optional[str]

	def load_method(self) -> Method:
		"""
		Load the method for this project from the specified file.
		"""

		return Method.from_toml(PathPlus(self.method).read_text())

	def load_config(self) -> Configuration:
		"""
		Load the configuration for this project from the specified file.
		"""

		return Configuration.from_toml(PathPlus(self.config).read_text())


@_fix_init_annotations
@attrs.define
class GlobalSettings(MethodBase, LoaderMixin):
	"""
	Settings applied for all projects.

	:param method:

	The method and config files may point to the same TOML file.

	.. autosummary-widths:: 25/100
	"""

	#: Relative or absolute path to the directory the output files should be placed in.
	output_directory: str = String.field(default="output")

	#: Relative or absolute filename to the method TOML file. The table name is "method".
	method: Optional[str] = attrs.field(default=None)

	#: Relative or absolute filename to the configuration TOML file. The table name is "gunshotmatch".
	config: Optional[str] = attrs.field(default=None)

	#: Relative or absolute path to the directory containing the data files.
	data_directory: Optional[str] = attrs.field(default=None)


@_fix_init_annotations
@attrs.define
class ProjectSettings(MethodBase, LoaderMixin):
	"""
	Settings for a specific project.

	.. autosummary-widths:: 30/100

	:param name: The project name.
	"""

	name: str = String.field(default=attrs.NOTHING)
	"""
	The project name.

	.. latex:clearpage::
	"""

	#: List of input datafiles (paths relative to the data_directory option)
	datafiles: List[str] = attrs.field(converter=_convert_datafiles)  # type: ignore[misc]
	# mypy is confused by the `default=attrs.NOTHING`

	#: Relative or absolute filename to the method TOML file. The table name is "method".
	method: Optional[str] = attrs.field(default=None)

	#: Relative or absolute filename to the configuration TOML file. The table name is "config".
	config: Optional[str] = attrs.field(default=None)

	#: Relative or absolute path to the directory containing the data files.
	data_directory: Optional[str] = attrs.field(default=None)

	def get_datafile_paths(self) -> Iterator[PathPlus]:
		"""
		Returns an iterator over paths to the datafiles.

		The paths start with :py:attr:`~.ProjectSettings.data_directory` if set.
		"""

		data_directory = PathPlus(self.data_directory)
		for filename in self.datafiles:
			yield data_directory / filename


@_fix_init_annotations
@attrs.define
class Projects(MethodBase):
	"""
	Reference data projects to process through the pipeline.

	:param global_settings:

	.. autosummary-widths:: 45/100
	"""

	#: Settings applied for all projects.
	global_settings: GlobalSettings = _submethod_field(GlobalSettings)

	#: Settings for specific projects.
	per_project_settings: Dict[str, ProjectSettings] = attrs.field(factory=dict)

	@classmethod
	def from_toml(cls: Type["Projects"], toml_string: str) -> "Projects":
		"""
		Parse a :class:`~.Projects` from a TOML string.

		:param toml_string:
		"""

		parsed_toml = tomllib.loads(toml_string)
		global_settings = parsed_toml.pop("global")

		per_project_settings: Dict[str, ProjectSettings] = {
				project_name: (ProjectSettings(project_name, **project_settings_toml))
				for project_name,
				project_settings_toml in parsed_toml.items()
				}
		# per_project_settings: Dict[str, ProjectSettings] = {}

		# for project_name, project_settings_toml in parsed_toml.items():
		# 	per_project_settings[project_name] = (ProjectSettings(project_name, **project_settings_toml))

		return cls(global_settings, per_project_settings)

	@classmethod
	def from_json(cls: Type["Projects"], json_string: str) -> "Projects":
		"""
		Parse a :class:`~.Projects` from a JSON string.

		:param json_string:
		"""

		parsed_json = json.loads(json_string)
		return cls(**parsed_json)

	def to_toml(self) -> str:
		"""
		Convert a :class:`~.Configuration` to a TOML string.
		"""

		return tomli_w.dumps(self.to_dict())

	@staticmethod
	def _get_shared_without_none(data: Mapping[str, Optional[str]]) -> MutableMapping[str, str]:
		global_keys = {"method", "config", "data_directory"}
		return {k: v for k, v in data.items() if k in global_keys and v is not None}

	def get_project_settings(self, project_name: str) -> ProjectSettings:
		"""
		Returns the settings for the given project, taking into account the global settings.

		:param project_name:

		:rtype:

		.. latex:clearpage::
		"""

		per_project_settings = self.per_project_settings[project_name].to_dict()

		per_project_dict = self._get_shared_without_none(per_project_settings)
		global_settings = self._get_shared_without_none(self.global_settings.to_dict())

		global_settings.update(per_project_dict)

		settings = ProjectSettings(**{**per_project_settings, **global_settings})

		if settings.method is None:
			raise ValueError(f"'method' unset for {settings.name!r}")
		if settings.config is None:
			raise ValueError(f"'config' unset for {settings.name!r}")

		return settings

	def iter_project_settings(self) -> Iterator[ProjectSettings]:
		"""
		Iterate over the per-project settings, taking into account the global settings.
		"""

		for project_name in self.per_project_settings.keys():
			yield self.get_project_settings(project_name)

	def load_project(self, project_name: str) -> Project:
		"""
		Load a previously created project.

		:param project_name:
		"""

		self.get_project_settings(project_name)  # Ensures the project name is known
		output_dir = PathPlus(self.global_settings.output_directory)
		return Project.from_file(output_dir / f"{project_name}.gsmp")

	def iter_loaded_projects(self) -> Iterator[Project]:
		"""
		Iterate :class:`~libgunshotmatch.project.Project` objects loaded from disk.
		"""

		for project_name in self.per_project_settings.keys():
			yield self.load_project(project_name)

	# @staticmethod
	# def _check_common(to_check: Set[Any], global_option: Any, name: str):
	# 	if to_check == {None} and global_option is None:
	# 		raise ValueError(f"{name!r} is unset for all projects and unset globally")
	# 	elif to_check == {None}:
	# 		return True
	# 	elif len(to_check) == 1:
	# 		return True
	# 	else:
	# 		return False

	def _check_common(self, name: str) -> bool:
		"""
		Returns whether all projects have a common method/comfig attribute.

		:param name: The attribute name in :class:`~.ProjectSettings`
		"""

		to_check = {getattr(v, name) for v in self.per_project_settings.values()}
		global_option = getattr(self.global_settings, name)
		if to_check == {None} and global_option is None:
			raise ValueError(f"{name!r} is unset for all projects and unset globally")
		elif to_check == {None}:
			return True
		elif len(to_check) == 1:
			return True
		else:
			return False

	def has_common_method(self) -> bool:
		"""
		Returns whether all projects have a common method.
		"""

		# return self._check_common({v.method for v in self.per_project_settings.values()}, self.global_settings.method, "method")
		return self._check_common("method")

	def has_common_config(self) -> bool:
		"""
		Returns whether all projects have common configuration.
		"""

		# return self._check_common({v.config for v in self.per_project_settings.values()})
		return self._check_common("config")

	def __len__(self) -> int:
		return len(self.per_project_settings)


def process_projects(projects: Projects, output_dir: PathLike, recreate: bool = False) -> Iterator[Project]:
	"""
	Process projects with common methods and config.

	:param projects:
	:param output_dir:
	:param recreate: Force regeneration of ``.gsmr`` and ``.gsmp`` files.
	"""

	output_dir = PathPlus(output_dir)
	output_dir.maybe_make()

	if projects.has_common_method():
		method = projects.global_settings.load_method()
	else:
		raise ValueError("'process_projects' requires all projects to have a common method.")

	if projects.has_common_config():
		config = projects.global_settings.load_config()
	else:
		raise ValueError("'process_projects' requires all projects to have common configuration.")

	# Initialise search engine.
	with engine_on_demand(config.pyms_nist_search) as search:
		for project_settings in projects.iter_project_settings():
			gsmp_filename = output_dir / f"{project_settings.name}.gsmp"
			if gsmp_filename.exists() and not recreate:
				print(f"Loading Project from file {gsmp_filename.as_posix()!r}")
				project = Project.from_file(gsmp_filename)
			else:

				repeats = []

				for filename in project_settings.get_datafile_paths():
					gsmr_filename = (output_dir / filename.name).with_suffix(".gsmr")
					print(gsmr_filename)
					if gsmr_filename.exists() and not recreate:
						print(f"Loading Repeat from file {gsmr_filename.as_posix()!r}")
						repeat = Repeat.from_file(gsmr_filename)
						repeat.peaks.datafile_name = repeat.name
					else:
						print("\nParsing", filename)
						repeat, gcms_data = prepare_datafile(filename, method)
						repeat.export(output_dir)

					repeats.append(repeat)

				project = project_from_repeats(repeats, project_settings.name, method, engine=search.engine)
				export_filename = project.export(output_dir)
				# print(f"Project saved to {export_filename!r}")

			if not project.consolidated_peaks:

				cp_filter = ConsolidatedPeakFilter.from_method(method.consolidate)
				ms_comparison_df = project.consolidate(search.engine, cp_filter)
				# print(ms_comparison_df)

				export_filename = project.export(output_dir)
				print(f"Project saved to {export_filename!r}")

			yield project
