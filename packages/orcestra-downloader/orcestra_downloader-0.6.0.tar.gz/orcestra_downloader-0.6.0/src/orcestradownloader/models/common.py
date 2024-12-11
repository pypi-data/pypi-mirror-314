"""
common.py

This module provides common data structures and abstract classes for the OrcestraDownloader project.
It includes enumerations, dataclasses, and an abstract base class for managing dataset records.
These shared components are designed to be used across different dataset models, minimizing redundancy
and ensuring consistency.

Classes:
    GenomeType: Enum representing the type of genome data.
    TypeEnum: Enum representing the type of dataset.
    Publication: Dataclass representing a publication related to a dataset.
    VersionInfo: Dataclass containing version and publication information.
    AvailableDatatype: Dataclass representing a datatype available in a dataset.
    Dataset: Dataclass representing a dataset with version information.
    AbstractRecord: Abstract base class for dataset records.

Author:
    Your Name <your.email@example.com>
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class GenomeType(Enum):
	"""Enum representing the type of genome data."""

	DNA = 'DNA'
	RNA = 'RNA'


class TypeEnum(Enum):
	"""Enum representing the type of dataset."""

	BOTH = 'both'
	PERTURBATION = 'perturbation'
	SENSITIVITY = 'sensitivity'


@dataclass
class Publication:
	"""
	Represents a publication related to a dataset.

	Attributes
	----------
	citation : str
	    The citation for the publication.
	link : str
	    The URL link to the publication.
	"""

	citation: str
	link: str


@dataclass
class VersionInfo:
	"""
	Contains version and publication information for a dataset.

	Attributes
	----------
	version : str
	    The version of the dataset.
	dataset_type : Optional[TypeEnum]
	    The type of dataset (e.g., sensitivity, perturbation, both).
	publication : List[Publication]
	    List of publications related to the dataset.
	"""

	version: str
	dataset_type: Optional[TypeEnum]
	publication: List[Publication]


@dataclass
class AvailableDatatype:
	"""
	Represents a datatype available in a dataset.

	Attributes
	----------
	name : str
	    The name of the datatype (e.g., RNAseq, DNAseq).
	genome_type : Optional[GenomeType]
	    The type of genome data (DNA or RNA).
	source : Optional[str]
	    The source of the datatype.
	"""

	name: str
	genome_type: Optional[GenomeType]
	source: Optional[str] = None


@dataclass
class Dataset:
	"""
	Represents a dataset with version information.

	Attributes
	----------
	name : str
	    The name of the dataset.
	version_info : VersionInfo
	    Version information for the dataset.
	"""

	name: str
	version_info: VersionInfo


class AbstractRecord(ABC):
	"""
	Abstract base class for dataset records.

	This class defines the interface for all dataset records, requiring implementations
	to provide methods for JSON deserialization and summary printing.

	Methods
	-------
	from_json(data: dict) -> AbstractRecord
	    Abstract method for creating an instance from a JSON object.
	print_summary() -> None
	    Abstract method for printing a summary of the record.
	"""

	@classmethod
	@abstractmethod
	def from_json(cls, data: dict) -> AbstractRecord:
		"""
		Abstract method for creating an instance from a JSON object.

		Parameters
		----------
		data : dict
		    The JSON object containing data for the record.

		Returns
		-------
		AbstractRecord
		    An instance of the implementing class.
		"""
		pass

	@abstractmethod
	def print_summary(self) -> None:
		"""
		Abstract method for printing a summary of the record.

		This method should be implemented by subclasses to provide a detailed
		summary of the record's attributes.
		"""
		pass
