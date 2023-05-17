# Spitfire-API

## To use video utils:

Clone the respository vertical-vid branch

```bash
git clone --branch vertical-vid https://github.com/patelisii/spitfire-API.git
```

Navigate to the repository and create a python virtual environment (or with anaconda). I used python 3.9.16
```bash
python -m venv spitfire_api_venv
```

Install Dependencies
```bash
pip install -r requirements.txt
```

# Video Utils

This Python file provides a set of utility functions to edit video and audio files. Below is a detailed explanation of each function and how to use them.

## Functions

### save_video_file(base64_video, file_path)

This function saves a video file from a base64 encoded string.

#### Parameters
- base64_video: The base64 encoded string of the video file.
- file_path: The desired file path to save the video file.

#### Usage
```python
save_video_file(base64_video_string, "output/video.mp4")
```

### read_audio_file(file_path)

This function reads an audio file and returns its base64 encoded string.

#### Parameters
- file_path: The file path of the audio file.

#### Returns
- A base64 encoded string of the audio file.

#### Usage
```python
base64_audio = read_audio_file("input/audio.mp3")
```

### get_mpeg_length(audio_file)

This function returns the length (in seconds) of an MPEG audio file.

#### Parameters
- audio_file: The file path of the MPEG audio file.

#### Returns
- The length of the audio file in seconds.

#### Usage
```python
audio_length = get_mpeg_length("input/audio.mp3")
```

```

### get_mp4_length(video_file)

This function returns the length (in seconds) of an MP4 video file.

#### Parameters
- video_file: The file path of the MP4 video file.

#### Returns
- The length of the video file in seconds.

#### Usage
```python
video_length = get_mp4_length("input/video.mp4")
```

### horizontal_combine_videos(video_file_1, video_file_2, output_file)

This function combines two video files horizontally and saves the result as a new video file.

#### Parameters
- video_file_1: The file path of the first video file.
- video_file_2: The file path of the second video file.
- output_file: The file path for the output video file.

#### Usage
```python
horizontal_combine_videos("input/video1.mp4", "input/video2.mp4", "output/combined_video.mp4")
```

### stack_videos_vertically(video1_path, video2_path, output_path)

This function stacks two video files vertically and saves the result as a new video file.

#### Parameters
- video1_path: The file path of the first video file.
- video2_path: The file path of the second video file.
- output_path: The file path for the output video file.

#### Usage
```python
stack_videos_vertically("input/video1.mp4", "input/video2.mp4", "output/stacked_video.mp4")
```

### append_vids(video1, video2, output)

This function appends two video files and saves the result as a new video file.

#### Parameters
- video1: The file path of the first video file.
- video2: The file path of the second video file.
- output: The file path for the output video file.

#### Usage
```python
append_vids("input/video1.mp4", "input/video2.mp4", "output/appended_video.mp4")
```

### trim_video(input_video_file, output_video_file, trim_seconds)

This function trims a video file to a specific length in seconds, removing audio in the process.

#### Parameters
- input_video_file: The file path of the input video file.
- output_video_file: The file path for the output trimmed video file.
- trim_seconds: The desired length of the trimmed video in seconds.

#### Usage
```python
trim_video("input/video.mp4", "output/trimmed_video.mp4", 10)
```

### loop_video_to_length(length, vid, output_path)

This function loops a video file until it reaches a specific length in seconds.

#### Parameters
- length: The desired length of the output video in seconds.
- vid: The file path of the input video file.
- output_path: The file path for the output looped video file.

#### Usage
```python
loop_video_to_length(30, "input/video.mp4", "output/looped_video.mp4")
```

### remove_audio_from_mp4(input_file, output_file)

This function removes audio from an MP4 video file and saves the result as a new video file.

#### Parameters
- input_file: The file path of the input video file.
- output_file: The file path for the output video file without audio.

#### Usage
```python
remove_audio_from_mp4("input/video.mp4", "output/video_without_audio.mp4")
```

### attach_audio_to_video(video_file, mp3_audio_file, output_file)

This function attaches an MP3 audio file to a video file and saves the result as a new video file.

#### Parameters
- video_file: The file path of the input video file.
- mp3_audio_file: The file path of the input MP3 audio file.
- output_file: The file path for the output video file with the attached audio.

#### Usage
```python
attach_audio_to_video("input/video.mp4", "input/audio.mp3", "output/video_with_audio.mp4")
```

### mix_audio_files(main_audio_file, background_audio_file, output_file, background_volume=-10)

This function mixes two audio files, adjusting the background audio volume, and saves the result as a new audio file.

#### Parameters
- main_audio_file: The file path of the main audio file.
- background_audio_file: The file path of the background audio file.
- output_file: The file path for the output mixed audio file.
- background_volume: The volume adjustment for the background audio in dB (default: -10 dB).

#### Usage
```python
mix_audio_files("input/main_audio.mp3", "input/background_audio.mp3", "output/mixed_audio.mp3")
```

### append_audio_files(audio_files, source, output_file)

This function appends a list of audio files and saves the result as a new audio file.

#### Parameters
- audio_files: A list of audio file names to be appended.
- source: The directory path containing the audio files.
- output_file: The file path for the output appended audio file.

#### Usage
```python
audio_files_list = ["audio1.mp3", "audio2.mp3", "audio3.mp3"]
append_audio_files(audio_files_list, "input/audio_files", "output/appended_audio.mp3")
```