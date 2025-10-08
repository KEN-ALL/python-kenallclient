"""Backward compatibility module for the old model API"""

# Import all models from compatible module for true backward compatibility
from kenallclient.models.compatible import (
    Address as KenAllResultItem,  # Old name mapping
)
from kenallclient.models.compatible import (
    AddressResolverResponse as KenAllResult,
)
from kenallclient.models.compatible import (
    AddressSearcherResponse as KenAllSearchResult,
)
from kenallclient.models.compatible import (
    Bank,
    BankBranch,
    City,
    CityResolverResponse,
    Holiday,
    HolidaySearchResult,
)
from kenallclient.models.compatible import (
    BankBranchesResponse as BankBranchesResult,
)
from kenallclient.models.compatible import (
    BankBranchResolverResponse as BankBranchResult,
)
from kenallclient.models.compatible import (
    BankResolverResponse as BankResult,
)
from kenallclient.models.compatible import (
    BanksResponse as BanksResult,
)
from kenallclient.models.compatible import (
    Corporation as KenAllCorporation,
)
from kenallclient.models.compatible import (
    NTACorporateInfo as HoujinResultItem,
)
from kenallclient.models.compatible import (
    NTACorporateInfoResolverResponse as HoujinResult,
)
from kenallclient.models.compatible import (
    NTACorporateInfoSearcherResponse as HoujinSearchResult,
)

# The compatible models handle all version differences transparently

# For backward compatibility, also expose the original constants
HOUJIN_KIND = {
    101: "国の機関",
    201: "地方公共団体",
    301: "株式会社",
    302: "有限会社",
    303: "合名会社",
    304: "合資会社",
    305: "合同会社",
    399: "その他の設立登記法人",
    401: "外国会社等",
    499: "その他",
}

HOUJIN_HIHYOJI = {
    0: "検索対象",
    1: "検索対象から除外",
}

HOUJIN_CLOSE_CAUSE = {
    "01": "精算の結了等",
    "11": "合併による解散等",
    "21": "登記官による閉鎖",
    "31": "その他の精算の結了等",
}

CORPORATION_CODE_TYPE = {
    0: "大口事業所",
    1: "私書箱",
}

__all__ = [
    "KenAllResultItem",
    "KenAllResult",
    "KenAllSearchResult",
    "KenAllCorporation",
    "HoujinResultItem",
    "HoujinResult",
    "HoujinSearchResult",
    "Holiday",
    "HolidaySearchResult",
    "Bank",
    "BankBranch",
    "BanksResult",
    "BankResult",
    "BankBranchesResult",
    "BankBranchResult",
    "City",
    "CityResolverResponse",
    "HOUJIN_KIND",
    "HOUJIN_HIHYOJI",
    "HOUJIN_CLOSE_CAUSE",
    "CORPORATION_CODE_TYPE",
]
