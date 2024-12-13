import requests

def hit_record_endpoint():
    data = {"engine_temperature": 0.3}
    response = requests.post("http://0.0.0.0:8000/record", json=data)
    return response.content

def hit_collect_endpoint():
    response = requests.post("http://0.0.0.0:8000/collect")
    return response.content

if __name__ == "__main__":
    # print(hit_record_endpoint())
    print(hit_collect_endpoint())
