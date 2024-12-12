from mio.web import *


assert isWebsite("google.com") == True

assert isWebsite("fshjaklfhasjkldsafa.com") == False

expected = '{"count":2274744,"name":"john","gender":"male","probability":1.0}'
assert requestText("https://api.genderize.io/?name=john") == expected

assert "fact" in requestJson("https://catfact.ninja/fact")