"""
Preload all search requests to avoid making the same searches many times while running models.
"""
import json
import os

from .log import logger
from .mocking.build_mock_search import create_search_results
from .mocking import RESULTS_PATH, enable_mock as _mock


def enable_preload(filepath: str = RESULTS_PATH, node: dict = None, overwrite_existing: bool = True):
    """
    Prefetch calls to HESTIA API in a local file.

    Parameters
    ----------
    filepath : str
        The path of the file containing the search results. Defaults to current library folder.
    node : dict
        Optional - The node used to run calculations. This is especially useful when running calculations on a Site.
    overwrite_existing : bool
        Optional - If the file already exists, the file can be used instead of generating it again.
        Will overwrite by default.
    """
    should_generate = overwrite_existing or not os.path.exists(filepath)

    if should_generate:
        logger.debug('Preloading search results and storing in %s', filepath)

        # build the search results
        data = create_search_results()

        # store in file
        with open(filepath, 'w') as f:
            f.write(json.dumps(data, indent=2, ensure_ascii=False))

    # enable mock search results from file
    _mock(filepath=filepath, node=node)
