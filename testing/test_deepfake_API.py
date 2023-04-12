import requests
import json
import base64

url = "http://127.0.0.1:5000/deepfake"  # Change the IP and port if needed

def read_audio_file(file_path):
    with open(file_path, "rb") as audio_file:
        return base64.b64encode(audio_file.read()).decode('utf-8')

def save_video_file(base64_video, file_path):
    with open(file_path, "wb") as video_file:
        video_file.write(base64.b64decode(base64_video))

audio_file_path = "audio/audio_1.mpeg"  # Replace with the path to your audio file
base64_audio = read_audio_file(audio_file_path)


data = {
    "name": "Tate",  # Replace with your desired name
    "audio": base64_audio
}

headers = {'Content-Type': 'application/json'}

response = requests.post(url, data=json.dumps(data), headers=headers)

received_data = response.json()

if received_data["status"] == "success":
    base64_video = received_data["base64_video"]
    output_video_path = "deep_fakes/test_success_fuck_yeah.mp4"
    save_video_file(base64_video, output_video_path)
    print(f"Video saved at {output_video_path}")
else:
    print("Error occurred")