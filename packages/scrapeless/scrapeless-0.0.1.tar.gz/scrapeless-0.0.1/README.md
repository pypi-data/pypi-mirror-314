# Scrapeless Python SDK

## install
```shell
pip install scrapeless-sdk-python
```

## Usage

Start using the API with your [API KEY](https://app.scrapeless.com/dashboard/account?tab=apiKey)

For more examples, please refer to the `examples` directory

For more information, please refer to our [documentation](https://docs.scrapeless.com/)

### Scraping API
```python
from scrapeless import ScrapelessClient

scrapeless = ScrapelessClient(api_key='your-api-key')

actor = "scraper.shopee"
input_data = {
  "type": "shopee.product",
  "url": "https://shopee.tw/2312312.10228173.24803858474"
}

result = scrapeless.scraper(actor, input=input_data)
```

### Web Unlocker
```python
from scrapeless import ScrapelessClient

scrapeless = ScrapelessClient(api_key='your-api-key')

actor = 'unlocker.webunlocker'
input_data = {
  "url": "https://www.scrapeless.com",
  "proxy_country": "ANY",
  "method": "GET",
  "redirect": false,
}

result = scrapeless.unlocker(actor, input=input_data)
```

### Captcha Solver
```python
from scrapeless import ScrapelessClient

scrapeless = ScrapelessClient(api_key='your-api-key')

actor = 'captcha.recaptcha'
input_data = {
  "version": "v2",
  "pageURL": "https://www.google.com",
  "siteKey": "6Le-wvkSAAAAAPBMRTvw0Q4Muexq9bi0DJwx_mJ-",
  "pageAction": ""
}

result = scrapeless.captcha(actor, input=input_data)
```