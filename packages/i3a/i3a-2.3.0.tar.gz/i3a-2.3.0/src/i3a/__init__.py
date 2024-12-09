# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2024 Michał Góral.

try:
    import importlib.metadata as importlib_metadata
except ModuleNotFoundError:
    import importlib_metadata

__version__ = importlib_metadata.version("i3a")
