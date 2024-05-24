import cv2, numpy as np
from tkinter import filedialog
import os

def encode_message(self):
    # Get the secret message from the entry field
    secret_message = self.secret_message_entry.get()

    # Check if the secret message is empty
    if not secret_message:
        print("Error: Secret message is empty.")
        return

    # Ask user to select an image file
    image_path = filedialog.askopenfilename()

    # Check if the user canceled the file dialog
    if not image_path:
        print("Error: No image selected.")
        return

    # Define the output directory and ask user for file name
    output_directory = filedialog.askdirectory()
    output_file_name = filedialog.asksaveasfilename(defaultextension=".png")

    # Check if the user canceled the save dialog
    if not output_file_name:
        print("Error: Save operation canceled.")
        return

    # Encode the secret message into the image
    try:
        encoded_image = self.encode(image_path, secret_message)
    except Exception as e:
        print("Error:", e)
        return

    # Save the encoded image to the specified location
    output_file_path = os.path.join(output_directory, output_file_name)
    cv2.imwrite(output_file_path, encoded_image)

    print("Encoded image saved successfully.")

def to_bin(self, data):
    """Convert `data` to binary format as string"""
    if isinstance(data, str):
        return ''.join([format(ord(i), "08b") for i in data])
    elif isinstance(data, bytes) or isinstance(data, np.ndarray):
        return [format(i, "08b") for i in data]
    elif isinstance(data, int) or isinstance(data, np.uint8):
        return format(data, "08b")
    else:
        raise TypeError("Type not supported.")

def piencode(self, image_name, secret_data):
    # Read the image
    image = cv2.imread(image_name)

    # Make a copy of the image to preserve the original
    encoded_image = np.copy(image)

    # Calculate the maximum bytes to encode
    n_bytes = encoded_image.shape[0] * encoded_image.shape[1] * 3 // 8
    print("[*] Maximum bytes to encode:", n_bytes)

    # Add stopping criteria to the secret data
    secret_data += "====="

    # Check if the secret data fits within the image
    if len(secret_data) > n_bytes:
        raise ValueError("[!] Insufficient bytes, need a bigger image or less data.")

    print("[*] Encoding data...")

    # Convert secret data to binary
    binary_secret_data = self.to_bin(secret_data)

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
            r_bin, g_bin, b_bin = self.to_bin((r, g, b))

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

def decode(image_name):
        print("[+] Decoding...")
        # read the image
        image = cv2.imread(image_name)
        binary_data = ""
        for row in image:
            for pixel in row:
                r, g, b = to_bin(pixel)
                binary_data += r[-1]
                binary_data += g[-1]
                binary_data += b[-1]
        # split by 8-bits
        all_bytes = [ binary_data[i: i+8] for i in range(0, len(binary_data), 8) ]
        # convert from bits to characters
        decoded_data = ""
        for byte in all_bytes:
            decoded_data += chr(int(byte, 2))
            if decoded_data[-5:] == "=====": # we keep decoding until we see the stopping criteria.
                break
        return decoded_data[:-5]

if __name__ == "__main__":
    input_image = "pokemon.PNG"
    output_image = "stego_pokemon.PNG"
    secret_data = "This is a top secret message."
    # encode the data into the image
    encoded_image = encode(image_name=input_image, secret_data=secret_data)
    # save the output image (encoded image)
    cv2.imwrite(output_image, encoded_image)
    # decode the secret data from the image
    decoded_data = decode(output_image)
    print("[+] Decoded data:", decoded_data)