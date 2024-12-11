"""
xevaset.py

This module provides the XevaSet class for managing xenograft datasets
in the OrcestraDownloader project.

Classes:
    XevaSet: Class representing a xenograft dataset.

Author:
    Your Name <your.email@example.com>
"""

from __future__ import annotations

from dataclasses import dataclass

from orcestradownloader.logging_config import logger as log
from orcestradownloader.models.base import BaseModel


@dataclass
class XevaSet(BaseModel):
	"""
	Represents a xenograft dataset.

	Inherits from BaseModel for shared functionality.
	"""

	@classmethod
	def from_json(cls, data: dict) -> XevaSet:
		"""
		Create a XevaSet instance from a JSON object.

		Parameters
		----------
		data : dict
		    The JSON object containing data for the record.

		Returns
		-------
		XevaSet
		    An instance of XevaSet.
		"""
		log.debug('Parsing XevaSet from JSON: %s', data)
		return super().from_json(data)
