import requests
import json
import base64

def save_video_file(base64_video, file_path):
    with open(file_path, "wb") as video_file:
        video_file.write(base64.b64decode(base64_video))
output_video_path = "test_success_fuck_yeah.mp4"

url = "http://71ef-2601-98a-4204-2fa0-71a8-da56-be3e-db35.ngrok.io/create_video"

with open('testing/test_call.json') as f:
  data = f.read()

data = json.loads(data)
data["videoType"] = "gif"
data["wav2lipURL"] = "http://81d1-34-86-179-3.ngrok.io/deepfake"

headers = {'Content-Type': 'application/json'}

response = requests.post(url, data=json.dumps(data), headers=headers)

received_data = response.json()

if received_data["status"] == "success":
    base64_video = received_data["base64_video"]
    save_video_file(base64_video, output_video_path)
    print(f"Video saved at {output_video_path}")
else:
    print("Error occurred")