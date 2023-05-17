import os
import json
import cv2
import numpy as np
from mutagen.mp3 import MP3
import ffmpeg
from pydub import AudioSegment
import requests
import base64
from video_utils import *


def gen_faces_video_deepfake(length, person_1, person_2, i, output_path):
    vid1 = "temp/left.mp4"
    vid2 = "temp/right.mp4"

    if i%2==0:
        trim_video(f"deep_fakes/vid_{i}.mp4", vid1, length)
        faceVid2 = f"D_face_videos/{person_2}_D.mp4"
        # vid_len = get_mp4_length(vid1)
        trim_video(faceVid2, vid2, length)
    else:
        trim_video(f"deep_fakes/vid_{i}.mp4", vid2, length)
        faceVid1 = f"D_face_videos/{person_1}_D.mp4"
        # vid_len = get_mp4_length(vid2)
        trim_video(faceVid1, vid1, length)

    horizontal_combine_videos(vid1, vid2, output_path)
    # vertical_combine_videos(vid1, vid2, output_path)

    if os.path.exists("temp/left.mp4"):
        os.remove("temp/left.mp4")
    if os.path.exists("temp/right.mp4"):
        os.remove("temp/right.mp4")

def gen_faces_video_gif(length, person_1, person_2, i, output_path):

    # TODO: Ensure videos length are at least audio length

    vid1 = "temp/left.mp4"
    vid2 = "temp/right.mp4"

    if i%2==0:
        faceVid1 = f"A_face_videos/{person_1}_ALong.mp4"
        faceVid2 = f"D_face_videos/{person_2}_D.mp4"
        trim_video(faceVid1, vid1, length)
        trim_video(faceVid2, vid2, length)
    else:
        faceVid2 = f"A_face_videos/{person_2}_ALong.mp4"
        faceVid1 = f"D_face_videos/{person_1}_D.mp4"
        trim_video(faceVid1, vid1, length)
        trim_video(faceVid2, vid2, length)

    horizontal_combine_videos(vid1, vid2, output_path)
    # vertical_combine_videos(vid1, vid2, output_path)

    if os.path.exists("temp/left.mp4"):
        os.remove("temp/left.mp4")
    if os.path.exists("temp/right.mp4"):
        os.remove("temp/right.mp4")


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

def create_deepfakes_from_files(url, audio_files, person1, person2):

    for i in range(len(audio_files)):
        print(f"Now making video for {audio_files[i]}...")
        if i%2==0:
            audio_bytes = read_audio_file(audio_files[i])
            request_deep_fake(url, person1, audio_bytes, f"deep_fakes/vid_{i}.mp4")
        else:
            audio_bytes = read_audio_file(audio_files[i])
            request_deep_fake(url, person2, audio_bytes, f"deep_fakes/vid_{i}.mp4")

def create_deepfakes_from_bytes(url, audio_files, person1, person2):

    for i in range(len(audio_files)):
        print(f"Now making video for audio{i}...")
        if i%2==0:
            request_deep_fake(url, person1, audio_files[i], f"deep_fakes/vid_{i}.mp4")
        else:
            request_deep_fake(url, person2, audio_files[i], f"deep_fakes/vid_{i}.mp4")

def clear_files(audio_files):
    for i in range(len(audio_files)):
        if os.path.exists(f"temp/face_video_{i}.mp4"):
            os.remove(f"temp/face_video_{i}.mp4")
        if os.path.exists(f"temp/final_{i}.mp4"):
            os.remove(f"temp/final_{i}.mp4")
        if os.path.exists(f"audio/audio_{i}.mpeg"):
            os.remove(f"audio/audio_{i}.mpeg")
        if os.path.exists(f"deep_fakes/vid_{i}.mp4"):
            os.remove(f"deep_fakes/vid_{i}.mp4")
    if os.path.exists("temp/audio_temp.mp3"):
        os.remove("temp/audio_temp.mp3")
    if os.path.exists("temp/mixed.mp3"):
        os.remove("temp/mixed.mp3")
    if os.path.exists("temp/temp_adhd.mp4"):
        os.remove("temp/temp_adhd.mp4")
    if os.path.exists("temp/draft.mp4"):
        os.remove("temp/draft.mp4")

def create_video(audio_files, first_speaker, second_speaker, type):
    """
    init_video = intro vid
    for each audio file:
      get length of audio file
      generate face videos of length audio file
      combine face vids
      add audio to vid
      add beat overlay to vid
      append vid to init_video
    """

    AUDIO_FILES_DIR = "audio"

    for i in range(len(audio_files)):
        face_temp_file = f"temp/face_video_{i}.mp4"
        file_path = os.path.join(AUDIO_FILES_DIR, audio_files[i])
        print(f"Making Video for {file_path}...")
        if type=="deepfake":
            gen_faces_video_deepfake(get_mpeg_length(file_path), first_speaker, second_speaker, i, face_temp_file)
        else:
            gen_faces_video_gif(get_mpeg_length(file_path), first_speaker, second_speaker, i, face_temp_file)

        final_temp = f"temp/final_{i}.mp4"
        if i==0:
            pass
        elif i==1:
            append_vids(f"temp/face_video_0.mp4", face_temp_file, final_temp)
        else:
            append_vids(f"temp/final_{i-1}.mp4", face_temp_file, final_temp)

    append_audio_files(audio_files, AUDIO_FILES_DIR, "temp/audio_temp.mp3")
    mix_audio_files("temp/audio_temp.mp3", "beats/beat1.mp3", "temp/mixed.mp3")

    # attach ADHD video
    adhd_vid = "ADD_vids/subway_surf.mp4"
    trim_video(adhd_vid, "temp/temp_adhd.mp4", get_mpeg_length("temp/mixed.mp3"))
    stack_videos_vertically(f"temp/final_{len(audio_files)-1}.mp4", "temp/temp_adhd.mp4", "temp/draft.mp4")

    attach_audio_to_video("temp/draft.mp4", "temp/mixed.mp3", "output.mp4")

    # Delete temporary files
    clear_files(audio_files)

