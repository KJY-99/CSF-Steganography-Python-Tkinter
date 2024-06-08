import cv2, numpy as np

# Image resize function (Keep aspect ratio)
def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]
    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))
    resized = cv2.resize(image, dim, interpolation = inter)
    return resized

def to_bin(data):
    """Convert `data` to binary format as string"""
    if isinstance(data, str):
        return ''.join([ format(ord(i), "08b") for i in data ])
    elif isinstance(data, bytes) or isinstance(data, np.ndarray):
        return [ format(i, "08b") for i in data ]
    elif isinstance(data, int) or isinstance(data, np.uint8):
        return format(data, "08b")
    else:
        raise TypeError("Type not supported.")

def encode_img(image_name, secret_data, bit_length):
    # Read image
    image = cv2.imread(image_name)
    # Height * Width * RGB (bytes)
    n_bytes = image.shape[0] * image.shape[1] * 3 // 8 * bit_length
    # Stopping criteria
    secret_data = "~~~~~" + secret_data
    secret_data += "====="
    # Check image data feasibility
    if len(secret_data) > n_bytes:
        raise ValueError("Need larger image or less data.")
    data_index = 0
    # Converts text data to binary
    binary_secret_data = to_bin(secret_data)
    data_len = len(binary_secret_data)
    for row in image:
        for pixel in row:
            # Convert pixel to binary
            rgb = to_bin(pixel)
            # Index last x elements of the pixel, append indexed secret data
            for i in range (len(rgb)):
                if data_len >= data_index + bit_length:
                    pixel[i] = int(rgb[i][:-bit_length] + binary_secret_data[data_index:data_index + bit_length], 2)
                    data_index += bit_length
                else:
                    pixel[i] = int(rgb[i][:-bit_length] + binary_secret_data[data_index:data_len] + rgb[i][(8-bit_length+data_len-data_index):], 2 )
                    data_index += (data_len-data_index)
                    break   
                # Exit once all data is encoded
                if data_index >= data_len:
                    break
            if data_index >= data_len:
                break
        if data_index >= data_len:
            break
    return image

def decode_img(image_name, bit_length):
    # Read image
    image = cv2.imread(image_name)
    if image is None:
        raise ValueError("Image not found.")
    binary_data = ""
    decoded_data = ""
    for row in image:
        for pixel in row:
            if len(binary_data) >= 8:
                decoded_data += chr (int(binary_data[0:8], 2))
                binary_data = binary_data[8:]
            if len(decoded_data) == 5  and decoded_data[:5] != "~~~~~":
                print("stopped")
                return ""
            if decoded_data[-5:] == "=====":
                decoded_data = decoded_data[5:]
                return decoded_data[:-5]
            r, g, b = to_bin(pixel)
            # Index last x elements (Bit length)
            binary_data += r[-bit_length:]
            binary_data += g[-bit_length:]
            binary_data += b[-bit_length:]
    return decoded_data


# input_image = "test.png"  #png file path
# output_image = "output.png"
# secret_data = "test" #text file path
# # encode the data into the image
# encoded_image = encode_img(image_name=input_image, secret_data=secret_data, bit_length=5)
# # save the output image (encoded image)
# cv2.imwrite(output_image, encoded_image)
# # decode the secret data from the image
# decoded_data = decode_img(output_image, 5)
# print("Decoded data:", decoded_data)
