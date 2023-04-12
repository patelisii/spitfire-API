
import os
import requests
import json
import base64


def save_video_file(base64_video, file_path):
    with open(file_path, "wb") as video_file:
        video_file.write(base64.b64decode(base64_video))

def request_deep_fake(url, person, base64_audio, output_path):

    data = {
        "name": person,  # Replace with your desired name
        "audio": base64_audio
    }

    headers = {'Content-Type': 'application/json'}

    response = requests.post(url, data=json.dumps(data), headers=headers)
    received_data = response.json()

    if received_data["status"] == "success":
        base64_video = received_data["base64_video"]
        save_video_file(base64_video, output_path)
        print(f"Video saved at {output_path}")
    else:
        print("Error occurred")
        print(received_data)

def create_deepfakes_from_bytes(url, audio_files, person1, person2):

    for i in range(len(audio_files)):
        print(f"Now making video for audio{i}...")
        if i%2==0:
            request_deep_fake(url, person1, audio_files[i], f"deep_fakes/vid_{i}.mp4")
        else:
            request_deep_fake(url, person2, audio_files[i], f"deep_fakes/vid_{i}.mp4")

with open('testing/test_call.json') as f:
  data1 = f.read()

jdata = json.loads(data1)

print("Calling API...")
create_deepfakes_from_bytes("http://12de-34-86-179-3.ngrok.io/deepfake", jdata["versesAudio"], "Trump", "Obama")

print("Done!")