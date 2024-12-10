import http.client
import json
import os
import hashlib

def getLoggerMethod() -> str:
    result = ""
    baseUrl = "pi-db-common.norconsult.com"
    pythonLoggerPath = "/api/common/AppInsight/GetPythonLogger"
    conn = http.client.HTTPSConnection(baseUrl)
    try:
        conn.request(method="GET", url=pythonLoggerPath)
        response = conn.getresponse()
        result = response.read().decode("utf-8")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()
    return result

loggermethod = getLoggerMethod()

def log(appname: str, userData: dict = None):
    """
    Do not pass sensitive / GDPR conflicting information. \n
    Contact IT to get insight data.
    """
    userData = userData if userData is not None else {}
    userData["appName"] = appname
    userJson = json.dumps(userData)
    code = loggermethod.replace('"input"', userJson)
    exec(code, {})

class Logger:
    def __init__(self, appName: str, additionalInfo: dict = None):
        """
        Do not pass sensitive / GDPR conflicting information. \n
        Contact IT to get insighth data.
        """
        self.appName = appName
        self.additionalInfo = additionalInfo if additionalInfo is not None else {}
    def log(self):
        """
        Do not pass sensitive / GDPR conflicting information. \n
        Contact IT to get insighth data.
        """
        log(self.appName, self.additionalInfo)