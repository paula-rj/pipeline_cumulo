#!/usr/bin/env python
# -*- coding: utf-8 -*-
# License: MIT (https://tldrlegal.com/license/mit-license)
# Copyright (c) 2023, Paula Romero Jure et al.
# All rights reserved.
# ==============================================================================

# ==============================================================================
# META
# ==============================================================================

r"""Bowtie effect Test.

A functio designed to detect the bowtie effect and stripping pattern in MODIS
images.

"""

__name__ = "bowtietest"
__version__ = "0.1.0"

# =============================================================================
# IMPORTS
# =============================================================================
import os

if os.getenv("__BOWTIE_IN_SETUP__") != "True":  # noqa
    from bowtietest import *  # noqa

del os
