import json
from datetime import datetime
from pathlib import Path
from typing import List, Optional

from orcestradownloader.logging_config import logger as log


class Cache:
	def __init__(
		self, cache_dir: Path, cache_file: str, cache_days_to_keep: int = 7
	) -> None:
		self.cache_dir = cache_dir
		self.cache_file = cache_dir / cache_file
		self.cache_days_to_keep = cache_days_to_keep

	def get_cached_response(self, name: str) -> Optional[List[dict]]:
		"""Retrieve cached response if it exists and is up-to-date."""
		log.debug('Checking for cached response...')
		if not self.cache_file.exists():
			log.info('Cache file not found.')
			return None
		try:
			with self.cache_file.open('r') as f:
				cached_data = json.load(f)
			cache_date = datetime.fromisoformat(cached_data['date'])
			if (datetime.now() - cache_date).days <= self.cache_days_to_keep:
				diff = datetime.now() - cache_date
				if diff.days > 0:
					daysago = f'{diff.days} days ago'
				else:
					minutes = diff.seconds // 60
					hours = minutes // 60
					if hours > 0:
						daysago = f'{hours} hours ago'
					else:
						daysago = f'{minutes} minutes ago'
				log.info(
					'[bold magenta]%s:[/] Using cached response from %s from file://%s',
					name,
					daysago,
					self.cache_file,
				)
				response_data: List[dict] = cached_data['data']
				return response_data
			else:
				log.info('Cache is outdated.')
		except (json.JSONDecodeError, KeyError, ValueError) as e:
			log.warning('Failed to load cache: %s', e)
		return None

	def cache_response(self, data: List[dict]) -> None:
		"""Save the response to the cache."""
		self.cache_dir.mkdir(parents=True, exist_ok=True)
		with self.cache_file.open('w') as f:
			json.dump({'date': datetime.now().isoformat(), 'data': data}, f)
		log.info('Response cached successfully.')
