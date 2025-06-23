import pytest
import requests

from src.weather_03.weather_wrapper import WeatherWrapper

@pytest.fixture
def weather_wrapper():
    return WeatherWrapper(api_key='GsG9OhlyhrQQOzGTaSAQCuL42LKAmTqo')


def test_init(weather_wrapper):
    assert weather_wrapper.api_key == 'GsG9OhlyhrQQOzGTaSAQCuL42LKAmTqo'
    assert weather_wrapper.location_cache == {}


def test_get_location_key_with_cache(weather_wrapper, mocker):
    # Добавляем значение в кэш
    weather_wrapper.location_cache = {"Moscow": "123_key"}

    key = weather_wrapper.get_location_key("Moscow")
    assert key == "123_key"
    # Проверяем, что запрос не выполнялся
    assert not mocker.spy(requests, 'get').called


def test_get_location_key_without_cache(weather_wrapper, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"Key": "456_key"}]

    mocker.patch('requests.get', return_value=mock_response)

    key = weather_wrapper.get_location_key("London")
    assert key == "456_key"
    requests.get.assert_called_once()


def test_get_location_key_city_not_found(weather_wrapper, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = []

    mocker.patch('requests.get', return_value=mock_response)

    with pytest.raises(ValueError, match="City Paris not found"):
        weather_wrapper.get_location_key("Paris")


def test_get_temperature(weather_wrapper, mocker):
    # Мокаем запросы
    mock_location_response = mocker.Mock()
    mock_location_response.status_code = 200
    mock_location_response.json.return_value = [{"Key": "789_key"}]

    mock_temp_response = mocker.Mock()
    mock_temp_response.status_code = 200
    mock_temp_response.json.return_value = [{
        "Temperature": {"Metric": {"Value": 15.5}}
    }]

    mocker.patch('requests.get', side_effect=[mock_location_response, mock_temp_response])

    temp = weather_wrapper.get_temperature("Berlin")
    assert temp == 15.5
    assert requests.get.call_count == 2


def test_get_tomorrow_temperature(weather_wrapper, mocker):
    mock_location_response = mocker.Mock()
    mock_location_response.status_code = 200
    mock_location_response.json.return_value = [{"Key": "101_key"}]

    mock_forecast_response = mocker.Mock()
    mock_forecast_response.status_code = 200
    mock_forecast_response.json.return_value = {
        "DailyForecasts": [
            {},
            {"Temperature": {"Maximum": {"Value": 18.2}}}
        ]
    }

    mocker.patch('requests.get', side_effect=[mock_location_response, mock_forecast_response])

    temp = weather_wrapper.get_tomorrow_temperature("Madrid")
    assert temp == 18.2


def test_find_diff_two_cities(weather_wrapper, mocker):
    # Настраиваем моки для двух городов
    mock_location_response1 = mocker.Mock()
    mock_location_response1.status_code = 200
    mock_location_response1.json.return_value = [{"Key": "111_key"}]

    mock_temp_response1 = mocker.Mock()
    mock_temp_response1.status_code = 200
    mock_temp_response1.json.return_value = [{
        "Temperature": {"Metric": {"Value": 20.0}}
    }]

    mock_location_response2 = mocker.Mock()
    mock_location_response2.status_code = 200
    mock_location_response2.json.return_value = [{"Key": "222_key"}]

    mock_temp_response2 = mocker.Mock()
    mock_temp_response2.status_code = 200
    mock_temp_response2.json.return_value = [{
        "Temperature": {"Metric": {"Value": 15.0}}
    }]

    mocker.patch('requests.get', side_effect=[
        mock_location_response1, mock_temp_response1,
        mock_location_response2, mock_temp_response2
    ])

    diff = weather_wrapper.find_diff_two_cities("Rome", "Paris")
    assert diff == 5.0


def test_get_diff_string_warmer(weather_wrapper, mocker):
    def mock_get(url, params):
        mock_resp = mocker.Mock()
        mock_resp.status_code = 200

        if "locations" in url:
            mock_resp.json.return_value = [{"Key": f"key_{params['q']}"}]
        elif "currentconditions" in url:
            city = params['q']
            if city == "Dubai":
                mock_resp.json.return_value = [{
                    "Temperature": {"Metric": {"Value": 35.0}}
                }]
            elif city == "Oslo":
                mock_resp.json.return_value = [{
                    "Temperature": {"Metric": {"Value": 10.0}}
                }]
        return mock_resp

    mocker.patch('requests.get', side_effect=mock_get)

    result = weather_wrapper.get_diff_string("Dubai", "Oslo")
    assert "Weather in Dubai is warmer than in Oslo by 25 degrees" in result

@pytest.mark.parametrize("today_temp,tomorrow_temp,expected_phrase", [
    (15.5, 30.2, "much warmer"),
    (15.5, 18.2, "warmer"),
    (15.5, 10.2, "much colder"),
    (15.5, 14.0, "colder"),
    (15.5, 15.0, "the same")
])
def test_get_diff_variants(weather_wrapper, mocker, today_temp, tomorrow_temp, expected_phrase):
    mock_location_response = mocker.Mock()
    mock_location_response.status_code = 200
    mock_location_response.json.return_value = [{"Key": "789_key"}]

    mock_forecast_response = mocker.Mock()
    mock_forecast_response.status_code = 200
    mock_forecast_response.json.return_value = {
        "DailyForecasts": [
            {},
            {"Temperature": {"Maximum": {"Value": tomorrow_temp}}}
        ]
    }

    mock_temp_response = mocker.Mock()
    mock_temp_response.status_code = 200
    mock_temp_response.json.return_value = [{
        "Temperature": {"Metric": {"Value": today_temp}}
    }]

    weather_wrapper.location_cache = {"Dubai": "123_key"}

    mocker.patch('requests.get', side_effect=[mock_forecast_response, mock_temp_response, mock_location_response])

    result = weather_wrapper.get_tomorrow_diff("Dubai")
    assert f"The weather in Dubai tomorrow will be {expected_phrase} than today" in result


def test_api_error_handling(weather_wrapper, mocker):
    mock_response = mocker.Mock()
    mock_response.status_code = 404

    mocker.patch('requests.get', return_value=mock_response)

    with pytest.raises(AttributeError, match="Incorrect city"):
        weather_wrapper.get_response_city("UnknownCity", "http://test.url")