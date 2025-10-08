"""Factory functions for creating version-specific model instances from JSON payloads"""

from typing import Any, Dict, Optional, Union

from kenallclient.types import APIVersion

from . import (
    compatible,
    v20220901,
    v20221101,
    v20230901,
    v20240101,
    v20250101,
)


def create_address_resolver_response(
    data: Dict[str, Any], api_version: Optional[APIVersion] = None
) -> Union[
    v20220901.AddressResolverResponse,
    v20221101.AddressResolverResponse,
    v20230901.AddressResolverResponse,
    v20240101.AddressResolverResponse,
    v20250101.AddressResolverResponse,
    compatible.AddressResolverResponse,
]:
    """Create an AddressResolverResponse instance for the specified API version"""
    if api_version == "2022-09-01":
        return v20220901.AddressResolverResponse.fromdict(data)
    elif api_version == "2022-11-01":
        return v20221101.AddressResolverResponse.fromdict(data)
    elif api_version == "2023-09-01":
        return v20230901.AddressResolverResponse.fromdict(data)
    elif api_version == "2024-01-01":
        return v20240101.AddressResolverResponse.fromdict(data)
    elif api_version == "2025-01-01":
        return v20250101.AddressResolverResponse.fromdict(data)
    else:
        return compatible.AddressResolverResponse.fromdict(data)


def create_address_searcher_response(
    data: Dict[str, Any], api_version: Optional[APIVersion] = None
) -> Union[
    v20220901.AddressSearcherResponse,
    v20221101.AddressSearcherResponse,
    v20230901.AddressSearcherResponse,
    v20240101.AddressSearcherResponse,
    v20250101.AddressSearcherResponse,
    compatible.AddressSearcherResponse,
]:
    """Create an AddressSearcherResponse instance for the specified API version"""
    if api_version == "2022-09-01":
        return v20220901.AddressSearcherResponse.fromdict(data)
    elif api_version == "2022-11-01":
        return v20221101.AddressSearcherResponse.fromdict(data)
    elif api_version == "2023-09-01":
        return v20230901.AddressSearcherResponse.fromdict(data)
    elif api_version == "2024-01-01":
        return v20240101.AddressSearcherResponse.fromdict(data)
    elif api_version == "2025-01-01":
        return v20250101.AddressSearcherResponse.fromdict(data)
    else:
        return compatible.AddressSearcherResponse.fromdict(data)


def create_city_resolver_response(
    data: Dict[str, Any], api_version: Optional[APIVersion] = None
) -> Union[
    v20220901.CityResolverResponse,
    v20221101.CityResolverResponse,
    v20230901.CityResolverResponse,
    v20240101.CityResolverResponse,
    v20250101.CityResolverResponse,
    compatible.CityResolverResponse,
]:
    """Create a CityResolverResponse instance for the specified API version"""
    if api_version == "2022-09-01":
        return v20220901.CityResolverResponse.fromdict(data)
    elif api_version == "2022-11-01":
        return v20221101.CityResolverResponse.fromdict(data)
    elif api_version == "2023-09-01":
        return v20230901.CityResolverResponse.fromdict(data)
    elif api_version == "2024-01-01":
        return v20240101.CityResolverResponse.fromdict(data)
    elif api_version == "2025-01-01":
        return v20250101.CityResolverResponse.fromdict(data)
    else:
        return compatible.CityResolverResponse.fromdict(data)


def create_corporate_info_resolver_response(
    data: Dict[str, Any], api_version: Optional[APIVersion] = None
) -> Union[
    v20220901.NTACorporateInfoResolverResponse,
    v20221101.NTACorporateInfoResolverResponse,
    v20230901.NTACorporateInfoResolverResponse,
    v20240101.NTACorporateInfoResolverResponse,
    v20250101.NTACorporateInfoResolverResponse,
    compatible.NTACorporateInfoResolverResponse,
]:
    """Create a NTACorporateInfoResolverResponse for the specified API version"""
    if api_version == "2022-09-01":
        return v20220901.NTACorporateInfoResolverResponse.fromdict(data)
    elif api_version == "2022-11-01":
        return v20221101.NTACorporateInfoResolverResponse.fromdict(data)
    elif api_version == "2023-09-01":
        return v20230901.NTACorporateInfoResolverResponse.fromdict(data)
    elif api_version == "2024-01-01":
        return v20240101.NTACorporateInfoResolverResponse.fromdict(data)
    elif api_version == "2025-01-01":
        return v20250101.NTACorporateInfoResolverResponse.fromdict(data)
    else:
        # Compatible mode: always convert to string close_cause
        return compatible.NTACorporateInfoResolverResponse.fromdict(data)


def create_corporate_info_searcher_response(
    data: Dict[str, Any], api_version: Optional[APIVersion] = None
) -> Union[
    v20220901.NTACorporateInfoSearcherResponse,
    v20221101.NTACorporateInfoSearcherResponse,
    v20230901.NTACorporateInfoSearcherResponse,
    v20240101.NTACorporateInfoSearcherResponse,
    v20250101.NTACorporateInfoSearcherResponse,
    compatible.NTACorporateInfoSearcherResponse,
]:
    """Create a NTACorporateInfoSearcherResponse for the specified API version"""
    if api_version == "2022-09-01":
        return v20220901.NTACorporateInfoSearcherResponse.fromdict(data)
    elif api_version == "2022-11-01":
        return v20221101.NTACorporateInfoSearcherResponse.fromdict(data)
    elif api_version == "2023-09-01":
        return v20230901.NTACorporateInfoSearcherResponse.fromdict(data)
    elif api_version == "2024-01-01":
        return v20240101.NTACorporateInfoSearcherResponse.fromdict(data)
    elif api_version == "2025-01-01":
        return v20250101.NTACorporateInfoSearcherResponse.fromdict(data)
    else:
        # Compatible mode: no conversion needed for search results
        return compatible.NTACorporateInfoSearcherResponse.fromdict(data)


def create_banks_response(
    data: Dict[str, Any], api_version: Optional[APIVersion] = None
) -> Union[
    v20230901.BanksResponse,
    v20240101.BanksResponse,
    v20250101.BanksResponse,
    compatible.BanksResponse,
]:
    """Create a BanksResponse instance for the specified API version"""
    # Bank API only available from 2023-09-01
    if api_version in ["2023-09-01", "2024-01-01", "2025-01-01", None]:
        return compatible.BanksResponse.fromdict(data)
    else:
        raise ValueError(f"Bank API not available for version {api_version}")


def create_bank_resolver_response(
    data: Dict[str, Any], api_version: Optional[APIVersion] = None
) -> Union[
    v20230901.BankResolverResponse,
    v20240101.BankResolverResponse,
    v20250101.BankResolverResponse,
    compatible.BankResolverResponse,
]:
    """Create a BankResolverResponse instance for the specified API version"""
    # Bank API only available from 2023-09-01
    if api_version in ["2023-09-01", "2024-01-01", "2025-01-01", None]:
        return compatible.BankResolverResponse.fromdict(data)
    else:
        raise ValueError(f"Bank API not available for version {api_version}")


def create_bank_branches_response(
    data: Dict[str, Any], api_version: Optional[APIVersion] = None
) -> Union[
    v20230901.BankBranchesResponse,
    v20240101.BankBranchesResponse,
    v20250101.BankBranchesResponse,
    compatible.BankBranchesResponse,
]:
    """Create a BankBranchesResponse instance for the specified API version"""
    # Bank API only available from 2023-09-01
    if api_version in ["2023-09-01", "2024-01-01", "2025-01-01", None]:
        return compatible.BankBranchesResponse.fromdict(data, api_version=api_version)
    else:
        raise ValueError(f"Bank API not available for version {api_version}")


def create_bank_branch_resolver_response(
    data: Dict[str, Any], api_version: Optional[APIVersion] = None
) -> Union[
    v20230901.BankBranchResolverResponse,
    v20240101.BankBranchResolverResponse,
    v20250101.BankBranchResolverResponse,
    compatible.BankBranchResolverResponse,
]:
    """Create a BankBranchResolverResponse for the specified API version"""
    # Bank API only available from 2023-09-01
    if api_version in ["2023-09-01", "2024-01-01", "2025-01-01", None]:
        return compatible.BankBranchResolverResponse.fromdict(
            data, api_version=api_version
        )
    else:
        raise ValueError(f"Bank API not available for version {api_version}")


def create_invoice_issuer_resolver_response(
    data: Dict[str, Any], api_version: Optional[APIVersion] = None
) -> Union[
    v20240101.NTAQualifiedInvoiceIssuerInfoResolverResponse,
    v20250101.NTAQualifiedInvoiceIssuerInfoResolverResponse,
    compatible.NTAQualifiedInvoiceIssuerInfoResolverResponse,
]:
    """Create a NTAQualifiedInvoiceIssuerInfoResolverResponse for the version"""
    # Invoice API only available from 2024-01-01
    if api_version in ["2024-01-01", "2025-01-01", None]:
        return compatible.NTAQualifiedInvoiceIssuerInfoResolverResponse.fromdict(data)
    else:
        raise ValueError(f"Invoice API not available for version {api_version}")


def create_school_resolver_response(
    data: Dict[str, Any], api_version: Optional[APIVersion] = None
) -> v20250101.SchoolResolverResponse:
    """Create a SchoolResolverResponse for the specified API version"""
    # School API only available from 2025-01-01
    if api_version in ["2025-01-01", None]:
        return v20250101.SchoolResolverResponse.fromdict(data)
    else:
        raise ValueError(f"School API not available for version {api_version}")


def create_school_searcher_response(
    data: Dict[str, Any], api_version: Optional[APIVersion] = None
) -> v20250101.SchoolSearcherResponse:
    """Create a SchoolSearcherResponse for the specified API version"""
    # School API only available from 2025-01-01
    if api_version in ["2025-01-01", None]:
        return v20250101.SchoolSearcherResponse.fromdict(data)
    else:
        raise ValueError(f"School API not available for version {api_version}")
