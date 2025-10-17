import io

import pytest


class DummyResponse(io.StringIO):
    headers: dict = {}


# API version availability constants
ALL_VERSIONS = ["2022-11-01", "2023-09-01", "2024-01-01", "2025-01-01"]
POSTAL_VERSIONS = ["2022-11-01", "2023-09-01", "2024-01-01", "2025-01-01"]
CORPORATE_VERSIONS = ["2024-01-01", "2025-01-01"]
BANK_VERSIONS = ["2023-09-01", "2024-01-01", "2025-01-01"]
INVOICE_VERSIONS = ["2024-01-01", "2025-01-01"]
SCHOOL_VERSIONS = ["2025-01-01"]


def test_it():
    pass


@pytest.mark.parametrize(
    "api_url,expected",
    [
        pytest.param(None, "https://api.kenall.jp"),
        pytest.param("https://kenall.example.com", "https://kenall.example.com"),
    ],
)
def test_api_url(api_url, expected):
    from kenallclient.client import KenAllClient

    target = KenAllClient("testing-api-key", api_url=api_url)
    assert target.api_url == expected


def test_create_request():
    from kenallclient.client import KenAllClient

    target = KenAllClient("testing-api-key")
    result = target.create_request("9999999")
    assert result.full_url == "https://api.kenall.jp/v1/postalcode/9999999"
    assert result.headers == {"Authorization": "Token testing-api-key"}


def test_create_houjin_request():
    from kenallclient.client import KenAllClient

    target = KenAllClient("testing-api-key")
    result = target.create_houjin_request("1234323")
    assert result.full_url == "https://api.kenall.jp/v1/houjinbangou/1234323"
    assert result.headers == {"Authorization": "Token testing-api-key"}


def test_fetch(mocker, postalcode_v20221101):
    import json

    from kenallclient.client import KenAllClient

    dummy_response = DummyResponse(json.dumps(postalcode_v20221101))
    dummy_response.headers = {"Content-Type": "application/json"}
    mock_urlopen = mocker.patch("kenallclient.client.urllib.request.urlopen")
    mock_urlopen.return_value = dummy_response

    request = mocker.Mock()
    target = KenAllClient("testing-api-key")
    result = target.fetch(request)
    mock_urlopen.assert_called_with(request)
    assert result


def test_fetch_unexpected_content_type(mocker, postalcode_v20221101):
    import json

    from kenallclient.client import KenAllClient

    dummy_response = DummyResponse(json.dumps(postalcode_v20221101))
    dummy_response.headers = {"Content-Type": "plain/text"}
    request_body = dummy_response.getvalue()
    mock_urlopen = mocker.patch("kenallclient.client.urllib.request.urlopen")
    mock_urlopen.return_value = dummy_response

    request = mocker.Mock()
    target = KenAllClient("testing-api-key")
    with pytest.raises(ValueError) as e:
        target.fetch(request)
    assert e.value.args == ("not json response", request_body)


def test_fetch_houjin(mocker, houjinbangou_v20240101):
    import json

    from kenallclient.client import KenAllClient

    dummy_response = DummyResponse(json.dumps(houjinbangou_v20240101))
    dummy_response.headers = {"Content-Type": "application/json"}
    mock_urlopen = mocker.patch("kenallclient.client.urllib.request.urlopen")
    mock_urlopen.return_value = dummy_response

    request = mocker.Mock()
    target = KenAllClient("testing-api-key")
    result = target.fetch_houjin_result(request)
    mock_urlopen.assert_called_with(request)
    assert result


def test_fetch_search_houjin_result(mocker, dummy_houjinbangou_search_json):
    import json

    from kenallclient.client import KenAllClient

    dummy_response = DummyResponse(json.dumps(dummy_houjinbangou_search_json))
    dummy_response.headers = {"Content-Type": "application/json"}
    mock_urlopen = mocker.patch("kenallclient.client.urllib.request.urlopen")
    mock_urlopen.return_value = dummy_response

    request = mocker.Mock()
    target = KenAllClient("testing-api-key")
    result = target.fetch_search_houjin_result(request)
    mock_urlopen.assert_called_with(request)
    assert result


def test_fetch_search_holiday_result(mocker, dummy_holiday_search_json):
    import json

    from kenallclient import model
    from kenallclient.client import KenAllClient

    dummy_response = DummyResponse(json.dumps(dummy_holiday_search_json))
    dummy_response.headers = {"Content-Type": "application/json"}
    mock_urlopen = mocker.patch("kenallclient.client.urllib.request.urlopen")
    mock_urlopen.return_value = dummy_response

    request = mocker.Mock()
    target = KenAllClient("testing-api-key")
    result = target.fetch_search_holiday_result(request)
    mock_urlopen.assert_called_with(request)
    assert result == model.HolidaySearchResult(
        data=[
            model.Holiday(
                title="元日",
                date="2022-01-01",
                day_of_week=6,
                day_of_week_text="saturday",
            ),
            model.Holiday(
                title="成人の日",
                date="2022-01-10",
                day_of_week=1,
                day_of_week_text="monday",
            ),
            model.Holiday(
                title="建国記念の日",
                date="2022-02-11",
                day_of_week=5,
                day_of_week_text="friday",
            ),
            model.Holiday(
                title="天皇誕生日",
                date="2022-02-23",
                day_of_week=3,
                day_of_week_text="wednesday",
            ),
            model.Holiday(
                title="春分の日",
                date="2022-03-21",
                day_of_week=1,
                day_of_week_text="monday",
            ),
            model.Holiday(
                title="昭和の日",
                date="2022-04-29",
                day_of_week=5,
                day_of_week_text="friday",
            ),
            model.Holiday(
                title="憲法記念日",
                date="2022-05-03",
                day_of_week=2,
                day_of_week_text="tuesday",
            ),
            model.Holiday(
                title="みどりの日",
                date="2022-05-04",
                day_of_week=3,
                day_of_week_text="wednesday",
            ),
            model.Holiday(
                title="こどもの日",
                date="2022-05-05",
                day_of_week=4,
                day_of_week_text="thursday",
            ),
            model.Holiday(
                title="海の日",
                date="2022-07-18",
                day_of_week=1,
                day_of_week_text="monday",
            ),
            model.Holiday(
                title="山の日",
                date="2022-08-11",
                day_of_week=4,
                day_of_week_text="thursday",
            ),
            model.Holiday(
                title="敬老の日",
                date="2022-09-19",
                day_of_week=1,
                day_of_week_text="monday",
            ),
            model.Holiday(
                title="秋分の日",
                date="2022-09-23",
                day_of_week=5,
                day_of_week_text="friday",
            ),
            model.Holiday(
                title="スポーツの日",
                date="2022-10-10",
                day_of_week=1,
                day_of_week_text="monday",
            ),
            model.Holiday(
                title="文化の日",
                date="2022-11-03",
                day_of_week=4,
                day_of_week_text="thursday",
            ),
            model.Holiday(
                title="勤労感謝の日",
                date="2022-11-23",
                day_of_week=3,
                day_of_week_text="wednesday",
            ),
        ]
    )


def test_get_banks(mocker, dummy_banks_json):
    import json

    from kenallclient.client import KenAllClient
    from kenallclient.models import compatible

    dummy_response = DummyResponse(json.dumps(dummy_banks_json))
    dummy_response.headers = {"Content-Type": "application/json"}
    mock_urlopen = mocker.patch("kenallclient.client.urllib.request.urlopen")
    mock_urlopen.return_value = dummy_response

    target = KenAllClient("testing-api-key")
    result = target.get_banks()

    # Check the request was made correctly
    request = mock_urlopen.call_args[0][0]
    assert request.full_url == "https://api.kenall.jp/v1/bank"
    assert request.headers == {"Authorization": "Token testing-api-key"}

    # Check the response
    assert isinstance(result, compatible.BanksResponse)
    assert result.version == "2023-09-01"
    assert len(result.data) == 3
    assert result.data[0].code == "0001"
    assert result.data[0].name == "みずほ銀行"
    assert result.data[0].katakana == "ミズホ"
    assert result.data[0].hiragana == "みずほ"
    assert result.data[0].romaji == "mizuho"


def test_get_bank(mocker, dummy_bank_json):
    import json

    from kenallclient.client import KenAllClient
    from kenallclient.models import compatible

    dummy_response = DummyResponse(json.dumps(dummy_bank_json))
    dummy_response.headers = {"Content-Type": "application/json"}
    mock_urlopen = mocker.patch("kenallclient.client.urllib.request.urlopen")
    mock_urlopen.return_value = dummy_response

    target = KenAllClient("testing-api-key")
    result = target.get_bank("0001")

    # Check the request was made correctly
    request = mock_urlopen.call_args[0][0]
    assert request.full_url == "https://api.kenall.jp/v1/bank/0001"
    assert request.headers == {"Authorization": "Token testing-api-key"}

    # Check the response
    assert isinstance(result, compatible.BankResolverResponse)
    assert result.version == "2023-09-01"
    assert result.data.code == "0001"
    assert result.data.name == "みずほ銀行"
    assert result.data.katakana == "ミズホ"
    assert result.data.hiragana == "みずほ"
    assert result.data.romaji == "mizuho"


def test_get_bank_branches(mocker, dummy_bank_branches_json):
    import json

    from kenallclient.client import KenAllClient
    from kenallclient.models import compatible

    dummy_response = DummyResponse(json.dumps(dummy_bank_branches_json))
    dummy_response.headers = {"Content-Type": "application/json"}
    mock_urlopen = mocker.patch("kenallclient.client.urllib.request.urlopen")
    mock_urlopen.return_value = dummy_response

    target = KenAllClient("testing-api-key")
    result = target.get_bank_branches("0001")

    # Check the request was made correctly
    request = mock_urlopen.call_args[0][0]
    assert request.full_url == "https://api.kenall.jp/v1/bank/0001/branches"
    assert request.headers == {"Authorization": "Token testing-api-key"}

    # Check the response
    assert isinstance(result, compatible.BankBranchesResponse)
    assert result.version == "2023-09-01"
    assert len(result.data) == 3
    assert "001" in result.data
    assert len(result.data["001"]) > 0
    assert result.data["001"][0].code == "001"
    assert result.data["001"][0].name == "東京営業部"
    assert result.data["001"][0].katakana == "トウキヨウ"
    assert result.data["001"][0].hiragana == "とうきょう"
    assert result.data["001"][0].romaji == "tokyo"


def test_get_bank_branch(mocker, dummy_bank_branch_json):
    import json

    from kenallclient.client import KenAllClient
    from kenallclient.models import compatible

    dummy_response = DummyResponse(json.dumps(dummy_bank_branch_json))
    dummy_response.headers = {"Content-Type": "application/json"}
    mock_urlopen = mocker.patch("kenallclient.client.urllib.request.urlopen")
    mock_urlopen.return_value = dummy_response

    target = KenAllClient("testing-api-key")
    result = target.get_bank_branch("0001", "001")

    # Check the request was made correctly
    request = mock_urlopen.call_args[0][0]
    assert request.full_url == "https://api.kenall.jp/v1/bank/0001/branches/001"
    assert request.headers == {"Authorization": "Token testing-api-key"}

    # Check the response
    assert isinstance(result, compatible.BankBranchResolverResponse)
    assert result.version == "2023-09-01"
    assert result.data[0]
    assert result.data[0].code == "001"
    assert result.data[0].name == "東京営業部"
    assert result.data[0].katakana == "トウキヨウ"
    assert result.data[0].hiragana == "とうきょう"
    assert result.data[0].romaji == "tokyo"


def test_get_banks_with_api_version(mocker, dummy_banks_json):
    import json

    from kenallclient.client import KenAllClient
    from kenallclient.models import v20230901

    dummy_response = DummyResponse(json.dumps(dummy_banks_json))
    dummy_response.headers = {"Content-Type": "application/json"}
    mock_urlopen = mocker.patch("kenallclient.client.urllib.request.urlopen")
    mock_urlopen.return_value = dummy_response

    target = KenAllClient("testing-api-key")
    result = target.get_banks(api_version="2023-09-01")

    # Check the request was made correctly with version header
    request = mock_urlopen.call_args[0][0]
    assert request.full_url == "https://api.kenall.jp/v1/bank"
    assert request.headers["Authorization"] == "Token testing-api-key"
    assert request.headers.get("Kenall-api-version") == "2023-09-01"

    # Check the response is version-specific
    assert isinstance(result, v20230901.BanksResponse)
    assert result.version == "2023-09-01"
    assert len(result.data) == 3


def test_bank_api_with_invalid_version(mocker):
    import json

    from kenallclient.client import KenAllClient

    # Mock the HTTP response to avoid actual network calls
    dummy_response = DummyResponse(json.dumps({"version": "2022-11-01", "data": []}))
    dummy_response.headers = {"Content-Type": "application/json"}
    mock_urlopen = mocker.patch("kenallclient.client.urllib.request.urlopen")
    mock_urlopen.return_value = dummy_response

    target = KenAllClient("testing-api-key")

    # Bank APIs are only available from 2023-09-01
    with pytest.raises(ValueError) as e:
        target.get_banks(api_version="2022-11-01")
    assert "Bank API not available for version 2022-11-01" in str(e.value)


def test_create_bank_request():
    from kenallclient.client import KenAllClient

    target = KenAllClient("testing-api-key")
    result = target.create_bank_request("0001")
    assert result.full_url == "https://api.kenall.jp/v1/bank/0001"
    assert result.headers == {"Authorization": "Token testing-api-key"}


def test_create_bank_request_with_api_version():
    from kenallclient.client import KenAllClient

    target = KenAllClient("testing-api-key")
    result = target.create_bank_request("0001", api_version="2023-09-01")
    assert result.full_url == "https://api.kenall.jp/v1/bank/0001"
    assert result.headers["Authorization"] == "Token testing-api-key"
    assert result.headers.get("Kenall-api-version") == "2023-09-01"


def test_fetch_banks_result(mocker, dummy_banks_json):
    import json

    from kenallclient.client import KenAllClient
    from kenallclient.models import compatible

    dummy_response = DummyResponse(json.dumps(dummy_banks_json))
    dummy_response.headers = {"Content-Type": "application/json"}
    mock_urlopen = mocker.patch("kenallclient.client.urllib.request.urlopen")
    mock_urlopen.return_value = dummy_response

    request = mocker.Mock()
    target = KenAllClient("testing-api-key")
    result = target.fetch_banks_result(request, api_version="2023-09-01")

    mock_urlopen.assert_called_with(request)
    assert isinstance(result, compatible.BanksResponse)
    assert result.version == "2023-09-01"


# ============================================================================
# Version-specific comprehensive tests
# ============================================================================


@pytest.mark.parametrize("api_version", POSTAL_VERSIONS)
def test_postal_code_get_all_versions(mocker, load_version_fixture, api_version):
    """Test postal code GET endpoint across all supported versions"""
    import json

    from kenallclient.client import KenAllClient

    # Load version-specific fixture
    fixture_data = load_version_fixture(api_version, "postalcode_get.json")

    dummy_response = DummyResponse(json.dumps(fixture_data))
    dummy_response.headers = {"Content-Type": "application/json"}
    mock_urlopen = mocker.patch("kenallclient.client.urllib.request.urlopen")
    mock_urlopen.return_value = dummy_response

    target = KenAllClient("testing-api-key")
    result = target.get("1008105", api_version=api_version)

    # Verify request
    request = mock_urlopen.call_args[0][0]
    assert request.full_url == "https://api.kenall.jp/v1/postalcode/1008105"
    assert request.headers["Authorization"] == "Token testing-api-key"
    assert request.headers.get("Kenall-api-version") == api_version

    # Verify response
    # Note: response version might differ from requested version, that's ok
    assert result.version is not None
    assert len(result.data) > 0
    assert result.data[0].postal_code == "1008105"


@pytest.mark.parametrize("api_version", POSTAL_VERSIONS)
def test_postal_code_search_all_versions(mocker, load_version_fixture, api_version):
    """Test postal code search endpoint across all supported versions"""
    import json

    from kenallclient.client import KenAllClient

    # Load version-specific fixture
    fixture_data = load_version_fixture(api_version, "postalcode_search.json")

    dummy_response = DummyResponse(json.dumps(fixture_data))
    dummy_response.headers = {"Content-Type": "application/json"}
    mock_urlopen = mocker.patch("kenallclient.client.urllib.request.urlopen")
    mock_urlopen.return_value = dummy_response

    target = KenAllClient("testing-api-key")
    result = target.search(q="東京都", t=None, api_version=api_version)

    # Verify request
    request = mock_urlopen.call_args[0][0]
    assert "https://api.kenall.jp/v1/postalcode/" in request.full_url
    assert "q=%E6%9D%B1%E4%BA%AC%E9%83%BD" in request.full_url
    assert request.headers["Authorization"] == "Token testing-api-key"
    assert request.headers.get("Kenall-api-version") == api_version

    # Verify response
    # Note: response version might differ from requested version, that's ok
    assert result.version is not None
    assert len(result.data) > 0


@pytest.mark.parametrize("api_version", POSTAL_VERSIONS)
def test_city_get_all_versions(mocker, load_version_fixture, api_version):
    """Test city GET endpoint across all supported versions"""
    import json

    from kenallclient.client import KenAllClient

    # Load version-specific fixture
    fixture_data = load_version_fixture(api_version, "city_get.json")

    dummy_response = DummyResponse(json.dumps(fixture_data))
    dummy_response.headers = {"Content-Type": "application/json"}
    mock_urlopen = mocker.patch("kenallclient.client.urllib.request.urlopen")
    mock_urlopen.return_value = dummy_response

    target = KenAllClient("testing-api-key")
    request = target.create_city_request("13101", api_version=api_version)
    result = target.fetch_city_result(request, api_version=api_version)

    # Verify request
    assert request.full_url == "https://api.kenall.jp/v1/cities/13101"
    assert request.headers["Authorization"] == "Token testing-api-key"
    assert request.headers.get("Kenall-api-version") == api_version

    # Verify response
    # Note: response version might differ from requested version, that's ok
    assert result.version is not None
    assert result.data
    assert result.data[0].jisx0402 is not None  # Verify city code exists


@pytest.mark.parametrize("api_version", CORPORATE_VERSIONS)
def test_corporate_get_all_versions(mocker, load_version_fixture, api_version):
    """Test corporate info GET endpoint across supported versions"""
    import json

    from kenallclient.client import KenAllClient

    # Load version-specific fixture
    fixture_data = load_version_fixture(api_version, "houjinbangou.json")

    dummy_response = DummyResponse(json.dumps(fixture_data))
    dummy_response.headers = {"Content-Type": "application/json"}
    mock_urlopen = mocker.patch("kenallclient.client.urllib.request.urlopen")
    mock_urlopen.return_value = dummy_response

    target = KenAllClient("testing-api-key")
    result = target.get_houjin("1234567890123", api_version=api_version)

    # Verify request
    request = mock_urlopen.call_args[0][0]
    assert request.full_url == "https://api.kenall.jp/v1/houjinbangou/1234567890123"
    assert request.headers["Authorization"] == "Token testing-api-key"
    assert request.headers.get("Kenall-api-version") == api_version

    # Verify response
    # Note: response version might differ from requested version, that's ok
    assert result.version is not None
    assert result.data is not None


@pytest.mark.parametrize("api_version", CORPORATE_VERSIONS)
def test_corporate_search_all_versions(mocker, load_version_fixture, api_version):
    """Test corporate info search endpoint across supported versions"""
    import json

    from kenallclient.client import KenAllClient

    # Load version-specific fixture
    fixture_data = load_version_fixture(api_version, "houjinbangou_search.json")

    dummy_response = DummyResponse(json.dumps(fixture_data))
    dummy_response.headers = {"Content-Type": "application/json"}
    mock_urlopen = mocker.patch("kenallclient.client.urllib.request.urlopen")
    mock_urlopen.return_value = dummy_response

    target = KenAllClient("testing-api-key")
    result = target.search_houjin(q="株式会社", api_version=api_version)

    # Verify request
    request = mock_urlopen.call_args[0][0]
    assert request.full_url.startswith("https://api.kenall.jp/v1/houjinbangou")
    assert request.headers["Authorization"] == "Token testing-api-key"
    assert request.headers.get("Kenall-api-version") == api_version

    # Verify response
    # Note: response version might differ from requested version, that's ok
    assert result.version is not None
    assert len(result.data) > 0


@pytest.mark.parametrize("api_version", BANK_VERSIONS)
def test_banks_get_all_versions(mocker, load_version_fixture, api_version):
    """Test banks GET endpoint across supported versions"""
    import json

    from kenallclient.client import KenAllClient

    # Load version-specific fixture
    fixture_data = load_version_fixture(api_version, "banks_get.json")

    dummy_response = DummyResponse(json.dumps(fixture_data))
    dummy_response.headers = {"Content-Type": "application/json"}
    mock_urlopen = mocker.patch("kenallclient.client.urllib.request.urlopen")
    mock_urlopen.return_value = dummy_response

    target = KenAllClient("testing-api-key")
    result = target.get_banks(api_version=api_version)

    # Verify request
    request = mock_urlopen.call_args[0][0]
    assert request.full_url == "https://api.kenall.jp/v1/bank"
    assert request.headers["Authorization"] == "Token testing-api-key"
    assert request.headers.get("Kenall-api-version") == api_version

    # Verify response
    # Note: response version might differ from requested version, that's ok
    assert result.version is not None
    assert len(result.data) > 0


@pytest.mark.parametrize("api_version", BANK_VERSIONS)
def test_bank_get_all_versions(mocker, load_version_fixture, api_version):
    """Test bank GET endpoint across supported versions"""
    import json

    from kenallclient.client import KenAllClient

    # Load version-specific fixture
    fixture_data = load_version_fixture(api_version, "bank_get.json")

    dummy_response = DummyResponse(json.dumps(fixture_data))
    dummy_response.headers = {"Content-Type": "application/json"}
    mock_urlopen = mocker.patch("kenallclient.client.urllib.request.urlopen")
    mock_urlopen.return_value = dummy_response

    target = KenAllClient("testing-api-key")
    result = target.get_bank("0001", api_version=api_version)

    # Verify request
    request = mock_urlopen.call_args[0][0]
    assert request.full_url == "https://api.kenall.jp/v1/bank/0001"
    assert request.headers["Authorization"] == "Token testing-api-key"
    assert request.headers.get("Kenall-api-version") == api_version

    # Verify response
    # Note: response version might differ from requested version, that's ok
    assert result.version is not None
    assert result.data.code == "0001"


@pytest.mark.parametrize("api_version", BANK_VERSIONS)
def test_bank_branches_get_all_versions(mocker, load_version_fixture, api_version):
    """Test bank branches GET endpoint across supported versions"""
    import json

    from kenallclient.client import KenAllClient

    # Load version-specific fixture
    fixture_data = load_version_fixture(api_version, "bank_branches_get.json")

    dummy_response = DummyResponse(json.dumps(fixture_data))
    dummy_response.headers = {"Content-Type": "application/json"}
    mock_urlopen = mocker.patch("kenallclient.client.urllib.request.urlopen")
    mock_urlopen.return_value = dummy_response

    target = KenAllClient("testing-api-key")
    result = target.get_bank_branches("0001", api_version=api_version)

    # Verify request
    request = mock_urlopen.call_args[0][0]
    assert request.full_url == "https://api.kenall.jp/v1/bank/0001/branches"
    assert request.headers["Authorization"] == "Token testing-api-key"
    assert request.headers.get("Kenall-api-version") == api_version

    # Verify response
    # Note: response version might differ from requested version, that's ok
    assert result.version is not None
    assert len(result.data) > 0


@pytest.mark.parametrize("api_version", BANK_VERSIONS)
def test_bank_branch_get_all_versions(mocker, load_version_fixture, api_version):
    """Test bank branch GET endpoint across supported versions"""
    import json

    from kenallclient.client import KenAllClient

    # Load version-specific fixture
    fixture_data = load_version_fixture(api_version, "bank_branch_get.json")

    dummy_response = DummyResponse(json.dumps(fixture_data))
    dummy_response.headers = {"Content-Type": "application/json"}
    mock_urlopen = mocker.patch("kenallclient.client.urllib.request.urlopen")
    mock_urlopen.return_value = dummy_response

    target = KenAllClient("testing-api-key")
    result = target.get_bank_branch("0001", "001", api_version=api_version)

    # Verify request
    request = mock_urlopen.call_args[0][0]
    assert request.full_url == "https://api.kenall.jp/v1/bank/0001/branches/001"
    assert request.headers["Authorization"] == "Token testing-api-key"
    assert request.headers.get("Kenall-api-version") == api_version

    # Verify response
    assert result.data[0]
    assert result.data[0].code == "001"


# ============================================================================
# Request creation tests with API version
# ============================================================================


@pytest.mark.parametrize("api_version", ALL_VERSIONS)
def test_create_request_with_api_version(api_version):
    """Test request creation includes API version header"""
    from kenallclient.client import KenAllClient

    target = KenAllClient("testing-api-key")
    result = target.create_request("1000000", api_version=api_version)
    assert result.full_url == "https://api.kenall.jp/v1/postalcode/1000000"
    assert result.headers["Authorization"] == "Token testing-api-key"
    assert result.headers.get("Kenall-api-version") == api_version


@pytest.mark.parametrize("api_version", CORPORATE_VERSIONS)
def test_create_houjin_request_with_api_version(api_version):
    """Test houjin request creation includes API version header"""
    from kenallclient.client import KenAllClient

    target = KenAllClient("testing-api-key")
    result = target.create_houjin_request("1234567890123", api_version=api_version)
    assert result.full_url == "https://api.kenall.jp/v1/houjinbangou/1234567890123"
    assert result.headers["Authorization"] == "Token testing-api-key"
    assert result.headers.get("Kenall-api-version") == api_version


@pytest.mark.parametrize("api_version", POSTAL_VERSIONS)
def test_create_address_search_request_with_api_version(api_version):
    """Test address search request creation includes API version header"""
    from kenallclient.client import KenAllClient

    target = KenAllClient("testing-api-key")
    result = target.create_address_search_request(
        q="東京", t=None, offset=0, limit=10, api_version=api_version
    )
    assert "https://api.kenall.jp/v1/postalcode/" in result.full_url
    assert "q=" in result.full_url
    assert result.headers["Authorization"] == "Token testing-api-key"
    assert result.headers.get("Kenall-api-version") == api_version


@pytest.mark.parametrize("api_version", CORPORATE_VERSIONS)
def test_create_houjin_search_request_with_api_version(api_version):
    """Test houjin search request creation includes API version header"""
    from kenallclient.client import KenAllClient

    target = KenAllClient("testing-api-key")
    result = target.create_houjin_search_request(
        q="株式会社", offset=0, limit=10, api_version=api_version
    )
    assert result.full_url.startswith("https://api.kenall.jp/v1/houjinbangou")
    assert "q=" in result.full_url
    assert result.headers["Authorization"] == "Token testing-api-key"
    assert result.headers.get("Kenall-api-version") == api_version


# ============================================================================
# School API tests
# ============================================================================


def test_get_school(mocker, school_v20250101):
    """Test school GET endpoint"""
    import json

    from kenallclient.client import KenAllClient
    from kenallclient.models import v20250101

    dummy_response = DummyResponse(json.dumps(school_v20250101))
    dummy_response.headers = {"Content-Type": "application/json"}
    mock_urlopen = mocker.patch("kenallclient.client.urllib.request.urlopen")
    mock_urlopen.return_value = dummy_response

    target = KenAllClient("testing-api-key")
    result = target.get_school("F113110102700", api_version="2025-01-01")

    # Check the request was made correctly
    request = mock_urlopen.call_args[0][0]
    assert request.full_url == "https://api.kenall.jp/v1/school/F113110102700"
    assert request.headers["Authorization"] == "Token testing-api-key"
    assert request.headers.get("Kenall-api-version") == "2025-01-01"

    # Check the response
    assert isinstance(result, v20250101.SchoolResolverResponse)
    assert result.version == "2025-01-01"
    assert result.data.code == "F113110102700"
    assert result.data.name == "東京大学"
    assert result.data.type == "F1"
    assert result.data.establishment_type == 1
    assert result.data.branch == 1


def test_search_school(mocker, school_search_v20250101):
    """Test school search endpoint"""
    import json

    from kenallclient.client import KenAllClient
    from kenallclient.models import v20250101

    dummy_response = DummyResponse(json.dumps(school_search_v20250101))
    dummy_response.headers = {"Content-Type": "application/json"}
    mock_urlopen = mocker.patch("kenallclient.client.urllib.request.urlopen")
    mock_urlopen.return_value = dummy_response

    target = KenAllClient("testing-api-key")
    result = target.search_school(
        q="東京都 AND type:F1",
        offset=0,
        limit=10,
        facet_type="/大学",
        api_version="2025-01-01",
    )

    # Check the request was made correctly
    request = mock_urlopen.call_args[0][0]
    assert "https://api.kenall.jp/v1/school/" in request.full_url
    assert "q=" in request.full_url
    assert request.headers["Authorization"] == "Token testing-api-key"
    assert request.headers.get("Kenall-api-version") == "2025-01-01"

    # Check the response
    assert isinstance(result, v20250101.SchoolSearcherResponse)
    assert result.version == "2025-01-01"
    assert result.count == 2
    assert len(result.data) == 2
    assert result.data[0].code == "F113110102700"
    assert result.data[0].name == "東京大学"
    assert result.data[1].code == "F113210103100"
    assert result.data[1].name == "早稲田大学"
    assert result.facets is not None
    assert result.facets.type is not None


def test_create_school_request():
    """Test school request creation"""
    from kenallclient.client import KenAllClient

    target = KenAllClient("testing-api-key")
    result = target.create_school_request("F113110102700")
    assert result.full_url == "https://api.kenall.jp/v1/school/F113110102700"
    assert result.headers == {"Authorization": "Token testing-api-key"}


def test_create_school_request_with_api_version():
    """Test school request creation with API version"""
    from kenallclient.client import KenAllClient

    target = KenAllClient("testing-api-key")
    result = target.create_school_request("F113110102700", api_version="2025-01-01")
    assert result.full_url == "https://api.kenall.jp/v1/school/F113110102700"
    assert result.headers["Authorization"] == "Token testing-api-key"
    assert result.headers.get("Kenall-api-version") == "2025-01-01"


def test_create_school_search_request():
    """Test school search request creation"""
    from kenallclient.client import KenAllClient

    target = KenAllClient("testing-api-key")
    result = target.create_school_search_request(
        q="東京都", offset=0, limit=10, facet_type="/大学"
    )
    assert "https://api.kenall.jp/v1/school/" in result.full_url
    assert "q=" in result.full_url
    assert "facet_type=" in result.full_url
    assert result.headers == {"Authorization": "Token testing-api-key"}


def test_create_school_search_request_with_api_version():
    """Test school search request creation with API version"""
    from kenallclient.client import KenAllClient

    target = KenAllClient("testing-api-key")
    result = target.create_school_search_request(
        q="東京都", offset=0, limit=10, api_version="2025-01-01"
    )
    assert "https://api.kenall.jp/v1/school/" in result.full_url
    assert "q=" in result.full_url
    assert result.headers["Authorization"] == "Token testing-api-key"
    assert result.headers.get("Kenall-api-version") == "2025-01-01"


def test_fetch_school_result(mocker, school_v20250101):
    """Test fetching school result"""
    import json

    from kenallclient.client import KenAllClient
    from kenallclient.models import v20250101

    dummy_response = DummyResponse(json.dumps(school_v20250101))
    dummy_response.headers = {"Content-Type": "application/json"}
    mock_urlopen = mocker.patch("kenallclient.client.urllib.request.urlopen")
    mock_urlopen.return_value = dummy_response

    request = mocker.Mock()
    target = KenAllClient("testing-api-key")
    result = target.fetch_school_result(request, api_version="2025-01-01")

    mock_urlopen.assert_called_with(request)
    assert isinstance(result, v20250101.SchoolResolverResponse)
    assert result.version == "2025-01-01"
    assert result.data.code == "F113110102700"


def test_fetch_school_search_result(mocker, school_search_v20250101):
    """Test fetching school search result"""
    import json

    from kenallclient.client import KenAllClient
    from kenallclient.models import v20250101

    dummy_response = DummyResponse(json.dumps(school_search_v20250101))
    dummy_response.headers = {"Content-Type": "application/json"}
    mock_urlopen = mocker.patch("kenallclient.client.urllib.request.urlopen")
    mock_urlopen.return_value = dummy_response

    request = mocker.Mock()
    target = KenAllClient("testing-api-key")
    result = target.fetch_school_search_result(request, api_version="2025-01-01")

    mock_urlopen.assert_called_with(request)
    assert isinstance(result, v20250101.SchoolSearcherResponse)
    assert result.version == "2025-01-01"
    assert len(result.data) == 2


@pytest.mark.parametrize("api_version", SCHOOL_VERSIONS)
def test_school_get_all_versions(mocker, load_version_fixture, api_version):
    """Test school GET endpoint across supported versions"""
    import json

    from kenallclient.client import KenAllClient

    # Load version-specific fixture
    fixture_data = load_version_fixture(api_version, "school_get.json")

    dummy_response = DummyResponse(json.dumps(fixture_data))
    dummy_response.headers = {"Content-Type": "application/json"}
    mock_urlopen = mocker.patch("kenallclient.client.urllib.request.urlopen")
    mock_urlopen.return_value = dummy_response

    target = KenAllClient("testing-api-key")
    result = target.get_school("F113110102700", api_version=api_version)

    # Verify request
    request = mock_urlopen.call_args[0][0]
    assert request.full_url == "https://api.kenall.jp/v1/school/F113110102700"
    assert request.headers["Authorization"] == "Token testing-api-key"
    assert request.headers.get("Kenall-api-version") == api_version

    # Verify response
    assert result.version is not None
    assert result.data.code == "F113110102700"


@pytest.mark.parametrize("api_version", SCHOOL_VERSIONS)
def test_school_search_all_versions(mocker, load_version_fixture, api_version):
    """Test school search endpoint across supported versions"""
    import json

    from kenallclient.client import KenAllClient

    # Load version-specific fixture
    fixture_data = load_version_fixture(api_version, "school_search.json")

    dummy_response = DummyResponse(json.dumps(fixture_data))
    dummy_response.headers = {"Content-Type": "application/json"}
    mock_urlopen = mocker.patch("kenallclient.client.urllib.request.urlopen")
    mock_urlopen.return_value = dummy_response

    target = KenAllClient("testing-api-key")
    result = target.search_school(q="東京都", api_version=api_version)

    # Verify request
    request = mock_urlopen.call_args[0][0]
    assert "https://api.kenall.jp/v1/school/" in request.full_url
    assert "q=" in request.full_url
    assert request.headers["Authorization"] == "Token testing-api-key"
    assert request.headers.get("Kenall-api-version") == api_version

    # Verify response
    assert result.version is not None
    assert len(result.data) > 0


def test_school_api_with_invalid_version(mocker):
    """Test school API with invalid version"""
    import json

    from kenallclient.client import KenAllClient

    # Mock the HTTP response to avoid actual network calls
    dummy_response = DummyResponse(json.dumps({"version": "2024-01-01", "data": {}}))
    dummy_response.headers = {"Content-Type": "application/json"}
    mock_urlopen = mocker.patch("kenallclient.client.urllib.request.urlopen")
    mock_urlopen.return_value = dummy_response

    target = KenAllClient("testing-api-key")

    # School APIs are only available from 2025-01-01
    with pytest.raises(ValueError) as e:
        target.get_school("F113110102700", api_version="2024-01-01")
    assert "School API not available for version 2024-01-01" in str(e.value)
