import os
import shutil
import cv2
import numpy as np
from mutagen.mp3 import MP3
import ffmpeg
from pydub import AudioSegment


def fetch_face_image(person, rap):
    # Import database module.
    from firebase_admin import db

    # Get a database reference to our posts
    ref = db.reference(f'path/to/faces/face_videos/{person} {rap} Video.mp4')

    # Read the data at the posts reference (this is a blocking operation)
    return ref.get()

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

def combine_videos(video_file_1, video_file_2, output_file):
    cap1 = cv2.VideoCapture(video_file_1)
    cap2 = cv2.VideoCapture(video_file_2)

    width1 = int(cap1.get(cv2.CAP_PROP_FRAME_WIDTH))
    height1 = int(cap1.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width2 = int(cap2.get(cv2.CAP_PROP_FRAME_WIDTH))
    height2 = int(cap2.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fps1 = int(cap1.get(cv2.CAP_PROP_FPS))
    fps2 = int(cap2.get(cv2.CAP_PROP_FPS))

    output_width = width1 + width2
    output_height = max(height1, height2)
    output_fps = min(fps1, fps2)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    out = cv2.VideoWriter(output_file, fourcc, output_fps, (output_width, output_height))

    while cap1.isOpened() and cap2.isOpened():
        ret1, frame1 = cap1.read()
        ret2, frame2 = cap2.read()

        if ret1 and ret2:
            frame1_resized = cv2.resize(frame1, (width1, output_height))
            frame2_resized = cv2.resize(frame2, (width2, output_height))

            combined_frame = np.hstack((frame1_resized, frame2_resized))
            out.write(combined_frame)

        else:
            break

    cap1.release()
    cap2.release()
    out.release()
    cv2.destroyAllWindows()

def append_video(video_file_1, video_file_2, output_file):
    cap1 = cv2.VideoCapture(video_file_1)
    cap2 = cv2.VideoCapture(video_file_2)

    width1 = int(cap1.get(cv2.CAP_PROP_FRAME_WIDTH))
    height1 = int(cap1.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps1 = int(cap1.get(cv2.CAP_PROP_FPS))

    width2 = int(cap2.get(cv2.CAP_PROP_FRAME_WIDTH))
    height2 = int(cap2.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps2 = int(cap2.get(cv2.CAP_PROP_FPS))

    output_width = min(width1, width2)
    output_height = min(height1, height2)
    output_fps = min(fps1, fps2)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    out = cv2.VideoWriter(output_file, fourcc, output_fps, (output_width, output_height))

    # Write video1 frames to output video
    while cap1.isOpened():
        ret, frame = cap1.read()

        if ret:
            frame_resized = cv2.resize(frame, (output_width, output_height))
            out.write(frame_resized)
        else:
            break

    # Write video2 frames to output video
    while cap2.isOpened():
        ret, frame = cap2.read()

        if ret:
            frame_resized = cv2.resize(frame, (output_width, output_height))
            out.write(frame_resized)
        else:
            break

    cap1.release()
    cap2.release()
    out.release()
    cv2.destroyAllWindows()



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

def gen_face_video(length, vid, output_path):

    append_video(vid, vid, "temp0.mp4")
    append_video("temp0.mp4", vid, "temp1.mp4")
    append_video("temp1.mp4", vid, "temp2.mp4")
    append_video("temp2.mp4", vid, "temp3.mp4")
    append_video("temp3.mp4", "temp2.mp4", "temp4.mp4")
    append_video("temp4.mp4", "temp3.mp4", "temp5.mp4")
    trim_video("temp5.mp4", output_path, length)

    if os.path.exists("temp0.mp4"):
        os.remove("temp0.mp4")
    if os.path.exists("temp1.mp4"):
        os.remove("temp1.mp4")
    if os.path.exists("temp2.mp4"):
        os.remove("temp2.mp4")
    if os.path.exists("temp3.mp4"):
        os.remove("temp3.mp4")
    if os.path.exists("temp4.mp4"):
        os.remove("temp4.mp4")
    if os.path.exists("temp5.mp4"):
        os.remove("temp5.mp4")


def gen_faces_video(length, person_1, person_2, i, output_path):
    faceVid1 = f"face_videos/{person_1} D Video.mp4"
    faceVid2 = f"face_videos/{person_2} A Video.mp4"
    if i%2==0:
        faceVid1 = f"face_videos/{person_1} A Video.mp4"
        faceVid2 = f"face_videos/{person_2} D Video.mp4"

    vid1 = "roastervid.mp4"
    vid2 = "roastedvid.mp4"

    gen_face_video(length, faceVid1, vid1)
    gen_face_video(length, faceVid2, vid2)

    combine_videos(vid1, vid2, output_path)

    if os.path.exists(vid1):
        os.remove(vid1)
    if os.path.exists(vid2):
        os.remove(vid2)

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



def create_video(audio_files, first_speaker, second_speaker):
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

    # for file in audio_files:
    #     os.rename("file")

    for i in range(len(audio_files)):
        face_temp_file = f"face_video_{i}.mp4"
        file_path = os.path.join(AUDIO_FILES_DIR, audio_files[i])
        gen_faces_video(get_mpeg_length(file_path), first_speaker, second_speaker, i, face_temp_file)

        final_temp = f"final_{i}.mp4"
        if i==0:
            pass
        elif i==1:
            append_video(f"face_video_0.mp4", face_temp_file, final_temp)
        else:
            append_video(f"final_{i-1}.mp4", face_temp_file, final_temp)

    append_audio_files(audio_files, AUDIO_FILES_DIR, "audio_temp.mp3")
    mix_audio_files("audio_temp.mp3", "beats/beat1.mp3", "mixed.mp3")
    attach_audio_to_video(f"final_{len(audio_files)-1}.mp4", "mixed.mp3", "output.mp4")

    # Delete temporary files
    for i in range(len(audio_files)):
        if os.path.exists(f"face_video_{i}.mp4"):
            os.remove(f"face_video_{i}.mp4")
        if os.path.exists(f"final_{i}.mp4"):
            os.remove(f"final_{i}.mp4")
        # if os.path.exists(f"audio/audio_{i}.mpeg"):
        #     os.remove(f"audio/audio_{i}.mpeg")
    if os.path.exists("audio_temp.mp3"):
        os.remove("audio_temp.mp3")
    if os.path.exists("mixed.mp3"):
        os.remove("mixed.mp3")



