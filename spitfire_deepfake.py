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
import moviepy.video.fx.all as vfx

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

# def horizontal_combine_videos(video_file_1, video_file_2, output_file):
#     cap1 = cv2.VideoCapture(video_file_1)
#     cap2 = cv2.VideoCapture(video_file_2)
#
#     width1 = int(cap1.get(cv2.CAP_PROP_FRAME_WIDTH))
#     height1 = int(cap1.get(cv2.CAP_PROP_FRAME_HEIGHT))
#     width2 = int(cap2.get(cv2.CAP_PROP_FRAME_WIDTH))
#     height2 = int(cap2.get(cv2.CAP_PROP_FRAME_HEIGHT))
#
#     fps1 = int(cap1.get(cv2.CAP_PROP_FPS))
#     fps2 = int(cap2.get(cv2.CAP_PROP_FPS))
#
#     output_width = width1 + width2
#     output_height = max(height1, height2)
#     output_fps = min(fps1, fps2)
#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#
#     out = cv2.VideoWriter(output_file, fourcc, output_fps, (output_width, output_height))
#
#     while cap1.isOpened() and cap2.isOpened():
#         ret1, frame1 = cap1.read()
#         ret2, frame2 = cap2.read()
#
#         if ret1 and ret2:
#             frame1_resized = cv2.resize(frame1, (width1, output_height))
#             frame2_resized = cv2.resize(frame2, (width2, output_height))
#
#             combined_frame = np.hstack((frame1_resized, frame2_resized))
#             out.write(combined_frame)
#
#         else:
#             break
#
#     cap1.release()
#     cap2.release()
#     out.release()
#     cv2.destroyAllWindows()

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


# def append_vids(video1, video2, output):
#     # Create a temporary file with the list of input video files
#     with open("input_list.txt", "w") as f:
#         f.write(f"file '{video1}'\n")
#         f.write(f"file '{video2}'\n")
#
#     # Call ffmpeg to concatenate the video files
#     command = f"ffmpeg -f concat -safe 0 -i input_list.txt -c copy {output}"
#     os.system(command)
#
#     if os.path.exists("input_list.txt"):
#         os.remove("input_list.txt")
def append_vids(video1, video2, output):
    clip1 = VideoFileClip(video1)
    clip2 = VideoFileClip(video2)

    final_clip = concatenate_videoclips([clip1, clip2])
    final_clip.write_videofile(output)

# def append_video(video_file_1, video_file_2, output_file):
#     cap1 = cv2.VideoCapture(video_file_1)
#     cap2 = cv2.VideoCapture(video_file_2)
#
#     width1 = int(cap1.get(cv2.CAP_PROP_FRAME_WIDTH))
#     height1 = int(cap1.get(cv2.CAP_PROP_FRAME_HEIGHT))
#     fps1 = int(cap1.get(cv2.CAP_PROP_FPS))
#
#     width2 = int(cap2.get(cv2.CAP_PROP_FRAME_WIDTH))
#     height2 = int(cap2.get(cv2.CAP_PROP_FRAME_HEIGHT))
#     fps2 = int(cap2.get(cv2.CAP_PROP_FPS))
#
#     output_width = min(width1, width2)
#     output_height = min(height1, height2)
#     output_fps = min(fps1, fps2)
#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#
#     out = cv2.VideoWriter(output_file, fourcc, output_fps, (output_width, output_height))
#
#     # Write video1 frames to output video
#     while cap1.isOpened():
#         ret, frame = cap1.read()
#
#         if ret:
#             frame_resized = cv2.resize(frame, (output_width, output_height))
#             out.write(frame_resized)
#         else:
#             break
#
#     # Write video2 frames to output video
#     while cap2.isOpened():
#         ret, frame = cap2.read()
#
#         if ret:
#             frame_resized = cv2.resize(frame, (output_width, output_height))
#             out.write(frame_resized)
#         else:
#             break
#
#     cap1.release()
#     cap2.release()
#     out.release()
#     cv2.destroyAllWindows()



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

# def trim_video(input_file, output_file, duration):
#     start_time=0
#     stream = ffmpeg.input(input_file)
#     stream = ffmpeg.trim(stream, start=start_time, duration=duration)
#     stream = ffmpeg.output(stream, output_file)
#     ffmpeg.run(stream)

# def trim_video(input_file, output_file, duration):
#     video = VideoFileClip(input_file)
#     trimmed_video = video.subclip(0, duration)
#     trimmed_video.write_videofile(output_file)

def loop_face_video(length, vid, output_path):
    i = 0
    append_vids(vid, vid, "temp/temp0.mp4")
    while get_mp4_length(f"temp/temp{i}.mp4") < 30:
        append_vids(vid, f"temp/temp{i}.mp4", f"temp/temp{i + 1}.mp4")
        i += 1

    append_vids(vid, f"temp/temp{i}.mp4", output_path)

    while os.path.exists(f"temp/temp{i}.mp4"):
        os.remove(f"temp/temp{i}.mp4")
        i -= 1

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

