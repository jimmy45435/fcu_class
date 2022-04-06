import requests
from core.login.login import Login

if __name__ == "__main__":
    request = requests.Session()
    Login(request).start()


