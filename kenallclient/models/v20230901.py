"""Models for API version 2023-09-01"""

import dataclasses
from typing import Any, Dict, List, Optional

__all__ = [
    "Corporation",
    "Address",
    "AddressResolverResponse",
    "AddressSearcherResponse",
    "City",
    "CityResolverResponse",
    "Bank",
    "BankBranch",
    "BanksResponse",
    "BankResolverResponse",
    "BankBranchesData",
    "BankBranchesResponse",
    "BankBranchData",
    "BankBranchResolverResponse",
]


# Models copied from v2022-11-01 to make this module self-contained
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
    """City model for v2023-09-01 - adds county_* and city_without_county_and_ward_*"""

    jisx0402: str
    prefecture: str
    prefecture_code: str
    prefecture_kana: str
    prefecture_roman: str
    city: str
    city_code: str
    city_kana: str
    city_roman: str
    county: str
    county_kana: str
    county_roman: str
    city_without_county_and_ward: str
    city_without_county_and_ward_kana: str
    city_without_county_and_ward_roman: str

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


# New models added in v2023-09-01 for Bank API
@dataclasses.dataclass()
class Bank:
    """Bank model for v2023-09-01"""

    code: str
    name: str
    katakana: str
    hiragana: str
    romaji: str

    @classmethod
    def fromdict(cls, d: Dict[str, Any]) -> "Bank":
        return cls(**d)


@dataclasses.dataclass()
class BankBranch:
    """Bank branch model for v2023-09-01"""

    code: str
    name: str
    katakana: str
    hiragana: str
    romaji: str

    @classmethod
    def fromdict(cls, d: Dict[str, Any]) -> "BankBranch":
        return cls(**d)


@dataclasses.dataclass()
class BanksResponse:
    """Banks response for v2023-09-01"""

    version: str
    data: List[Bank]

    @classmethod
    def fromdict(cls, d: Dict[str, Any]) -> "BanksResponse":
        data = [Bank.fromdict(i) for i in d["data"]]
        return cls(version=d["version"], data=data)


@dataclasses.dataclass()
class BankResolverResponse:
    """Bank resolver response for v2023-09-01"""

    version: str
    data: Bank

    @classmethod
    def fromdict(cls, d: Dict[str, Any]) -> "BankResolverResponse":
        return cls(version=d["version"], data=Bank.fromdict(d["data"]))


@dataclasses.dataclass()
class BankBranchesData:
    """Nested data structure for bank branches response in v2023-09-01"""

    bank: Bank
    branches: Dict[str, BankBranch]

    @classmethod
    def fromdict(cls, d: Dict[str, Any]) -> "BankBranchesData":
        bank = Bank.fromdict(d["bank"])
        branches = {
            code: BankBranch.fromdict(branch) for code, branch in d["branches"].items()
        }
        return cls(bank=bank, branches=branches)


@dataclasses.dataclass()
class BankBranchesResponse:
    """Bank branches response for v2023-09-01"""

    version: str
    data: BankBranchesData

    @classmethod
    def fromdict(cls, d: Dict[str, Any]) -> "BankBranchesResponse":
        data = BankBranchesData.fromdict(d["data"])
        return cls(version=d["version"], data=data)


@dataclasses.dataclass()
class BankBranchData:
    """Nested data structure for bank branch resolver response in v2023-09-01"""

    bank: Bank
    branch: BankBranch

    @classmethod
    def fromdict(cls, d: Dict[str, Any]) -> "BankBranchData":
        bank = Bank.fromdict(d["bank"])
        branch = BankBranch.fromdict(d["branch"])
        return cls(bank=bank, branch=branch)


@dataclasses.dataclass()
class BankBranchResolverResponse:
    """Bank branch resolver response for v2023-09-01"""

    version: str
    data: BankBranchData

    @classmethod
    def fromdict(cls, d: Dict[str, Any]) -> "BankBranchResolverResponse":
        data = BankBranchData.fromdict(d["data"])
        return cls(version=d["version"], data=data)
