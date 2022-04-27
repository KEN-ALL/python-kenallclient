import io
import pytest

from tests.conftest import dummy_holiday_search_json


class DummyResponse(io.StringIO):
    headers: dict = {}


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


def test_fetch(mocker, dummy_json):
    import json
    from kenallclient.client import KenAllClient

    dummy_response = DummyResponse(json.dumps(dummy_json))
    dummy_response.headers = {"Content-Type": "application/json"}
    mock_urlopen = mocker.patch("kenallclient.client.urllib.request.urlopen")
    mock_urlopen.return_value = dummy_response

    request = mocker.Mock()
    target = KenAllClient("testing-api-key")
    result = target.fetch(request)
    mock_urlopen.assert_called_with(request)
    assert result


def test_fetch_unexpected_content_type(mocker, dummy_json):
    import json
    from kenallclient.client import KenAllClient

    dummy_response = DummyResponse(json.dumps(dummy_json))
    dummy_response.headers = {"Content-Type": "plain/text"}
    request_body = dummy_response.getvalue()
    mock_urlopen = mocker.patch("kenallclient.client.urllib.request.urlopen")
    mock_urlopen.return_value = dummy_response

    request = mocker.Mock()
    target = KenAllClient("testing-api-key")
    with pytest.raises(ValueError) as e:
        target.fetch(request)
    assert e.value.args == ("not json response", request_body)


def test_fetch_houjin(mocker, dummy_houjinbangou_json):
    import json
    from kenallclient.client import KenAllClient

    dummy_response = DummyResponse(json.dumps(dummy_houjinbangou_json))
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
    from kenallclient.client import KenAllClient
    from kenallclient import model

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


def test_handle_response_200(mocker, dummy_json):
    import json
    from kenallclient.client import KenAllClient

    dummy_response = DummyResponse(json.dumps(dummy_json))
    dummy_response.headers = {"Content-Type": "application/json"}
    mock_urlopen = mocker.patch("kenallclient.client.urllib.request.urlopen")
    mock_urlopen.return_value = dummy_response

    request = mocker.Mock()
    target = KenAllClient("testing-api-key")
    result = target._handle_response(request)
    mock_urlopen.assert_called_with(request)
    assert result


def test_handle_response_404(mocker, dummy_json):
    import json
    from urllib.error import HTTPError
    from kenallclient.client import KenAllClient

    dummy_response = DummyResponse(json.dumps(dummy_json))
    dummy_response.headers = {"Content-Type": "application/json"}
    mock_urlopen = mocker.patch("kenallclient.client.urllib.request.urlopen")
    mock_urlopen.side_effect = HTTPError("dummy", 404, "dummy", None, None)

    request = mocker.Mock()
    target = KenAllClient("testing-api-key")
    result = target._handle_response(request)
    mock_urlopen.assert_called_with(request)
    assert result is False


def test_handle_response_400(mocker, dummy_json):
    import json
    from urllib.error import HTTPError
    from kenallclient.client import KenAllClient

    dummy_response = DummyResponse(json.dumps(dummy_json))
    dummy_response.headers = {"Content-Type": "application/json"}
    mock_urlopen = mocker.patch("kenallclient.client.urllib.request.urlopen")
    mock_urlopen.side_effect = HTTPError("dummy", 400, "dummy", None, None)

    request = mocker.Mock()
    target = KenAllClient("testing-api-key")
    with pytest.raises(Exception) as e:
        _ = target._handle_response(request)

    mock_urlopen.assert_called_with(request)
    assert str(e.value) == "('not valid http-response code', 'dummy')"
