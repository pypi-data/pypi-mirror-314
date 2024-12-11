import hashlib
import json, os, requests
import time

def inference_gateway(api_url):
    data = data_mgt.read_json()
    data["api_url"] = api_url
    data_mgt.write_json(data)

## 驗證certificate.hash
def generate_hash(data):
    # Combine values into a single string
    combined_string = f"""{data["register"]["application_token"]}{data["register"]["position_uid"]}{data["register"]["inference_client_name"]}"""

    # Create a hash object using SHA-256 (you can choose a different algorithm)
    # Get the hexadecimal representation of the hash
    hash_value = hashlib.sha256(combined_string.encode()).hexdigest()
    return hash_value


## data_mgt
class Data_mgt:
    def __init__(self, file_name="config.json"):
        # 获取脚本所在目录
        self.script_dir = os.path.dirname(os.path.abspath(__file__))
        # 构建文件路径
        self.json_file_path = os.path.join(self.script_dir, file_name)
        # print(self.json_file_path)

    def read_json(self):
        with open(self.json_file_path, "r") as json_file:
            data = json.load(json_file)
        return data

    def write_json(self, data):
        with open(self.json_file_path, "w") as json_file:
            json.dump(data, json_file, indent=2)


## interact with inference_layer
def send_register_request(register_data):
    data = data_mgt.read_json()
    data["register"]["application_uid"] = register_data["application_uid"]
    data["register"]["application_token"] = register_data["application_token"]
    data["register"]["inference_client_name"] = register_data["inference_client_name"]
    data["register"]["position_uid"] = register_data["position_uid"]

    # API endpoint for registration
    registration_endpoint = f"""{data["api_url"]}/entrypoint/authentication/{register_data["position_uid"]}"""

    # Data to be sent in the POST request
    payload = {
        "application_uid": data["register"]["application_uid"],
        "application_token": data["register"]["application_token"],
        "inference_client_name": data["register"]["inference_client_name"],
        "position_uid": data["register"]["position_uid"]
    }

    try:
        # Make the POST request
        response = requests.post(registration_endpoint, json=payload)
        access_data = response.json()

        # Check the response status code
        if response.status_code == 200:
            print("status:", response.status_code, "<application_source_mgt>/<SourceCertificateHandler>/<certificate_issuing>")
            data["certificate_receiver"]["status"] = access_data.get('status')
            data["certificate_receiver"]["certificate"] = access_data.get('certificate')
        else:
            print("ERROR", response.status_code, "<certificate_issuing> Register")
            data["certificate_receiver"]["status"] = "error"

    except Exception as e:
        print(f"Error during registration: {e}")

    data_mgt.write_json(data)


## 驗證certificate是否有效
def check_identity(data):
    
    if data["certificate_receiver"]["status"] == "success":
        if data["certificate_receiver"]["certificate"][:64] == generate_hash(data):
            if int(data["certificate_receiver"]["certificate"][64:]) >=  int(time.time()):
                print("certificate is valid")
                # print("the diff between timeout_timestamp and current_time:", int(data["certificate_receiver"]["certificate"][64:]) - int(time.time()))
            else:
                print("Timeout, certificate is invalid")
                data["certificate_receiver"]["status"] = "error"
                send_register_request(data["register"])
        else:
            print("Invalid hash, certificate is invalid")
            data["certificate_receiver"]["status"] = "error"
    else:
        print("unregister, status error")
        data["certificate_receiver"]["status"] = "error"
    return data


data_mgt = Data_mgt()
