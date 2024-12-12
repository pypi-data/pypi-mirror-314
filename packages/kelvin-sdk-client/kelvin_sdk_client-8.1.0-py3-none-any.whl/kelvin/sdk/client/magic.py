"""
Kelvin API Client IPython magic: %client
"""

from __future__ import annotations

import datetime
from os import getenv
from typing import Any, Dict

from IPython.core.magic import register_line_magic
from IPython.terminal.interactiveshell import InteractiveShell

from kelvin.sdk.client.client import MODELS, Client

try:
    from kelvin.sdk.client.io import dataframe_to_timeseries, timeseries_to_dataframe
except ModuleNotFoundError:
    dataframe_to_timeseries = timeseries_to_dataframe = None  # type: ignore


def load_ipython_extension(shell: InteractiveShell) -> None:
    """Load Kelvin API Client IPython extension."""

    @register_line_magic
    def client(line: str) -> Client:
        """Set up Kelvin API Client session and import all API classes."""

        shell.push({k: v for k, v in vars(datetime).items() if isinstance(v, type)})
        shell.push({T.__name__: T for T in MODELS.values()})
        shell.push(
            {
                "dataframe_to_timeseries": dataframe_to_timeseries,
                "timeseries_to_dataframe": timeseries_to_dataframe,
            }
        )

        line = line.strip()

        kwargs: Dict[str, Any] = {}

        if not line:
            site = getenv("CURRENT_URL")
            if not site:
                raise ValueError("No site provided")
        elif " " in line:
            site, options = line.split(" ", 1)
            try:
                kwargs.update(eval(f"dict({options})"))  # nosec
            except Exception as e:
                raise ValueError(f"Unable to process options: {e}")
        else:
            site = line

        site = site.strip("'\"")

        return Client.from_file(site=site, **kwargs)
