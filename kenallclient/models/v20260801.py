"""Models for API version 2026-08-01

The 2026-08-01 API version leaves every response payload identical to
2025-01-01; what it adds is the ability to narrow the bank APIs down with a set
of query parameters.  The models are therefore re-exported as-is, and only the
request-side types are declared, in :mod:`kenallclient.types`.
"""

from .v20250101 import (
    Address,
    AddressResolverResponse,
    AddressSearcherResponse,
    Bank,
    BankBranch,
    BankBranchData,
    BankBranchesData,
    BankBranchesResponse,
    BankBranchResolverResponse,
    BankResolverResponse,
    BanksResponse,
    City,
    CityResolverResponse,
    Corporation,
    NTACorporateInfo,
    NTACorporateInfoFacetResults,
    NTACorporateInfoResolverResponse,
    NTACorporateInfoSearcherResponse,
    NTAEntityAddress,
    NTAQualifiedInvoiceIssuerInfo,
    NTAQualifiedInvoiceIssuerInfoResolverResponse,
    School,
    SchoolFacetResults,
    SchoolResolverResponse,
    SchoolSearcherResponse,
)

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
    "School",
    "SchoolResolverResponse",
    "SchoolSearcherResponse",
    "SchoolFacetResults",
]
