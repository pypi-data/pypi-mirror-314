import time
import json, requests

class Counter:
    def __init__(self):
        self.value = float(time.time())

    def get_value(self):
        float(time.time())-self.value
        return float(time.time())-self.value

    def reset(self):
        self.value = float(time.time())

# 在這裡創建一個全局計數器變數
global_counter = Counter()

def send_closed_loop(data):

    # API endpoint for closed_loop
    closed_loop_endpoint = f"""{data["api_url"]}/entrypoint/closed_loop/{data["closed_loop"]["position_uid"]}"""

    data["closed_loop"]["value"] = global_counter.get_value()
    payload = {
        "application_uid": data["closed_loop"]["application_uid"],
        "position_uid": data["closed_loop"]["position_uid"],
        "packet_uid": data["closed_loop"]["packet_uid"],
        "inference_client_name": data["closed_loop"]["inference_client_name"],
        "value": data["closed_loop"]["value"]
    }

    try:
        # Make the POST request
        response = requests.post(closed_loop_endpoint, json=payload)
        access_data = response.json()

        # Check the response status code
        if response.status_code == 200:
            print("status:", response.status_code, "<closed_loop_data>/<ClosedLoopHandler>/<closed_loop_data_receiving>")
        else:
            print("ERROR", response.status_code, "<closed_loop_data_receiving>")

    except Exception as e:
        print(f"Error during registration: {e}")
    return data
