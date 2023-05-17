import os
import json
import cv2
import numpy as np
from mutagen.mp3 import MP3
import ffmpeg
from pydub import AudioSegment
import requests
import base64
from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip, clips_array

def save_video_file(base64_video, file_path):
    with open(file_path, "wb") as video_file:
        video_file.write(base64.b64decode(base64_video))

def read_audio_file(file_path):
    with open(file_path, "rb") as audio_file:
        return base64.b64encode(audio_file.read()).decode('utf-8')

def get_mpeg_length(audio_file):
    audio = MP3(audio_file)
    audio_length = audio.info.length
    return audio_length

def get_mp4_length(video_file):
    cap = cv2.VideoCapture(video_file)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    video_length = frame_count / fps
    cap.release()
    return video_length


def horizontal_combine_videos(video_file_1, video_file_2, output_file):
    video1 = VideoFileClip(video_file_1)
    video2 = VideoFileClip(video_file_2)

    video1 = video1.resize(height=video2.h)  # ensure both videos have the same height
    combined_video = clips_array([[video1, video2]])

    combined_video.write_videofile(output_file)

def stack_videos_vertically(video1_path, video2_path, output_path):
    # Load video clips
    video1 = VideoFileClip(video1_path)
    video2 = VideoFileClip(video2_path)

    # Make sure both videos have the same width
    width = max(video1.w, video2.w)
    video1 = video1.resize(width=width)
    video2 = video2.resize(width=width)

    # Stack the videos vertically
    stacked_videos = clips_array([[video1], [video2]])

    # Write the result to a file
    stacked_videos.write_videofile(output_path, codec='libx264', audio_codec='aac')


def append_vids(video1, video2, output):
    clip1 = VideoFileClip(video1)
    clip2 = VideoFileClip(video2)

    final_clip = concatenate_videoclips([clip1, clip2])
    final_clip.write_videofile(output)


# USING OPENCV - REMOVES AUDIO
def trim_video(input_video_file, output_video_file, trim_seconds):
    cap = cv2.VideoCapture(input_video_file)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video_file, fourcc, fps, (width, height))

    max_frames = trim_seconds * fps
    current_frame = 0

    while cap.isOpened():
        ret, frame = cap.read()

        if ret and current_frame < max_frames:
            out.write(frame)
            current_frame += 1
        else:
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

# USING MOVIEPY - keeps audio
# def trim_video(input_file, output_file, duration):
#     video = VideoFileClip(input_file)
#     trimmed_video = video.subclip(0, duration)
#     trimmed_video.write_videofile(output_file)

def loop_video_to_length(length, vid, output_path):
    i = 0
    append_vids(vid, vid, "temp/loop_temp0.mp4")
    while get_mp4_length(f"temp/loop_temp{i}.mp4") < 30:
        append_vids(vid, f"temp/loop_temp{i}.mp4", f"temp/loop_temp{i + 1}.mp4")
        i += 1

    append_vids(vid, f"temp/loop_temp{i}.mp4", output_path)

    while os.path.exists(f"temp/loop_temp{i}.mp4"):
        os.remove(f"temp/loop_temp{i}.mp4")
        i -= 1

def remove_audio_from_mp4(input_file, output_file):
    # Load the input video file
    video = VideoFileClip(input_file)

    # Remove audio
    video_without_audio = video.without_audio()

    # Write the output video file
    video_without_audio.write_videofile(output_file, codec='libx264')

def attach_audio_to_video(video_file, mp3_audio_file, output_file):
    video_stream = ffmpeg.input(video_file)
    audio_stream = ffmpeg.input(mp3_audio_file)

    output = ffmpeg.output(video_stream, audio_stream, output_file, vcodec='copy', acodec='aac', strict='experimental')
    ffmpeg.run(output)

def mix_audio_files(main_audio_file, background_audio_file, output_file, background_volume=-10):
    main_audio = AudioSegment.from_mp3(main_audio_file)
    background_audio = AudioSegment.from_mp3(background_audio_file)

    # Set the background audio volume
    background_audio = background_audio + background_volume

    # Overlay the audio files
    combined_audio = main_audio.overlay(background_audio)

    # Export the output file
    combined_audio.export(output_file, format="mp3")

def append_audio_files(audio_files, source, output_file):
    combined_audio = AudioSegment.empty()

    for audio_file in audio_files:
        audio = AudioSegment.from_mp3(os.path.join(source, audio_file))
        combined_audio += audio

    combined_audio.export(output_file, format="mp3")




