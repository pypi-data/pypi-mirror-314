import warnings

warnings.warn(
    "This package is no longer in use! Use the main Python SDK instead: "
    "https://github.com/cognitedata/cognite-sdk-python",
    UserWarning,
)

from cognite.experimental._client import CogniteClient  # noqa: E402

__all__ = ["CogniteClient"]
