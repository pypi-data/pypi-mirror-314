import requests, json
from AppAuthN.CloseLoopCounter import global_counter, send_closed_loop
from AppAuthN.CertificationReceiver import data_mgt, check_identity
import uuid

## send rawdata to inference layer for receiving inference result
def send_rawdata(rawdata):
    check_identity(data_mgt.read_json())
    data = data_mgt.read_json()

    new_packet_uid = str(uuid.uuid4())

    data["raw_data"]["packet_uid"] = new_packet_uid
    data["raw_data"]["application_uid"] = rawdata["application_uid"]
    data["raw_data"]["position_uid"] = rawdata["position_uid"]
    data["raw_data"]["inference_client_name"] = rawdata["inference_client_name"]
    data["raw_data"]["value"] = rawdata["value"]
 

    # API endpoint for inference_service
    inference_service_endpoint = f"""{data["api_url"]}/entrypoint/inference_service/{data["raw_data"]["position_uid"]}"""
    
    data["closed_loop"]["packet_uid"] = new_packet_uid
    data["closed_loop"]["application_uid"] = data["raw_data"]["application_uid"]
    data["closed_loop"]["position_uid"] = data["raw_data"]["position_uid"]
    data["closed_loop"]["multi_input"] = data["raw_data"]["multi_input"]
    data["closed_loop"]["inference_client_name"] = data["raw_data"]["inference_client_name"]

    payload = {
        "application_uid": data["raw_data"]["application_uid"],
        "position_uid": data["raw_data"]["position_uid"],
        "packet_uid": data["raw_data"]["packet_uid"],
        "inference_client_name": data["raw_data"]["inference_client_name"],
        "value": data["raw_data"]["value"]
    }

    try:
        # Make the POST request
        global_counter.reset()
        response = requests.post(inference_service_endpoint, json=payload)
        # start a timer
        access_data = response.json()

        # Check the response status code
        if response.status_code == 200:
            data = send_closed_loop(data)
            print("status:", response.status_code, "<inference_exe>/<InferenceServiceHandler>/<inference_service>")
            data["result_receiver"]["status"] = access_data.get('status')
            data["result_receiver"]["value"] = access_data.get('value')
        else:
            print("ERROR", response.status_code, "<inference_service>")
            # data["certificate_receiver"]["status"] = "error"

    except Exception as e:
        print(f"Error during registration: {e}")

    data_mgt.write_json(data)
    return data["result_receiver"]