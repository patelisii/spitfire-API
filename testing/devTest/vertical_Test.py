import os
import cv2
import ffmpeg
from moviepy.editor import VideoFileClip, clips_array

os.chdir("/Users/patrickelisii/PycharmProjects/spitfire-API")
print(os.getcwd())

def trim_video(input_file, output_file, duration):
    start_time=0
    stream = ffmpeg.input(input_file)
    stream = ffmpeg.trim(stream, start=start_time, duration=duration)
    stream = ffmpeg.output(stream, output_file)
    ffmpeg.run(stream)


def ffmpeg_trim(input_video_file, output_video_file, trim_seconds):


    os.system(f"ffmpeg -i {input_video_file} -ss 00:00:00 -t 00:00:{trim_seconds} -c:v copy -c:a copy {output_video_file}")

# def trim_video(input_video_file, output_video_file, trim_seconds):
#     cap = cv2.VideoCapture(input_video_file)
#     width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#     height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#     fps = int(cap.get(cv2.CAP_PROP_FPS))
#
#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#     out = cv2.VideoWriter(output_video_file, fourcc, fps, (width, height))
#
#     max_frames = trim_seconds * fps
#     current_frame = 0
#
#     while cap.isOpened():
#         ret, frame = cap.read()
#
#         if ret and current_frame < max_frames:
#             out.write(frame)
#             current_frame += 1
#         else:
#             break
#
#     cap.release()
#     out.release()
#     cv2.destroyAllWindows()

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


input1 = "bigvid.mp4"
input2 = "ADD_vids/subway_surf.mp4"

trim_video(input1, "testing/devTest/top.mp4", 2)
trim_video(input2, "testing/devTest/bottom.mp4", 2)


output = "testing/devTest/vert.mp4"
# os.system(f"ffmpeg -i testing/devTest/top.mp4 -vf scale=640:480 -preset fast -crf 18 testing/devTest/temp_top.mp4")
# os.system(f"ffmpeg -i testing/devTest/bottom.mp4 -vf scale=640:480 -preset fast -crf 18 testing/devTest/temp_bottom.mp4")
print("DONE!")
stack_videos_vertically("testing/devTest/top.mp4", "testing/devTest/bottom.mp4", "testing/devTest/vert.mp4")
# os.system(f"ffmpeg -i testing/devTest/temp_top.mp4 -i testing/devTest/temp_bottom.mp4 -filter_complex vstack=inputs=2 -c:v h264_videotoolbox -preset fast -threads 0 {output}")


