class Base:
    def __init__(self, stage, username=None, key=None):
        self.__version__ = "0.5.7"  # update here and in setup.py
        if stage == "develop":
            self.headers = {"Authorization": username + "," + key, "Api_key": username + "," + key}
            self.url = "https://test-api.dcentralab.com/"  # DUB backend URL
            self.w3i_url = "https://test-api.web3index.com/"  # Web3Index backend URL
        if stage == "staging":
            self.headers = {"Authorization": username + "," + key, "Api_key": username + "," + key}
            self.url = "https://staging.dcentralab.com/"
            self.w3i_url = "https://staging-api.web3index.com/"
        if stage == "preprod":
            self.headers = {"Authorization": username + "," + key, "Api_key": username + "," + key}
            self.url = "https://preprod-api.dcentralab.com/"
            self.w3i_url = "https://preprod-api.web3index.com/"
        if stage == "main":
            self.headers = {"Authorization": username + "," + key, "Api_key": username + "," + key}
            self.url = "https://api.dcentralab.com/"
            self.w3i_url = "https://api.web3index.com/"
        if stage == "staging-api":
            self.headers = {"Authorization": username + "," + key, "Api_key": username + "," + key}
            self.url = "https://staging-api.dcentralab.com/"
            self.w3i_url = "https://staging-api.web3index.com/"


class DapiError(Exception):
    def __init__(self, message=None, status_code=None, response=None, exception=None):
        super().__init__(message)
        self.status_code = status_code
        self.response = response
        self.exception = exception
