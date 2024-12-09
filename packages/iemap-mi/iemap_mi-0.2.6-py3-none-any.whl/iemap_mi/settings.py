# settings.py

class APISettings:
    BASE_URL = "https://iemap.enea.it/rest"

    AUTH_JWT_LOGIN = f"{BASE_URL}/auth/jwt/login"
    PROJECT_LIST = f"{BASE_URL}/api/v1/project/list/"
    PROJECT_ADD = f"{BASE_URL}/api/v1/project/add"
    PROJECT_QUERY = f"{BASE_URL}/api/v1/project/query/"
    ADD_FILE_TO_PROJECT = f"{BASE_URL}/api/v1/project/add/file/"
    AI_GEOCGNN = f"https://iemap.enea.it/ai/"
    STATS = f"{BASE_URL}/api/v1/stats"

    # Add other endpoints as needed


settings = APISettings()
