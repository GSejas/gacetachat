import requests 

API_URL = "http://localhost:8007/"


def get_execution_session_by_date(date):
    response = requests.get(f"{API_URL}/execution_session_by_date/", params={"date": date})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to get execution session for the given date.")

def list_available_index_days():
    response = requests.get(f"{API_URL}/execution_session/available")
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to list available index days.")

def get_last_execution_session(session_id):
    response = requests.get(f"{API_URL}/execution_session/", params={"session_id": session_id})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to display last execution session.")


def fetch_recent_exec_logs(limit=3):
    response = requests.get(f"{API_URL}/content_logs/?limit={limit}")
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to load execution logs.")
    