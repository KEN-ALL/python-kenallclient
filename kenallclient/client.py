import json
import re
import urllib.parse
import urllib.request
from typing import Dict, List, Literal, Optional, Tuple, overload

from kenallclient.models import (
    compatible,
    v20221101,
    v20230901,
    v20240101,
    v20250101,
    v20260801,
)
from kenallclient.models.compatible import (
    BusinessDayCheckResponse,
    HolidaySearchResult,
    WhoamiResponse,
)
from kenallclient.models.factories import (
    create_address_resolver_response,
    create_address_searcher_response,
    create_bank_branch_resolver_response,
    create_bank_branches_response,
    create_bank_resolver_response,
    create_banks_response,
    create_city_resolver_response,
    create_corporate_info_resolver_response,
    create_corporate_info_searcher_response,
    create_invoice_issuer_resolver_response,
    create_school_resolver_response,
    create_school_searcher_response,
)
from kenallclient.types import (
    APIVersion,
    BankSearchAPIVersion,
    BankSearchMatchMode,
    BankType,
)

_HYPHENATED_POSTAL_CODE = re.compile(r"^(\d{3})-(\d{4})$")


def normalize_postal_code(postal_code: str) -> str:
    """Strip the hyphen off a postal code written as ``NNN-NNNN``"""
    match = _HYPHENATED_POSTAL_CODE.match(postal_code)
    if match:
        return match.group(1) + match.group(2)
    return postal_code


class KenAllClient:
    api_url = "https://api.kenall.jp"
    api_version: Optional[APIVersion] = None

    def __init__(
        self,
        api_key: str,
        api_url: Optional[str] = None,
    ) -> None:
        self.api_key = api_key
        if api_url is not None:
            self.api_url = api_url

    @property
    def authorization(self) -> Dict[str, str]:
        auth = {"Authorization": f"Token {self.api_key}"}
        return auth

    def _build_headers(
        self, api_version: Optional[APIVersion] = None
    ) -> Dict[str, str]:
        headers = self.authorization.copy()
        version = api_version or self.api_version
        if version:
            headers["KenAll-API-Version"] = version
        return headers

    # Address resolver with version-specific return types
    @overload
    def get(
        self,
        postal_code: str,
        api_version: Literal["2022-11-01"] = ...,
        *,
        version: Optional[str] = None,
    ) -> v20221101.AddressResolverResponse: ...

    @overload
    def get(
        self,
        postal_code: str,
        api_version: Literal["2023-09-01"] = ...,
        *,
        version: Optional[str] = None,
    ) -> v20230901.AddressResolverResponse: ...

    @overload
    def get(
        self,
        postal_code: str,
        api_version: Literal["2024-01-01"] = ...,
        *,
        version: Optional[str] = None,
    ) -> v20240101.AddressResolverResponse: ...

    @overload
    def get(
        self,
        postal_code: str,
        api_version: Literal["2025-01-01"] = ...,
        *,
        version: Optional[str] = None,
    ) -> v20250101.AddressResolverResponse: ...

    @overload
    def get(
        self,
        postal_code: str,
        api_version: Literal["2026-08-01"] = ...,
        *,
        version: Optional[str] = None,
    ) -> v20260801.AddressResolverResponse: ...

    @overload
    def get(
        self,
        postal_code: str,
        api_version: None = None,
        *,
        version: Optional[str] = None,
    ) -> compatible.AddressResolverResponse: ...

    def get(
        self,
        postal_code: str,
        api_version: Optional[APIVersion] = None,
        *,
        version: Optional[str] = None,
    ):
        """Get address information by postal code

        `version` pins the database version the query is performed against,
        and defaults to the latest available one.
        """
        req = self.create_request(postal_code, api_version, version=version)
        return self.fetch(req, api_version)

    # Address search with version-specific return types
    @overload
    def search(
        self,
        *,
        q: Optional[str] = None,
        t: Optional[str] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        facet: Optional[str] = None,
        version: Optional[str] = None,
        api_version: Literal["2022-11-01"] = ...,
    ) -> v20221101.AddressSearcherResponse: ...

    @overload
    def search(
        self,
        *,
        q: Optional[str] = None,
        t: Optional[str] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        facet: Optional[str] = None,
        version: Optional[str] = None,
        api_version: Literal["2023-09-01"] = ...,
    ) -> v20230901.AddressSearcherResponse: ...

    @overload
    def search(
        self,
        *,
        q: Optional[str] = None,
        t: Optional[str] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        facet: Optional[str] = None,
        version: Optional[str] = None,
        api_version: Literal["2024-01-01"] = ...,
    ) -> v20240101.AddressSearcherResponse: ...

    @overload
    def search(
        self,
        *,
        q: Optional[str] = None,
        t: Optional[str] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        facet: Optional[str] = None,
        version: Optional[str] = None,
        api_version: Literal["2025-01-01"] = ...,
    ) -> v20250101.AddressSearcherResponse: ...

    @overload
    def search(
        self,
        *,
        q: Optional[str] = None,
        t: Optional[str] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        facet: Optional[str] = None,
        version: Optional[str] = None,
        api_version: Literal["2026-08-01"] = ...,
    ) -> v20260801.AddressSearcherResponse: ...

    @overload
    def search(
        self,
        *,
        q: Optional[str] = None,
        t: Optional[str] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        facet: Optional[str] = None,
        version: Optional[str] = None,
        api_version: None = None,
    ) -> compatible.AddressSearcherResponse: ...

    def search(
        self,
        *,
        q: Optional[str] = None,
        t: Optional[str] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        facet: Optional[str] = None,
        version: Optional[str] = None,
        api_version: Optional[APIVersion] = None,
    ):
        """Search addresses

        `version` pins the database version the query is performed against,
        and defaults to the latest available one.
        """
        req = self.create_address_search_request(
            q=q,
            t=t,
            offset=offset,
            limit=limit,
            facet=facet,
            version=version,
            api_version=api_version,
        )
        # Use the internal fetch method but since it's for addresses,
        # we need to use a specialized fetch for search results
        return self.fetch_address_search_result(req, api_version)

    # City resolver with version-specific return types
    @overload
    def get_cities(
        self,
        prefecture_code: str,
        api_version: Literal["2022-11-01"] = ...,
        *,
        version: Optional[str] = None,
    ) -> v20221101.CityResolverResponse: ...

    @overload
    def get_cities(
        self,
        prefecture_code: str,
        api_version: Literal["2023-09-01"] = ...,
        *,
        version: Optional[str] = None,
    ) -> v20230901.CityResolverResponse: ...

    @overload
    def get_cities(
        self,
        prefecture_code: str,
        api_version: Literal["2024-01-01"] = ...,
        *,
        version: Optional[str] = None,
    ) -> v20240101.CityResolverResponse: ...

    @overload
    def get_cities(
        self,
        prefecture_code: str,
        api_version: Literal["2025-01-01"] = ...,
        *,
        version: Optional[str] = None,
    ) -> v20250101.CityResolverResponse: ...

    @overload
    def get_cities(
        self,
        prefecture_code: str,
        api_version: Literal["2026-08-01"] = ...,
        *,
        version: Optional[str] = None,
    ) -> v20260801.CityResolverResponse: ...

    @overload
    def get_cities(
        self,
        prefecture_code: str,
        api_version: None = None,
        *,
        version: Optional[str] = None,
    ) -> compatible.CityResolverResponse: ...

    def get_cities(
        self,
        prefecture_code: str,
        api_version: Optional[APIVersion] = None,
        *,
        version: Optional[str] = None,
    ):
        """Get the cities that belong to the prefecture

        `version` pins the database version the query is performed against,
        and defaults to the latest available one.
        """
        req = self.create_city_request(prefecture_code, api_version, version=version)
        return self.fetch_city_result(req, api_version)

    # Houjin/Corporate info methods with version-specific return types
    @overload
    def get_houjin(
        self, houjinbangou: str, api_version: Literal["2024-01-01"] = ...
    ) -> v20240101.NTACorporateInfoResolverResponse: ...

    @overload
    def get_houjin(
        self, houjinbangou: str, api_version: Literal["2025-01-01"] = ...
    ) -> v20250101.NTACorporateInfoResolverResponse: ...

    @overload
    def get_houjin(
        self, houjinbangou: str, api_version: Literal["2026-08-01"] = ...
    ) -> v20260801.NTACorporateInfoResolverResponse: ...

    @overload
    def get_houjin(
        self, houjinbangou: str, api_version: None = None
    ) -> compatible.NTACorporateInfoResolverResponse: ...

    def get_houjin(self, houjinbangou: str, api_version: Optional[APIVersion] = None):
        """Get corporate info by houjinbangou"""
        req = self.create_houjin_request(houjinbangou, api_version)
        return self.fetch_houjin_result(req, api_version)

    @overload
    def search_houjin(
        self,
        q: str,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        mode: Optional[str] = None,
        facet_area: Optional[str] = None,
        facet_kind: Optional[str] = None,
        facet_process: Optional[str] = None,
        facet_close_cause: Optional[str] = None,
        api_version: Literal["2024-01-01"] = ...,
    ) -> v20240101.NTACorporateInfoSearcherResponse: ...

    @overload
    def search_houjin(
        self,
        q: str,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        mode: Optional[str] = None,
        facet_area: Optional[str] = None,
        facet_kind: Optional[str] = None,
        facet_process: Optional[str] = None,
        facet_close_cause: Optional[str] = None,
        api_version: Literal["2025-01-01"] = ...,
    ) -> v20250101.NTACorporateInfoSearcherResponse: ...

    @overload
    def search_houjin(
        self,
        q: str,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        mode: Optional[str] = None,
        facet_area: Optional[str] = None,
        facet_kind: Optional[str] = None,
        facet_process: Optional[str] = None,
        facet_close_cause: Optional[str] = None,
        api_version: Literal["2026-08-01"] = ...,
    ) -> v20260801.NTACorporateInfoSearcherResponse: ...

    @overload
    def search_houjin(
        self,
        q: str,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        mode: Optional[str] = None,
        facet_area: Optional[str] = None,
        facet_kind: Optional[str] = None,
        facet_process: Optional[str] = None,
        facet_close_cause: Optional[str] = None,
        api_version: None = None,
    ) -> compatible.NTACorporateInfoSearcherResponse: ...

    def search_houjin(
        self,
        q: str,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        mode: Optional[str] = None,
        facet_area: Optional[str] = None,
        facet_kind: Optional[str] = None,
        facet_process: Optional[str] = None,
        facet_close_cause: Optional[str] = None,
        api_version: Optional[APIVersion] = None,
    ):
        """Search corporate info"""
        req = self.create_houjin_search_request(
            q=q,
            offset=offset,
            limit=limit,
            mode=mode,
            facet_area=facet_area,
            facet_kind=facet_kind,
            facet_process=facet_process,
            facet_close_cause=facet_close_cause,
            api_version=api_version,
        )
        return self.fetch_search_houjin_result(req, api_version)

    # Qualified invoice issuer info (available from 2024-01-01)
    @overload
    def get_invoice_issuer(
        self, issuer_number: str, api_version: Literal["2024-01-01"] = ...
    ) -> v20240101.NTAQualifiedInvoiceIssuerInfoResolverResponse: ...

    @overload
    def get_invoice_issuer(
        self, issuer_number: str, api_version: Literal["2025-01-01"] = ...
    ) -> v20250101.NTAQualifiedInvoiceIssuerInfoResolverResponse: ...

    @overload
    def get_invoice_issuer(
        self, issuer_number: str, api_version: Literal["2026-08-01"] = ...
    ) -> v20260801.NTAQualifiedInvoiceIssuerInfoResolverResponse: ...

    @overload
    def get_invoice_issuer(
        self, issuer_number: str, api_version: None = None
    ) -> compatible.NTAQualifiedInvoiceIssuerInfoResolverResponse: ...

    def get_invoice_issuer(
        self, issuer_number: str, api_version: Optional[APIVersion] = None
    ):
        """Get qualified invoice issuer info by issuer number"""
        req = self.create_invoice_issuer_request(issuer_number, api_version)
        return self.fetch_invoice_issuer_result(req, api_version)

    # Holiday search (same across all versions)
    def search_holiday(
        self,
        year: Optional[int] = None,
        from_: Optional[str] = None,
        to: Optional[str] = None,
        api_version: Optional[APIVersion] = None,
    ) -> HolidaySearchResult:
        """Search holidays"""

        req = self.create_holiday_search_request(
            year=year, from_date=from_, to_date=to, api_version=api_version
        )
        return self.fetch_search_holiday_result(req, api_version)

    # Business day check (same across all versions)
    def check_business_day(
        self, date: str, api_version: Optional[APIVersion] = None
    ) -> BusinessDayCheckResponse:
        """Tell whether the date is a business day

        `date` is written as ``"YYYY-MM-DD"``.  A business day is a day that is
        neither a weekend nor a public holiday.
        """
        req = self.create_business_day_check_request(date, api_version)
        return self.fetch_business_day_check_result(req, api_version)

    # Whoami (same across all versions)
    def whoami(self, api_version: Optional[APIVersion] = None) -> WhoamiResponse:
        """Get the IP address the request was made from"""
        req = self.create_whoami_request(api_version)
        return self.fetch_whoami_result(req, api_version)

    # Bank APIs with version-specific return types (available from 2023-09-01)
    @overload
    def get_banks(
        self, api_version: Literal["2023-09-01"] = ...
    ) -> v20230901.BanksResponse: ...

    @overload
    def get_banks(
        self, api_version: Literal["2024-01-01"] = ...
    ) -> v20240101.BanksResponse: ...

    @overload
    def get_banks(
        self, api_version: Literal["2025-01-01"] = ...
    ) -> v20250101.BanksResponse: ...

    @overload
    def get_banks(
        self, api_version: Literal["2026-08-01"] = ...
    ) -> v20260801.BanksResponse: ...

    @overload
    def get_banks(self, api_version: None = None) -> compatible.BanksResponse: ...

    def get_banks(self, api_version: Optional[APIVersion] = None):
        """Get all banks"""
        req = self.create_banks_request(api_version)
        return self.fetch_banks_result(req, api_version)

    # Bank search (available from 2026-08-01)
    @overload
    def search_banks(
        self,
        *,
        q: Optional[str] = None,
        match: Optional[BankSearchMatchMode] = None,
        type: Optional[BankType] = None,
        version: Optional[str] = None,
        api_version: Literal["2026-08-01"] = ...,
    ) -> v20260801.BanksResponse: ...

    @overload
    def search_banks(
        self,
        *,
        q: Optional[str] = None,
        match: Optional[BankSearchMatchMode] = None,
        type: Optional[BankType] = None,
        version: Optional[str] = None,
        api_version: None = None,
    ) -> compatible.BanksResponse: ...

    def search_banks(
        self,
        *,
        q: Optional[str] = None,
        match: Optional[BankSearchMatchMode] = None,
        type: Optional[BankType] = None,
        version: Optional[str] = None,
        api_version: Optional[BankSearchAPIVersion] = None,
    ):
        """Search banks by name, by kana reading, or by institution category

        Every parameter is optional; an empty query simply retrieves the whole
        set, just like `get_banks`. Unlike `get_banks`, though, an empty result
        is not an error: as long as `q` or `type` is given, the API responds
        with a 200 and an empty `data` instead of a 404.

        `q` matches both the names and the kana readings. Hiragana, katakana
        and kanji are all accepted; the differences in small kana, prolonged
        sound marks and character width are normalized away before matching,
        and a trailing institution-type suffix such as `"銀行"` or
        `"信用金庫"` is ignored. `match` tells how it is matched, and defaults
        to `"prefix"`.

        The search parameters were introduced in the 2026-08-01 API version;
        earlier versions ignore them and return the whole set, which is why
        `api_version` cannot be an older one.
        """
        req = self.create_bank_search_request(
            q=q, match=match, type=type, version=version, api_version=api_version
        )
        return self.fetch_banks_result(req, api_version)

    @overload
    def get_bank(
        self, bank_code: str, api_version: Literal["2023-09-01"] = ...
    ) -> v20230901.BankResolverResponse: ...

    @overload
    def get_bank(
        self, bank_code: str, api_version: Literal["2024-01-01"] = ...
    ) -> v20240101.BankResolverResponse: ...

    @overload
    def get_bank(
        self, bank_code: str, api_version: Literal["2025-01-01"] = ...
    ) -> v20250101.BankResolverResponse: ...

    @overload
    def get_bank(
        self, bank_code: str, api_version: Literal["2026-08-01"] = ...
    ) -> v20260801.BankResolverResponse: ...

    @overload
    def get_bank(
        self, bank_code: str, api_version: None = None
    ) -> compatible.BankResolverResponse: ...

    def get_bank(self, bank_code: str, api_version: Optional[APIVersion] = None):
        """Get specific bank"""
        req = self.create_bank_request(bank_code, api_version)
        return self.fetch_bank_result(req, api_version)

    @overload
    def get_bank_branches(
        self, bank_code: str, api_version: Literal["2023-09-01"] = ...
    ) -> v20230901.BankBranchesResponse: ...

    @overload
    def get_bank_branches(
        self, bank_code: str, api_version: Literal["2024-01-01"] = ...
    ) -> v20240101.BankBranchesResponse: ...

    @overload
    def get_bank_branches(
        self, bank_code: str, api_version: Literal["2025-01-01"] = ...
    ) -> v20250101.BankBranchesResponse: ...

    @overload
    def get_bank_branches(
        self, bank_code: str, api_version: Literal["2026-08-01"] = ...
    ) -> v20260801.BankBranchesResponse: ...

    @overload
    def get_bank_branches(
        self, bank_code: str, api_version: None = None
    ) -> compatible.BankBranchesResponse: ...

    def get_bank_branches(
        self, bank_code: str, api_version: Optional[APIVersion] = None
    ):
        """Get branches for a bank"""
        req = self.create_bank_branches_request(bank_code, api_version)
        return self.fetch_bank_branches_result(req, api_version)

    # Bank branch search (available from 2026-08-01)
    @overload
    def search_bank_branches(
        self,
        bank_code: str,
        *,
        q: Optional[str] = None,
        match: Optional[BankSearchMatchMode] = None,
        version: Optional[str] = None,
        api_version: Literal["2026-08-01"] = ...,
    ) -> v20260801.BankBranchesResponse: ...

    @overload
    def search_bank_branches(
        self,
        bank_code: str,
        *,
        q: Optional[str] = None,
        match: Optional[BankSearchMatchMode] = None,
        version: Optional[str] = None,
        api_version: None = None,
    ) -> compatible.BankBranchesResponse: ...

    def search_bank_branches(
        self,
        bank_code: str,
        *,
        q: Optional[str] = None,
        match: Optional[BankSearchMatchMode] = None,
        version: Optional[str] = None,
        api_version: Optional[BankSearchAPIVersion] = None,
    ):
        """Search the branches of a bank by name or by kana reading

        Unlike `get_bank_branches`, an empty result is not an error: as long as
        `q` is given and the bank itself exists, the API responds with a 200
        and an empty set of branches instead of a 404.

        The same normalization as `search_banks` applies to `q`, except that
        the suffix being ignored is `"支店"`. Note that there is no `type`
        here, as the category is already determined by the bank being queried.

        The search parameters were introduced in the 2026-08-01 API version;
        earlier versions ignore them and return every branch, which is why
        `api_version` cannot be an older one.
        """
        req = self.create_bank_branches_search_request(
            bank_code, q=q, match=match, version=version, api_version=api_version
        )
        return self.fetch_bank_branches_result(req, api_version)

    @overload
    def get_bank_branch(
        self, bank_code: str, branch_code: str, api_version: Literal["2023-09-01"] = ...
    ) -> v20230901.BankBranchResolverResponse: ...

    @overload
    def get_bank_branch(
        self, bank_code: str, branch_code: str, api_version: Literal["2024-01-01"] = ...
    ) -> v20240101.BankBranchResolverResponse: ...

    @overload
    def get_bank_branch(
        self, bank_code: str, branch_code: str, api_version: Literal["2025-01-01"] = ...
    ) -> v20250101.BankBranchResolverResponse: ...

    @overload
    def get_bank_branch(
        self, bank_code: str, branch_code: str, api_version: Literal["2026-08-01"] = ...
    ) -> v20260801.BankBranchResolverResponse: ...

    @overload
    def get_bank_branch(
        self, bank_code: str, branch_code: str, api_version: None = None
    ) -> compatible.BankBranchResolverResponse: ...

    def get_bank_branch(
        self, bank_code: str, branch_code: str, api_version: Optional[APIVersion] = None
    ):
        """Get specific branch"""
        req = self.create_bank_branch_request(bank_code, branch_code, api_version)
        return self.fetch_bank_branch_result(req, api_version)

    # Backward compatibility methods for existing tests
    def create_request(
        self,
        postal_code: str,
        api_version: Optional[APIVersion] = None,
        *,
        version: Optional[str] = None,
    ) -> urllib.request.Request:
        """Create request for postal code lookup"""
        url = urllib.parse.urljoin(
            f"{self.api_url}/v1/postalcode/", normalize_postal_code(postal_code)
        )
        if version is not None:
            url = f"{url}?{urllib.parse.urlencode([('version', version)])}"
        return urllib.request.Request(url, headers=self._build_headers(api_version))

    def create_address_search_request(
        self,
        *,
        q: Optional[str] = None,
        t: Optional[str] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        facet: Optional[str] = None,
        version: Optional[str] = None,
        api_version: Optional[APIVersion] = None,
    ) -> urllib.request.Request:
        """Create request for address search"""
        query_mapping: List[Tuple[str, Optional[str]]] = [
            ("q", q),
            ("t", t),
            ("offset", str(offset) if offset is not None else None),
            ("limit", str(limit) if limit is not None else None),
            ("facet", facet),
            ("version", version),
        ]

        query = urllib.parse.urlencode(
            [(k, v) for k, v in query_mapping if v is not None]
        )
        url = f"{self.api_url}/v1/postalcode/?{query}"
        return urllib.request.Request(url, headers=self._build_headers(api_version))

    def fetch(
        self, req: urllib.request.Request, api_version: Optional[APIVersion] = None
    ):
        """Backward compatibility method for tests"""
        with urllib.request.urlopen(req) as res:
            if not res.headers["Content-Type"].startswith("application/json"):
                raise ValueError("not json response", res.read())
            d = json.load(res)

        return create_address_resolver_response(d, api_version)

    def fetch_address_search_result(
        self, req: urllib.request.Request, api_version: Optional[APIVersion] = None
    ):
        """Fetch address search result with version awareness"""
        with urllib.request.urlopen(req) as res:
            if not res.headers["Content-Type"].startswith("application/json"):
                raise ValueError("not json response", res.read())
            d = json.load(res)

        return create_address_searcher_response(d, api_version)

    def create_houjin_request(
        self, houjinbangou: str, api_version: Optional[APIVersion] = None
    ) -> urllib.request.Request:
        """Backward compatibility method for tests"""
        url = f"{self.api_url}/v1/houjinbangou/{houjinbangou}"
        return urllib.request.Request(url, headers=self._build_headers(api_version))

    def create_houjin_search_request(
        self,
        q: str,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        mode: Optional[str] = None,
        facet_area: Optional[str] = None,
        facet_kind: Optional[str] = None,
        facet_process: Optional[str] = None,
        facet_close_cause: Optional[str] = None,
        api_version: Optional[APIVersion] = None,
    ) -> urllib.request.Request:
        """Create request for houjin search"""
        query_mapping: List[Tuple[str, Optional[str]]] = [
            ("q", q),
            ("offset", str(offset) if offset is not None else None),
            ("limit", str(limit) if limit is not None else None),
            ("mode", mode),
        ]

        # Add facets separately
        if facet_area:
            query_mapping.append(("facet_area", facet_area))
        if facet_kind:
            query_mapping.append(("facet_kind", facet_kind))
        if facet_process:
            query_mapping.append(("facet_process", facet_process))
        if facet_close_cause:
            query_mapping.append(("facet_close_cause", facet_close_cause))

        query = urllib.parse.urlencode(
            [(k, v) for k, v in query_mapping if v is not None]
        )
        url = f"{self.api_url}/v1/houjinbangou?{query}"
        return urllib.request.Request(url, headers=self._build_headers(api_version))

    def fetch_houjin_result(
        self, req: urllib.request.Request, api_version: Optional[APIVersion] = None
    ):
        """Backward compatibility method for tests"""
        with urllib.request.urlopen(req) as res:
            if not res.headers["Content-Type"].startswith("application/json"):
                raise ValueError("not json response", res.read())
            d = json.load(res)

        return create_corporate_info_resolver_response(d, api_version)

    def fetch_search_houjin_result(
        self, req: urllib.request.Request, api_version: Optional[APIVersion] = None
    ):
        """Backward compatibility method for tests"""
        with urllib.request.urlopen(req) as res:
            if not res.headers["Content-Type"].startswith("application/json"):
                raise ValueError("not json response", res.read())
            d = json.load(res)

        return create_corporate_info_searcher_response(d, api_version)

    def create_invoice_issuer_request(
        self, issuer_number: str, api_version: Optional[APIVersion] = None
    ) -> urllib.request.Request:
        """Create request for qualified invoice issuer lookup"""
        url = f"{self.api_url}/v1/invoice/{issuer_number}"
        return urllib.request.Request(url, headers=self._build_headers(api_version))

    def fetch_invoice_issuer_result(
        self, req: urllib.request.Request, api_version: Optional[APIVersion] = None
    ):
        """Fetch invoice issuer result with version awareness"""
        with urllib.request.urlopen(req) as res:
            if not res.headers["Content-Type"].startswith("application/json"):
                raise ValueError("not json response", res.read())
            d = json.load(res)

        return create_invoice_issuer_resolver_response(d, api_version)

    def create_whoami_request(
        self, api_version: Optional[APIVersion] = None
    ) -> urllib.request.Request:
        """Create request for whoami"""
        url = f"{self.api_url}/v1/whoami"
        return urllib.request.Request(url, headers=self._build_headers(api_version))

    def fetch_whoami_result(
        self, req: urllib.request.Request, api_version: Optional[APIVersion] = None
    ) -> WhoamiResponse:
        """Fetch whoami result"""
        with urllib.request.urlopen(req) as res:
            if not res.headers["Content-Type"].startswith("application/json"):
                raise ValueError("not json response", res.read())
            d = json.load(res)
        # Whoami is not versioned
        return WhoamiResponse.fromdict(d)

    def create_business_day_check_request(
        self, date: str, api_version: Optional[APIVersion] = None
    ) -> urllib.request.Request:
        """Create request for business day check"""
        query = urllib.parse.urlencode([("date", date)])
        url = f"{self.api_url}/v1/businessdays/check?{query}"
        return urllib.request.Request(url, headers=self._build_headers(api_version))

    def fetch_business_day_check_result(
        self, req: urllib.request.Request, api_version: Optional[APIVersion] = None
    ) -> BusinessDayCheckResponse:
        """Fetch business day check result"""
        with urllib.request.urlopen(req) as res:
            if not res.headers["Content-Type"].startswith("application/json"):
                raise ValueError("not json response", res.read())
            d = json.load(res)
        # The business day check is not versioned
        return BusinessDayCheckResponse.fromdict(d)

    def fetch_search_holiday_result(
        self, req: urllib.request.Request, api_version: Optional[APIVersion] = None
    ):
        """Backward compatibility method for tests"""
        with urllib.request.urlopen(req) as res:
            if not res.headers["Content-Type"].startswith("application/json"):
                raise ValueError("not json response", res.read())
            d = json.load(res)
        # Holiday model is the same across all versions
        from kenallclient.models.compatible import HolidaySearchResult

        return HolidaySearchResult.fromdict(d)

    def create_holiday_search_request(
        self,
        year: Optional[int] = None,
        from_date: Optional[str] = None,
        to_date: Optional[str] = None,
        api_version: Optional[APIVersion] = None,
    ) -> urllib.request.Request:
        """Create request for holiday search"""
        query_mapping: List[Tuple[str, Optional[str]]] = [
            ("year", str(year) if year is not None else None),
            ("from", from_date),
            ("to", to_date),
        ]

        query = urllib.parse.urlencode(
            [(k, v) for k, v in query_mapping if v is not None]
        )
        url = f"{self.api_url}/v1/holidays?{query}"
        return urllib.request.Request(url, headers=self._build_headers(api_version))

    def create_city_request(
        self,
        city_code: str,
        api_version: Optional[APIVersion] = None,
        *,
        version: Optional[str] = None,
    ) -> urllib.request.Request:
        """Create request for city lookup"""
        url = f"{self.api_url}/v1/cities/{city_code}"
        if version is not None:
            url = f"{url}?{urllib.parse.urlencode([('version', version)])}"
        return urllib.request.Request(url, headers=self._build_headers(api_version))

    def fetch_city_result(
        self, req: urllib.request.Request, api_version: Optional[APIVersion] = None
    ):
        """Fetch city result with version awareness"""
        with urllib.request.urlopen(req) as res:
            if not res.headers["Content-Type"].startswith("application/json"):
                raise ValueError("not json response", res.read())
            d = json.load(res)

        return create_city_resolver_response(d, api_version)

    # Bank API helper methods
    def create_banks_request(
        self, api_version: Optional[APIVersion] = None
    ) -> urllib.request.Request:
        """Create request for getting all banks"""
        url = f"{self.api_url}/v1/bank"
        return urllib.request.Request(url, headers=self._build_headers(api_version))

    def fetch_banks_result(
        self, req: urllib.request.Request, api_version: Optional[APIVersion] = None
    ):
        """Fetch banks result with version awareness"""
        with urllib.request.urlopen(req) as res:
            if not res.headers["Content-Type"].startswith("application/json"):
                raise ValueError("not json response", res.read())
            d = json.load(res)

        return create_banks_response(d, api_version)

    def create_bank_search_request(
        self,
        *,
        q: Optional[str] = None,
        match: Optional[BankSearchMatchMode] = None,
        type: Optional[BankType] = None,
        version: Optional[str] = None,
        api_version: Optional[BankSearchAPIVersion] = None,
    ) -> urllib.request.Request:
        """Create request for bank search"""
        query_mapping: List[Tuple[str, Optional[str]]] = [
            ("q", q),
            ("match", match),
            ("type", type),
            ("version", version),
        ]

        query = urllib.parse.urlencode(
            [(k, v) for k, v in query_mapping if v is not None]
        )
        url = f"{self.api_url}/v1/bank"
        if query:
            url = f"{url}?{query}"
        return urllib.request.Request(url, headers=self._build_headers(api_version))

    def create_bank_request(
        self, bank_code: str, api_version: Optional[APIVersion] = None
    ) -> urllib.request.Request:
        """Create request for getting specific bank"""
        url = f"{self.api_url}/v1/bank/{bank_code}"
        return urllib.request.Request(url, headers=self._build_headers(api_version))

    def fetch_bank_result(
        self, req: urllib.request.Request, api_version: Optional[APIVersion] = None
    ):
        """Fetch bank result with version awareness"""
        with urllib.request.urlopen(req) as res:
            if not res.headers["Content-Type"].startswith("application/json"):
                raise ValueError("not json response", res.read())
            d = json.load(res)

        return create_bank_resolver_response(d, api_version)

    def create_bank_branches_request(
        self, bank_code: str, api_version: Optional[APIVersion] = None
    ) -> urllib.request.Request:
        """Create request for getting bank branches"""
        url = f"{self.api_url}/v1/bank/{bank_code}/branches"
        return urllib.request.Request(url, headers=self._build_headers(api_version))

    def create_bank_branches_search_request(
        self,
        bank_code: str,
        *,
        q: Optional[str] = None,
        match: Optional[BankSearchMatchMode] = None,
        version: Optional[str] = None,
        api_version: Optional[BankSearchAPIVersion] = None,
    ) -> urllib.request.Request:
        """Create request for bank branch search"""
        query_mapping: List[Tuple[str, Optional[str]]] = [
            ("q", q),
            ("match", match),
            ("version", version),
        ]

        query = urllib.parse.urlencode(
            [(k, v) for k, v in query_mapping if v is not None]
        )
        url = f"{self.api_url}/v1/bank/{bank_code}/branches"
        if query:
            url = f"{url}?{query}"
        return urllib.request.Request(url, headers=self._build_headers(api_version))

    def fetch_bank_branches_result(
        self, req: urllib.request.Request, api_version: Optional[APIVersion] = None
    ):
        """Fetch bank branches result with version awareness"""
        with urllib.request.urlopen(req) as res:
            if not res.headers["Content-Type"].startswith("application/json"):
                raise ValueError("not json response", res.read())
            d = json.load(res)

        return create_bank_branches_response(d, api_version)

    def create_bank_branch_request(
        self, bank_code: str, branch_code: str, api_version: Optional[APIVersion] = None
    ) -> urllib.request.Request:
        """Create request for getting specific bank branch"""
        url = f"{self.api_url}/v1/bank/{bank_code}/branches/{branch_code}"
        return urllib.request.Request(url, headers=self._build_headers(api_version))

    def fetch_bank_branch_result(
        self, req: urllib.request.Request, api_version: Optional[APIVersion] = None
    ):
        """Fetch bank branch result with version awareness"""
        with urllib.request.urlopen(req) as res:
            if not res.headers["Content-Type"].startswith("application/json"):
                raise ValueError("not json response", res.read())
            d = json.load(res)

        return create_bank_branch_resolver_response(d, api_version)

    # School APIs (available from 2025-01-01)
    @overload
    def get_school(
        self, school_code: str, api_version: Literal["2025-01-01"] = ...
    ) -> v20250101.SchoolResolverResponse: ...

    @overload
    def get_school(
        self, school_code: str, api_version: Literal["2026-08-01"] = ...
    ) -> v20260801.SchoolResolverResponse: ...

    @overload
    def get_school(
        self, school_code: str, api_version: None = None
    ) -> v20250101.SchoolResolverResponse: ...

    def get_school(self, school_code: str, api_version: Optional[APIVersion] = None):
        """Get school information by school code"""
        req = self.create_school_request(school_code, api_version)
        return self.fetch_school_result(req, api_version)

    @overload
    def search_school(
        self,
        q: str,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        facet_area: Optional[str] = None,
        facet_prefecture: Optional[str] = None,
        facet_type: Optional[str] = None,
        facet_establishment_type: Optional[str] = None,
        facet_branch: Optional[str] = None,
        api_version: Literal["2025-01-01"] = ...,
    ) -> v20250101.SchoolSearcherResponse: ...

    @overload
    def search_school(
        self,
        q: str,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        facet_area: Optional[str] = None,
        facet_prefecture: Optional[str] = None,
        facet_type: Optional[str] = None,
        facet_establishment_type: Optional[str] = None,
        facet_branch: Optional[str] = None,
        api_version: Literal["2026-08-01"] = ...,
    ) -> v20260801.SchoolSearcherResponse: ...

    @overload
    def search_school(
        self,
        q: str,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        facet_area: Optional[str] = None,
        facet_prefecture: Optional[str] = None,
        facet_type: Optional[str] = None,
        facet_establishment_type: Optional[str] = None,
        facet_branch: Optional[str] = None,
        api_version: None = None,
    ) -> v20250101.SchoolSearcherResponse: ...

    def search_school(
        self,
        q: str,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        facet_area: Optional[str] = None,
        facet_prefecture: Optional[str] = None,
        facet_type: Optional[str] = None,
        facet_establishment_type: Optional[str] = None,
        facet_branch: Optional[str] = None,
        api_version: Optional[APIVersion] = None,
    ):
        """Search school information"""
        req = self.create_school_search_request(
            q=q,
            offset=offset,
            limit=limit,
            facet_area=facet_area,
            facet_prefecture=facet_prefecture,
            facet_type=facet_type,
            facet_establishment_type=facet_establishment_type,
            facet_branch=facet_branch,
            api_version=api_version,
        )
        return self.fetch_school_search_result(req, api_version)

    # School API helper methods
    def create_school_request(
        self, school_code: str, api_version: Optional[APIVersion] = None
    ) -> urllib.request.Request:
        """Create request for school lookup"""
        url = f"{self.api_url}/v1/school/{school_code}"
        return urllib.request.Request(url, headers=self._build_headers(api_version))

    def fetch_school_result(
        self, req: urllib.request.Request, api_version: Optional[APIVersion] = None
    ):
        """Fetch school result with version awareness"""
        with urllib.request.urlopen(req) as res:
            if not res.headers["Content-Type"].startswith("application/json"):
                raise ValueError("not json response", res.read())
            d = json.load(res)

        return create_school_resolver_response(d, api_version)

    def create_school_search_request(
        self,
        q: str,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
        facet_area: Optional[str] = None,
        facet_prefecture: Optional[str] = None,
        facet_type: Optional[str] = None,
        facet_establishment_type: Optional[str] = None,
        facet_branch: Optional[str] = None,
        api_version: Optional[APIVersion] = None,
    ) -> urllib.request.Request:
        """Create request for school search"""
        query_mapping: List[Tuple[str, Optional[str]]] = [
            ("q", q),
            ("offset", str(offset) if offset is not None else None),
            ("limit", str(limit) if limit is not None else None),
        ]

        # Add facets separately
        if facet_area:
            query_mapping.append(("facet_area", facet_area))
        if facet_prefecture:
            query_mapping.append(("facet_prefecture", facet_prefecture))
        if facet_type:
            query_mapping.append(("facet_type", facet_type))
        if facet_establishment_type:
            query_mapping.append(("facet_establishment_type", facet_establishment_type))
        if facet_branch:
            query_mapping.append(("facet_branch", facet_branch))

        query = urllib.parse.urlencode(
            [(k, v) for k, v in query_mapping if v is not None]
        )
        url = f"{self.api_url}/v1/school/?{query}"
        return urllib.request.Request(url, headers=self._build_headers(api_version))

    def fetch_school_search_result(
        self, req: urllib.request.Request, api_version: Optional[APIVersion] = None
    ):
        """Fetch school search result with version awareness"""
        with urllib.request.urlopen(req) as res:
            if not res.headers["Content-Type"].startswith("application/json"):
                raise ValueError("not json response", res.read())
            d = json.load(res)

        return create_school_searcher_response(d, api_version)
