"""
Defines custom exception classes for handling errors related to Mattermost API interactions.

These exception classes allow for specific error handling in cases of general errors,
request errors, and not-found scenarios during Mattermost API interactions.
"""

__all__ = ["MattermostError", "ReqError", "NotFoundError"]


class MattermostError(Exception):
    """Raised for general errors related to Mattermost API interactions."""


class ReqError(MattermostError):
    """Raised when there is an error with the Mattermost request."""


class NotFoundError(ReqError):
    """Raised when a specific resource is not found in Mattermost."""
