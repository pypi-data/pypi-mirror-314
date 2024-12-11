# Copyright © 2024 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.

import importlib.metadata
import os
import pkgutil
import sys
from typing import Generator, Iterable, List, Optional, Tuple
from zlib import crc32

from contrast.utils.library_reader.utils import (
    get_installed_dist_names,
    normalize_dist_name,
)
from contrast_vendor import structlog as logging


logger = logging.getLogger("contrast")


def artifact_fingerprint(app_root=sys.path[0] or ".") -> str:
    """
    Compute a fingerprint of the running code artifact.

    This fingerprint is smudgy. It prefers to be fast and simple over being
    completely accurate.

    It may return an empty string if it fails to compute a meaningful fingerprint.

    The returned fingerprint is based on the installed distribution packages,
    their versions, and the names and sized of the application source files.
    """
    app_ids = app_source_ids(app_root)
    if not app_ids:
        logger.debug("failed to compute fingerprint, no app sources found")
        return ""
    deps_ids = distribution_ids(get_installed_dist_names())
    artifact_id = f"app_sources={app_ids};deps={deps_ids}"
    logger.debug(
        "computed fingerprint",
        artifact_id=artifact_id,
        app_sources_count=len(app_ids),
        installed_distributions_count=len(deps_ids),
    )
    return str(crc32(artifact_id.encode()))


def distribution_ids(dist_names: Iterable[str]) -> List[str]:
    return [
        f"{dist_name}=={importlib.metadata.version(dist_name)}"
        for dist_name in sorted(map(normalize_dist_name, dist_names))
    ]


def app_source_ids(app_root: str) -> List[str]:
    return [
        module_id(info, origin)
        for info, origin in sorted(
            scan_app_modules([app_root], prefix="."), key=lambda x: x[0].name
        )
    ]


def module_id(info: pkgutil.ModuleInfo, origin: str):
    file_size = os.stat(origin).st_size
    return f"{info.name}:{file_size}"


def scan_app_modules(
    search_locations: Optional[List[str]], prefix=""
) -> Generator[Tuple[pkgutil.ModuleInfo, str], None, None]:
    if not search_locations:
        return
    for mod_info in pkgutil.iter_modules(search_locations, prefix):
        spec = mod_info.module_finder.find_spec(mod_info.name)
        if not spec or not spec.origin:
            continue
        yield mod_info, spec.origin
        yield from scan_app_modules(
            spec.submodule_search_locations, prefix=f"{mod_info.name}."
        )
