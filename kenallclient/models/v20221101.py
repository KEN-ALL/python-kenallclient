"""Models for API version 2022-11-01"""

import dataclasses
from typing import Any, Dict, List, Optional, Tuple

__all__ = [
    "Address",
    "AddressResolverResponse",
    "AddressSearcherResponse",
    "City",
    "CityResolverResponse",
    "Corporation",
    "NTACorporateInfo",
    "NTACorporateInfoFacetResults",
    "NTACorporateInfoResolverResponse",
    "NTACorporateInfoSearcherResponse",
]


@dataclasses.dataclass()
class Corporation:
    """Corporation model for v2022-11-01"""

    name: str
    name_kana: str
    block_lot: str
    block_lot_num: Optional[str]
    post_office: str
    code_type: int

    @classmethod
    def fromdict(cls, d: Dict[str, Any]) -> "Corporation":
        return cls(**d)


@dataclasses.dataclass()
class NTACorporateInfo:
    """Corporate info model for v2022-11-01"""

    sequence_number: int
    corporate_number: str
    process: int
    correct: int
    update_date: str
    change_date: str
    name: str
    name_image_id: Optional[str]
    kind: int
    prefecture_name: str
    city_name: str
    published_date: str
    hihyoji: int
    furigana: str
    en_address_outside: Optional[str]
    en_address_line: Optional[str]
    en_prefecture_name: str
    en_name: str
    assignment_date: str
    change_cause: str
    successor_corporate_number: Optional[str]
    close_cause: Optional[str]
    close_date: Optional[str]
    address_outside_image_id: Optional[str]
    address_outside: str
    post_code: str
    jisx0402: str
    address_image_id: Optional[str]
    street_number: str

    @classmethod
    def fromdict(cls, d: Dict[str, Any]) -> "NTACorporateInfo":
        return cls(**d)


@dataclasses.dataclass()
class NTACorporateInfoResolverResponse:
    """Corporate info resolver response for v2022-11-01"""

    version: str
    data: List[NTACorporateInfo]

    @classmethod
    def fromdict(cls, d: Dict[str, Any]) -> "NTACorporateInfoResolverResponse":
        data = [NTACorporateInfo.fromdict(i) for i in d["data"]]
        return cls(version=d["version"], data=data)


@dataclasses.dataclass()
class NTACorporateInfoFacetResults:
    area: Optional[List[Tuple[str, int]]]
    kind: Optional[List[Tuple[str, int]]]
    process: Optional[List[Tuple[str, int]]]
    close_cause: Optional[List[Tuple[str, int]]]

    def __getitem__(self, v: Any) -> List[Tuple[str, int]]:
        if v == "area":
            if self.area is not None:
                return self.area
        elif v == "kind":
            if self.kind is not None:
                return self.kind
        elif v == "process":
            if self.process is not None:
                return self.process
        elif v == "close_cause":
            if self.close_cause is not None:
                return self.close_cause
        raise KeyError(v)

    def __contains__(self, v: Any) -> bool:
        if v == "area":
            return self.area is not None
        elif v == "kind":
            return self.kind is not None
        elif v == "process":
            return self.process is not None
        elif v == "close_cause":
            return self.close_cause is not None
        return False

    @classmethod
    def fromdict(cls, d: Dict[str, Any]) -> "NTACorporateInfoFacetResults":
        return cls(
            area=[tuple(pair) for pair in d["area"]] if "area" in d else None,
            kind=[tuple(pair) for pair in d["kind"]] if "kind" in d else None,
            process=[tuple(pair) for pair in d["process"]] if "process" in d else None,
            close_cause=[tuple(pair) for pair in d["close_cause"]]
            if "close_cause" in d
            else None,
        )


@dataclasses.dataclass()
class NTACorporateInfoSearcherResponse:
    """Corporate info searcher response for v2022-11-01"""

    version: str
    data: List[str]
    query: str
    count: int
    offset: int
    limit: int
    facets: List[List[Any]]

    @classmethod
    def fromdict(cls, d: Dict[str, Any]) -> "NTACorporateInfoSearcherResponse":
        dd = dict(d)
        dd["data"] = [NTACorporateInfo.fromdict(i) for i in dd["data"]]
        dd["facets"] = NTACorporateInfoFacetResults.fromdict(dd.get("facets", {}))
        return cls(**dd)


@dataclasses.dataclass()
class Address:
    """Address model for v2022-11-01 - adds romanization and more fields"""

    jisx0402: str
    old_code: str
    postal_code: str
    prefecture_kana: str
    city_kana: str
    town_kana: str
    town_kana_raw: str
    prefecture: str
    city: str
    town: str
    koaza: str
    kyoto_street: str
    building: str
    floor: str
    town_partial: bool
    town_addressed_koaza: bool
    town_chome: bool
    town_multi: bool
    town_raw: str
    corporation: Optional[Corporation]
    # New fields in v2022-11-01
    prefecture_roman: str
    city_roman: str
    county: str
    county_kana: str
    county_roman: str
    city_without_county_and_ward: str
    city_without_county_and_ward_kana: str
    city_without_county_and_ward_roman: str
    city_ward: str
    city_ward_kana: str
    city_ward_roman: str
    town_roman: str
    town_jukyohyoji: bool
    update_status: int
    update_reason: int

    @classmethod
    def fromdict(cls, i: Dict[str, Any]) -> "Address":
        if i.get("corporation"):
            i = dict(i)
            i["corporation"] = Corporation.fromdict(i["corporation"])
        return cls(**i)


@dataclasses.dataclass()
class AddressResolverResponse:
    """Address resolver response for v2022-11-01"""

    version: str
    data: List[Address]

    @classmethod
    def fromdict(cls, d: Dict[str, Any]) -> "AddressResolverResponse":
        data = [Address.fromdict(i) for i in d["data"]]
        return cls(version=d["version"], data=data)


@dataclasses.dataclass()
class AddressSearcherResponse:
    """Address searcher response for v2022-11-01"""

    version: str
    data: List[Address]
    query: str
    count: int
    offset: Optional[int]
    limit: Optional[int]
    facets: Optional[List[List[Any]]]

    @classmethod
    def fromdict(cls, d: Dict[str, Any]) -> "AddressSearcherResponse":
        data = [Address.fromdict(i) for i in d["data"]]
        dd = dict(d)
        dd["data"] = data
        if dd.get("facets") is not None:
            dd["facets"] = [list(f) for f in dd["facets"]]
        return cls(**dd)


@dataclasses.dataclass()
class City:
    """City model for v2022-11-01 - adds romanization"""

    jisx0402: str
    prefecture: str
    prefecture_code: str
    prefecture_kana: str
    city: str
    city_code: str
    city_kana: str
    # New fields in v2022-11-01
    prefecture_roman: str
    city_roman: str

    @classmethod
    def fromdict(cls, d: Dict[str, Any]) -> "City":
        return cls(**d)


@dataclasses.dataclass()
class CityResolverResponse:
    """City resolver response for v2022-11-01"""

    version: str
    data: List[City]

    @classmethod
    def fromdict(cls, d: Dict[str, Any]) -> "CityResolverResponse":
        data = [City.fromdict(i) for i in d["data"]]
        return cls(version=d["version"], data=data)
