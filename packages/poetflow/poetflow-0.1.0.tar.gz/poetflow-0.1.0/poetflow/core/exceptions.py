"""Custom exceptions for PoetFlow."""


class PoetFlowError(Exception):
    """Base exception for all PoetFlow errors."""

    pass


class MonoRepoError(PoetFlowError):
    """Exception raised for monorepo-related errors."""

    pass


class ConfigError(PoetFlowError):
    """Exception raised for configuration-related errors."""

    pass


class PackageError(PoetFlowError):
    """Exception raised for package-related errors."""

    pass
