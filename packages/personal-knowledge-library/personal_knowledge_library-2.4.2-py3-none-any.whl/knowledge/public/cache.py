# -*- coding: utf-8 -*-
# Copyright © 2023-24 Wacom. All rights reserved.
from pathlib import Path
from typing import Optional, Dict

import ndjson

from knowledge.public.wikidata import WikidataThing, WikiDataAPIClient


def cache_wikidata_object(wikidata_object: WikidataThing):
    """
    Caches a Wikidata object.
    Parameters
    ----------
    wikidata_object: WikidataObject
        The Wikidata object
    """
    wikidata_cache[wikidata_object.qid] = wikidata_object


def get_wikidata_object(qid_object: str) -> WikidataThing:
    """
    Returns a Wikidata object from the cache.

    Parameters
    ----------
    qid_object: str
        The QID of the Wikidata object.
    Returns
    -------
    wikidata_object: WikidataThing
        The Wikidata object.
    """
    if qid_object not in wikidata_cache:
        raise ValueError(f'Wikidata object {qid_object} not in cache.')
    return wikidata_cache[qid_object]


def pull_wikidata_object(qid_object: str) -> Optional[WikidataThing]:
    """
    Pulls a Wikidata object from the cache or from the Wikidata API.
    Parameters
    ----------
    qid_object: str
        The QID of the Wikidata object.
    Returns
    -------
    wikidata_object: Optional[WikidataThing]
        The Wikidata object, if it exists, otherwise None.
    """
    if qid_object in wikidata_cache:
        return wikidata_cache[qid_object]
    wikidata_object: Optional[WikidataThing] = WikiDataAPIClient.retrieve_entity(qid_object)
    cache_wikidata_object(wikidata_object)
    return wikidata_object


def cache_wikidata_objects() -> Dict[str, WikidataThing]:
    """
    Returns the Wikidata cache.
    Returns
    -------
    wikidata_cache: Dict[str, WikidataThing]
        Wikidata cache.
    """
    return wikidata_cache


def number_of_cached_objects() -> int:
    """
    Returns the number of cached objects.
    Returns
    -------
    number_of_cached_objects: int
        Number of cached objects.
    """
    return len(wikidata_cache)


def load_cache(cache: Path):
    """
    Load the cache from the file.
    Parameters
    ----------
    cache: Path
        The path to the cache file.
    """
    if cache.exists():
        with cache.open('r') as r:
            reader = ndjson.reader(r)
            for line in reader:
                wiki_data_thing: WikidataThing = WikidataThing.create_from_dict(line)
                # Cache the object
                cache_wikidata_object(wiki_data_thing)


def qid_in_cache(ref_qid: str) -> bool:
    """
    Checks if a QID is in the cache.
    Parameters
    ----------
    ref_qid: str
        The QID to check.

    Returns
    -------
    in_cache: bool
        True if the QID is in the cache, otherwise False.
    """
    return ref_qid in wikidata_cache


wikidata_cache: Dict[str, WikidataThing] = {}
# Wikidata cache
