from __future__ import annotations

import asyncio
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, Generic, List, Optional, Type, TypeVar

import aiohttp
from rich.console import Console
from rich.progress import Progress
from rich.table import Table

from orcestradownloader.cache import Cache
from orcestradownloader.logging_config import logger as log
from orcestradownloader.models.base import BaseModel

# Type variable for subclasses of BaseModel
T = TypeVar('T', bound=BaseModel)

CACHE_DIR = Path.home() / '.cache/orcestradownloader'


CACHE_DAYS_TO_KEEP = 7


class TablePrinter:
	"""Handles table rendering for datasets using Rich."""

	def __init__(self, title: str, headers: List[str]) -> None:
		self.title = title
		self.headers = headers

	@property
	def color_list(self) -> List[str]:
		"""Simple list of colors for use in Rich."""
		return ['bold white', 'magenta', 'cyan', 'green', 'yellow', 'red', 'blue']

	def print_table(self, items: List[Any], row_generator: Callable) -> None:
		"""
		Prints a table of items.

		Parameters
		----------
		items : List[Any]
				A list of dataset items.
		row_generator : callable
				A function to generate rows from items.
		"""
		console = Console()
		table = Table(title=self.title)

		for header in self.headers:
			# table.add_column(header, justify="left", style="cyan", no_wrap=True)
			table.add_column(
				header,
				justify='left',
				style=self.color_list[self.headers.index(header)],
				no_wrap=True,
			)

		for item in items:
			table.add_row(*row_generator(item))

		console.print(table)


@dataclass
class DatasetManager(Generic[T]):
	"""Base class for managing datasets."""

	url: str
	cache_file: str
	dataset_type: Type[T]
	datasets: List[T] = field(default_factory=list)

	def __post_init__(self) -> None:
		self.cache = Cache(CACHE_DIR, self.cache_file, CACHE_DAYS_TO_KEEP)

	async def fetch_data(self, name: str, force: bool = False) -> None:
		"""Fetch datasets from API or cache."""
		log.info(
			'[bold magenta]%s:[/] Fetching data from %s (force=%s)...',
			name,
			self.url,
			force,
		)
		if not force and (cached_data := self.cache.get_cached_response(name=name)):
			self.datasets = [self.dataset_type.from_json(item) for item in cached_data]
			return

		async with aiohttp.ClientSession() as session:  # noqa: SIM117
			async with session.get(self.url) as response:
				data = await response.json()
				log.info(
					'[bold magenta]%s:[/] Fetched %d items from API.', name, len(data)
				)
				self.cache.cache_response(name, data)
				self.datasets = [self.dataset_type.from_json(item) for item in data]

	def print(self, title: str, row_generator: Callable) -> None:
		"""Print datasets in a formatted table."""
		printer = TablePrinter(
			title, headers=['Name', 'Dataset Name', 'Date Created', 'Datatypes']
		)
		printer.print_table(self.datasets, row_generator)

	def names(self) -> List[str]:
		"""List all datasets."""
		return [ds.name for ds in self.datasets]

	def __getitem__(self, name: str) -> T:
		"""Get a dataset by name."""
		try:
			return next(ds for ds in self.datasets if ds.name == name)
		except StopIteration as se:
			msg = f'Dataset {name} not found in {self.__class__.__name__}.'
			msg += f' Available datasets: {", ".join(self.names())}'
			raise ValueError(msg) from se


class DatasetRegistry:
	"""Registry to hold dataset manager instances."""

	def __init__(self) -> None:
		self.registry: Dict[str, DatasetManager] = {}

	def register(self, name: str, manager: DatasetManager) -> None:
		self.registry[name] = manager

	def get_manager(self, name: str) -> DatasetManager:
		return self.registry[name]

	def get_all_managers(self) -> Dict[str, DatasetManager]:
		return self.registry


# Register dataset managers
REGISTRY = DatasetRegistry()


class UnifiedDataManager:
	"""Unified manager to handle all dataset types."""

	def __init__(self, force: bool = False) -> None:
		self.force = force
		self.registry = REGISTRY

	def fetch_one(self, name: str) -> None:
		asyncio.run(self.fetch_by_name(name, force=self.force))

	def hydrate_cache(self) -> None:
		"""Hydrate the cache."""
		asyncio.run(self.fetch_all(force=True))

	async def fetch_by_name(
		self, name: str, force: bool = False, progress: Optional[Progress] = None
	) -> None:
		"""Fetch a specific dataset by name."""
		manager = self.registry.get_all_managers()[name]
		task = (
			progress.add_task(f'[cyan]Fetching {name}...', total=None)
			if progress
			else None
		)
		await manager.fetch_data(name=name, force=force)
		if progress and task is not None:
			progress.update(task, completed=True)

	async def fetch_all(self, force: bool = False) -> None:
		"""Fetch all datasets asynchronously."""
		with Progress(transient=True) as progress:
			await asyncio.gather(
				*[
					self.fetch_by_name(name, force, progress)
					for name in self.registry.get_all_managers()
				]
			)

	def print_one_table(self, name: str) -> None:
		"""Print a single dataset."""
		# Fetch data asynchronously
		try:
			self.fetch_one(name)
		except Exception as e:
			log.exception('Error fetching %s: %s', name, e)
			return

		manager = self.registry.get_manager(name)
		manager.print(
			title=name.capitalize(),
			row_generator=lambda item: [
				item.name,
				item.dataset.name,
				item.date_created.strftime('%Y-%m-%d') if item.date_created else 'N/A',
				', '.join(item.datatypes),
			],
		)

	def print_all_table(self) -> None:
		"""Print all datasets."""
		# Fetch data asynchronously
		asyncio.run(self.fetch_all(self.force))

		# Print datasets
		for name, manager in self.registry.get_all_managers().items():
			manager.print(
				title=name.capitalize(),
				row_generator=lambda item: [
					item.name,
					item.dataset.name,
					item.date_created.strftime('%Y-%m-%d')
					if item.date_created
					else 'N/A',
					', '.join(item.datatypes),
				],
			)

	def list_one(self, name: str, pretty: bool = True) -> None:
		"""List a single dataset."""
		# Fetch data asynchronously
		try:
			self.fetch_one(name)
		except Exception as e:
			log.exception('Error fetching %s: %s', name, e)
			return

		manager = self.registry.get_manager(name)
		ds_names = manager.names()

		if pretty:
			Console().print(f'[bold]{name}:[/]')
			for ds_name in ds_names:
				Console().print(f'  - [green]{ds_name}[/]')
		else:
			import click

			for ds_name in ds_names:
				click.echo(ds_name)

	def list_all(self, pretty: bool = True, force: bool = False) -> None:
		"""List all datasets."""
		# Fetch data asynchronously
		if force:
			asyncio.run(self.fetch_all(self.force))

		ds_dict = defaultdict(list)

		for name, manager in self.registry.get_all_managers().items():
			ds_names = manager.names()
			ds_dict[name] = ds_names

		if pretty:
			for name, ds_names in ds_dict.items():
				Console().print(f'[bold]{name}:[/]')
				for ds_name in ds_names:
					Console().print(f'  - [green]{ds_name}[/]')
		else:
			for name, ds_names in ds_dict.items():
				import click

				for ds_name in ds_names:
					click.echo(f'{name},{ds_name}')

	def download_one(self, 
									 manager_name: str, 
									 ds_name: List[str],
									 directory: Path, 
									 overwrite: bool = False, 
									 force: bool = False
	) -> Path:
		"""Download a single dataset."""
		# Fetch data asynchronously
		try:
			self.fetch_one(manager_name)
		except Exception as e:
			log.exception('Error fetching %s: %s', manager_name, e)
			errmsg = f'Error fetching {manager_name}: {e}'
			raise ValueError(errmsg) from e
		
		manager = self.registry.get_manager(manager_name)
		dataset_list = [manager[ds_name] for ds_name in ds_name]

		for ds in dataset_list:
			if not ds.download_link:
				msg = f'Dataset {ds.name} does not have a download link.'
				raise ValueError(msg)
			
			file_path = directory / f'{ds.name}.zip'
		return file_path

	def names(self) -> List[str]:
		"""List all managers."""
		return list(self.registry.get_all_managers().keys())

	def __getitem__(self, name: str) -> DatasetManager:
		"""Get a manager by name."""
		try:
			return self.registry.get_manager(name)
		except StopIteration as se:
			msg = f'Manager {name} not found in {self.__class__.__name__}.'
			msg += f' Available managers: {", ".join(self.names())}'
			raise ValueError(msg) from se