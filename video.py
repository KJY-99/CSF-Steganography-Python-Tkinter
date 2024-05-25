import cv2, numpy as np
from tkinter import filedialog
from moviepy.editor import VideoFileClip, AudioFileClip
import os
import shutil

def video_split(video_path,frame_dir):
    # Folder creation
    # If it exists, delete it
    if os.path.exists(frame_dir):
        shutil.rmtree(frame_dir)

    # Creates the folder
    os.makedirs(frame_dir, exist_ok=True)

    # Opens the video
    vidcap = cv2.VideoCapture(video_path)
    if not vidcap.isOpened():
        print("Error: Could not open video.")
        return

    # splits the frame of video
    count=0
    while True:
        success, image = vidcap.read()
        if not success:
            break
        cv2.imwrite(os.path.join(frame_dir, "{:d}.png".format(count)), image)
        count += 1
    vidcap.release()
    print("Video has been split in frames.")


def extract_audio(video_path,audio_dir):
    # Load the video
    video = VideoFileClip(video_path)
    
    # Extract the audio
    audio = video.audio
    
    # If it exists, delete it
    if os.path.exists(audio_dir):
        shutil.rmtree(audio_dir)

    # Creates the folder
    os.makedirs(audio_dir, exist_ok=True)

    # Write the audio to file
    audio.write_audiofile(audio_dir +"\\audio.wav")

def frame_encode(frame_list,secret):
    secret = secret +"-----"
    segment_length = len(secret) // len(frame_list)
    remainder = len(secret) % len(frame_list)
    message_segments = [segment_length * i + min(i, remainder) for i in range(len(frame_list))]
    message_segments.append(len(secret))
    message_segments = message_segments[1:]
    split_parts = [secret[start:end] for start, end in zip([0] + message_segments, message_segments)]
    for i in range(0,len(frame_list)):
        encode_message(split_parts[i],frame_list[i],frame_list[i])
    print("Encoded video frames saved successfully.")
    

def frames_to_video(video_path,secret):
    # Get the list of frame files
    frames= [f for f in os.listdir("frameholder") if f.endswith('.png')]
    frames= sorted(frames, key=lambda x: int(x.split('.')[0]))
    frames= [os.path.join("frameholder", f) for f in frames]
    frame_encode(frames,secret)
    # Read the first frame to get the width and height
    frame = cv2.imread(frames[0])
    height, width, layers = frame.shape

    # Initialize the video writer
    fourcc = cv2.VideoWriter_fourcc(*'FFV1')

    # Folder creation
    video_dir = "videoholder"
    # If it exists, delete it
    if os.path.exists(video_dir):
        shutil.rmtree(video_dir)
    # Creates the folder
    os.makedirs(video_dir, exist_ok=True)
    # Opens the video
    vidcap = cv2.VideoCapture(video_path)
    if not vidcap.isOpened():
        print("Error: Could not open video.")
        return
    fps = vidcap.get(cv2.CAP_PROP_FPS)
    vidcap.release()

    video = cv2.VideoWriter(video_dir +"\\noaudio.avi", fourcc, fps, (width, height))

    # Write each frame to the video
    for frame in frames:
        img = cv2.imread(frame)
        video.write(img)

    # Release the video writer
    video.release()

def add_audio_to_video():
    # Load the video clip
    video_clip = VideoFileClip("videoholder\\noaudio.avi")
    
    # Load the audio clip
    audio_clip = AudioFileClip("audioholder\\audio.wav")
    
    # Set the audio of the video clip
    video_with_audio = video_clip.set_audio(audio_clip)
    
    # Write the final video file
    video_with_audio.write_videofile("output_video.avi", codec='ffv1', audio_codec='aac')

def encode_message(secret_message,image_path,output_file_path):
    # Encode the secret message into the image
    try:
        encoded_image = encode(image_path, secret_message)
    except Exception as e:
        print("Error:", e)
        return
    cv2.imwrite(output_file_path, encoded_image)

def to_bin(data):
    """Convert `data` to binary format as string"""
    if isinstance(data, str):
        return ''.join([format(ord(i), "08b") for i in data])
    elif isinstance(data, bytes) or isinstance(data, np.ndarray):
        return [format(i, "08b") for i in data]
    elif isinstance(data, int) or isinstance(data, np.uint8):
        return format(data, "08b")
    else:
        raise TypeError("Type not supported.")

def encode(image_name, secret_data):
    # Read the image
    image = cv2.imread(image_name)

    # Make a copy of the image to preserve the original
    encoded_image = np.copy(image)

    # Calculate the maximum bytes to encode
    n_bytes = encoded_image.shape[0] * encoded_image.shape[1] * 3 // 8
    #print("[*] Maximum bytes to encode:", n_bytes)

    # Add stopping criteria to the secret data
    secret_data += "====="

    # Check if the secret data fits within the image
    if len(secret_data) > n_bytes:
        raise ValueError("[!] Insufficient bytes, need a bigger image or less data.")

    #print("[*] Encoding data...")

    # Convert secret data to binary
    binary_secret_data = to_bin(secret_data)

    # Get the size of data to hide
    data_len = len(binary_secret_data)

    # Index to keep track of the current data position
    data_index = 0

    # Iterate through each pixel in the image
    for row in range(encoded_image.shape[0]):
        for col in range(encoded_image.shape[1]):
            # Get the pixel value (RGB)
            r, g, b = encoded_image[row, col]
            # Convert RGB values to binary format
            r_bin = to_bin(r)
            g_bin = to_bin(g)
            b_bin = to_bin(b)
            # Modify the least significant bit only if there is still data to store
            if data_index < data_len:
                r_bin = r_bin[:-1] + binary_secret_data[data_index]
                data_index += 1
            if data_index < data_len:
                g_bin = g_bin[:-1] + binary_secret_data[data_index]
                data_index += 1
            if data_index < data_len:
                b_bin = b_bin[:-1] + binary_secret_data[data_index]
                data_index += 1

            # Convert modified binary values back to decimal
            r = int(r_bin, 2)
            g = int(g_bin, 2)
            b = int(b_bin, 2)

            # Update the pixel value in the encoded image
            encoded_image[row, col] = [r, g, b]

            # Break out of the loop if data is encoded
            if data_index >= data_len:
                break

    return encoded_image

def frame_decode():
    print("Start decoding")
    message = ""
    frames= [f for f in os.listdir("encodedframeholder") if f.endswith('.png')]
    frames= sorted(frames, key=lambda x: int(x.split('.')[0]))
    frames= [os.path.join("encodedframeholder", f) for f in frames]
    for f in frames:
        print(message)
        message += decode(f)
        if message[-5:] == "-----":
            break
    print("Secret message retrieved.")
    return message[:-5]

def decode (image_name) :
    #print("[+] Decoding...")
    # read the image
    image = cv2.imread(image_name)
    binary_data = ""
    decoded_data = ""
    for row in image:
        for pixel in row:
            if len(binary_data) >= 8:
                decoded_data += chr (int(binary_data[0:8], 2))
                binary_data = binary_data[8:]
            if decoded_data[-5:] == "=====":
                break
            r, g, b = to_bin (pixel)
            binary_data += r[-1]
            binary_data += g[-1]
            binary_data += b[-1]
    return decoded_data[:-5]


video_path = "D:\\Downloads\\video.mp4"
encoded_video_path ="D:\\Documents\\Sem 3\\INF2005\\Project\\CSF-Steganography-Python-Tkinter\\output_video.avi"
secret = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Morbi consectetur aliquet nibh. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Curabitur ultrices porta risus vitae mollis. Donec posuere maximus volutpat. Praesent vestibulum ipsum vel mi interdum, nec semper mauris vulputate. Phasellus efficitur ac est faucibus viverra. Cras id dapibus augue, non accumsan diam. Suspendisse ac orci interdum, porttitor mi a, malesuada nisl. Pellentesque iaculis consectetur elit, eu iaculis lectus efficitur a. Suspendisse finibus, nibh vel varius hendrerit, ex justo fringilla dui, in egestas tortor nulla vitae erat. Aliquam erat volutpat. Quisque bibendum, ante et ultricies viverra, lorem neque aliquet ex, sit amet rhoncus mi massa ac justo. Nulla euismod, magna vel vehicula viverra, urna diam tincidunt sem, at laoreet orci nunc a nisl."
# video encryption
video_split(video_path,"frameholder")
extract_audio(video_path,"audioholder")
frames_to_video(video_path,secret)
add_audio_to_video()
# video decryption
video_split(encoded_video_path,"encodedframeholder")
frame_decode()
