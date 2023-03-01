HTTPCore, the perfect choice for your HTTP needs.

```python
Requests = HttpCore().Requests()

request = Requests.httpsRequest("GET", "https://0.0.0.0/api", 
  headers = {"HeadersTest": "Works"},
  body = {"JsonTest": "Works"},
  params = {"ParamTest": "Works"},
  cookies = "CookiesTest=Works;",
  timeout = 5
)

url = request.url
body = request.body
headers = request.headers
params = request.params
status_code = request.status_code
data = request.data
test = request.text
```
* Ill be adding more and better documentation with more features including a websocket library
* Ill compile it into a PIP soon.
