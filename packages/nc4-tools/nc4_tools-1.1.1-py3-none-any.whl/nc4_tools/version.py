from pathlib import Path

import single_version  # type: ignore

__version__ = single_version.get_version(
    __name__.split(".")[0], Path(__file__).parent.parent
)
