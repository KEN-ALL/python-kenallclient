import os

import pytest

here = os.path.dirname(__file__)


# Version-specific fixture loaders
@pytest.fixture
def load_version_fixture():
    """Factory to load version-specific fixtures"""

    def _load(version, fixture_name):
        fixture_path = os.path.join(here, "fixtures", version, fixture_name)
        import json

        with open(fixture_path) as f:
            return json.load(f)

    return _load


# Default versions for backward compatibility
# These map old fixtures to specific API versions
DEFAULT_POSTALCODE_VERSION = "2022-11-01"
DEFAULT_HOUJINBANGOU_VERSION = "2024-01-01"
DEFAULT_BANK_VERSION = "2023-09-01"


@pytest.fixture
def dummy_houjinbangou_search_json():
    import json

    # Use v2022-09-01 fixture with proper format
    with open(
        os.path.join(
            here, "fixtures", DEFAULT_HOUJINBANGOU_VERSION, "houjinbangou_search.json"
        )
    ) as f:
        return json.load(f)


@pytest.fixture
def dummy_holiday_search_json():
    import json

    # Use common fixture (same across all versions)
    with open(os.path.join(here, "fixtures/common/holiday_search.json")) as f:
        return json.load(f)


@pytest.fixture
def dummy_banks_json():
    import json

    # Use v2023-09-01 fixture
    with open(os.path.join(here, "fixtures/2023-09-01/banks_get.json")) as f:
        return json.load(f)


@pytest.fixture
def dummy_bank_json():
    import json

    # Use v2023-09-01 fixture
    with open(os.path.join(here, "fixtures/2023-09-01/bank_get.json")) as f:
        return json.load(f)


@pytest.fixture
def dummy_bank_branches_json():
    import json

    # Use v2023-09-01 fixture
    with open(os.path.join(here, "fixtures/2023-09-01/bank_branches_get.json")) as f:
        return json.load(f)


@pytest.fixture
def dummy_bank_branch_json():
    import json

    # Use v2023-09-01 fixture
    with open(os.path.join(here, "fixtures/2023-09-01/bank_branch_get.json")) as f:
        return json.load(f)


# Version-specific fixtures
@pytest.fixture
def postalcode_v20221101(load_version_fixture):
    return load_version_fixture("2022-11-01", "postalcode_get.json")


@pytest.fixture
def postalcode_search_v20221101(load_version_fixture):
    return load_version_fixture("2022-11-01", "postalcode_search.json")


@pytest.fixture
def city_v20221101(load_version_fixture):
    return load_version_fixture("2022-11-01", "city_get.json")


@pytest.fixture
def houjinbangou_v20240101(load_version_fixture):
    return load_version_fixture("2024-01-01", "houjinbangou.json")


@pytest.fixture
def houjinbangou_v20250101(load_version_fixture):
    return load_version_fixture("2025-01-01", "houjinbangou.json")


@pytest.fixture
def banks_v20230901(load_version_fixture):
    return load_version_fixture("2023-09-01", "banks_get.json")


@pytest.fixture
def bank_v20230901(load_version_fixture):
    return load_version_fixture("2023-09-01", "bank_get.json")


@pytest.fixture
def bank_branches_v20230901(load_version_fixture):
    return load_version_fixture("2023-09-01", "bank_branches_get.json")


@pytest.fixture
def bank_branch_v20230901(load_version_fixture):
    return load_version_fixture("2023-09-01", "bank_branch_get.json")


@pytest.fixture
def invoice_issuer_v20240101(load_version_fixture):
    return load_version_fixture("2024-01-01", "invoice_issuer_get.json")


# Corporate info search fixtures


@pytest.fixture
def houjinbangou_search_v20230901(load_version_fixture):
    return load_version_fixture("2023-09-01", "houjinbangou_search.json")


@pytest.fixture
def houjinbangou_search_v20240101(load_version_fixture):
    return load_version_fixture("2024-01-01", "houjinbangou_search.json")


@pytest.fixture
def houjinbangou_search_v20250101(load_version_fixture):
    return load_version_fixture("2025-01-01", "houjinbangou_search.json")


@pytest.fixture
def school_v20250101(load_version_fixture):
    return load_version_fixture("2025-01-01", "school_get.json")


@pytest.fixture
def school_search_v20250101(load_version_fixture):
    return load_version_fixture("2025-01-01", "school_search.json")
