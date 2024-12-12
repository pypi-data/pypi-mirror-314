from dataclasses import dataclass
from typing import Dict, Type

from orcestradownloader.models import (
	ICBSet,
	PharmacoSet,
	RadiomicSet,
	RadioSet,
	ToxicoSet,
	XevaSet,
)


@dataclass
class DatasetConfig:
	url: str
	cache_file: str
	dataset_type: Type


DATASET_CONFIG: Dict[str, DatasetConfig] = {
	'pharmacosets': DatasetConfig(
		url='https://orcestra.ca/api/pset/available',
		cache_file='pharmacosets.json',
		dataset_type=PharmacoSet,
	),
	'icbsets': DatasetConfig(
		url='https://orcestra.ca/api/clinical_icb/available',
		cache_file='icbsets.json',
		dataset_type=ICBSet,
	),
	'radiosets': DatasetConfig(
		url='https://orcestra.ca/api/radioset/available',
		cache_file='radiosets.json',
		dataset_type=RadioSet,
	),
	'xevasets': DatasetConfig(
		url='https://orcestra.ca/api/xevaset/available',
		cache_file='xevasets.json',
		dataset_type=XevaSet,
	),
	'toxicosets': DatasetConfig(
		url='https://orcestra.ca/api/toxicoset/available',
		cache_file='toxicosets.json',
		dataset_type=ToxicoSet,
	),
	'radiomicsets': DatasetConfig(
		url='https://orcestra.ca/api/radiomicset/available',
		cache_file='radiomicsets.json',
		dataset_type=RadiomicSet,
	),
}
