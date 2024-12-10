# -*- coding: utf-8 -*-
# Copyright © 2023-24 Wacom. All rights reserved.
import hashlib
import multiprocessing
import urllib
from abc import ABC
from datetime import datetime
from multiprocessing import Pool
from typing import Optional, Union, Any, Dict, List, Tuple, Set

import requests
from requests import Response
from requests.adapters import HTTPAdapter
from tqdm import tqdm
from urllib3 import Retry

from knowledge import logger
from knowledge.base.entity import Description, DESCRIPTIONS_TAG, Label, LanguageCode, LABELS_TAG, REPOSITORY_TAG, \
    DISPLAY_TAG, DESCRIPTION_TAG
from knowledge.public import PROPERTY_MAPPING, INSTANCE_OF_PROPERTY, IMAGE_PROPERTY
from knowledge.public.helper import __waiting_request__, __waiting_multi_request__, QID_TAG, REVISION_TAG, \
    PID_TAG, LABEL_TAG, CLAIMS_TAG, LABEL_VALUE_TAG, WIKIDATA_LANGUAGE_TAG, ALIASES_TAG, MODIFIED_TAG, \
    ONTOLOGY_TYPES_TAG, SITELINKS_TAG, parse_date, ID_TAG, LAST_REVID_TAG, wikidate, WikiDataAPIException, \
    WIKIDATA_SPARQL_URL, SOURCE_TAG, URLS_TAG, TITLES_TAG, image_url, WIKIDATA_SEARCH_URL, SUPERCLASSES_TAG, API_LIMIT
from knowledge.base.language import LANGUAGE_LOCALE_MAPPING, EN_US, LocaleCode

# Constants
QUALIFIERS_TAG: str = "QUALIFIERS"
LITERALS_TAG: str = "LITERALS"


def chunks(lst: List[str], chunk_size: int):
    """
    Yield successive n-sized chunks from lst.Yield successive n-sized chunks from lst.
    Parameters
    ----------
    lst: List[str]
        Full length.
    chunk_size: int
        Chunk size.

    """
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]


class WikidataProperty:
    """
    WikidataProperty
    ----------------
    Property id and its label from wikidata.

    Parameters
    ----------
    pid: str
        Property ID.

    """
    def __init__(self, pid: str, label: Optional[str] = None):
        super().__init__()
        self.__pid: str = pid
        self.__label: Optional[str] = label

    @property
    def pid(self):
        """Property id."""
        return self.__pid

    @property
    def label(self) -> str:
        """Label with lazy loading mechanism."""
        if self.__label:
            return self.__label
        if self.pid in PROPERTY_MAPPING:  # only English mappings
            self.__label = PROPERTY_MAPPING[self.pid]
        else:
            prop_dict = __waiting_request__(self.pid)
            self.__label = prop_dict['labels'].get('en', self.__pid) if prop_dict.get('labels') else self.__pid
        return self.__label

    @property
    def label_cached(self) -> str:
        """Label with cached value."""
        if self.__label:
            return self.__label
        if self.pid in PROPERTY_MAPPING:  # only English mappings
            self.__label = PROPERTY_MAPPING[self.pid]
        return self.__label

    def __dict__(self):
        return {
            PID_TAG: self.pid,
            LABEL_TAG: self.label_cached
        }

    @classmethod
    def create_from_dict(cls, prop_dict: Dict[str, Any]) -> 'WikidataProperty':
        """Create a property from a dictionary.
        Parameters
        ----------
        prop_dict: Dict[str, Any]
            Property dictionary.

        Returns
        -------
        instance: WikidataProperty
            Instance of WikidataProperty.
        """
        return WikidataProperty(prop_dict[PID_TAG], prop_dict.get(LABEL_TAG))

    def __repr__(self):
        return f'<Property:={self.pid}]>'


class WikidataSearchResult:
    """
    WikidataSearchResult
    --------------------
    Search result from wikidata.
    """

    def __init__(self, qid: str, label: Label, description: Optional[Description], repository: str, aliases: List[str]):
        self.__qid: str = qid
        self.__label: Label = label
        self.__description: Optional[Description] = description
        self.__repository: str = repository
        self.__aliases: List[str] = aliases

    @property
    def qid(self) -> str:
        """QID of the search result."""
        return self.__qid

    @property
    def label(self) -> Label:
        """Label of the search result."""
        return self.__label

    @property
    def description(self) -> Optional[Description]:
        """Description of the search result."""
        return self.__description

    @property
    def repository(self) -> str:
        """Repository of the search result."""
        return self.__repository

    @property
    def aliases(self) -> List[str]:
        """Aliases of the search result."""
        return self.__aliases

    @classmethod
    def from_dict(cls, search_result: Dict[str, Any]) -> 'WikidataSearchResult':
        """
        Create a search result from a dictionary.
        Parameters
        ----------
        search_result: Dict[str, Any]
            Search result dictionary.

        Returns
        -------
        WikidataSearchResult
            Instance of WikidataSearchResult.
        """
        qid: str = search_result[ID_TAG]
        display: Dict[str, Any] = search_result[DISPLAY_TAG]
        label: Label = Label(content=display[LABEL_TAG]['value'],
                             language_code=LANGUAGE_LOCALE_MAPPING.get(LanguageCode(display[LABEL_TAG]['language']),
                                                                       EN_US))
        description: Optional[Description] = None
        if DESCRIPTION_TAG in display:
            description: Description = Description(description=display[DESCRIPTION_TAG]['value'],
                                                   language_code=display[DESCRIPTION_TAG]['language'])
        aliases: List[str] = [alias['value'] for alias in display.get(ALIASES_TAG, [])]
        repository: str = search_result[REPOSITORY_TAG]
        return WikidataSearchResult(
            qid=qid,
            label=label,
            description=description,
            repository=repository,
            aliases=aliases
        )

    def __repr__(self):
        desc_str: str = ''
        if self.description:
            desc_str: str = f' - description:= {self.description}'
        return f'<Search Result:={self.qid} - label:= {self.label}{desc_str}>'


class WikidataClass:
    """
    WikidataClass
    ----------------
    In Wikidata, classes are used to group items together based on their common characteristics.
    Classes in Wikidata are represented as items themselves, and they are typically identified by the prefix "Q"
    followed by a unique number.

    There are several types of classes in Wikidata, including:

    - **Main Classes**: These are the most general classes in Wikidata, and they represent broad categories of items.
    Examples of main classes include "person" (Q215627), "physical location" (Q17334923), and "event" (occurrence).
    - **Subclasses**: These are more specific classes that are grouped under a main class.
    For example, "politician" (Q82955) is a subclass of "person" (Q215627), and "city" (Q515) is a subclass
    of "location" (Q17334923).
    - **Properties**: These are classes that represent specific attributes or characteristics of items. For example,
    "gender" (Q48277) is a property that can be used to describe the gender of a person.
    - **Instances**: These are individual items that belong to a class. For example, Barack Obama (Q76) is an instance
    of the "person" (Q215627) class.
    - **Meta-classes**: These are classes that are used to group together other classes based on their properties or
    characteristics. For example, the "monotypic taxon" (Q310890) class groups together classes that represent
    individual species of organisms.

    Overall, classes in Wikidata are a tool for organizing and categorizing information in a structured and consistent
    way, which makes it easier to search and analyze data across a wide range of topics and domains.

    Parameters
    ----------
    qid: str
        Class QID.

    """
    def __init__(self, qid: str, label: Optional[str] = None):
        super().__init__()
        self.__qid: str = qid
        self.__label: Optional[str] = label
        self.__superclasses: List[WikidataClass] = []

    @property
    def qid(self):
        """Property id."""
        return self.__qid

    @property
    def label(self) -> str:
        """Label with lazy loading mechanism."""
        if self.__label:
            return self.__label

        class_dict = __waiting_request__(self.qid)
        self.__label = class_dict['labels'].get('en').get('value', self.__qid) \
            if class_dict.get('labels') and class_dict['labels'].get('en') else self.__qid
        return self.__label

    @property
    def superclasses(self) -> List['WikidataClass']:
        """Superclasses."""
        return self.__superclasses

    @classmethod
    def create_from_dict(cls, class_dict: Dict[str, Any]) -> 'WikidataClass':
        """
        Create a class from a dictionary.
        Parameters
        ----------
        class_dict: Dict[str, Any]
            Class dictionary.

        Returns
        -------
        instance: WikidataClass
            Instance of WikidataClass.
        """
        wiki_cls: WikidataClass = cls(class_dict[QID_TAG], class_dict.get(LABEL_TAG))
        for superclass in class_dict.get(SUPERCLASSES_TAG, []):
            wiki_cls.__superclasses.append(WikidataClass.create_from_dict(superclass))

        return wiki_cls

    def __dict__(self):
        return {
            QID_TAG: self.qid,
            LABEL_TAG: self.label,
            SUPERCLASSES_TAG: [superclass.__dict__() for superclass in self.superclasses]
        }

    def __repr__(self):
        return f'<WikidataClass:={self.qid}]>'


class Claim:
    """
    Claim
    ------
    A Wikidata claim is a statement that describes a particular property-value relationship about an item in the
    Wikidata knowledge base. In Wikidata, an item represents a specific concept, such as a person, place, or
    organization, and a property describes a particular aspect of that concept, such as its name, date of birth,
    or location.

    A claim consists of three elements:

    - Subject: The item to which the statement applies
    - Predicate: The property that describes the statement
    - Object: The value of the property for the given item

    For example, a claim could be "Barack Obama (subject) has a birthdate (predicate) of August 4, 1961 (object)."
    Claims in Wikidata help to organize information and provide a structured way to represent knowledge that can
    be easily queried, analyzed, and visualized.
    """

    def __init__(self, pid: WikidataProperty, literal: List[Dict[str, Any]], qualifiers: List[Dict[str, Any]]):
        super().__init__()
        self.__pid: WikidataProperty = pid
        self.__literals: List[Dict[str, Any]] = literal
        self.__qualifiers: List[Dict[str, Any]] = qualifiers

    @property
    def pid(self) -> WikidataProperty:
        """Property name. Predicate of the claim."""
        return self.__pid

    @property
    def literals(self) -> List[Dict[str, Any]]:
        """Literals. Objects of the statement."""
        return self.__literals

    @property
    def qualifiers(self) -> List[Dict[str, Any]]:
        """Qualifiers."""
        return self.__qualifiers

    def __dict__(self):
        return {
            PID_TAG: self.pid.__dict__(),
            LITERALS_TAG: self.literals,
            QUALIFIERS_TAG: self.qualifiers
        }

    def __eq__(self, other):
        if not isinstance(other, Claim):
            return False
        return self.pid == other.pid

    def __hash__(self):
        return hash(self.pid)

    def __repr__(self):
        return f'<Claim:={self.pid}, {self.literals}]>'

    @classmethod
    def create_from_dict(cls, claim) -> 'Claim':
        """Create a claim from a dictionary."""
        pid: WikidataProperty = WikidataProperty.create_from_dict(claim['pid'])
        literals = claim[LITERALS_TAG]
        qualifiers = claim[QUALIFIERS_TAG]
        return cls(pid, literals, qualifiers)


class SiteLinks:
    """
    SiteLinks
    ---------
    Sitelinks in Wikidata are links between items in Wikidata and pages on external websites, such as Wikipedia,
    Wikimedia Commons, and other Wikimedia projects. A site-link connects a Wikidata item to a specific page on an
    external website that provides more information about the topic represented by the item.

    For example, a Wikidata item about a particular city might have sitelinks to the corresponding page on the English,
    French, and German Wikipedia sites. Each site-link connects the Wikidata item to a specific page on the external
    website that provides more detailed information about the city.

    Sitelinks in Wikidata help to connect and integrate information across different languages and projects,
    making it easier to access and share knowledge on a wide range of topics. They also help to provide context and
    additional information about Wikidata items, improving the overall quality and usefulness of the knowledge base.

    Parameters
    ----------
    source: str
        Source of sitelinks.
    """

    def __init__(self, source: str,
                 urls: Union[Dict[str, str], None] = None,
                 titles: Union[Dict[str, str], None] = None):
        self.__source: str = source
        self.__urls: Dict[str, str] = {} if urls is None else urls
        self.__title: Dict[str, str] = {} if titles is None else titles

    @property
    def urls(self) -> Dict[str, str]:
        """URLs for the source."""
        return self.__urls

    @property
    def titles(self) -> Dict[str, str]:
        """Titles for the source."""
        return self.__title

    @property
    def urls_languages(self) -> List[str]:
        """List of all supported languages."""
        return list(self.__urls.keys())

    @property
    def source(self) -> str:
        """Sitelinks source."""
        return self.__source

    @classmethod
    def create_from_dict(cls, entity_dict: Dict[str, Any]) -> 'SiteLinks':
        """
        Create a SiteLinks object from a dictionary.

        Parameters
        ----------
        entity_dict: Dict[str, Any]
            dictionary containing the entity information.

        Returns
        -------
        instance: SiteLinks
            The SiteLinks instance.
        """
        return SiteLinks(source=entity_dict[SOURCE_TAG], urls=entity_dict.get(URLS_TAG),
                         titles=entity_dict.get(TITLES_TAG))

    def __dict__(self):
        return {
            SOURCE_TAG: self.__source,
            URLS_TAG: self.__urls,
            TITLES_TAG: self.__title
        }

    def __repr__(self):
        return f'<SiteLinks:={self.source}, supported languages:=[{"|".join(self.urls_languages)}]>'


class WikidataThing:
    """
    WikidataEntity
    -----------
    Generic entity within wikidata.

    Each entity is derived from this object, thus all entity shares:
    - **qid**: A unique resource identity to identify the entity and reference it in relations
    - **label**: Human understandable label
    - **description**: Description of entity

    Parameters
    ----------
    revision: str
        Revision of the entity
    qid: str
        QID for entity. For new entities the URI is None, as the knowledge graph backend assigns this.
    modified: datetime
        Last modified date
    label: List[Label]
        List of labels
    description: List[Description] (optional)
        List of descriptions
    qid: str
         QID for entity. For new entities the URI is None, as the knowledge graph backend assigns this.
    """

    def __init__(self, revision: str, qid: str, modified: datetime,
                 label: Optional[Dict[str, Label]] = None, aliases: Optional[Dict[str, List[Label]]] = None,
                 description: Optional[Dict[str, Description]] = None):
        self.__qid: str = qid
        self.__revision: str = revision
        self.__modified: datetime = modified
        self.__label: Dict[str, Label] = label if label else {}
        self.__description: Dict[str, Description] = description if description else {}
        self.__aliases: Dict[str, List[Label]] = aliases if aliases else {}
        self.__claims: Dict[str, Claim] = {}
        self.__sitelinks: Dict[str, SiteLinks] = {}
        self.__ontology_types: List[str] = []

    @property
    def qid(self) -> str:
        """QID for entity."""
        return self.__qid

    @property
    def revision(self) -> str:
        """Revision version of entity."""
        return self.__revision

    @property
    def modified(self) -> datetime:
        """Modification date of entity."""
        return self.__modified

    @property
    def label(self) -> Dict[str, Label]:
        """Labels of the entity."""
        return self.__label

    @property
    def ontology_types(self) -> List[str]:
        """Ontology types of the entity."""
        return self.__ontology_types

    @ontology_types.setter
    def ontology_types(self, ontology_types: List[str]):
        self.__ontology_types = ontology_types

    @property
    def label_languages(self) -> List[str]:
        """All available languages for a labels."""
        return list(self.__label.keys())

    @property
    def aliases(self) -> Dict[str, List[Label]]:
        """Alternative labels of the concept."""
        return self.__aliases

    @property
    def alias_languages(self) -> List[str]:
        """All available languages for a aliases."""
        return list(self.__aliases.keys())

    @property
    def description(self) -> Dict[str, Description]:
        """Description of the thing (optional)."""
        return self.__description

    @description.setter
    def description(self, description: Dict[str, Description]):
        self.__description = description

    @property
    def description_languages(self) -> List[str]:
        """All available languages for a description."""
        return list(self.__description.keys())

    def add_label(self, label: str, language_code: str):
        """Adding a label for entity.

        Parameters
        ----------
        label: str
            Label
        language_code: str
            ISO-3166 Country Codes and ISO-639 Language Codes in the format '<language_code>_<country>', e.g., 'en_US'.
        """
        self.__label[language_code] = Label(label, LocaleCode(language_code), True)

    def label_lang(self, language_code: str) -> Optional[Label]:
        """
        Get label for language_code code.

        Parameters
        ----------
        language_code: LanguageCode
            Requested language_code code
        Returns
        -------
        label: Optional[Label]
            Returns the label for a specific language code
        """
        return self.label.get(language_code)

    def add_description(self, description: str, language_code: str):
        """Adding a description for entity.

        Parameters
        ----------
        description: str
            Description
        language_code: str
            ISO-3166 Country Codes and ISO-639 Language Codes in the format '<language_code>_<country>', e.g., 'en_US'.
        """
        self.__description[language_code] = Description(description=description,
                                                        language_code=LocaleCode(language_code))

    def description_lang(self, language_code: str) -> Optional[Description]:
        """
        Get description for entity.

        Parameters
        ----------
        language_code: LanguageCode
            ISO-3166 Country Codes and ISO-639 Language Codes in the format '<language_code>_<country>', e.g., 'en_US'.
        Returns
        -------
        label: LocalizedContent
            Returns the  label for a specific language_code code
        """
        return self.description.get(language_code)

    def alias_lang(self, language_code: str) -> List[Label]:
        """
        Get alias for language_code code.

        Parameters
        ----------
        language_code: str
            Requested language_code code
        Returns
        -------
        aliases: List[Label]
            Returns a list of aliases for a specific language code
        """
        return self.aliases.get(language_code)

    def add_alias(self, alias: str, language_code: str):
        """Adding an alias for entity.

        Parameters
        ----------
        alias: str
            Alias
        language_code: str
            ISO-3166 Country Codes and ISO-639 Language Codes in the format '<language_code>_<country>', e.g., 'en_US'.
        """
        if language_code not in self.__aliases:
            self.aliases[language_code] = []
        self.__aliases[language_code].append(Label(alias, LocaleCode(language_code), False))

    def image(self, dpi: int = 500) -> Optional[str]:
        """
        Generate URL for image from Wikimedia.

        Parameters
        ----------
        dpi: int
            DPI value. Range: [50-1000]

        Returns
        -------
        wikimedia_url: str
            URL for Wikimedia
        """
        if not (50 <= dpi <= 1000):
            raise ValueError(f"DPI should bei with range of [50-1000]. Value:={dpi}")
        claim: Optional[Claim] = self.claims.get(IMAGE_PROPERTY)
        if claim and len(claim.literals) > 0:
            img = claim.literals[0]['value']
            if isinstance(img, dict) and 'image_url' in img:
                return img['image_url']
            extension: str = ''
            conversion: str = ''
            fixed_img: str = img.replace(' ', '_')
            if fixed_img.lower().endswith('svg'):
                extension: str = '.png'
            if fixed_img.lower().endswith('tif') or fixed_img.lower().endswith('tiff'):
                extension: str = '.jpg'
                conversion: str = 'lossy-page1-'
            hash_img: str = hashlib.md5(fixed_img.encode('utf-8')).hexdigest()
            url_img_part: str = urllib.parse.quote_plus(fixed_img)
            return f'https://upload.wikimedia.org/wikipedia/commons/thumb/' \
                   f'{hash_img[0]}/{hash_img[:2]}/{url_img_part}/{dpi}px-{conversion + url_img_part + extension}'
        return None

    @property
    def instance_of(self) -> List[WikidataClass]:
        """Instance of."""
        claim: Optional[Claim] = self.claims.get(INSTANCE_OF_PROPERTY)
        if claim:
            return [WikidataClass(li['value'].get('id')) for li in claim.literals if 'value' in li]
        return []

    @property
    def sitelinks(self) -> Dict[str, SiteLinks]:
        """Different sitelinks assigned to entity."""
        return self.__sitelinks

    def __dict__(self):
        return {
            QID_TAG: self.qid,
            REVISION_TAG: self.revision,
            MODIFIED_TAG: self.modified.isoformat(),
            LABELS_TAG: {lang: la.__dict__() for lang, la in self.label.items() },
            DESCRIPTIONS_TAG: {lang: la.__dict__() for lang, la in self.description.items()},
            ALIASES_TAG: {lang: [a.__dict__() for a in al] for lang, al in self.aliases.items()},
            CLAIMS_TAG: {pid: cl.__dict__() for pid, cl in self.claims.items()},
            ONTOLOGY_TYPES_TAG: self.ontology_types,
            SITELINKS_TAG: {source: site.__dict__() for source, site in self.sitelinks.items()}
        }

    @classmethod
    def create_from_dict(cls, entity_dict: Dict[str, Any]) -> 'WikidataThing':
        """
        Create WikidataThing from dict.

        Parameters
        ----------
        entity_dict: Dict[str, Any]
            dictionary with WikidataThing information.

        Returns
        -------
        thing: WikidataThing
            Instance of WikidataThing
        """
        labels: Dict[str, Label] = {}
        aliases: Dict[str, List[Label]] = {}
        descriptions: Dict[str, Description] = {}
        for language, la in entity_dict[LABELS_TAG].items():
            labels[language] = Label.create_from_dict(la)
        for language, de in entity_dict[DESCRIPTIONS_TAG].items():
            descriptions[language] = Description.create_from_dict(de)
        for language, al in entity_dict[ALIASES_TAG].items():
            aliases[language] = []
            for a in al:
                aliases[language].append(Label.create_from_dict(a))
        # Initiate the wikidata thing
        thing: WikidataThing = WikidataThing(qid=entity_dict[QID_TAG], revision=entity_dict[REVISION_TAG],
                                             modified=parse_date(entity_dict[MODIFIED_TAG]), label=labels,
                                             aliases=aliases,
                                             description=descriptions)
        # Load the ontology types
        thing.ontology_types = entity_dict.get(ONTOLOGY_TYPES_TAG, [])
        # Load the claims
        for pid, claim in entity_dict[CLAIMS_TAG].items():
            thing.claims[pid] = Claim.create_from_dict(claim)
        # Load the sitelinks
        for wiki_source, site_link in entity_dict[SITELINKS_TAG].items():
            thing.sitelinks[wiki_source] = SiteLinks.create_from_dict(site_link)
        return thing

    @staticmethod
    def from_wikidata(entity_dict: Dict[str, Any], supported_languages: Optional[List[str]] = None) -> 'WikidataThing':
        """
        Create WikidataThing from Wikidata JSON response.
        Parameters
        ----------
        entity_dict: Dict[str, Any]
            dictionary with WikidataThing information.
        supported_languages: Optional[List[str]]
            List of supported languages. If None, all languages are supported.

        Returns
        -------
        thing: WikidataThing
            Instance of WikidataThing.
        """
        labels: Dict[str, Label] = {}
        aliases: Dict[str, List[Label]] = {}
        descriptions: Dict[str, Description] = {}
        if LABELS_TAG in entity_dict:
            # Extract the labels
            for label in entity_dict[LABELS_TAG].values():
                if supported_languages is None or label[WIKIDATA_LANGUAGE_TAG] in supported_languages:
                    la_content: str = label[LABEL_VALUE_TAG]
                    la_lang: LanguageCode = LanguageCode(label[WIKIDATA_LANGUAGE_TAG])
                    if la_lang in LANGUAGE_LOCALE_MAPPING:
                        la: Label = Label(content=la_content,
                                          language_code=LANGUAGE_LOCALE_MAPPING[la_lang], main=True)
                        labels[la.language_code] = la
        else:
            labels['en_US'] = Label('No Label', EN_US)
        if ALIASES_TAG in entity_dict:
            # Extract the aliases
            for alias in entity_dict[ALIASES_TAG].values():
                if supported_languages is None or alias[WIKIDATA_LANGUAGE_TAG] in supported_languages:
                    for a in alias:
                        la_content: str = a[LABEL_VALUE_TAG]
                        la_lang: LanguageCode = LanguageCode(a[WIKIDATA_LANGUAGE_TAG])
                        if la_lang in LANGUAGE_LOCALE_MAPPING:
                            la: Label = Label(content=la_content,
                                              language_code=LANGUAGE_LOCALE_MAPPING[la_lang], main=False)
                            if la.language_code not in aliases:
                                aliases[la.language_code] = []
                            aliases[la.language_code].append(la)
        if DESCRIPTIONS_TAG in entity_dict:
            # Extracting the descriptions
            for desc in entity_dict[DESCRIPTIONS_TAG].values():
                if supported_languages is None or desc[WIKIDATA_LANGUAGE_TAG] in supported_languages:
                    desc_content: str = desc[LABEL_VALUE_TAG]
                    desc_lang: LanguageCode = LanguageCode(desc[WIKIDATA_LANGUAGE_TAG])
                    if desc_lang in LANGUAGE_LOCALE_MAPPING:
                        de: Description = Description(description=desc_content,
                                                      language_code=LANGUAGE_LOCALE_MAPPING[desc_lang])
                        descriptions[de.language_code] = de
        # Initiate the wikidata thing
        thing: WikidataThing = WikidataThing(qid=entity_dict[ID_TAG], revision=entity_dict[LAST_REVID_TAG],
                                             modified=parse_date(entity_dict[MODIFIED_TAG]), label=labels,
                                             aliases=aliases, description=descriptions)

        # Iterate over the claims
        for pid, claim_group in entity_dict[CLAIMS_TAG].items():
            literal: List[Dict[str, Any]] = []
            qualifiers: List[Dict[str, Any]] = []
            for claim in claim_group:
                try:
                    snak_type: str = claim['mainsnak']['snaktype']
                    if snak_type == "value":
                        data_value: Dict[str, Any] = claim['mainsnak']['datavalue']
                        data_type: str = claim['mainsnak']['datatype']
                        val: Dict[str, Any] = {}
                        if data_type == 'monolingualtext':
                            val = data_value['value']
                        elif data_type in {'string', 'external-id', 'url'}:
                            val = data_value['value']
                        elif data_type == 'commonsMedia':
                            val = {
                                'image_url': image_url(data_value['value'])
                            }
                        elif data_type == 'time':
                            val = wikidate(data_value['value'])
                        elif data_type == 'quantity':
                            if 'amount' in data_value['value']:
                                val = {
                                    "amount": data_value['value']['amount'],
                                    "unit": data_value['value']['unit']
                                }
                        elif data_type == 'wikibase-lexeme':
                            val = {
                                'id': data_value['value']['id']
                            }
                        elif data_type in {'geo-shape', 'wikibase-property'}:
                            # Not supported
                            val = data_value['value']
                        elif data_type in {'globe-coordinate', 'globecoordinate'}:
                            val = {
                                'longitude': data_value['value'].get('longitude'),
                                'latitude': data_value['value'].get('latitude'),
                                'altitude': data_value['value'].get('altitude'),
                                'globe': data_value['value'].get('globe'),
                                'precision': data_value['value'].get('precision')
                            }
                        elif data_type in {"wikibase-entityid", 'wikibase-item'}:
                            val = {
                                'id': data_value['value']['id']
                            }
                        elif data_type == 'math':
                            val = {
                                'math': data_value['value']
                            }
                        elif data_type == "tabular-data":
                            val = {
                                'tabular': data_value['value']
                            }
                        else:
                            raise WikiDataAPIException(f"Data type: {data_type} not supported.")
                        literal.append({
                            'type': data_type,
                            'value': val
                        })

                    if 'qualifiers' in claim:
                        for p, qual in claim['qualifiers'].items():
                            for elem in qual:
                                if 'datavalue' in elem:
                                    qualifiers.append({
                                        "property": p,
                                        "datatype": elem['datavalue']['type'],
                                        "value": elem['datavalue']['value']
                                    })
                except Exception as e:
                    logger.exception(e)
            thing.add_claim(pid, Claim(WikidataProperty(pid), literal, qualifiers))
        # Extract sitelinks
        if SITELINKS_TAG in entity_dict:
            for source, sitelink in entity_dict[SITELINKS_TAG].items():
                try:
                    start_idx = source.find('wiki')
                    language_code: str = source[:start_idx]
                    wiki_source: str = source[start_idx:]
                    url: Optional[str] = sitelink.get('url')
                    title: Optional[str] = sitelink.get('title')
                    if wiki_source not in thing.sitelinks:
                        thing.sitelinks[wiki_source] = SiteLinks(source=wiki_source)
                    if url and language_code not in thing.sitelinks[wiki_source].urls:
                        thing.sitelinks[wiki_source].urls[language_code] = requests.utils.unquote(url)
                    if title and language_code not in thing.sitelinks[wiki_source].titles:
                        thing.sitelinks[wiki_source].titles[language_code] = title
                except Exception as e:
                    logger.warning(f"Unexpected source: {source}. Exception: {e}")
        return thing

    @property
    def claims(self) -> Dict[str, Claim]:
        """ Returns the claims. """
        return self.__claims

    @property
    def claims_dict(self) -> Dict[str, Claim]:
        """ Returns the claims as a dictionary. """
        return dict(list(self.__claims.items()))

    @property
    def claim_properties(self) -> List[WikidataProperty]:
        """ Returns the list of properties of the claims. """
        return [p.pid for p in self.__claims.values()]

    def add_claim(self, pid: str, claim: Claim):
        """
        Adding a claim.

        Parameters
        ----------
        pid: str
            Property ID.
        claim: Claim
            Wikidata claim
        """
        self.__claims[pid] = claim

    def __hash__(self):
        return 0

    def __eq__(self, other):
        # another object is equal to self, iff
        # it is an instance of MyClass
        return isinstance(other, WikidataThing) and other.qid == self.qid

    def __repr__(self):
        return f'<WikidataThing [QID:={self.qid}]>'

    def __getstate__(self) -> Dict[str, Any]:
        return self.__dict__().copy()

    def __setstate__(self, state: Dict[str, Any]):
        labels: Dict[str, Label] = {}
        aliases: Dict[str, List[Label]] = {}
        descriptions: Dict[str, Description] = {}
        for language, la in state[LABELS_TAG].items():
            labels[language] = Label.create_from_dict(la)
        for language, de in state[DESCRIPTIONS_TAG].items():
            descriptions[language] = Description.create_from_dict(de)
        for language, al in state[ALIASES_TAG].items():
            aliases[language] = []
            for a in al:
                aliases[language].append(Label.create_from_dict(a))
        # Initiate the wikidata thing
        self.__qid = state[QID_TAG]
        self.__revision = state.get(REVISION_TAG)
        self.__modified = parse_date(state[MODIFIED_TAG]) if MODIFIED_TAG in state else None
        self.__label = labels
        self.__aliases = aliases
        self.__description = descriptions
        # Load the ontology types
        self.__ontology_types = state.get(ONTOLOGY_TYPES_TAG, [])
        # Load the claims
        self.__claims = {}
        for pid, claim in state[CLAIMS_TAG].items():
            self.__claims[pid] = Claim.create_from_dict(claim)
        # Load the sitelinks
        self.__sitelinks = {}
        for wiki_source, site_link in state[SITELINKS_TAG].items():
            self.__sitelinks[wiki_source] = SiteLinks.create_from_dict(site_link)


def detect_cycle(super_class_qid: str, cycle_detector: List[Tuple[str, str]]) -> bool:
    """
    Detects if there is a cycle in the super class hierarchy.
    Parameters
    ----------
    super_class_qid: str
        Super class QID
    cycle_detector: List[Tuple[str, str]]
        List of tuples of the form (subclass_qid, super_class_qid)

    Returns
    -------
    cycle: bool
        True if there is a cycle, False otherwise.
    """
    return any(e[0] == super_class_qid for e in cycle_detector)


class WikiDataAPIClient(ABC):
    """
    WikiDataAPIClient
    -----------------
    Utility class for the WikiData.

    """

    def __init__(self):
        pass

    @staticmethod
    def sparql_query(
            query_string: str, wikidata_sparql_url: str = WIKIDATA_SPARQL_URL, max_retries: int = 3
    ) -> dict:
        """Send a SPARQL query and return the JSON formatted result.

        Parameters
        -----------
        query_string: str
          SPARQL query string
        wikidata_sparql_url: str
          Wikidata SPARQL endpoint to use
        max_retries: int
            Maximum number of retries
        """
        # Define the retry policy
        retry_policy: Retry = Retry(
            total=max_retries,  # maximum number of retries
            backoff_factor=1,  # factor by which to multiply the delay between retries
            status_forcelist=[429, 500, 502, 503, 504],  # HTTP status codes to retry on
            respect_retry_after_header=True  # respect the Retry-After header
        )

        # Create a session and mount the retry adapter
        with requests.Session() as session:
            retry_adapter = HTTPAdapter(max_retries=retry_policy)
            session.mount("https://", retry_adapter)

            # Make a request using the session
            response: Response = session.get(wikidata_sparql_url, params={"query": query_string, "format": "json"},
                                             timeout=200000)
        if response.ok:
            return response.json()
        raise WikiDataAPIException(f'Failed to query entities. '
                                   f'Response code:={response.status_code}, Exception:= {response.content}.')

    @staticmethod
    def superclasses(qid: str) -> Optional[WikidataClass]:
        """
        Returns the superclasses of the given QID.
        Parameters
        ----------
        qid: str
            Wikidata QID

        Returns
        -------
        wikidata_classes: Optional[WikidataClass]
            Wikidata class
        """
        query: str = f'''SELECT ?class ?classLabel ?superclass ?superclassLabel
        WHERE
        {{
            wd:{qid} wdt:P279* ?class.
            ?class wdt:P279 ?superclass.
            SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
        }}'''
        reply: Dict[str, Any] = WikiDataAPIClient.sparql_query(query)
        wikidata_classes: Dict[str, WikidataClass] = {}
        cycle_detector: List[Tuple[str, str]] = []
        if 'results' in reply:
            for b in reply['results']['bindings']:
                superclass_qid: str = b['superclass']['value'].split('/')[-1]
                class_qid: str = b['class']['value'].split('/')[-1]
                superclass_label: str = b['superclassLabel']['value']
                class_label: str = b['classLabel']['value']
                if class_qid not in wikidata_classes:
                    wikidata_classes[class_qid] = WikidataClass(qid=class_qid, label=class_label)
                if superclass_qid not in wikidata_classes:
                    wikidata_classes[superclass_qid] = WikidataClass(qid=superclass_qid, label=superclass_label)
                if not detect_cycle(superclass_qid, cycle_detector):
                    wikidata_classes[class_qid].superclasses.append(wikidata_classes[superclass_qid])
                    cycle_detector.append((class_qid, superclass_qid))
        return wikidata_classes.get(qid)

    @staticmethod
    def search_term(search_term: str, language: LanguageCode, url: str = WIKIDATA_SEARCH_URL) \
            -> List[WikidataSearchResult]:
        """
        Search for a term in the WikiData.
        Parameters
        ----------
        search_term: str
            The term to search for.
        language: str
            The language to search in.
        url: str
            The URL of the WikiData search API.

        Returns
        -------
        search_results_dict: List[WikidataSearchResult]
            The search results.
        """
        search_results_dict: List[WikidataSearchResult] = []
        # Define the retry policy
        retry_policy: Retry = Retry(
            total=3,  # maximum number of retries
            backoff_factor=1,  # factor by which to multiply the delay between retries
            status_forcelist=[429, 500, 502, 503, 504],  # HTTP status codes to retry on
            respect_retry_after_header=True  # respect the Retry-After header
        )

        # Create a session and mount the retry adapter
        with requests.Session() as session:
            retry_adapter = HTTPAdapter(max_retries=retry_policy)
            session.mount("https://", retry_adapter)
            params: Dict[str, str] = {
                "action": "wbsearchentities",
                "format": "json",
                "language": language,
                "search": search_term
            }
            # Make a request using the session
            response: Response = session.get(url, params=params, timeout=200000)

            # Check the response status code
            if not response.ok:
                raise WikiDataAPIException(f"Search request failed with status code : {response.status_code}. "
                                           f"URL:= {url}")
            search_result_dict_full: Dict[str, Any] = response.json()
            for search_result_dict in search_result_dict_full['search']:
                search_results_dict.append(WikidataSearchResult.from_dict(search_result_dict))
            return search_results_dict

    @staticmethod
    def __wikidata_task__(qid: str) -> WikidataThing:
        """Retrieve a single Wikidata thing.

        Parameters
        ----------
        qid: str
            QID of the entity.

        Returns
        -------
        instance: WikidataThing
            Single wikidata thing
        """
        try:
            return WikidataThing.from_wikidata(__waiting_request__(qid))
        except Exception as e:
            logger.exception(e)
            raise WikiDataAPIException(e) from e

    @staticmethod
    def __wikidata_multiple_task__(qids: List[str]) -> List[WikidataThing]:
        """Retrieve multiple Wikidata things.

        Parameters
        ----------
        qids: List[str]
            QIDs of the entities.

        Returns
        -------
        instances: List[WikidataThing]
            List of wikidata things
        """
        try:
            return [WikidataThing.from_wikidata(e) for e in __waiting_multi_request__(qids)]
        except Exception as e:
            logger.exception(e)
            raise WikiDataAPIException(e) from e

    @staticmethod
    def retrieve_entity(qid: str) -> WikidataThing:
        """
        Retrieve a single Wikidata thing.

        Parameters
        ----------
        qid: str
            QID of the entity.

        Returns
        -------
        instance: WikidataThing
            Single wikidata thing
        """
        return WikiDataAPIClient.__wikidata_task__(qid)

    @staticmethod
    def retrieve_entities(qids: Union[List[str], Set[str]]) -> List[WikidataThing]:
        """
        Retrieve multiple Wikidata things.
        Parameters
        ----------
        qids: List[str]
            QIDs of the entities.

        Returns
        -------
        instances: List[WikidataThing]
            List of wikidata things.
        """
        pulled: List[WikidataThing] = []
        if len(qids) == 0:
            return []
        jobs: List[List[str]] = list(chunks(list(qids), API_LIMIT))
        num_processes: int = min(len(jobs), multiprocessing.cpu_count())
        if num_processes > 1:
            with Pool(processes=num_processes) as pool:
                # Wikidata thing is not support in multiprocessing
                with tqdm(total=len(jobs)) as pbar:
                    for lst in pool.imap_unordered(__waiting_multi_request__, jobs):
                        pulled.extend([WikidataThing.from_wikidata(e) for e in lst])
                        pbar.set_description_str(f"{len(pulled)} / {len(qids)} entities retrieved.")
                        pbar.update(1)
        else:
            pulled = WikiDataAPIClient.__wikidata_multiple_task__(jobs[0])
        return pulled
