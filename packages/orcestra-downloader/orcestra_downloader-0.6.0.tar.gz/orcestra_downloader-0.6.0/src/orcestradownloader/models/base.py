"""
base.py

This module provides a BaseModel class for managing shared attributes and functionality
across various dataset models in the OrcestraDownloader project. It minimizes redundancy
by centralizing common logic such as data parsing, summary printing, and datatype management.

Classes:
    BaseModel: Abstract base class for dataset records.

Author:
    Your Name <your.email@example.com>
"""

from __future__ import annotations

from abc import ABC
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional, Type, TypeVar

from rich.console import Console
from rich.table import Table

from orcestradownloader.models.common import (
	AbstractRecord,
	AvailableDatatype,
	Dataset,
	GenomeType,
	Publication,
	VersionInfo,
)

# Type variable for subclasses of BaseModel
T = TypeVar('T', bound='BaseModel')


@dataclass
class BaseModel(AbstractRecord, ABC):
	"""
	Abstract base class for dataset records.

	Centralizes common attributes and methods across all dataset models, such as PharmacoSet,
	ToxicoSet, and RadioSet.

	Attributes
	----------
	name : str
	    The name of the dataset record.
	doi : str
	    The DOI of the dataset record.
	download_link : str
	    The link to download the dataset.
	date_created : Optional[datetime]
	    The date when the dataset was created.
	dataset : Dataset
	    The dataset associated with the record.
	available_datatypes : List[AvailableDatatype]
	    A list of available datatypes for the dataset.
	"""

	name: str
	doi: str
	download_link: str
	date_created: Optional[datetime]
	dataset: Dataset
	available_datatypes: List[AvailableDatatype] = field(default_factory=list)

	@classmethod
	def from_json(cls: Type[T], data: dict) -> T:
		"""
		Create an instance of the subclass from a JSON object.

		Parameters
		----------
		data : dict
		    The JSON object containing data for the record.

		Returns
		-------
		T
		    An instance of the implementing subclass.
		"""
		date_created = cls.parse_date(data.get('dateCreated'))
		dataset = cls.parse_dataset(data['dataset'])
		datatypes = cls.parse_datatypes(data.get('availableDatatypes', []))
		return cls(
			name=data['name'],
			doi=data['doi'],
			download_link=data['downloadLink'],
			date_created=date_created,
			dataset=dataset,
			available_datatypes=datatypes,
		)

	@staticmethod
	def parse_date(date_str: Optional[str]) -> Optional[datetime]:
		"""
		Parse a date string into a datetime object.

		Parameters
		----------
		date_str : Optional[str]
		    The date string to parse.

		Returns
		-------
		Optional[datetime]
		    A datetime object if parsing is successful, else None.
		"""
		return datetime.fromisoformat(date_str.rstrip('Z')) if date_str else None

	@staticmethod
	def parse_dataset(dataset_data: dict) -> Dataset:
		"""
		Parse dataset information from a JSON object.

		Parameters
		----------
		dataset_data : dict
		    The JSON object containing dataset information.

		Returns
		-------
		Dataset
		    A Dataset instance.
		"""
		version_info = VersionInfo(
			version=dataset_data['versionInfo']['version'],
			dataset_type=None,  # Can be customized by subclasses
			publication=[
				Publication(**pub) for pub in dataset_data['versionInfo']['publication']
			],
		)
		return Dataset(name=dataset_data['name'], version_info=version_info)

	@staticmethod
	def parse_datatypes(datatypes: List[dict]) -> List[AvailableDatatype]:
		"""
		Parse available datatypes from a JSON object.

		Parameters
		----------
		datatypes : List[dict]
		    A list of JSON objects containing datatype information.

		Returns
		-------
		List[AvailableDatatype]
		    A list of AvailableDatatype instances.
		"""
		return [
			AvailableDatatype(
				name=dt['name'],
				genome_type=GenomeType(dt['genomeType'])
				if 'genomeType' in dt
				else None,
				source=dt.get('source'),
			)
			for dt in datatypes
		]

	@property
	def datatypes(self) -> List[str]:
		"""
		Get a list of available datatype names.

		Returns
		-------
		List[str]
		    A list of datatype names.
		"""
		return [datatype.name for datatype in self.available_datatypes]

	def print_summary(self, title: str | None = None) -> None:
		"""
		Print a summary of the dataset record.

		This method uses Rich to display a well-formatted table of the record's attributes.
		"""
		table = Table(
			title=title if title else f'{self.__class__.__name__} Summary'
		)

		table.add_column('Field', style='bold cyan', no_wrap=True)
		table.add_column('Value', style='magenta')

		table.add_row('Name', self.name)
		table.add_row('DOI', self.doi)
		table.add_row(
			'Date Created',
			self.date_created.isoformat() if self.date_created else 'N/A',
		)
		table.add_row('Download Link', self.download_link)
		table.add_row('Dataset Name', self.dataset.name)
		table.add_row('Dataset Version', self.dataset.version_info.version)
		table.add_row(
				'Dataset Type',
				self.dataset.version_info.dataset_type.name if self.dataset.version_info.dataset_type else 'N/A',
		)
		table.add_row(
			'Available Datatypes',
			', '.join(self.datatypes) if self.datatypes else 'N/A',
		)
		table.add_row(
			'Publications',
			', '.join([f"{pub.citation} ({pub.link})" for pub in self.dataset.version_info.publication])
		)

		console = Console()
		console.print(table)
