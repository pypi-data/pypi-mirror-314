import requests

class ScrapelessClient:
  api_url = "https://api.scrapeless.com/api/v1"

  def __init__(self, api_key: str):
    self.api_key = api_key

  def scraper(self, actor: str, input: dict = None, webhook: str = None, proxy: dict = None):
    data = self._assemble_data(actor, input, webhook, proxy)
    return self._worker("/scraper/request", data)

  def unlocker(self, actor: str, input: dict = None, proxy: dict = None):
    data = self._assemble_data(actor, input, proxy=proxy)
    return self._worker("/unlocker/request", data)

  def captcha(self, actor: str, input: dict = None, webhook: str = None, proxy: dict = None):
    data = self._assemble_data(actor, input, webhook, proxy)
    return self._worker("/createTask", data)

  def get_scraper_result(self, taskId: str):
    return self._get(f"/scraper/result/{taskId}")

  def get_captcha_result(self, taskId: str):
    return self._get(f"/getTaskResult/{taskId}")

  def _assemble_data(self, actor: str, input: dict = None, webhook: str = None, proxy: dict = None):
    data = { "actor": actor, "input": input }

    if webhook:
      data["webhook"] = webhook

    if proxy:
      data["proxy"] = proxy

    return data

  def _worker(self, url: str, data: dict = None):
    headers = { "x-api-token": self.api_key }

    resp = requests.post(f"{self.api_url}{url}", headers=headers, json=data)
    status_code = resp.status_code

    if status_code == 504:
      return { "message": "Gateway Timeout", "code": 504 }

    return resp.json()

  def _get(self, url: str):
    headers = { "x-api-token": self.api_key }

    resp = requests.get(f"{self.api_url}{url}", headers=headers)
    status_code = resp.status_code

    if status_code == 504:
      return { "message": "Gateway Timeout", "code": 504 }

    return resp.json()