from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Type, List

import click
from click import Group, MultiCommand, Context, HelpFormatter

from pathlib import Path
from orcestradownloader.logging_config import set_log_verbosity
from orcestradownloader.managers import REGISTRY, DatasetManager, UnifiedDataManager
from orcestradownloader.models import ICBSet, PharmacoSet, RadioSet, ToxicoSet, XevaSet, RadiomicSet

DEFAULT_DATA_DIR = Path.cwd() / 'rawdata' / 'orcestradata'

@dataclass
class DatasetConfig:
	url: str
	cache_file: str
	dataset_type: Type


DATASET_CONFIG: Dict[str, DatasetConfig] = {
	'pharmacosets': DatasetConfig(
		url='https://orcestra.ca/api/pset/available',
		cache_file='pharmacosets.json',
		dataset_type=PharmacoSet
	),
	'icbsets': DatasetConfig(
		url='https://orcestra.ca/api/clinical_icb/available',
		cache_file='icbsets.json',
		dataset_type=ICBSet
	),
	'radiosets': DatasetConfig(
		url='https://orcestra.ca/api/radioset/available',
		cache_file='radiosets.json',
		dataset_type=RadioSet
	),
	'xevasets': DatasetConfig(
		url='https://orcestra.ca/api/xevaset/available',
		cache_file='xevasets.json',
		dataset_type=XevaSet
	),
	'toxicosets': DatasetConfig(
		url='https://orcestra.ca/api/toxicoset/available',
		cache_file='toxicosets.json',
		dataset_type=ToxicoSet
	),
	'radiomicsets': DatasetConfig(
		url='https://orcestra.ca/api/radiomicset/available',
		cache_file='radiomicsets.json',
		dataset_type=RadiomicSet
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
				"""List ALL datasets for this data type.""" 
				manager = UnifiedDataManager(force=force)
				manager.list_one(name, pretty=not no_pretty)

			@ds_group.command(name='table')
			@set_log_verbosity()
			@click.argument('ds_name', nargs=1, type=str, required=False, metavar='[NAME OF DATASET]')
			@click.option('--force', is_flag=True, help='Force fetch new data')
			@click.pass_context
			def _table(ctx, force: bool = False, verbose: int = 1, quiet: bool = False, ds_name: str | None = None):
				"""Print a table summary items for this dataset.
				
				If no dataset name is provided, prints a table of all datasets.
				If a dataset name is provided, prints a table of the specified dataset.
				""" 
				manager = UnifiedDataManager(force=force)
				manager.fetch_one(name)
				ds_manager = manager[name]
				if ds_name:
					ds_manager[ds_name].print_summary(title=f'{ds_name} Summary')
				else:
					manager.print_one_table(name)
					

			@ds_group.command(name='download')
			@click.option('--overwrite', '-o', is_flag=True, help='Overwrite existing file, if it exists.', default=False, show_default=True)
			@click.option(
				'--directory', 
				'-d', 
				help=f'Directory to save the file to. Defaults to ./{DEFAULT_DATA_DIR.relative_to(Path.cwd())}',
				default=DEFAULT_DATA_DIR,
				type=click.Path(
					exists=False, 
					file_okay=False, 
					dir_okay=True, 
					writable=True, 
					path_type=Path
				), 
			)
			@click.argument(
				'ds_name',
				type=str,
				required=True,
				nargs=-1,
				metavar='[NAME OF DATASET]'
			)
			@click.option('--force', is_flag=True, help='Force fetch new data from the API. Useful if the data has been updated on the API.', default=False, show_default=True)
			@set_log_verbosity()
			@click.pass_context
			def _download(
				ctx, 
				ds_name: List[str],
				directory: Path,
				force: bool = False, 
				verbose: int = 1, 
				quiet: bool = False, 
				overwrite: bool = False
			):
				"""Download a file for this dataset."""
				manager = UnifiedDataManager(force=force)
				file_paths = manager.download_by_name(name, ds_name, directory, overwrite, force)
				for file_path in file_paths:
					click.echo(f'Downloaded {file_path}')
			return ds_group
		return None

	def format_commands(self, ctx: Context, formatter: HelpFormatter) -> None:
		"""Extra format methods for multi methods that adds all the commands
		after the options.
		"""
		commands = []
		for subcommand in self.list_commands(ctx):
				cmd = self.get_command(ctx, subcommand)
				# What is this, the tool lied about a command.  Ignore it
				if cmd is None:
						continue
				if cmd.hidden:
						continue

				commands.append((subcommand, cmd))

		# allow for 3 times the default spacing
		if len(commands):
				limit = formatter.width - 6 - max(len(cmd[0]) for cmd in commands)

				rows = []
				for subcommand, cmd in commands:
						help = cmd.get_short_help_str(limit)
						rows.append((subcommand, help))

				if rows:
						with formatter.section("Dataset Types"):
								formatter.write_dl(rows)

	def format_usage(self, ctx, formatter):
		"""Custom string for the Usage section of the help page."""
		formatter.write_usage(
			"orcestra",
			"[DATASET_TYPE] [SUBCOMMAND] [ARGS]..."
		)

	def format_options(self, ctx: Context, formatter: HelpFormatter) -> None:
		"""Custom override so the dataset types are listed first."""
		self.format_commands(ctx, formatter)
		super(MultiCommand, self).format_options(ctx, formatter)

@click.command(cls=DatasetMultiCommand, context_settings=CONTEXT_SETTINGS, invoke_without_command=True)
@click.option('-r', '--refresh', is_flag=True, help='Fetch all datasets and hydrate the cache.', default=False, show_default=True)
@click.help_option("-h", "--help", help="Show this message and exit.")
@set_log_verbosity()
@click.pass_context
def cli(ctx, refresh: bool = False, verbose: int = 0, quiet: bool = False):
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
		list radiosets
		$ orcestra radiosets list

	\b
		print a table of all xevasets while refreshing the cache
		$ orcestra xevasets table --force

	\b
		print a table of a specific dataset with more details
		$ orcestra pharmacosets table 'GDSC_2020(v2-8.2)'
	
	To get help on a subcommand, use:

		orcestra [dataset_type] [subcommand] --help

	"""
	ctx.ensure_object(dict)

	# if user wants to refresh all datasets in the cache
	if refresh:
		manager = UnifiedDataManager(force=True)
		manager.hydrate_cache()
		manager.list_all()
		return

	# if no subcommand is provided, print help
	elif ctx.invoked_subcommand is None:
		click.echo(ctx.get_help())
		return

if __name__ == '__main__':
	cli()