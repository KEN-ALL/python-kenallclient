"""Type definitions for the KenAll client"""

from typing import Literal

APIVersion = Literal[
    "2022-11-01", "2023-09-01", "2024-01-01", "2025-01-01", "2026-08-01"
]

# The API versions in which the bank APIs honor the search parameters
# (``q``, ``match`` and ``type``). Older versions silently ignore them and keep
# returning the whole set, so ``search_banks`` and ``search_bank_branches``
# only accept the versions listed here.
BankSearchAPIVersion = Literal["2026-08-01"]

# How the search text is matched against the names and the kana readings of
# the records. ``prefix`` matches from the beginning and is the default;
# ``contains`` matches anywhere.
BankSearchMatchMode = Literal["prefix", "contains"]

# A category of the financial institutions, derived from the number ranges of
# the Zengin institution code system.
BankType = Literal[
    # Banks (0001-0999).
    "bank",
    # Shinkin banks (1000-1999), including Shinkin Central Bank.
    "shinkin",
    # Credit cooperatives and labour banks (2000-2999), including
    # Shoko Chukin Bank and Zenshinkumiren.
    "shinkumi_rokin",
    # Agricultural and fishery cooperatives (3000-9899), including
    # Norinchukin Bank and the prefectural credit federations.
    "nokyo_gyokyo",
    # Japan Post Bank (9900-9999).
    "yucho",
]
