from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Type

import click
from click import Group, MultiCommand


from orcestradownloader.logging_config import set_log_verbosity
from orcestradownloader.managers import REGISTRY, DatasetManager, UnifiedDataManager
from orcestradownloader.models import ICBSet, PharmacoSet, RadioSet, ToxicoSet, XevaSet


@dataclass
class DatasetConfig:
	url: str
	cache_file: str
	dataset_type: Type


DATASET_CONFIG: Dict[str, DatasetConfig] = {
	'pharmacosets': DatasetConfig(
		url='https://orcestra.ca/api/psets/available',
		cache_file='pharmacosets.json',
		dataset_type=PharmacoSet
	),
	'icbsets': DatasetConfig(
		url='https://orcestra.ca/api/clinical_icb/available',
		cache_file='icbsets.json',
		dataset_type=ICBSet
	),
	'radiosets': DatasetConfig(
		url='https://orcestra.ca/api/radiosets/available',
		cache_file='radiosets.json',
		dataset_type=RadioSet
	),
	'xevasets': DatasetConfig(
		url='https://orcestra.ca/api/xevasets/available',
		cache_file='xevasets.json',
		dataset_type=XevaSet
	),
	'toxicosets': DatasetConfig(
		url='https://orcestra.ca/api/toxicosets/available',
		cache_file='toxicosets.json',
		dataset_type=ToxicoSet
	),
}

# Register all dataset managers automatically
for name, config in DATASET_CONFIG.items():
	manager = DatasetManager(
		url=config.url,
		cache_file=config.cache_file,
		dataset_type=config.dataset_type
	)
	REGISTRY.register(name, manager)


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


class DatasetMultiCommand(MultiCommand):
	"""
	A custom MultiCommand that dynamically creates subcommands based on DATASET_CONFIG.
	Each dataset type gets its own group with 'list' and 'table' subcommands.
	"""

	def list_commands(self, ctx):
		return list(DATASET_CONFIG.keys())

	def get_command(self, ctx, name):
		if name in DATASET_CONFIG:
			ds_group = Group(name=name, context_settings=CONTEXT_SETTINGS)

			@ds_group.command(name='list')
			@set_log_verbosity()
			@click.option('--force', is_flag=True, help='Force fetch new data')
			@click.option('--no-pretty', is_flag=True, help='Disable pretty printing')
			@click.pass_context
			def _list(ctx, force: bool = False, no_pretty: bool = False, verbose: int = 1, quiet: bool = False):
				"""List items for this dataset."""
				manager = UnifiedDataManager(force=force)
				manager.list_one(name, pretty=not no_pretty)

			@ds_group.command(name='table')
			@set_log_verbosity()
			@click.option('--force', is_flag=True, help='Force fetch new data')
			@click.pass_context
			def _table(ctx, force: bool = False, verbose: int = 1, quiet: bool = False):
				"""Print a table of items for this dataset."""
				manager = UnifiedDataManager(force=force)
				manager.print_one_table(name)

			return ds_group
		return None

	def format_usage(self, ctx, formatter):
		formatter.write_usage(
			"orcestra",
			"[DATASET_TYPE] [SUBCOMMAND] [ARGS]..."
		)

@click.command(cls=DatasetMultiCommand, context_settings=CONTEXT_SETTINGS)
@click.help_option("-h", "--help", help="Show this message and exit.")
@click.pass_context
def cli(ctx, force: bool = False, verbose: int = 1, quiet: bool = False):
	"""
	Interactive CLI for datasets on orcestra.ca
	-------------------------------------------

	\b
	Each dataset currently supports the following subcommands:
	\b
		list: List all items in the dataset
		table: Print a table of items in the dataset

	\b
	Example:
	\b
		orcestra pharmacosets list
		orcestra xevasets table --force
	
	To get help on a subcommand, use:

		orcestra [dataset_type] [subcommand] --help

	"""
	ctx.ensure_object(dict)
	ctx.obj['force'] = force


if __name__ == '__main__':
	cli()