"""
toxicoset.py

This module provides the ToxicoSet class for managing toxicogenomic datasets
in the OrcestraDownloader project.

Classes:
    ToxicoSet: Class representing a toxicogenomic dataset.

Author:
    Your Name <your.email@example.com>
"""

from __future__ import annotations

from dataclasses import dataclass

from orcestradownloader.logging_config import logger as log
from orcestradownloader.models.base import BaseModel


@dataclass
class ToxicoSet(BaseModel):
	"""
	Represents a toxicogenomic dataset.

	Inherits from BaseModel for shared functionality.
	"""

	@classmethod
	def from_json(cls, data: dict) -> ToxicoSet:
		"""
		Create a ToxicoSet instance from a JSON object.

		Parameters
		----------
		data : dict
		    The JSON object containing data for the record.

		Returns
		-------
		ToxicoSet
		    An instance of ToxicoSet.
		"""
		log.debug('Parsing ToxicoSet from JSON: %s', data)
		return super().from_json(data)
