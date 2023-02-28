from flask import Flask, Response, jsonify, request
import json 

app = Flask(__name__)

@app.route('/api')
def headers():
  ParamTest = request.args.get("ParamTest")
  JsonTest = json.loads(request.data)
  HeadersTest = request.headers.get("HeadersTest")
  CookiesTest = request.cookies.get("CookiesTest")
  
  data = {"Param Test": ParamTest, "JSON Test": JsonTest["JsonTest"], "Headers Test": HeadersTest, "Cookies Test": CookiesTest}
  
  return data

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=8080)
