"""Compatible models - maintains backward compatibility with string close_cause"""

import dataclasses
from collections.abc import Sequence
from typing import Any, Dict, List, Optional, Tuple

from . import APIVersion
from .v20230901 import (
    Bank,
    BankBranch,
    BankResolverResponse,
    BanksResponse,
)
from .v20240101 import (
    NTAEntityAddress,
    NTAQualifiedInvoiceIssuerInfo,
    NTAQualifiedInvoiceIssuerInfoResolverResponse,
)

__all__ = [
    "Address",
    "AddressResolverResponse",
    "AddressSearcherResponse",
    "Bank",
    "BankBranch",
    "BankBranchesResponse",
    "BankBranchResolverResponse",
    "BankResolverResponse",
    "BanksResponse",
    "City",
    "CityResolverResponse",
    "Corporation",
    "Holiday",
    "HolidaySearchResult",
    "NTACorporateInfo",
    "NTACorporateInfoFacetResults",
    "NTACorporateInfoResolverResponse",
    "NTACorporateInfoSearcherResponse",
    "NTAEntityAddress",
    "NTAQualifiedInvoiceIssuerInfo",
    "NTAQualifiedInvoiceIssuerInfoResolverResponse",
]


# Base classes merged from v20220901 (used only internally for compatibility)
@dataclasses.dataclass()
class Corporation:
    """Corporation model (base class for compatibility)"""

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
class NTACorporateInfoFacetResults:
    """Facet results for corporate info (base class for compatibility)"""

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
class Address:
    """Compatible Address model that works with both v20220901 and v20221101"""

    # Common fields present in both versions
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

    # Fields added in v20221101 (made optional for compatibility)
    prefecture_roman: Optional[str] = None
    city_roman: Optional[str] = None
    county: Optional[str] = None
    county_kana: Optional[str] = None
    county_roman: Optional[str] = None
    city_without_county_and_ward: Optional[str] = None
    city_without_county_and_ward_kana: Optional[str] = None
    city_without_county_and_ward_roman: Optional[str] = None
    city_ward: Optional[str] = None
    city_ward_kana: Optional[str] = None
    city_ward_roman: Optional[str] = None
    town_roman: Optional[str] = None
    town_jukyohyoji: Optional[bool] = None
    update_status: Optional[int] = None
    update_reason: Optional[int] = None

    @classmethod
    def fromdict(cls, i: Dict[str, Any]) -> "Address":
        # Create a copy to avoid modifying the original
        data = dict(i)

        # Handle corporation field
        if data.get("corporation"):
            data["corporation"] = Corporation.fromdict(data["corporation"])

        # Filter out only the fields that exist in the class
        field_names = {f.name for f in dataclasses.fields(cls)}
        filtered_data = {k: v for k, v in data.items() if k in field_names}

        return cls(**filtered_data)


@dataclasses.dataclass()
class AddressResolverResponse:
    """Compatible Address resolver response"""

    version: str
    data: List[Address]

    @classmethod
    def fromdict(cls, d: Dict[str, Any]) -> "AddressResolverResponse":
        data = [Address.fromdict(i) for i in d["data"]]
        return cls(version=d["version"], data=data)


@dataclasses.dataclass()
class AddressSearcherResponse:
    """Compatible Address searcher response"""

    version: str
    data: List[Address]
    query: str
    count: int
    offset: Optional[int]
    limit: Optional[int]
    facets: Optional[List[Any]]

    @classmethod
    def fromdict(cls, d: Dict[str, Any]) -> "AddressSearcherResponse":
        data = [Address.fromdict(i) for i in d["data"]]
        dd = dict(d)
        dd["data"] = data
        if dd.get("facets") is not None:
            # Keep facets as-is, don't convert to tuple
            dd["facets"] = dd["facets"]
        return cls(**dd)


@dataclasses.dataclass()
class City:
    """Compatible City model that works with both v20220901 and v20221101"""

    # Common fields present in both versions
    jisx0402: str
    prefecture: str
    prefecture_code: str
    prefecture_kana: str
    city: str
    city_code: str
    city_kana: str

    # Fields added in v20221101 (made optional for compatibility)
    prefecture_roman: Optional[str] = None
    city_roman: Optional[str] = None

    @classmethod
    def fromdict(cls, d: Dict[str, Any]) -> "City":
        # Filter out only the fields that exist in the class
        field_names = {f.name for f in dataclasses.fields(cls)}
        filtered_data = {k: v for k, v in d.items() if k in field_names}
        return cls(**filtered_data)


@dataclasses.dataclass()
class CityResolverResponse:
    """Compatible City resolver response"""

    version: str
    data: List[City]

    @classmethod
    def fromdict(cls, d: Dict[str, Any]) -> "CityResolverResponse":
        data = [City.fromdict(i) for i in d["data"]]
        return cls(version=d["version"], data=data)


@dataclasses.dataclass()
class Holiday:
    """Holiday model (same across all versions)"""

    title: str
    date: str
    day_of_week: int
    day_of_week_text: str

    @classmethod
    def fromdict(cls, d: Dict[str, Any]) -> "Holiday":
        return cls(**d)


@dataclasses.dataclass()
class HolidaySearchResult:
    """Holiday search result (same across all versions)"""

    data: List[Holiday]

    @classmethod
    def fromdict(cls, d: Dict[str, Any]) -> "HolidaySearchResult":
        data = [Holiday.fromdict(i) for i in d["data"]]
        return HolidaySearchResult(data=data)


@dataclasses.dataclass()
class NTACorporateInfo:
    """Compatible NTACorporateInfo that ensures close_cause is always string"""

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
    town: Optional[str]
    kyoto_street: Optional[str]
    block_lot_num: Optional[str]
    building: Optional[str]
    floor_room: Optional[str]

    @classmethod
    def fromdict(
        cls, d: Dict[str, Any], api_version: Optional[APIVersion] = None
    ) -> "NTACorporateInfo":
        # Determine the data format based on structure, not the API version
        # v2025-01-01+ uses nested address object, earlier versions use flat structure
        has_nested_address = "address" in d and isinstance(d["address"], dict)

        if has_nested_address:
            dd = {
                "published_date": d["published_date"],
                "sequence_number": str(d["sequence_number"]),
                "corporate_number": d["corporate_number"],
                "process": d["process"],
                "correct": str(d["correct"]),
                "update_date": d["update_date"],
                "change_date": d["change_date"],
                "name": d["name"],
                "name_image_id": d["name_image_id"],
                "kind": str(d["kind"]),
                "prefecture_name": d["address"]["prefecture"],
                "city_name": d["address"]["city"],
                "street_number": d["address"]["street_number"],
                "town": d["address"]["town"],
                "kyoto_street": d["address"]["kyoto_street"],
                "block_lot_num": d["address"]["block_lot_num"],
                "building": d["address"]["building"],
                "floor_room": d["address"]["floor_room"],
                "address_image_id": d["address_image_id"],
                "jisx0402": d["address"]["jisx0402"],
                "post_code": d["address"]["postal_code"],
                "address_outside": d["address_outside"],
                "address_outside_image_id": d["address_outside_image_id"],
                "close_date": d["close_date"],
                "close_cause": str(d["close_cause"])
                if d["close_cause"] is not None
                else None,
                "successor_corporate_number": d["successor_corporate_number"],
                "change_cause": d["change_cause"],
                "assignment_date": d["assignment_date"],
                "en_name": d["en_name"],
                "en_prefecture_name": d["address"]["prefecture_roman"],
                "en_address_line": d["en_address_line"],
                "en_address_outside": d["en_address_outside"],
                "furigana": d["furigana"],
                "hihyoji": str(d["hihyoji"]),
            }
        else:
            dd = d

        return cls(**dd)


@dataclasses.dataclass()
class NTACorporateInfoResolverResponse:
    """Compatible resolver response that converts numeric close_cause to string"""

    version: str
    data: NTACorporateInfo

    @classmethod
    def fromdict(
        cls, d: Dict[str, Any], api_version: Optional[APIVersion] = None
    ) -> "NTACorporateInfoResolverResponse":
        return cls(
            version=d["version"], data=NTACorporateInfo.fromdict(d["data"], api_version)
        )


@dataclasses.dataclass()
class NTACorporateInfoSearcherResponse:
    """Compatible searcher response (no conversion needed for search results)"""

    version: str
    data: List[NTACorporateInfo]
    query: str
    count: int
    offset: int
    limit: int
    facets: NTACorporateInfoFacetResults

    @classmethod
    def fromdict(
        cls, d: Dict[str, Any], api_version: Optional[APIVersion] = None
    ) -> "NTACorporateInfoSearcherResponse":
        dd = dict(d)
        dd["facets"] = NTACorporateInfoFacetResults.fromdict(dd.get("facets", {}))
        dd["data"] = [NTACorporateInfo.fromdict(i, api_version) for i in dd["data"]]
        return cls(**dd)


@dataclasses.dataclass()
class BankBranchesResponse:
    """Compatible bank branches response that flattens the nested structure"""

    version: str
    data: Dict[str, List[BankBranch]]

    @classmethod
    def fromdict(
        cls, d: Dict[str, Any], api_version: Optional[APIVersion] = None
    ) -> "BankBranchesResponse":
        # Parse using the version-specific model
        # Infer API version from data structure if not provided
        if api_version is None:
            # Check if branches contains arrays (v2025-01-01) or single objects
            # (v2023-09-01/v2024-01-01)
            if "data" in d and "branches" in d["data"] and d["data"]["branches"]:
                first_value = next(iter(d["data"]["branches"].values()), None)
                if isinstance(first_value, Sequence):
                    api_version = "2025-01-01"
                else:
                    api_version = "2023-09-01"
            else:
                api_version = "2023-09-01"

        if api_version >= "2025-01-01":
            branches = {
                k: [BankBranch.fromdict(i) for i in v]
                for k, v in d["data"]["branches"].items()
            }
            return cls(version=d["version"], data=branches)
        elif api_version >= "2023-09-01":
            branches = {
                k: [BankBranch.fromdict(v)] for k, v in d["data"]["branches"].items()
            }
            return cls(version=d["version"], data=branches)
        else:
            raise ValueError(f"Bank API not available for version {api_version}")


@dataclasses.dataclass()
class BankBranchResolverResponse:
    """Compatible bank branch resolver response that flattens the nested structure"""

    version: str
    data: List[BankBranch]

    @classmethod
    def fromdict(
        cls, d: Dict[str, Any], api_version: Optional[APIVersion] = None
    ) -> "BankBranchResolverResponse":
        # Parse using the version-specific model
        # Infer API version from data structure if not provided
        if api_version is None:
            # Check if branch is an array (v2025-01-01) or single object
            # (v2023-09-01/v2024-01-01)
            if "data" in d and "branch" in d["data"]:
                if isinstance(d["data"]["branch"], Sequence):
                    api_version = "2025-01-01"
                else:
                    api_version = "2023-09-01"
            else:
                api_version = "2023-09-01"

        if api_version >= "2025-01-01":
            branches = [BankBranch.fromdict(i) for i in d["data"]["branch"]]
            return cls(version=d["version"], data=branches)
        elif api_version >= "2023-09-01":
            return cls(
                version=d["version"], data=[BankBranch.fromdict(d["data"]["branch"])]
            )
        else:
            raise ValueError(f"Bank API not available for version {api_version}")
