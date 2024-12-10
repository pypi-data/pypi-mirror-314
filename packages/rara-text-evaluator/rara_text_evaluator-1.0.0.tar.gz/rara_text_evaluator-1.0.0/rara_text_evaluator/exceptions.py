class InvalidInputError(Exception):
	"""Raised when something incorrect given to parse."""
	pass

class InvalidRegistryError(Exception):
    """Raised when fallback key is missing from the model registry."""
    pass
