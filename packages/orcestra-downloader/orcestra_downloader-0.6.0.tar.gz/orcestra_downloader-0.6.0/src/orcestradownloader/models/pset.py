"""
pset.py

This module provides the PharmacoSet class, which extends the BaseModel class, for managing
pharmacogenomic datasets in the OrcestraDownloader project.

Classes:
    PharmacoSet: Class representing a pharmacogenomic dataset.

Author:
    Your Name <your.email@example.com>
"""

from __future__ import annotations

from dataclasses import dataclass

from orcestradownloader.logging_config import logger as log
from orcestradownloader.models.base import BaseModel


@dataclass
class PharmacoSet(BaseModel):
	"""
	Represents a pharmacogenomic dataset.

	This class inherits common attributes and methods from BaseModel and may include
	additional logic or methods specific to pharmacogenomic datasets.

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

	@classmethod
	def from_json(cls, data: dict) -> PharmacoSet:
		"""
		Create a PharmacoSet instance from a JSON object.

		Parameters
		----------
		data : dict
		    The JSON object containing data for the record.

		Returns
		-------
		PharmacoSet
		    An instance of PharmacoSet.
		"""
		log.debug('Parsing PharmacoSet from JSON: %s', data)
		return super().from_json(data)


# Example usage
if __name__ == '__main__':
	import json
	from pathlib import Path

	# Path to the cache file
	cache_file = Path.home() / '.cache/orcestradownloader/psets.json'

	# Read the JSON data
	with cache_file.open('r') as f:
		data = json.load(f)

	# Create a list of PharmacoSet instances
	psets = [PharmacoSet.from_json(pset_data) for pset_data in data['data']]

	# Print summaries of each PharmacoSet
	for pset in psets:
		pset.print_summary()
