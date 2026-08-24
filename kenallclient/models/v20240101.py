"""Models for API version 2024-01-01"""

import dataclasses
from typing import Any

__all__ = [
    "Address",
    "AddressResolverResponse",
    "AddressSearcherResponse",
    "Bank",
    "BankBranch",
    "BankBranchesData",
    "BankBranchesResponse",
    "BankBranchData",
    "BankBranchResolverResponse",
    "BankResolverResponse",
    "BanksResponse",
    "City",
    "CityResolverResponse",
    "Corporation",
    "NTACorporateInfo",
    "NTACorporateInfoFacetResults",
    "NTACorporateInfoResolverResponse",
    "NTACorporateInfoSearcherResponse",
    "NTAEntityAddress",
    "NTAQualifiedInvoiceIssuerInfo",
    "NTAQualifiedInvoiceIssuerInfoResolverResponse",
]


# Models copied from v2023-09-01 to make this module self-contained
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


@dataclasses.dataclass()
class NTAEntityAddress:
    """Enhanced address structure for invoice/school APIs"""

    jisx0402: str
    postal_code: str
    prefecture: str
    prefecture_kana: str
    prefecture_roman: str
    city: str
    city_kana: str
    city_roman: str
    street_number: str
    town: str
    kyoto_street: str
    block_lot_num: str
    building: str
    floor_room: str

    @classmethod
    def fromdict(cls, d: dict[str, Any]) -> "NTAEntityAddress":
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
    name_image_id: str | None
    kind: int
    published_date: str
    hihyoji: int
    furigana: str
    en_address_outside: str | None
    en_address_line: str | None
    en_name: str
    assignment_date: str
    change_cause: str
    successor_corporate_number: str | None
    close_cause: str | None
    close_date: str | None
    address_outside_image_id: str | None
    address_outside: str
    address_image_id: str | None
    qualified_invoice_issuer_number: str | None
    address: NTAEntityAddress

    @classmethod
    def fromdict(cls, d: dict[str, Any]) -> "NTACorporateInfo":
        dd = dict(d)
        if dd.get("address"):
            dd["address"] = NTAEntityAddress.fromdict(dd["address"])
        return cls(**dd)


@dataclasses.dataclass()
class NTACorporateInfoResolverResponse:
    """Corporate info resolver response for v2022-11-01"""

    version: str
    data: NTACorporateInfo

    @classmethod
    def fromdict(cls, d: dict[str, Any]) -> "NTACorporateInfoResolverResponse":
        return cls(version=d["version"], data=NTACorporateInfo.fromdict(d["data"]))


@dataclasses.dataclass()
class NTACorporateInfoFacetResults:
    area: list[tuple[str, int]] | None
    kind: list[tuple[str, int]] | None
    process: list[tuple[str, int]] | None
    close_cause: list[tuple[str, int]] | None

    def __getitem__(self, v: Any) -> list[tuple[str, int]]:
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
    def fromdict(cls, d: dict[str, Any]) -> "NTACorporateInfoFacetResults":
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
    """Corporate info searcher response for v2024-01-01"""

    version: str
    data: list[str]
    query: str
    count: int
    offset: int
    limit: int
    facets: NTACorporateInfoFacetResults

    @classmethod
    def fromdict(cls, d: dict[str, Any]) -> "NTACorporateInfoSearcherResponse":
        dd = dict(d)
        dd["data"] = [NTACorporateInfo.fromdict(i) for i in dd["data"]]
        dd["facets"] = NTACorporateInfoFacetResults.fromdict(dd.get("facets") or {})
        return cls(**dd)


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
    def fromdict(cls, d: dict[str, Any]) -> "Bank":
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
    def fromdict(cls, d: dict[str, Any]) -> "BankBranch":
        return cls(**d)


@dataclasses.dataclass()
class BanksResponse:
    """Banks response for v2023-09-01"""

    version: str
    data: list[Bank]

    @classmethod
    def fromdict(cls, d: dict[str, Any]) -> "BanksResponse":
        data = [Bank.fromdict(i) for i in d["data"]]
        return cls(version=d["version"], data=data)


@dataclasses.dataclass()
class BankResolverResponse:
    """Bank resolver response for v2023-09-01"""

    version: str
    data: Bank

    @classmethod
    def fromdict(cls, d: dict[str, Any]) -> "BankResolverResponse":
        return cls(version=d["version"], data=Bank.fromdict(d["data"]))


@dataclasses.dataclass()
class BankBranchesData:
    """Nested data structure for bank branches response in v2024-01-01"""

    bank: Bank
    branches: dict[str, BankBranch]

    @classmethod
    def fromdict(cls, d: dict[str, Any]) -> "BankBranchesData":
        bank = Bank.fromdict(d["bank"])
        branches = {
            code: BankBranch.fromdict(branch) for code, branch in d["branches"].items()
        }
        return cls(bank=bank, branches=branches)


@dataclasses.dataclass()
class BankBranchesResponse:
    """Bank branches response for v2024-01-01"""

    version: str
    data: BankBranchesData

    @classmethod
    def fromdict(cls, d: dict[str, Any]) -> "BankBranchesResponse":
        data = BankBranchesData.fromdict(d["data"])
        return cls(version=d["version"], data=data)


@dataclasses.dataclass()
class BankBranchData:
    """Nested data structure for bank branch resolver response in v2024-01-01"""

    bank: Bank
    branch: BankBranch

    @classmethod
    def fromdict(cls, d: dict[str, Any]) -> "BankBranchData":
        bank = Bank.fromdict(d["bank"])
        branch = BankBranch.fromdict(d["branch"])
        return cls(bank=bank, branch=branch)


@dataclasses.dataclass()
class BankBranchResolverResponse:
    """Bank branch resolver response for v2024-01-01"""

    version: str
    data: BankBranchData

    @classmethod
    def fromdict(cls, d: dict[str, Any]) -> "BankBranchResolverResponse":
        data = BankBranchData.fromdict(d["data"])
        return cls(version=d["version"], data=data)


@dataclasses.dataclass()
class NTAQualifiedInvoiceIssuerInfo:
    """Invoice issuer info for v2024-01-01"""

    published_date: str
    sequence_number: int
    qualified_invoice_issuer_number: str | None
    process: int
    correct: int | None
    kind: int
    country: int
    latest: int
    registration_date: str
    update_date: str
    disposal_date: str
    expire_date: str | None
    name: str
    kana: str | None
    trade_name: str | None
    popular_name_previous_name: str | None
    address_inside: NTAEntityAddress | None
    address_request: NTAEntityAddress | None
    address: NTAEntityAddress | None

    @classmethod
    def fromdict(cls, d: dict[str, Any]) -> "NTAQualifiedInvoiceIssuerInfo":
        dd = dict(d)
        if dd.get("address_inside"):
            dd["address_inside"] = NTAEntityAddress.fromdict(dd["address_inside"])
        if dd.get("address_request"):
            dd["address_request"] = NTAEntityAddress.fromdict(dd["address_request"])
        if dd.get("address"):
            dd["address"] = NTAEntityAddress.fromdict(dd["address"])
        return cls(**dd)


@dataclasses.dataclass()
class NTAQualifiedInvoiceIssuerInfoResolverResponse:
    """Invoice issuer resolver response for v2024-01-01"""

    version: str
    data: NTAQualifiedInvoiceIssuerInfo

    @classmethod
    def fromdict(
        cls, d: dict[str, Any]
    ) -> "NTAQualifiedInvoiceIssuerInfoResolverResponse":
        return cls(
            version=d["version"], data=NTAQualifiedInvoiceIssuerInfo.fromdict(d["data"])
        )
