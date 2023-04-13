from spitfire_deepfake import *

print(get_mpeg_length("../temp/mixed.mp3"))
print(get_mp4_length("../temp/final_7.mp4"))

attach_audio_to_video(f"../temp/final_7.mp4", "../temp/mixed.mp3", "output.mp4")