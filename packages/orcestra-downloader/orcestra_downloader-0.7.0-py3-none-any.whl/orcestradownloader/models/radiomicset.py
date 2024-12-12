"""
radiomicset.py

This module provides the radiomicset class for managing radiogenomic datasets
in the OrcestraDownloader project.

Classes:
    radiomicset: Class representing a radiogenomic dataset.

Author:
    Your Name <your.email@example.com>
"""

from __future__ import annotations

from dataclasses import dataclass

from orcestradownloader.logging_config import logger as log
from orcestradownloader.models.base import BaseModel


@dataclass
class RadiomicSet(BaseModel):
	"""
	Represents a radiogenomic dataset.

	Inherits from BaseModel for shared functionality.
	"""

	@classmethod
	def from_json(cls, data: dict) -> RadiomicSet:
		"""
		Create a RadiomicSet instance from a JSON object.

		Parameters
		----------
		data : dict
		    The JSON object containing data for the record.

		Returns
		-------
		RadiomicSet
		    An instance of RadiomicSet.
		"""
		log.debug('Parsing RadiomicSet from JSON: %s', data)
		return super().from_json(data)
