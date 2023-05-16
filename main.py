from flask import Flask, request, jsonify
from spitfire_deepfake import *
import base64
import traceback


app = Flask(__name__)



@app.route('/')
def hello():
    return "Welcome to the Spitfire API!"


@app.route('/create_video', methods=['POST'])
def create_video_api():

    data = request.get_json()

    first_speaker = data['rapper1']
    second_speaker = data['rapper2']
    audio_files = data['versesAudio']
    video_type = data['videoType']
    wav2lipURL = data['wav2lipURL']

    file_paths=[]
    w=0
    try:
        for i in range(len(audio_files)):
            if audio_files[i] is None:
                continue
            save_mpeg_from_base64(audio_files[i], f"audio/audio_{w}.mpeg")
            file_paths.append(f"audio_{w}.mpeg")
            w+=1

        if video_type=="deepfake":
            # create deep fake videos
            print("Creating Deepfakes...")

            create_deepfakes_from_bytes(wav2lipURL, audio_files, first_speaker, second_speaker)
            print("Done!")

        # check if wav2lip failed
        if (len(os.listdir("deep_fakes")) != len(os.listdir("audio"))) and video_type == "deepfake":
            print("Deep fake failed, using gifs...")
            video_type = "gif"

        print("Creating Videos...")
        # Call the create_video function
        create_video(file_paths, first_speaker, second_speaker, video_type)
        print("Done!")

        # Send back the final output.mp4
        base64_video = mp4_to_base64("output.mp4")
        # os.remove("output.mp4")

        response = jsonify({
            "status": "success",
            "base64_video": base64_video
        })
        response.headers.set('Content-Type', 'application/json')
    except Exception as e:
        error_message = str(e) + "\n" + traceback.format_exc()
        clear_files(audio_files)
        response = jsonify({
            "status": "failed",
            "error": error_message
        })
        response.headers.set('Content-Type', 'application/json')

    return response

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def save_mpeg_from_base64(base64_data, output_path):
    with open(output_path, 'wb') as f:
        f.write(base64.b64decode(base64_data))

def mp4_to_base64(file_path):
    with open(file_path, 'rb') as f:
        file_data = f.read()
        base64_data = base64.b64encode(file_data).decode('utf-8')
    return base64_data

if __name__ == '__main__':
    # FOR DEPLOYMENT:
    # port = int(os.environ.get("PORT", 8080))
    # app.run(debug=True, host='0.0.0.0', port=port)
    app.run()

