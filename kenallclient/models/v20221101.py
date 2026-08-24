"""Models for API version 2022-11-01"""

import dataclasses
from typing import Any

__all__ = [
    "Address",
    "AddressResolverResponse",
    "AddressSearcherResponse",
    "City",
    "CityResolverResponse",
    "Corporation",
]


@dataclasses.dataclass()
class Corporation:
    """Corporation model for v2022-11-01"""

    name: str
    name_kana: str
    block_lot: str
    block_lot_num: str | None
    post_office: str
    code_type: int

    @classmethod
    def fromdict(cls, d: dict[str, Any]) -> "Corporation":
        return cls(**d)


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
    corporation: Corporation | None
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
    def fromdict(cls, i: dict[str, Any]) -> "Address":
        if i.get("corporation"):
            i = dict(i)
            i["corporation"] = Corporation.fromdict(i["corporation"])
        return cls(**i)


@dataclasses.dataclass()
class AddressResolverResponse:
    """Address resolver response for v2022-11-01"""

    version: str
    data: list[Address]

    @classmethod
    def fromdict(cls, d: dict[str, Any]) -> "AddressResolverResponse":
        data = [Address.fromdict(i) for i in d["data"]]
        return cls(version=d["version"], data=data)


@dataclasses.dataclass()
class AddressSearcherResponse:
    """Address searcher response for v2022-11-01"""

    version: str
    data: list[Address]
    query: str
    count: int
    offset: int | None
    limit: int | None
    facets: list[tuple[str, int]] | None

    @classmethod
    def fromdict(cls, d: dict[str, Any]) -> "AddressSearcherResponse":
        data = [Address.fromdict(i) for i in d["data"]]
        dd = dict(d)
        dd["data"] = data
        dd["facets"] = [
            tuple(pair) for pair in (dd.get("facets") or {}).get("area", [])
        ]
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
    def fromdict(cls, d: dict[str, Any]) -> "City":
        return cls(**d)


@dataclasses.dataclass()
class CityResolverResponse:
    """City resolver response for v2022-11-01"""

    version: str
    data: list[City]

    @classmethod
    def fromdict(cls, d: dict[str, Any]) -> "CityResolverResponse":
        data = [City.fromdict(i) for i in d["data"]]
        return cls(version=d["version"], data=data)
