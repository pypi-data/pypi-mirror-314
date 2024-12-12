"""A wrapper around the data provided by the ISO 10383 specification.

:copyright: (c) 2024 Tanner Corcoran
:license: Apache 2.0, see LICENSE for more details.

"""

__title__ = "iso10383"
__author__ = "Tanner Corcoran"
__email__ = "tannerbcorcoran@gmail.com"
__license__ = "Apache 2.0 License"
__copyright__ = "Copyright (c) 2024 Tanner Corcoran"
__version__ = "2024.12.09"
__description__ = (
    "A wrapper around the data provided by the ISO 10383 specification."
)
__url__ = "https://github.com/tanrbobanr/iso10383"
__download_url__ = "https://pypi.org/project/iso10383"


from ._iso10383 import (
    MCC,
    ISOCC,
    _City,
    City,
    Status,
    MICEntry,
    MIC,
)


__all__ = (
    "MCC",
    "ISOCC",
    "_City",
    "City",
    "Status",
    "MICEntry",
    "MIC",
)
