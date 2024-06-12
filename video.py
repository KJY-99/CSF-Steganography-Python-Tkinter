import cv2, numpy as np
from tkinter import filedialog
from moviepy.editor import VideoFileClip, AudioFileClip
from img import encode_img, decode_img, to_bin
import os
import shutil

def video_split(video_path):
    frame_dir = "frameholder"
    if os.path.exists(frame_dir):
        shutil.rmtree(frame_dir)
    os.makedirs(frame_dir, exist_ok=True)
    vidcap = cv2.VideoCapture(video_path)
    if not vidcap.isOpened():
        print("Error: Could not open video.")
        return
    count=0
    while True:
        success, image = vidcap.read()
        if not success:
            break
        cv2.imwrite((frame_dir + "\\{:d}.png".format(count)), image)
        count += 1
    vidcap.release()
    print("Video has been split in frames.")


def extract_audio(video_path):
    audio_dir = "audioholder"
    if os.path.exists(audio_dir):
        shutil.rmtree(audio_dir)
    os.makedirs(audio_dir, exist_ok=True)
    video = VideoFileClip(video_path)
    audio = video.audio
    if audio == None:
        print("Video has no audio")
        return
    audio.write_audiofile(audio_dir +"\\audio.wav")
    video.close()
    audio.close()

def frame_encode(frame_list,secret,bit_length):
    secret = "-----" + secret
    secret += "-----"
    segment_length = len(secret) // len(frame_list)
    remainder = len(secret) % len(frame_list)
    message_segments = [segment_length * i + min(i, remainder) for i in range(len(frame_list))]
    message_segments.append(len(secret))
    message_segments = message_segments[1:]
    split_parts = [secret[start:end] for start, end in zip([0] + message_segments, message_segments)]
    for i in range(0,len(frame_list)):
        print(split_parts[i])
        print(bit_length)
        encode_message(split_parts[i],frame_list[i],frame_list[i],bit_length)
    print("Encoded video frames saved successfully.")
    

def frames_to_video(video_path,secret,bit_length):
    frames= [f for f in os.listdir("frameholder") if f.endswith('.png')]
    frames= sorted(frames, key=lambda x: int(x.split('.')[0]))
    frames= [os.path.join("frameholder", f) for f in frames]
    frame_encode(frames,secret,bit_length)
    frame = cv2.imread(frames[0])
    height, width, layers = frame.shape
    fourcc = cv2.VideoWriter_fourcc(*'FFV1')
    video_dir = "videoholder"
    if os.path.exists(video_dir):
        shutil.rmtree(video_dir)
    os.makedirs(video_dir, exist_ok=True)
    vidcap = cv2.VideoCapture(video_path)
    if not vidcap.isOpened():
        print("Error: Could not open video.")
        return
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    vidcap.release()
    video = cv2.VideoWriter(video_dir +"\\noaudio.avi", fourcc, fps, (width, height))
    for frame in frames:
        img = cv2.imread(frame)
        video.write(img)
    video.release()

def add_audio_to_video():
    try :
        video_clip = VideoFileClip("videoholder\\noaudio.avi")
        audio_clip = AudioFileClip("audioholder\\audio.wav")
        video_clip = video_clip.set_audio(audio_clip)
    except Exception as e:
        print("Error:", e)
    finally:
        video_clip.write_videofile("output_video.avi", codec='ffv1', audio_codec='aac')
    

def encode_message(secret_message,image_path,output_file_path,bit_length):
    # Encode the secret message into the image
    try:
        encoded_image = encode_img(image_path, secret_message,bit_length)
    except Exception as e:
        print("Error:", e)
        return
    cv2.imwrite(output_file_path, encoded_image)

def frame_decode(bit_length):
    print("Start decoding")
    message = ""
    frames= [f for f in os.listdir("frameholder") if f.endswith('.png')]
    frames= sorted(frames, key=lambda x: int(x.split('.')[0]))
    frames= [os.path.join("frameholder", f) for f in frames]
    for f in frames:
        try:
            message += decode_img(f,bit_length)
        except Exception as e:
            raise ValueError(e)
        if len(message) >= 5  and message[:5] != "-----":
                print("stopped")
                raise ValueError("Error Decoding")
        if len(message) >= 10  and message[-5:] == "-----":
            print("Secret message retrieved.")
            message = message[5:]
            return message[:-5]
    return message


def cleandir():
        # If it exists, delete it
    if os.path.exists("audioholder"):
        shutil.rmtree("audioholder")
    if os.path.exists("frameholder"):
        shutil.rmtree("frameholder")
    if os.path.exists("encodedframeholder"):
        shutil.rmtree("encodedframeholder")
    if os.path.exists("videoholder"):
        shutil.rmtree("videoholder")

# video encryption
def video_encryption(video_path,secret,bit_length):
    video_split(video_path)
    extract_audio(video_path)
    frames_to_video(video_path,secret,bit_length)
    add_audio_to_video()
    cleandir()
# video decryption
def video_decryption(encoded_video_path,bit_length):
    video_split(encoded_video_path)
    return(frame_decode(bit_length))

def image_to_binary(image_path):
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    success, encoded_image = cv2.imencode('.png', image)
    if not success:
        raise ValueError("Image encoding failed")
    binary_data = encoded_image.tobytes()
    binary_string = ''.join(format(byte, '08b') for byte in binary_data)
    decoded_data = ""
    all_bytes = [ binary_string[i: i+8] for i in range(0, len (binary_string), 8) ]
    for byte in all_bytes:
        decoded_data += chr (int(byte, 2))
    return decoded_data

def binary_to_image(binary_data):
    binary_string = to_bin(binary_data)
    binary_data = bytes(int(binary_string[i:i+8], 2) for i in range(0, len(binary_string), 8))
    nparr = np.frombuffer(binary_data, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if image is None:
        raise ValueError("Image decoding failed")
    return image
# video_path = "video.avi"
# encoded_video_path ="output_video.avi"
# bit_length = 2
# input_image_path = "test.png"
# #secret = image_to_binary(input_image_path)
# secret = "test"
# output_image_path = "hidden.png"

# video_encryption(video_path,secret,bit_length)
# secret_encoded =video_decryption(encoded_video_path,bit_length)
# print(secret_encoded)
# #binary_to_image(secret_encoded)
# cleandir()