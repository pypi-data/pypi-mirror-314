import logging
from logging import ERROR, getLevelName, getLogger
from typing import Any, Callable

import click
from click.decorators import FC
from rich.logging import RichHandler


def setup_logger(name: str) -> logging.Logger:
	logging.basicConfig(
		level=logging.INFO,
		format='%(message)s',
		datefmt='[%X]',
		handlers=[
			RichHandler(rich_tracebacks=True, tracebacks_show_locals=True, markup=True)
		],
	)
	return logging.getLogger(name)


def set_log_verbosity(
	*param_decls: str,
	logger_name: str = 'orcestra',
	quiet_decl: tuple = ('--quiet', '-q'),
	**kwargs: Any,  # noqa
) -> Callable[[FC], FC]:
	"""
	Add a `--verbose` option to set the logging level based on verbosity count
	and a `--quiet` option to suppress all logging except errors.

	Parameters
	----------
	*param_decls : str
		Custom names for the verbosity flag.
	quiet_decl : tuple
		Tuple containing custom names for the quiet flag.
	**kwargs : Any
		Additional keyword arguments for the click option.

	Returns
	-------
	Callable
		The decorated function with verbosity and quiet options.
	"""

	def callback(ctx: click.Context, param: click.Parameter, value: int) -> None:
		levels = {0: 'ERROR', 1: 'WARNING', 2: 'INFO', 3: 'DEBUG'}
		level = levels.get(value, 'DEBUG')  # Default to DEBUG if verbosity is high
		logger = getLogger(logger_name)
		# Check if `--quiet` is passed
		if ctx.params.get('quiet', False):
			logger.setLevel(ERROR)
			return

		levelvalue = getLevelName(level)

		logger.setLevel(levelvalue)

	# Default verbosity options
	if not param_decls:
		param_decls = ('--verbose', '-v')

	# Set default options for verbosity
	kwargs.setdefault('count', True)
	kwargs.setdefault(
		'help',
		'Increase verbosity of logging, defaults to WARNING. '
		'(0-3: ERROR, WARNING, INFO, DEBUG).',
	)
	kwargs['callback'] = callback

	# Add the `--quiet` option
	def decorator(func: FC) -> FC:
		func = click.option(*param_decls, **kwargs)(func)
		func = click.option(
			*quiet_decl,
			is_flag=True,
			help='Suppress all logging except errors, overrides verbosity options.',
		)(func)
		return func

	return decorator


logger = setup_logger('orcestra')
