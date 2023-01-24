"""Main module for Restless."""
__author__ = "Anthony Pagan <get-tony@outlook.com>"


class Service:
    """Base class for all services."""

    def __init__(self):
        """Initialize the service."""

    def __call__(self, *args, **kwargs):
        """Call the service."""
        return self.run(*args, **kwargs)

    def run(self, *args, **kwargs):
        """Run the service."""
        raise NotImplementedError("Service.run() must be implemented.")
