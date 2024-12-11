"""
clinical_icb.py

This module provides the ICBSet class for managing clinical datasets
in the OrcestraDownloader project.

Classes:
    ICBSet: Class representing a clinical dataset.

Author:
    Your Name <your.email@example.com>
"""

from __future__ import annotations

from dataclasses import dataclass

from orcestradownloader.logging_config import logger as log
from orcestradownloader.models.base import BaseModel


@dataclass
class ICBSet(BaseModel):
	"""
	Represents a clinical dataset record.

	Inherits from BaseModel for shared functionality.
	"""

	@classmethod
	def from_json(cls, data: dict) -> ICBSet:
		"""
		Create a ICBSet instance from a JSON object.

		Parameters
		----------
		data : dict
		    The JSON object containing data for the record.

		Returns
		-------
		ICBSet
		    An instance of ICBSet.
		"""
		log.debug('Parsing ICBSet from JSON: %s', data)
		return super().from_json(data)
