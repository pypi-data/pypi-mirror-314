"""_logging.py - Augments logging to include a TRACE level & adds a `trace()` function to
log at that level."""

import logging
from collections.abc import Mapping
from types import TracebackType
from typing import TYPE_CHECKING, Optional, Type, Union

from typing_extensions import TypeAlias

# pulled from typeshed
_SysExcInfoType: TypeAlias = Union[
    tuple[Type[BaseException], BaseException, TracebackType], tuple[None, None, None]
]
_ExcInfoType: TypeAlias = Union[None, bool, _SysExcInfoType, BaseException]

# monkey patch TRACE level into logging
TRACE = 5
logging._levelToName[TRACE] = "TRACE"
logging._nameToLevel["TRACE"] = TRACE

if TYPE_CHECKING:

    def trace(
        logger: logging.Logger,
        msg: object,
        *args: object,
        exc_info: _ExcInfoType = None,
        stack_info: bool = False,
        stacklevel: int = 1,
        extra: Optional[Mapping[str, object]] = None,
    ) -> None:
        """Log 'msg % args' with severity 'TRACE'.

        To pass exception information, use the keyword argument exc_info with
        a true value, e.g.

        logger.info("Houston, we have a %s", "very specific problem", exc_info=1)
        """
else:

    def trace(logger, msg, *args, **kwargs):
        if logger.isEnabledFor(TRACE):
            logger._log(TRACE, msg, args, **kwargs)
