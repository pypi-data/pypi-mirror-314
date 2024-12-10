# -*- coding: utf-8 -*-
# Copyright © 2022-2024 Wacom. All rights reserved.
"""Mapping of Wikidata property ids to its string."""
import json
from pathlib import Path
from typing import Dict

# OntologyPropertyReference constants
INSTANCE_OF_PROPERTY: str = 'P31'
IMAGE_PROPERTY: str = 'P18'

# Mapping for property names
PROPERTY_MAPPING: Dict[str, str] = {}

CWD: Path = Path(__file__).parent
CONFIGURATION_FILE: Path = CWD / '../../pkl-cache/property_cache.json'
if CONFIGURATION_FILE.exists():
    with CONFIGURATION_FILE.open('r') as f:
        PROPERTY_MAPPING = json.load(f)

from knowledge.public import wikidata
from knowledge.public import helper
from knowledge.public import relations
from knowledge.public import cache


__all__ = ['wikidata', 'helper', 'relations', 'cache', 'PROPERTY_MAPPING', 'INSTANCE_OF_PROPERTY', 'IMAGE_PROPERTY']

