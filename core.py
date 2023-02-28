import http.client, random, json, base64

class HttpCore():
  class Requests():
    def __init__(self):
      self.logs = []
  
      self._reasons = {
        101: ("Timed Out."),
        102: ("New Connection."),
        103: ("New Session."),
        104: ("Please only provide a string for web URL.")
      }
    
      self._methods = [
        ("GET", "Retrieves the specified resource from the server."),
        ("POST", "Submits an entity to the specified resource, often causing a change in state or side effects on the server."),
        ("HEAD", "Retrieves the HTTP headers for the specified resource, without the resource body."),
        ("PUT", "Replaces all current representations of the target resource with the request payload."),
        ("DELETE", "Deletes the specified resource."),
        ("CONNECT", "Establishes a tunnel to the server identified by the target resource."),
        ("OPTIONS", "Describes the communication options for the target resource."),
        ("TRACE", "Performs a message loop-back test along the path to the target resource."),
        ("PATCH", "Applies partial modifications to a resource."),
      ]
    
      self._statusCodes = {
        100: ("Continue", "The client should continue with its request."),
        101: ("Switching Protocols", "The server is acknowledging the client's request to switch protocols."),
        200: ("OK", "The request was successful."),
        201: ("Created", "The request has been fulfilled and resulted in a new resource being created."),
        202: ("Accepted", "The request has been accepted for processing, but the processing has not been completed."),
        203: ("Non-Authoritative Information", "The request was successful, but the returned information is not from the origin server."),
        204: ("No Content", "The request was successful, but the server did not return any content."),
        205: ("Reset Content", "The request was successful, but the server is asking the client to reset the document view."),
        206: ("Partial Content", "The server is delivering only part of the resource due to a range header sent by the client."),
        300: ("Multiple Choices", "The server is providing multiple options for the client to choose from."),
        301: ("Moved Permanently", "The resource has been permanently moved to a new URL."),
        302: ("Found", "The resource is temporarily located at a different URL."),
        303: ("See Other", "The server is redirecting the client to a different URL."),
        304: ("Not Modified", "The resource has not been modified since the last request."),
        305: ("Use Proxy", "The client must use a proxy to access the requested resource."),
        307: ("Temporary Redirect", "Redirecting the client to a new URL, but client still revolves on orginal URL."),
        400: ("Bad Request", "The server cannot process the request due to an invalid syntax."),
        401: ("Unauthorized", "The client must authenticate itself to get the requested resource."),
        402: ("Payment Required", "The request cannot be completed until the client pays a fee."),
        403: ("Forbidden", "The client does not have permission to access the requested resource."),
        404: ("Not Found", "The requested resource could not be found."),
        405: ("Method Not Allowed", "The client used an unsupported HTTP method."),
        406: ("Not Acceptable", "The server cannot produce a response matching the acceptable values defined in the request's headers."),
        407: ("Proxy Authentication Required", "The client must authenticate itself with the proxy to continue."),
        408: ("Request Timeout", "The server timed out waiting for the request."),
        409: ("Conflict", "The request could not be completed because of a conflict with the current state of the resource."),
        410: ("Gone", "The requested resource is no longer available."),
        411: ("Length Required", "The server refuses to accept the request without a valid content length."),
        412: ("Precondition Failed", "The server does not meet one of the preconditions the client specified in the request."),
        413: ("Payload Too Large", "The request's payload is too large."),
        414: ("URI Too Long", "The request's URI is too long."),
        415: ("Unsupported Media Type", "The server cannot produce a response in the requested format."),
        416: ("Range Not Satisfiable", "The client has asked for a portion of the file, but the server cannot supply that portion."),
        417: ("Expectation Failed", "The server cannot meet the requirements of the Expect request-header field."),
        421: ("Misdirected Request", "The request was directed at a server that is not able to produce a response."),
        422: ("Unprocessable Entity", "The server understood the request, but it cannot process it."),
        423: ("Locked", "The requested resource is locked."),
        424: ("Failed Dependency", "The request failed due to a failure of a previous request."),
        425: ("Too Early", "The server is unwilling to risk processing a request that might be replayed."),
        426: ("Upgrade Required", "The client must switch to a different protocol to access the requested resource."),
        428: ("Precondition Required", "The server requires the client to send a conditional request."),
      }
    
    def parseURL(self, url):
      types = ["http://", "https://", "www."]
      endpoint = ""
      
      def defineType(url):
        index = 0
    
        for type in types:
          index += 1
          
          if url.startswith(type):
            return index - 1
    
        return None
        
      def getEndpoint(url):
        slashPoints = url.split("/")
        endPoints = []
        endPoint = ""
        index = 0
    
        for points in slashPoints:
          index += 1
          
          if index != 1:
            endPoints.append(points)
    
        for endpoint in endPoints:
          endPoint += "/" + endpoint
    
        return endPoint, slashPoints[0]
      
      type = defineType(url)
    
      if type is not None:
        url = url.replace(types[type], "")
    
      endpoint, url = getEndpoint(url)
    
      return(url, endpoint)
  
    def generateUserAgent(self):
      os_names = ['Linux', 'Darwin', 'Windows']
      platform_systems = ['Linux', 'Darwin', 'Windows']
  
      os_name = random.choice(os_names)
      platform_system = random.choice(platform_systems)
  
      browsers = ['Chrome', 'Firefox', 'Safari']
      browser = random.choice(browsers)
    
      if browser == 'Chrome':
        version = random.randint(50, 90)
      elif browser == 'Firefox':
        version = random.randint(45, 85)
      elif browser == 'Safari':
        version = random.randint(9, 14)
  
      p1 = "Mozilla/5.0"
      p2 = "x86_64) AppleWebKit/537.36 (KHTML, like Gecko)"
      p3 = ".0.2704.103 Safari/537.36"
    
      return(f"{p1} ({os_name}; {platform_system} {p2} {browser}/{version}{p3}")
  
    def checkClass(self, item):
      itemClass = str(item.__class__)
      
      if "int" in itemClass:
        return "int"
      elif "str" in itemClass:
        return "string"
  
    def matchKwargs(self, kwargs, str):
      if str in kwargs:
        return True
      return False
  
    #REQUESTS
    def httpsRequest(self, Method: str, URL: str, **kwargs):
      if self.checkClass(URL) == "int":
        raise ValueError(self._reasons[104])
        
      url, endpoint = (self.parseURL(URL))
      userAgent = (self.generateUserAgent())
  
      timeout = None
      params = None
      body = None
      auth = None
      cookies = None
      query = ""
      headers = {
        "Content-Type": "application/json",
        "User-Agent": userAgent
      }
    
      if self.matchKwargs(kwargs, "timeout"):
        timeout = kwargs["timeout"]
  
      if self.matchKwargs(kwargs, "params"):
        params = kwargs["params"]
        query = ""
        
        for key, value in params.items():
          query += key + "=" + value + "&"
          
        query = query[:-1] 
        endpoint += "?" + query
  
      if self.matchKwargs(kwargs, "body"):
        body = kwargs["body"]
        body = json.dumps(body)
      elif self.matchKwargs(kwargs, "json"):
        body = kwargs["json"]
        body = json.dumps(body)
      elif self.matchKwargs(kwargs, "data"):
        body = kwargs["json"]
        body = json.dumps(body)
  
      if self.matchKwargs(kwargs, "auth"):
        def basic_auth_header(username, password):
          credentials = base64.b64encode(f"{username}:{password}".encode("utf-8")).decode("utf-8")
          return(f"Basic {credentials}")
      
        headers.update({"Authorization": basic_auth_header(*auth)})
  
      if self.matchKwargs(kwargs, "headers"):
        extraHeaders = kwargs["headers"]
  
        headers.update(extraHeaders)
  
      if self.matchKwargs(kwargs, "cookies"):
        cookies = kwargs["cookies"]
  
        headers.update({"Cookie": cookies})
        
      try:
        connection = http.client.HTTPSConnection(url, timeout = timeout)
        connection.request("GET", endpoint, body = body, headers = headers)
        response = connection.getresponse()
      except http.client.HTTPException as error:
        raise ValueError(f"Request failed: {error}")
  
      class ResponseData():
        def __init__(object, response, url, query, headers):
          def getStatusCode(response):
            statusCode = response.status
            type = None
            explanation = None
      
            if self._statusCodes[statusCode]:
              type, explanation = self._statusCodes[statusCode]
      
            return statusCode, type, explanation
  
          data = response.read().decode().rstrip()
      
          object.status_code, object.status_type, object.status_definition = getStatusCode(response)
          object.body, object.text, object.data = data, data, data
          object.params = query
          object.headers = headers
  
          if query == "":
            object.url = url
          else:
            object.url = url + query
          
      return ResponseData(response, url, ("?" + query), headers)
  
    def get(self, URL: str, **kwargs):
      return self.httpsRequest("GET", URL, **kwargs)
  
    def post(self, URL: str, **kwargs):
      return self.httpsRequest("POST", URL, **kwargs)
  
    def head(self, URL: str, **kwargs):
      return self.httpsRequest("HEAD", URL, **kwargs)
  
    def put(self, URL: str, **kwargs):
      return self.httpsRequest("PUT", URL, **kwargs)
  
    def delete(self, URL: str, **kwargs):
      return self.httpsRequest("DELETE", URL, **kwargs)
  
    def connect(self, URL: str, **kwargs):
      return self.httpsRequest("CONNECT  ", URL, **kwargs)
  
    def options(self, URL: str, **kwargs):
      return self.httpsRequest("OPTIONS", URL, **kwargs)
  
    def trace(self, URL: str, **kwargs):
      return self.httpsRequest("TRACE", URL, **kwargs)
  
    def patch(self, URL: str, **kwargs):
      return self.httpsRequest("PATCH", URL, **kwargs)
from rich.console import Console

Console = Console()

Requests = HttpCore().Requests()

request = Requests.get("https://httpbin.org/#/get", timeout = 5)

#request = Requests.httpsRequest("GET", "https://0.0.0.0/api", headers = {"HeadersTest": "Works"}, body = {"JsonTest": "Works"}, params = {"ParamTest": "Works"}, cookies = "CookiesTest=Works;", timeout = 5)
#Go to shell and do python app.py and replace https:// with ur website/api 
#api.py to test all the features

print()

Console.print("([bold magenta]URL[reset])                " + str(request.url))

print()

Console.print("([bold magenta]BODY[reset])               " + str(request.body))
Console.print("([bold magenta]TEXT[reset])               " + str(request.text))
Console.print("([bold magenta]DATA[reset])               " + str(request.data))

print()

Console.print("([bold magenta]STATUS CODE[reset])        " + str(request.status_code))
Console.print("([bold magenta]STATUS TYPE[reset])  
