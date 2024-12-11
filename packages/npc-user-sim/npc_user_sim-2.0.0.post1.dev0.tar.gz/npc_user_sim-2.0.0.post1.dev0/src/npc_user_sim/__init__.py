from importlib.metadata import version, PackageNotFoundError

try:
	__version__ = version('npc_user_sim')
except PackageNotFoundError:
	# package is not installed
	pass
