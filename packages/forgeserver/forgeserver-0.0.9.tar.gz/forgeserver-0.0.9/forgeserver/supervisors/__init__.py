from __future__ import annotations

from typing import TYPE_CHECKING

from forgeserver.supervisors.basereload import BaseReload
from forgeserver.supervisors.multiprocess import Multiprocess

if TYPE_CHECKING:
    ChangeReload: type[BaseReload]
else:
    try:
        from forgeserver.supervisors.watchfilesreload import WatchFilesReload as ChangeReload
    except ImportError:  # pragma: no cover
        try:
            from forgeserver.supervisors.watchgodreload import WatchGodReload as ChangeReload
        except ImportError:
            from forgeserver.supervisors.statreload import StatReload as ChangeReload

__all__ = ["Multiprocess", "ChangeReload"]
