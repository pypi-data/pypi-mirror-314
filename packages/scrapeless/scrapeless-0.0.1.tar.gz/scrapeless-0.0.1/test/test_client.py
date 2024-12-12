import unittest
from unittest.mock import patch, Mock
from scrapeless import ScrapelessClient

class TestScrapelessClient(unittest.TestCase):
  def setUp(self):
    self.api_key = "your-api-key"
    self.client = ScrapelessClient(api_key=self.api_key)

  @patch("scrapeless.client.requests.post")
  def test_scraper(self, mock_post):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"taskId": "12345"}
    mock_post.return_value = mock_response

    actor = "scraper.shopee"
    input_data = {"type": "shopee.product", "url": "https://shopee.tw/2312312.10228173.24803858474"}

    result = self.client.scraper(actor, input=input_data)

    self.assertIn("taskId", result)

    mock_post.assert_called_once_with(
      f"{self.client.api_url}/scraper/request",
      headers={"x-api-token": self.api_key},
      json={"actor": actor, "input": input_data}
    )

  @patch("scrapeless.client.requests.post")
  def test_unlocker(self, mock_post):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"taskId": "12345"}
    mock_post.return_value = mock_response

    actor = "unlocker.akamaiweb"
    input_data = {
      "type": "cookie",
      "proxy_country": "ANY",
      "url": "https://www.iberia.com/",
      "userAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36",
    }

    result = self.client.unlocker(actor, input=input_data)

    self.assertIn("taskId", result)

    mock_post.assert_called_once_with(
      f"{self.client.api_url}/unlocker/request",
      headers={"x-api-token": self.api_key},
      json={"actor": actor, "input": input_data}
    )

  @patch("scrapeless.client.requests.post")
  def test_captcha(self, mock_post):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"taskId": "12345"}
    mock_post.return_value = mock_response

    actor = "captcha.recaptcha"
    input_data = {
      "version": "v2",
      "pageURL": "https://www.google.com",
      "siteKey": "6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
      "pageAction": ""
    }

    result = self.client.captcha(actor, input=input_data)

    self.assertIn("taskId", result)

    mock_post.assert_called_once_with(
      f"{self.client.api_url}/createTask",
      headers={"x-api-token": self.api_key},
      json={"actor": actor, "input": input_data}
    )

  @patch("scrapeless.client.requests.get")
  def test_get_captcha_result(self, mock_get):
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
      "status": "ready",
      "solution": {
        "token": "xxx"
      },
    }
    mock_get.return_value = mock_response

    taskId = "12345"

    result = self.client.get_scraper_result(taskId)

    self.assertIn("status", result)

    mock_get.assert_called_once_with(
      f"{self.client.api_url}/scraper/result/{taskId}",
      headers={"x-api-token": self.api_key}
    )

if __name__ == "__main__":
  unittest.main()
